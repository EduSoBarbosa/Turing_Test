from datetime import UTC
from random import SystemRandom
from threading import Lock
from time import perf_counter
from uuid import uuid4

from app.database import repository
from app.database.models import Evaluation, Experiment, Message, PromptVersion, utc_now
from app.schemas import Group, MessageView, RevealView, SessionView, Status, TurnView
from app.services.base_chatbot import ChatbotError
from app.services.eliza_service import Eliza
from app.services.gemini_service import Gemini
from app.services.prompt_service import TECHNIQUES


NOTICE = (
    "This educational conversation experiment involves artificial chatbots. "
    "Please write in English and avoid sharing personal information. "
    "Rate how human-like the conversation felt before the chatbot is revealed."
)
TRANSITIONS = {
    Status.CREATED: Status.IN_PROGRESS,
    Status.IN_PROGRESS: Status.AWAITING_EVALUATION,
    Status.AWAITING_EVALUATION: Status.EVALUATED,
    Status.EVALUATED: Status.REVEALED,
}


class ExperimentService:
    def __init__(self, settings, sessions, prompt_versions):
        self.settings = settings
        self.sessions = sessions
        self.prompt_versions = prompt_versions
        self.eliza = Eliza()
        self.gemini = Gemini(settings)
        self.random = SystemRandom()
        self.assignment_lock = Lock()
        self.session_locks = [Lock() for _ in range(64)]

    def availability(self):
        if self.settings.gemini_enabled:
            return "All experimental conditions are configured."
        return "Only the local chatbot is available. The three Gemini conditions are unavailable."

    def _view(self, experiment):
        return SessionView(
            id=experiment.id,
            status=experiment.status,
            remaining_messages=experiment.max_messages - experiment.turns,
            max_messages=experiment.max_messages,
            max_message_length=experiment.max_message_length,
            notice=NOTICE,
        )

    @staticmethod
    def _message_view(message):
        view = MessageView.model_validate(message)
        return view.model_copy(update={"created_at": view.created_at.replace(tzinfo=UTC)})

    @staticmethod
    def _get(db, id):
        experiment = db.get(Experiment, str(id))
        if experiment is None:
            raise ChatbotError(404, "Experiment not found.")
        return experiment

    @staticmethod
    def _save(db, experiment, **updates):
        if not repository.update_session(db, experiment, **updates):
            raise ChatbotError(409, "The session changed. Refresh its history and try again.")

    def start(self, acknowledged):
        if not acknowledged:
            raise ChatbotError(422, "Please acknowledge the educational chatbot experiment.")
        with self.assignment_lock, self.sessions.begin() as db:
            groups = list(Group) if self.settings.gemini_enabled else [Group.ELIZA]
            counts = repository.group_counts(db)
            minimum = min(counts.get(group, 0) for group in groups)
            group = self.random.choice([group for group in groups if counts.get(group, 0) == minimum])
            experiment = Experiment(
                id=str(uuid4()),
                experimental_group=group,
                model_name="ELIZA (NLTK)" if group == Group.ELIZA else self.settings.gemini_model.strip(),
                prompt_version=self.prompt_versions.get(group),
                status=Status.CREATED,
                max_messages=self.settings.max_messages_per_experiment,
                max_message_length=self.settings.max_message_length,
                temperature=self.settings.gemini_temperature,
                top_p=self.settings.gemini_top_p,
                max_output_tokens=self.settings.gemini_max_output_tokens,
            )
            db.add(experiment)
            db.flush()
            self._save(db, experiment, status=TRANSITIONS[Status.CREATED])
            return self._view(experiment)

    def history(self, id):
        with self.sessions() as db:
            experiment = self._get(db, id)
            entries = repository.messages(db, experiment.id)
            return TurnView(session=self._view(experiment), messages=list(map(self._message_view, entries)))

    def send(self, id, content):
        with self.session_locks[id.int % len(self.session_locks)], self.sessions.begin() as db:
            experiment = self._get(db, id)
            if experiment.status != Status.IN_PROGRESS or experiment.turns >= experiment.max_messages:
                raise ChatbotError(409, "This conversation is closed.")
            if len(content) > experiment.max_message_length:
                raise ChatbotError(422, f"Messages must contain at most {experiment.max_message_length} characters.")

            user = Message(experiment_id=experiment.id, role="user", content=content)
            history = repository.messages(db, experiment.id) + [user]
            version = db.get(PromptVersion, experiment.prompt_version) if experiment.prompt_version else None
            chatbot = self.eliza if experiment.experimental_group == Group.ELIZA else self.gemini
            started = perf_counter()
            reply = chatbot.reply(experiment, history, version.content if version else None)
            latency_ms = (perf_counter() - started) * 1000
            assistant = Message(
                experiment_id=experiment.id, role="assistant", content=reply.content,
                latency_ms=latency_ms, input_tokens=reply.input_tokens, output_tokens=reply.output_tokens,
            )
            turns = experiment.turns + 1
            updates = {"turns": turns}
            if turns == experiment.max_messages:
                updates.update(status=TRANSITIONS[Status.IN_PROGRESS], finished_at=utc_now())
            self._save(db, experiment, **updates)
            db.add_all([user, assistant])
            db.flush()
            return TurnView(session=self._view(experiment), messages=list(map(self._message_view, [user, assistant])))

    def finish(self, id):
        with self.session_locks[id.int % len(self.session_locks)], self.sessions.begin() as db:
            experiment = self._get(db, id)
            if experiment.status == Status.AWAITING_EVALUATION:
                return self._view(experiment)
            if experiment.status != Status.IN_PROGRESS or experiment.turns == 0:
                raise ChatbotError(409, "Exchange at least one message before finishing the conversation.")
            self._save(db, experiment, status=TRANSITIONS[Status.IN_PROGRESS], finished_at=utc_now())
            return self._view(experiment)

    def evaluate(self, id, evaluation):
        with self.session_locks[id.int % len(self.session_locks)], self.sessions.begin() as db:
            experiment = self._get(db, id)
            if experiment.status != Status.AWAITING_EVALUATION:
                raise ChatbotError(409, "Evaluation requires a finished conversation and can be submitted once.")
            self._save(db, experiment, status=TRANSITIONS[Status.AWAITING_EVALUATION])
            db.add(Evaluation(experiment_id=experiment.id, **evaluation.model_dump()))
            return self._view(experiment)

    def reveal(self, id):
        with self.session_locks[id.int % len(self.session_locks)], self.sessions.begin() as db:
            experiment = self._get(db, id)
            if experiment.status == Status.EVALUATED:
                self._save(db, experiment, status=TRANSITIONS[Status.EVALUATED])
            if experiment.status != Status.REVEALED:
                raise ChatbotError(409, "Submit your evaluation before revealing the chatbot.")
            group = Group(experiment.experimental_group)
            return RevealView(
                session=self._view(experiment),
                experimental_group=group,
                model_name=experiment.model_name,
                provider="NLTK" if group == Group.ELIZA else "Google",
                technique=TECHNIQUES[group],
                prompt_version=experiment.prompt_version,
            )
