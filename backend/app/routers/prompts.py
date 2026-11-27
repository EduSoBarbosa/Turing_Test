from fastapi import APIRouter, Depends, Request
from sqlalchemy import select

from app.database.models import PromptVersion
from app.routers.admin import authenticate
from app.schemas import PromptView


router = APIRouter(prefix="/admin/prompts", tags=["Administration"], dependencies=[Depends(authenticate)])


@router.get("", response_model=list[PromptView])
def prompts(request: Request):
    with request.app.state.experiments.sessions() as db:
        return db.scalars(select(PromptVersion).order_by(PromptVersion.technique, PromptVersion.created_at)).all()
