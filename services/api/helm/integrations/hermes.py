import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from helm.config import get_settings

REQUIRED_FEATURES = {"run_submission", "run_status", "run_events_sse"}


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
        self.timeout = httpx.Timeout(10, read=300)
        self.transport = transport

    async def submit_run(
        self,
        content: str,
        session_id: str,
        history: list[dict[str, str]],
    ) -> str:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            capabilities = await client.get("/v1/capabilities")
            capabilities.raise_for_status()
            features = capabilities.json().get("features", {})
            if not all(features.get(feature) is True for feature in REQUIRED_FEATURES):
                raise HermesError("Hermes Runs API is not compatible")
            response = await client.post(
                "/v1/runs",
                json={
                    "input": content,
                    "session_id": session_id,
                    "conversation_history": history,
                },
            )
            response.raise_for_status()
        payload = response.json()
        run_id = payload.get("run_id")
        if response.status_code != 202 or not isinstance(run_id, str):
            raise HermesError("Hermes returned an invalid run response")
        return run_id

    async def events(self, run_id: str) -> AsyncIterator[dict[str, Any]]:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            async with client.stream("GET", f"/v1/runs/{run_id}/events") as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    event = json.loads(line.removeprefix("data:").strip())
                    if not isinstance(event, dict):
                        raise HermesError("Hermes returned an invalid run event")
                    yield event

    async def status(self, run_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            response = await client.get(f"/v1/runs/{run_id}")
            response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise HermesError("Hermes returned an invalid run status")
        return payload

    async def stop(self, run_id: str) -> None:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
            transport=self.transport,
        ) as client:
            response = await client.post(f"/v1/runs/{run_id}/stop")
            response.raise_for_status()


def get_hermes_client() -> HermesClient:
    settings = get_settings()
    return HermesClient(
        settings.hermes_base_url,
        settings.hermes_api_key.get_secret_value(),
    )
