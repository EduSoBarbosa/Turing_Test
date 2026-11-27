import csv
from hashlib import sha256
from io import StringIO
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import httpx
import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.database.models import Experiment
from app.main import create_app
from app.schemas import Group
from app.services import gemini_service


API = "/api/v1"
ADMIN = {"X-Admin-API-Key": "test-secret"}
EVALUATION = dict(
    classification="human", confidence=85, naturalness=4, coherence=5,
    emotional_understanding=3, comment="The responses felt spontaneous.",
)


@pytest.fixture
def app(tmp_path):
    return make_app(tmp_path)


def make_app(tmp_path, **overrides):
    settings = dict(
        database_url=f"sqlite:///{(tmp_path / 'test.db').as_posix()}",
        gemini_api_key="", gemini_model="", admin_api_key="test-secret",
        max_message_length=30, max_messages_per_experiment=2,
    )
    return create_app(Settings(_env_file=None, **(settings | overrides)))


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


def start(client):
    response = client.post(f"{API}/experiments", json={"acknowledged": True})
    assert response.status_code == 201
    data = response.json()
    assert set(data) == {"id", "status", "remaining_messages", "max_messages", "max_message_length", "notice"}
    assert data["status"] == "IN_PROGRESS"
    return f"{API}/experiments/{data['id']}"


def send(client, path, content="I need some help."):
    return client.post(f"{path}/messages", json={"content": content})


def complete(client, path, evaluation=EVALUATION):
    assert send(client, path).status_code == 201
    assert client.post(f"{path}/finish").json()["status"] == "AWAITING_EVALUATION"
    assert client.post(f"{path}/evaluation", json=evaluation).status_code == 201


def assigned_group(app, path):
    with app.state.experiments.sessions() as db:
        return db.get(Experiment, path.rsplit("/", 1)[-1]).experimental_group


def test_local_eliza_and_disclosure(client):
    health = client.get(f"{API}/health").json()
    assert health["gemini_available"] is False
    assert "artificial chatbots" in health["notice"]
    assert "Gemini conditions are unavailable" in health["availability"]
    assert client.post(f"{API}/experiments", json={"acknowledged": False}).status_code == 422
    assert client.post(f"{API}/experiments", json={"acknowledged": 1}).status_code == 422
    path = start(client)
    result = send(client, path).json()
    assert result["session"]["remaining_messages"] == 1
    user, assistant = result["messages"]
    assert user["content"] == "I need some help."
    assert assistant["role"] == "assistant" and assistant["content"]
    assert set(assistant) == {"role", "content", "created_at"}


def test_transitions_limits_and_reveal(client):
    path = start(client)
    assert client.get(f"{path}/reveal").status_code == 409
    assert client.post(f"{path}/finish").status_code == 409
    assert client.post(f"{path}/evaluation", json=EVALUATION).status_code == 409
    assert send(client, path, " ").status_code == 422
    assert send(client, path, "a" * 31).status_code == 422
    assert send(client, path).status_code == 201
    assert send(client, path).json()["session"]["status"] == "AWAITING_EVALUATION"
    assert send(client, path).status_code == 409
    assert client.post(f"{path}/finish").status_code == 200
    assert client.get(f"{path}/reveal").status_code == 409
    assert client.post(f"{path}/evaluation", json=EVALUATION).json()["status"] == "EVALUATED"
    first = client.get(f"{path}/reveal")
    assert first.headers["cache-control"] == "no-store"
    assert first.json()["model_name"] == "ELIZA (NLTK)"
    assert first.json()["session"]["status"] == "REVEALED"
    assert client.get(f"{path}/reveal").json() == first.json()
    assert client.post(f"{path}/evaluation", json=EVALUATION).status_code == 409
    assert client.post(f"{path}/finish").status_code == 409


@pytest.mark.parametrize("change", [
    {"classification": "bot"}, {"confidence": True}, {"confidence": -1},
    {"naturalness": 6}, {"coherence": "4"}, {"emotional_understanding": 0},
    {"comment": "x" * 2001}, {"email": "unexpected"},
])
def test_validation(client, change):
    path = start(client)
    send(client, path)
    client.post(f"{path}/finish")
    assert client.post(f"{path}/evaluation", json=EVALUATION | change).status_code == 422
    assert client.get(f"{path}/reveal").status_code == 409


def test_persisted_history_and_isolation(tmp_path):
    app = make_app(tmp_path)
    with TestClient(app) as client:
        first, second = start(client), start(client)
        original = send(client, first).json()
        assert client.get(f"{API}/experiments/{uuid4()}/messages").status_code == 404
    with TestClient(make_app(tmp_path)) as client:
        assert client.get(f"{first}/messages").json() == original
        assert client.get(f"{second}/messages").json()["messages"] == []


@pytest.mark.parametrize("route", ["results", "results/export", "prompts"])
def test_admin_protection(client, route):
    url = f"{API}/admin/{route}"
    assert client.get(url).status_code == 401
    assert client.get(url, headers={"X-Admin-API-Key": "wrong"}).status_code == 401
    assert client.get(url, headers=ADMIN).status_code == 200


def test_unconfigured_admin(tmp_path):
    with TestClient(make_app(tmp_path, admin_api_key="")) as client:
        assert client.get(f"{API}/admin/results", headers=ADMIN).status_code == 401


