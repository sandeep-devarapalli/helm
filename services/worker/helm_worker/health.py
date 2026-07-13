from typing import Literal, TypedDict

from helm_worker import __version__


class HealthPayload(TypedDict):
    status: Literal["ok"]
    service: Literal["helm-worker"]
    version: str


def health_payload() -> HealthPayload:
    return {"status": "ok", "service": "helm-worker", "version": __version__}
