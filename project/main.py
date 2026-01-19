from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from project.config import Settings, get_settings
from project.db.db import engine
from project.db.models.base import Base
from project.routers import auth_router, tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure FastAPI application."""
    if settings is None:
        settings = get_settings()

    app = FastAPI(
        title="Task Manager API",
        description="Demo API for pytest unit testing workshop",
        version="1.0.0",
        lifespan=lifespan,
        debug=settings.DEBUG,
    )

    # cors middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.DEBUG else ["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # register routers
    app.include_router(auth_router)
    app.include_router(tasks_router)

    # basic endpoints
    @app.get("/", status_code=status.HTTP_200_OK, tags=["Root"])
    def root() -> dict[str, str]:
        return {"message": "Task Manager API"}

    @app.get("/health", status_code=status.HTTP_200_OK, tags=["Root"])
    def health_check() -> dict[str, str]:
        return {"status": "healthy"}

    return app


app = create_app()
