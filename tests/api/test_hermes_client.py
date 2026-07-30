import asyncio
import json

import httpx
import pytest
from helm.integrations.hermes import (
    MAX_SESSION_RESPONSE_BYTES,
    HermesClient,
    HermesError,
    HermesRunRejected,
    HermesSessionMissing,
    HermesSubmissionUncertain,
)


def test_runs_contract_and_sse_parsing() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        assert request.headers["authorization"] == "Bearer test-key"
        if request.url.path == "/v1/capabilities":
            return httpx.Response(
                200,
                json={
                    "object": "hermes.api_server.capabilities",
                    "platform": "hermes-agent",
                    "features": {
                        "approval_events": True,
                        "run_submission": True,
                        "run_status": True,
                        "run_events_sse": True,
                        "run_stop": True,
                        "session_resources": True,
                    },
                    "endpoints": {
                        "runs": {"method": "POST", "path": "/v1/runs"},
                        "run_status": {
                            "method": "GET",
                            "path": "/v1/runs/{run_id}",
                        },
                        "run_events": {
                            "method": "GET",
                            "path": "/v1/runs/{run_id}/events",
                        },
                        "run_stop": {
                            "method": "POST",
                            "path": "/v1/runs/{run_id}/stop",
                        },
                        "session_messages": {
                            "method": "GET",
                            "path": "/api/sessions/{session_id}/messages",
                        },
                    },
                },
            )
        if request.url.path == "/v1/runs":
            assert request.headers["x-hermes-session-key"] == "helm:workspace:one"
            assert json.loads(request.content) == {
                "input": "Resolve AAPL",
                "session_id": "helm:workspace:conversation:one",
                "conversation_history": [{"role": "user", "content": "Earlier"}],
            }
            return httpx.Response(
                202,
                json={"run_id": f"run_{'a' * 32}", "status": "started"},
            )
        if request.url.path == f"/v1/runs/run_{'a' * 32}/events":
            return httpx.Response(
                200,
                text=(
                    ": keepalive\n\n"
                    'data: {"event":"message.delta","delta":"AAPL"}\n\n'
                    'data: {"event":"run.completed","output":"AAPL.US"}\n\n'
                    ": stream closed\n\n"
                ),
                headers={"content-type": "text/event-stream"},
            )
        if request.url.path == f"/v1/runs/run_{'a' * 32}/stop":
            return httpx.Response(
                200,
                json={"run_id": f"run_{'a' * 32}", "status": "stopping"},
            )
        if request.url.path == f"/v1/runs/run_{'a' * 32}":
            return httpx.Response(
                200,
                json={
                    "object": "hermes.run",
                    "run_id": f"run_{'a' * 32}",
                    "status": "completed",
                },
            )
        raise AssertionError(request.url)

    async def exercise() -> None:
        client = HermesClient(
            "http://hermes:8642",
            "test-key",
            httpx.MockTransport(handler),
        )
        run_id = await client.submit_run(
            "Resolve AAPL",
            "helm:workspace:conversation:one",
            "helm:workspace:one",
            [{"role": "user", "content": "Earlier"}],
        )
        events = [event async for event in client.events(run_id)]
        snapshot = await client.status(run_id)
        await client.stop(run_id)

        assert run_id == f"run_{'a' * 32}"
        assert snapshot["status"] == "completed"
        assert [event["event"] for event in events] == [
            "message.delta",
            "run.completed",
        ]

    asyncio.run(exercise())
    assert [request.url.path for request in requests] == [
        "/v1/capabilities",
        "/v1/runs",
        f"/v1/runs/run_{'a' * 32}/events",
        f"/v1/runs/run_{'a' * 32}",
        f"/v1/runs/run_{'a' * 32}/stop",
    ]


def test_malformed_capabilities_fail_before_submission() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert request.url.path == "/v1/capabilities"
        return httpx.Response(200, json=[])

    async def exercise() -> None:
        client = HermesClient(
            "http://hermes:8642",
            "test-key",
            httpx.MockTransport(handler),
        )

        with pytest.raises(HermesError, match="not compatible"):
            await client.submit_run("Hello", "session", "workspace", [])

    asyncio.run(exercise())
    assert calls == 1


def test_run_instructions_use_ephemeral_gateway_field() -> None:
    submitted: dict[str, object] = {}
    instructions = "é" * 2048

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/capabilities":
            return httpx.Response(
                200,
                json={
                    "object": "hermes.api_server.capabilities",
                    "platform": "hermes-agent",
                    "features": {
                        "approval_events": True,
                        "run_submission": True,
                        "run_status": True,
                        "run_events_sse": True,
                        "run_stop": True,
                        "session_resources": True,
                    },
                    "endpoints": {
                        "runs": {"method": "POST", "path": "/v1/runs"},
                        "run_status": {
                            "method": "GET",
                            "path": "/v1/runs/{run_id}",
                        },
                        "run_events": {
                            "method": "GET",
                            "path": "/v1/runs/{run_id}/events",
                        },
                        "run_stop": {
                            "method": "POST",
                            "path": "/v1/runs/{run_id}/stop",
                        },
                        "session_messages": {
                            "method": "GET",
                            "path": "/api/sessions/{session_id}/messages",
                        },
                    },
                },
            )
        submitted.update(json.loads(request.content))
        return httpx.Response(
            202,
            json={"run_id": f"run_{'a' * 32}", "status": "started"},
        )

    async def exercise() -> None:
        client = HermesClient(
            "http://hermes:8642",
            "test-key",
            httpx.MockTransport(handler),
        )
        await client.submit_run(
            "Resolve AAPL",
            "session",
            "workspace",
            [],
            instructions,
        )

    asyncio.run(exercise())
    assert submitted["instructions"] == instructions


