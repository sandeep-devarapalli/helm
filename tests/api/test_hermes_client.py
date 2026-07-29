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
                    "features": {
                        "run_submission": True,
                        "run_status": True,
                        "run_events_sse": True,
                    }
                },
            )
        if request.url.path == "/v1/runs":
            assert json.loads(request.content) == {
                "input": "Resolve AAPL",
                "session_id": "helm:workspace:conversation:one",
                "conversation_history": [{"role": "user", "content": "Earlier"}],
            }
            return httpx.Response(202, json={"run_id": "run_123", "status": "started"})
        if request.url.path == "/v1/runs/run_123/events":
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
            [{"role": "user", "content": "Earlier"}],
        )
        events = [event async for event in client.events(run_id)]

        assert run_id == "run_123"
        assert [event["event"] for event in events] == [
            "message.delta",
            "run.completed",
        ]

    asyncio.run(exercise())
    assert [request.url.path for request in requests] == [
        "/v1/capabilities",
        "/v1/runs",
        "/v1/runs/run_123/events",
    ]


def test_missing_runs_capability_fails_before_submission() -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert request.url.path == "/v1/capabilities"
        return httpx.Response(200, json={"features": {}})

    async def exercise() -> None:
        client = HermesClient(
            "http://hermes:8642",
            "test-key",
            httpx.MockTransport(handler),
        )

        with pytest.raises(HermesError, match="not compatible"):
            await client.submit_run("Hello", "session", [])

    asyncio.run(exercise())
    assert calls == 1
