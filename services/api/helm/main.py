import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from helm import __version__
from helm.api.conversations import router as conversations_router
from helm.api.memory import router as memory_router
from helm.api.runs import cleanup_upstream_run, recover_orphaned_runs
from helm.api.runs import router as runs_router
from helm.config import get_settings
from helm.database import dispose_database, get_session_factory
from helm.integrations.hermes import get_hermes_client


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: Literal["helm-api"]
    version: str
    environment: str


class VersionResponse(BaseModel):
    service: Literal["helm-api"]
    version: str
    runtimes: dict[str, str]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    if not hasattr(app.state, "session_factory"):
        app.state.session_factory = get_session_factory()
    hermes = get_hermes_client()
    unresolved = await recover_orphaned_runs(app.state.session_factory)
    cleanup_tasks = {
        asyncio.create_task(cleanup_upstream_run(hermes, run_id))
        for run_id in unresolved
    }
    try:
        yield
    finally:
        for task in cleanup_tasks:
            task.cancel()
        await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        await dispose_database()


app = FastAPI(
    title="helm control plane",
    description="API foundation for helm. Trading capabilities are not enabled.",
    version=__version__,
    lifespan=lifespan,
)
app.include_router(conversations_router)
app.include_router(memory_router)
app.include_router(runs_router)


@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service="helm-api",
        version=__version__,
        environment=settings.environment,
    )


@app.get("/version", response_model=VersionResponse, tags=["system"])
async def version() -> VersionResponse:
    settings = get_settings()
    return VersionResponse(
        service="helm-api",
        version=__version__,
        runtimes={
            "hermes": settings.hermes_version,
            "vibe": settings.vibe_version,
        },
    )
