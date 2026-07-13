from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

from helm import __version__
from helm.config import get_settings


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: Literal["helm-api"]
    version: str
    environment: str


class VersionResponse(BaseModel):
    service: Literal["helm-api"]
    version: str
    runtimes: dict[str, str]


app = FastAPI(
    title="helm control plane",
    description="API foundation for helm. Trading capabilities are not enabled.",
    version=__version__,
)


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