def test_prompt_versions(tmp_path, monkeypatch):
    original = gemini_service.genai.Client
    monkeypatch.setattr(gemini_service.genai, "Client", Mock(wraps=original))
    for _ in range(2):
        with TestClient(make_app(tmp_path)) as client:
            prompts = client.get(f"{API}/admin/prompts", headers=ADMIN).json()
            assert len(prompts) == 3
    prompts = {prompt["technique"]: prompt for prompt in prompts}
    assert prompts["baseline"]["content"] == "Respond to the user's messages in English."
    assert prompts["few_shot"]["content"].startswith(prompts["zero_shot"]["content"])
    assert "Pretty quiet, actually." in prompts["few_shot"]["content"]
    for prompt in prompts.values():
        digest = sha256(prompt["content"].encode()).hexdigest()
        assert prompt["content_hash"] == digest
        assert prompt["id"] == f"{prompt['technique']}:v1-{digest[:12]}"
    gemini_service.genai.Client.assert_not_called()


@pytest.fixture
def gemini_app(tmp_path, monkeypatch):
    mock = Mock()
    mock.models.generate_content.return_value = SimpleNamespace(
        text="That sounds interesting.",
        usage_metadata=SimpleNamespace(prompt_token_count=20, candidates_token_count=5),
    )
    factory = Mock(return_value=mock)
    monkeypatch.setattr(gemini_service.genai, "Client", factory)
    app = make_app(tmp_path, gemini_api_key="test-key", gemini_model="configured-test-model", gemini_requests_per_minute=8)
    with TestClient(app) as client:
        factory.assert_not_called()
        yield app, client, mock.models.generate_content


def test_balance_and_gemini_history(gemini_app):
    app, client, generate = gemini_app
    blocks = []
    for _ in range(2):
        block = {}
        for _ in Group:
            path = start(client)
            block[assigned_group(app, path)] = path
        assert set(block) == set(Group)
        blocks.append(block)
    first, second = [block[Group.BASELINE] for block in blocks]
    assert send(client, first, "First conversation").status_code == 201
    assert send(client, second, "Second conversation").status_code == 201
    assert send(client, first, "A follow-up").status_code == 201
    calls = [call.kwargs for call in generate.call_args_list]
    assert [p.parts[0].text for p in calls[1]["contents"]] == ["Second conversation"]
    assert [p.parts[0].text for p in calls[2]["contents"]] == [
        "First conversation", "That sounds interesting.", "A follow-up",
    ]
    assert [p.role for p in calls[2]["contents"]] == ["user", "model", "user"]
    assert calls[2]["model"] == "configured-test-model"
    assert calls[2]["config"].system_instruction == "Respond to the user's messages in English."


def test_metrics_and_csv(gemini_app):
    app, client, generate = gemini_app
    paths = {}
    for _ in Group:
        path = start(client)
        paths[assigned_group(app, path)] = path
    initial = client.get(f"{API}/admin/results", headers=ADMIN).json()
    assert initial["groups"]["A"]["human_perception_rate"] is None
    assert initial["absolute_difference_vs_baseline_pp"] == {"C": None, "D": None}
    for group, path in paths.items():
        payload = EVALUATION | {"classification": "machine"} if group == Group.BASELINE else EVALUATION
        complete(client, path, payload)
    results = client.get(f"{API}/admin/results", headers=ADMIN).json()
    groups = results["groups"]
    assert results["absolute_difference_vs_baseline_pp"] == {"C": 100, "D": 100}
    assert groups["A"]["mean_input_tokens"] is None
    assert groups["B"]["completed_experiments"] == groups["B"]["valid_evaluations"] == 1
    assert groups["B"]["human_perception_rate"] == 0 and groups["B"]["machine_percentage"] == 100
    assert groups["D"]["mean_confidence"] == 85
    assert groups["D"]["mean_naturalness"] == 4
    assert groups["D"]["mean_coherence"] == 5
    assert groups["D"]["mean_emotional_understanding"] == 3
    assert groups["D"]["mean_latency_ms"] == groups["D"]["median_latency_ms"]
    assert (groups["D"]["mean_input_tokens"], groups["D"]["mean_output_tokens"]) == (20, 5)
    configs = [call.kwargs["config"] for call in generate.call_args_list]
    assert len({config.system_instruction for config in configs}) == 3
    assert all(config.model_dump(exclude={"system_instruction"}) ==
               configs[0].model_dump(exclude={"system_instruction"}) for config in configs)
    export = client.get(f"{API}/admin/results/export", headers=ADMIN)
    rows = list(csv.DictReader(StringIO(export.text)))
    assert export.headers["content-type"].startswith("text/csv")
    assert len(rows) == 4 and rows[1]["classification"] == "machine"
    assert {"id", "experiment_id", "content", "comment"}.isdisjoint(rows[0])


@pytest.mark.parametrize("failure,status", [
    (httpx.ReadTimeout("private details"), 504),
    (httpx.ConnectError("private details"), 502),
    (gemini_service.errors.APIError(503, {"error": {"message": "private details"}}), 502),
])
def test_gemini_failure_has_no_fallback(gemini_app, failure, status):
    app, client, generate = gemini_app
    paths = [start(client) for _ in Group]
    path = next(path for path in paths if assigned_group(app, path) == Group.BASELINE)
    generate.side_effect = failure
    error = send(client, path)
    assert error.status_code == status
    assert "private details" not in error.text
    history = client.get(f"{path}/messages").json()
    assert history["messages"] == [] and history["session"]["remaining_messages"] == 2
    generate.side_effect = None
    assert send(client, path).status_code == 201
    assert assigned_group(app, path) == Group.BASELINE


def test_gemini_rate_limit(gemini_app):
    app, client, generate = gemini_app
    gemini = app.state.experiments.gemini
    gemini.settings.gemini_requests_per_minute = 1
    paths = [start(client) for _ in Group]
    path = next(path for path in paths if assigned_group(app, path) == Group.BASELINE)
    assert send(client, path).status_code == 201
    assert send(client, path).status_code == 429
    assert generate.call_count == 1
    assert client.get(f"{path}/messages").json()["session"]["remaining_messages"] == 1
