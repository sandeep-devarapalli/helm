import json
import re
from collections.abc import AsyncIterator
from typing import Any

import httpx

from helm.config import get_settings

REQUIRED_FEATURES = {
    "approval_events",
    "run_events_sse",
    "run_status",
    "run_stop",
    "run_submission",
}
REQUIRED_ENDPOINTS = {
    "runs": ("POST", "/v1/runs"),
    "run_status": ("GET", "/v1/runs/{run_id}"),
    "run_events": ("GET", "/v1/runs/{run_id}/events"),
    "run_stop": ("POST", "/v1/runs/{run_id}/stop"),
}


class HermesError(RuntimeError):
    pass


class HermesClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.control_timeout = httpx.Timeout(10)
        self.stream_timeout = httpx.Timeout(10, read=300)
        self.transport = transport

    async def submit_run(
        self,
        content: str,
        session_id: str,
        session_key: str,
        history: list[dict[str, str]],
    ) -> str:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.control_timeout,
            transport=self.transport,
        ) as client:
            capabilities = await client.get("/v1/capabilities")
            capabilities.raise_for_status()
            contract = capabilities.json()
            features = contract.get("features", {})
            endpoints = contract.get("endpoints", {})
            endpoints_match = all(
                endpoints.get(name) == {"method": method, "path": path}
                for name, (method, path) in REQUIRED_ENDPOINTS.items()
            )
            if (
                contract.get("object") != "hermes.api_server.capabilities"
                or contract.get("platform") != "hermes-agent"
                or not all(features.get(feature) is True for feature in REQUIRED_FEATURES)
                or not endpoints_match
            ):
                raise HermesError("Hermes Runs API is not compatible")
            response = await client.post(
                "/v1/runs",
                headers={"X-Hermes-Session-Key": session_key},
                json={
                    "input": content,
                    "session_id": session_id,
                    "conversation_history": history,
                },
            )
            response.raise_for_status()
        payload = response.json()
        run_id = payload.get("run_id")
        if (
            response.status_code != 202
            or not isinstance(run_id, str)
            or not _valid_run_id(run_id)
        ):
            raise HermesError("Hermes returned an invalid run response")
        return run_id

    async def events(self, run_id: str) -> AsyncIterator[dict[str, Any]]:
        _require_run_id(run_id)
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.stream_timeout,
            transport=self.transport,
        ) as client:
            async with client.stream("GET", f"/v1/runs/{run_id}/events") as response:
                response.raise_for_status()
                if not response.headers.get("content-type", "").startswith(
                    "text/event-stream"
                ):
                    raise HermesError("Hermes returned an invalid event stream")
                async for line in response.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    event = json.loads(line.removeprefix("data:").strip())
                    if not isinstance(event, dict):
                        raise HermesError("Hermes returned an invalid run event")
                    yield event

    async def status(self, run_id: str) -> dict[str, Any]:
        _require_run_id(run_id)
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.control_timeout,
            transport=self.transport,
        ) as client:
            response = await client.get(f"/v1/runs/{run_id}")
            response.raise_for_status()
        payload = response.json()
        if (
            not isinstance(payload, dict)
            or payload.get("object") != "hermes.run"
            or payload.get("run_id") != run_id
            or payload.get("status")
            not in {
                "queued",
                "running",
                "waiting_for_approval",
                "stopping",
                "completed",
                "failed",
                "cancelled",
            }
        ):
            raise HermesError("Hermes returned an invalid run status")
        return payload

    async def stop(self, run_id: str) -> None:
        _require_run_id(run_id)
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.control_timeout,
            transport=self.transport,
        ) as client:
            response = await client.post(f"/v1/runs/{run_id}/stop")
            response.raise_for_status()
        payload = response.json()
        if payload != {"run_id": run_id, "status": "stopping"}:
            raise HermesError("Hermes returned an invalid stop response")


def get_hermes_client() -> HermesClient:
    settings = get_settings()
    return HermesClient(
        settings.hermes_base_url,
        settings.hermes_api_key.get_secret_value(),
    )


def _valid_run_id(value: str) -> bool:
    return re.fullmatch(r"run_[a-f0-9]{32}", value) is not None


def _require_run_id(run_id: str) -> None:
    if not _valid_run_id(run_id):
        raise HermesError("Hermes run ID is invalid")
