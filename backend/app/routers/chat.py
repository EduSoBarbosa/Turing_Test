from uuid import UUID

from fastapi import APIRouter, Request

from app.schemas import MessageInput, TurnView


router = APIRouter(prefix="/experiments/{id}/messages", tags=["Conversation"])


@router.post("", response_model=TurnView, status_code=201)
def send(id: UUID, payload: MessageInput, request: Request):
    return request.app.state.experiments.send(id, payload.content)


@router.get("", response_model=TurnView)
def history(id: UUID, request: Request):
    return request.app.state.experiments.history(id)
