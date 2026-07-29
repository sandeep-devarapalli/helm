from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from helm import __version__
from helm.api.conversations import router as conversations_router
from helm.config import get_settings
from helm.database import dispose_database


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
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    await dispose_database()


app = FastAPI(
    title="helm control plane",
    description="API foundation for helm. Trading capabilities are not enabled.",
    version=__version__,
    lifespan=lifespan,
)
app.include_router(conversations_router)


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
