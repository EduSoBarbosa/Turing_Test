from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import Settings
from app.database.connection import connect
from app.database.models import Base
from app.routers import chat, experiments, health, prompts, results
from app.services.base_chatbot import ChatbotError
from app.services.experiment_service import ExperimentService
from app.services.prompt_service import register_prompts


def create_app(settings: Settings | None = None):
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app):
        engine, sessions = connect(settings.database_url)
        try:
            Base.metadata.create_all(engine)
            with sessions.begin() as db:
                versions = register_prompts(db)
            app.state.experiments = ExperimentService(settings, sessions, versions)
            try:
                yield
            finally:
                app.state.experiments.gemini.close()
        finally:
            engine.dispose()

    app = FastAPI(title="Can Machines Fool Humans?", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    @app.exception_handler(ChatbotError)
    async def experiment_error(request: Request, error: ChatbotError):
        return JSONResponse(
            status_code=error.status_code, content={"detail": str(error)},
            headers={"Cache-Control": "no-store"},
        )

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, error: RequestValidationError):
        details = [
            {"loc": item["loc"], "msg": item["msg"], "type": item["type"]}
            for item in error.errors()
        ]
        return JSONResponse(status_code=422, content={"detail": details})

    for router in (health, experiments, chat, results, prompts):
        app.include_router(router.router, prefix="/api/v1")
    return app


app = create_app()
