import json
import re
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

import httpx

from helm.config import get_settings

REQUIRED_FEATURES = {
    "approval_events",
    "run_events_sse",
    "run_status",
    "run_stop",
    "run_submission",
    "session_resources",
}
REQUIRED_ENDPOINTS = {
    "runs": ("POST", "/v1/runs"),
    "run_status": ("GET", "/v1/runs/{run_id}"),
    "run_events": ("GET", "/v1/runs/{run_id}/events"),
    "run_stop": ("POST", "/v1/runs/{run_id}/stop"),
    "session_messages": ("GET", "/api/sessions/{session_id}/messages"),
}
MAX_SESSION_RESPONSE_BYTES = 2 * 1024 * 1024
MAX_SESSION_MESSAGES = 10_000


@dataclass(frozen=True)
class HermesTranscript:
    resolved_session_id: str
    messages: tuple[dict[str, Any], ...]


class HermesError(RuntimeError):
    pass


class HermesRunRejected(HermesError):
    pass


class HermesSubmissionUncertain(HermesError):
    pass


class HermesRunMissing(HermesError):
    pass


class HermesSessionMissing(HermesError):
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
            try:
                capabilities = await client.get("/v1/capabilities")
                capabilities.raise_for_status()
                contract = capabilities.json()
            except (httpx.HTTPError, ValueError) as error:
                raise HermesRunRejected("Hermes Runs API preflight failed") from error
            if not isinstance(contract, dict):
                raise HermesRunRejected("Hermes Runs API is not compatible")
            features = contract.get("features", {})
            endpoints = contract.get("endpoints", {})
            endpoints_match = all(
                endpoints.get(name) == {"method": method, "path": path}
                for name, (method, path) in REQUIRED_ENDPOINTS.items()
            ) if isinstance(endpoints, dict) else False
            if (
                contract.get("object") != "hermes.api_server.capabilities"
                or contract.get("platform") != "hermes-agent"
                or not isinstance(features, dict)
                or not all(features.get(feature) is True for feature in REQUIRED_FEATURES)
                or not endpoints_match
            ):
                raise HermesRunRejected("Hermes Runs API is not compatible")
            try:
                response = await client.post(
                    "/v1/runs",
                    headers={"X-Hermes-Session-Key": session_key},
                    json={
                        "input": content,
                        "session_id": session_id,
                        "conversation_history": history,
                    },
                )
            except httpx.HTTPError as error:
                raise HermesSubmissionUncertain(
                    "Hermes submission outcome is uncertain"
                ) from error
        if 400 <= response.status_code < 500:
            raise HermesRunRejected("Hermes rejected the run submission")
        if response.status_code >= 500:
            raise HermesSubmissionUncertain("Hermes submission outcome is uncertain")
        try:
            payload = response.json()
        except ValueError as error:
            raise HermesSubmissionUncertain(
                "Hermes submission outcome is uncertain"
            ) from error
        if not isinstance(payload, dict):
            raise HermesSubmissionUncertain("Hermes returned an invalid run response")
        run_id = payload.get("run_id")
        if (
            response.status_code != 202
            or not isinstance(run_id, str)
            or not _valid_run_id(run_id)
        ):
            raise HermesSubmissionUncertain("Hermes returned an invalid run response")
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

    async def session_messages(self, session_id: str) -> HermesTranscript:
        if not session_id or len(session_id) > 256:
            raise HermesError("Hermes session ID is invalid")
        path = f"/api/sessions/{quote(session_id, safe='')}/messages"
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.control_timeout,
            transport=self.transport,
        ) as client:
            async with client.stream("GET", path) as response:
                if response.status_code == 404:
                    raise HermesSessionMissing("Hermes session does not exist")
                response.raise_for_status()
                body = bytearray()
                async for chunk in response.aiter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_SESSION_RESPONSE_BYTES:
                        raise HermesError("Hermes session transcript is oversized")
        try:
            payload = json.loads(body)
        except (UnicodeDecodeError, ValueError) as error:
            raise HermesError("Hermes returned an invalid session transcript") from error
        if (
            not isinstance(payload, dict)
            or payload.get("object") != "list"
            or not isinstance(payload.get("session_id"), str)
            or not 1 <= len(payload["session_id"]) <= 256
            or not isinstance(payload.get("data"), list)
            or len(payload["data"]) > MAX_SESSION_MESSAGES
        ):
            raise HermesError("Hermes returned an invalid session transcript")

        resolved_session_id = payload["session_id"]
        messages: list[dict[str, Any]] = []
        previous_id = 0
        for raw_message in payload["data"]:
            if not isinstance(raw_message, dict):
                raise HermesError("Hermes returned an invalid session transcript")
            message_id = raw_message.get("id")
            role = raw_message.get("role")
            content = raw_message.get("content")
            if (
                not isinstance(message_id, int)
                or isinstance(message_id, bool)
                or message_id <= previous_id
                or raw_message.get("session_id") != resolved_session_id
                or role not in {"user", "assistant", "system", "tool"}
                or not isinstance(content, str)
            ):
                raise HermesError("Hermes returned an invalid session transcript")
            tool_call_id = raw_message.get("tool_call_id")
            tool_name = raw_message.get("tool_name")
            tool_calls = raw_message.get("tool_calls")
            if tool_call_id is not None and not isinstance(tool_call_id, str):
                raise HermesError("Hermes returned an invalid session transcript")
            if tool_name is not None and not isinstance(tool_name, str):
                raise HermesError("Hermes returned an invalid session transcript")
            if tool_calls is not None and not isinstance(tool_calls, list):
                raise HermesError("Hermes returned an invalid session transcript")
            messages.append(
                {
                    "id": message_id,
                    "role": role,
                    "content": content,
                    "tool_call_id": tool_call_id,
                    "tool_calls": tool_calls,
                    "tool_name": tool_name,
                }
            )
            previous_id = message_id
        return HermesTranscript(
            resolved_session_id=resolved_session_id,
            messages=tuple(messages),
        )

    async def status(self, run_id: str) -> dict[str, Any]:
        _require_run_id(run_id)
        async with httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.control_timeout,
            transport=self.transport,
        ) as client:
            response = await client.get(f"/v1/runs/{run_id}")
            if response.status_code == 404:
                raise HermesRunMissing("Hermes run no longer exists")
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
            if response.status_code == 404:
                raise HermesRunMissing("Hermes run no longer exists")
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
