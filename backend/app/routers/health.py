from fastapi import APIRouter, Request

from app.services.experiment_service import NOTICE


router = APIRouter(tags=["Health"])


@router.get("/health")
def health(request: Request):
    service = request.app.state.experiments
    return {
        "status": "ok",
        "notice": NOTICE,
        "gemini_available": service.settings.gemini_enabled,
        "availability": service.availability(),
        "max_messages": service.settings.max_messages_per_experiment,
        "max_message_length": service.settings.max_message_length,
    }
