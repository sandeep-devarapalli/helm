import asyncio
import json

import httpx
import pytest
from helm.integrations.hermes import HermesClient, HermesError


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


def test_missing_runs_capability_fails_before_submission() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert request.url.path == "/v1/capabilities"
        return httpx.Response(
            200,
            json={
                "object": "hermes.api_server.capabilities",
                "platform": "hermes-agent",
                "features": {},
                "endpoints": {},
            },
        )

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