def test_invalid_run_id_is_rejected_without_network_call() -> None:
    client = HermesClient(
        "http://hermes:8642",
        "test-key",
        httpx.MockTransport(lambda request: pytest.fail(str(request.url))),
    )

    async def exercise() -> None:
        with pytest.raises(HermesError, match="run ID"):
            await client.status("../run")

    asyncio.run(exercise())


@pytest.mark.parametrize(
    "instructions",
    [
        "   ",
        "x" * 4097,
        "é" * 2049,
        "\ud800",
        7,
    ],
)
def test_invalid_run_instructions_are_rejected_without_network_call(
    instructions: object,
) -> None:
    client = HermesClient(
        "http://hermes:8642",
        "test-key",
        httpx.MockTransport(lambda request: pytest.fail(str(request.url))),
    )

    async def exercise() -> None:
        with pytest.raises(HermesRunRejected, match="instructions"):
            await client.submit_run(
                "Hello",
                "session",
                "workspace",
                [],
                instructions,  # type: ignore[arg-type]
            )

    asyncio.run(exercise())


@pytest.mark.parametrize(
    ("response", "error_type"),
    [
        (httpx.Response(401), HermesRunRejected),
        (httpx.Response(500), HermesSubmissionUncertain),
    ],
)
def test_submission_errors_distinguish_rejection_from_uncertainty(
    response: httpx.Response,
    error_type: type[HermesError],
) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/capabilities":
            return httpx.Response(
                200,
                json={
                    "object": "hermes.api_server.capabilities",
                    "platform": "hermes-agent",
                    "features": {feature: True for feature in (
                        "approval_events",
                        "run_events_sse",
                        "run_status",
                        "run_stop",
                        "run_submission",
                        "session_resources",
                    )},
                    "endpoints": {
                        name: {"method": method, "path": path}
                        for name, (method, path) in {
                            "runs": ("POST", "/v1/runs"),
                            "run_status": ("GET", "/v1/runs/{run_id}"),
                            "run_events": ("GET", "/v1/runs/{run_id}/events"),
                            "run_stop": ("POST", "/v1/runs/{run_id}/stop"),
                            "session_messages": (
                                "GET",
                                "/api/sessions/{session_id}/messages",
                            ),
                        }.items()
                    },
                },
            )
        return response

    async def exercise() -> None:
        client = HermesClient(
            "http://hermes:8642",
            "test-key",
            httpx.MockTransport(handler),
        )
        with pytest.raises(error_type):
            await client.submit_run("Hello", "session", "workspace", [])

    asyncio.run(exercise())


def test_session_messages_are_bounded_and_drop_reasoning() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["authorization"] == "Bearer test-key"
        assert request.url.raw_path == b"/api/sessions/helm%3Aworkspace%3Aone/messages"
        return httpx.Response(
            200,
            json={
                "object": "list",
                "session_id": "compressed-tip",
                "data": [
                    {
                        "id": 7,
                        "session_id": "compressed-tip",
                        "role": "assistant",
                        "content": "",
                        "tool_calls": [],
                        "reasoning": "never expose this",
                        "reasoning_content": "or this",
                    }
                ],
            },
        )

    async def exercise() -> None:
        client = HermesClient(
            "http://hermes:8642",
            "test-key",
            httpx.MockTransport(handler),
        )
        transcript = await client.session_messages("helm:workspace:one")
        assert transcript.resolved_session_id == "compressed-tip"
        assert transcript.messages[0] == {
            "id": 7,
            "role": "assistant",
            "content": "",
            "tool_call_id": None,
            "tool_calls": [],
            "tool_name": None,
        }
        assert "reasoning" not in str(transcript)

    asyncio.run(exercise())


@pytest.mark.parametrize(
    ("response", "error_type"),
    [
        (httpx.Response(404), HermesSessionMissing),
        (httpx.Response(503), httpx.HTTPStatusError),
        (httpx.Response(200, content=b"not-json"), HermesError),
        (
            httpx.Response(200, content=b"x" * (MAX_SESSION_RESPONSE_BYTES + 1)),
            HermesError,
        ),
    ],
)
def test_session_message_failures_are_explicit(
    response: httpx.Response,
    error_type: type[Exception],
) -> None:
    async def exercise() -> None:
        client = HermesClient(
            "http://hermes:8642",
            "test-key",
            httpx.MockTransport(lambda request: response),
        )
        with pytest.raises(error_type):
            await client.session_messages("session")

    asyncio.run(exercise())
