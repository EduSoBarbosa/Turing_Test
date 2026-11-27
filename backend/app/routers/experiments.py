from uuid import UUID

from fastapi import APIRouter, Request, Response

from app.schemas import EvaluationInput, RevealView, SessionView, Start


router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post("", response_model=SessionView, status_code=201)
def start(payload: Start, request: Request):
    return request.app.state.experiments.start(payload.acknowledged)


@router.post("/{id}/finish", response_model=SessionView)
def finish(id: UUID, request: Request):
    return request.app.state.experiments.finish(id)


@router.post("/{id}/evaluation", response_model=SessionView, status_code=201)
def evaluate(id: UUID, payload: EvaluationInput, request: Request):
    return request.app.state.experiments.evaluate(id, payload)


@router.get("/{id}/reveal", response_model=RevealView)
def reveal(id: UUID, request: Request, response: Response):
    response.headers["Cache-Control"] = "no-store"
    return request.app.state.experiments.reveal(id)
