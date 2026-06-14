from fastapi import FastAPI

from app.api.routes import health
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    app.include_router(health.router)
    return app


app = create_app()