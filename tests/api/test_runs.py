import asyncio
from collections.abc import AsyncIterator
from typing import Any
from uuid import UUID, uuid4

import helm.api.runs as runs_api
import httpx
import pytest
from helm.api.runs import (
    Reconciliation,
    persist_reconciliation,
    persisted_event_stream,
    reconcile_run_provenance,
    reconcile_transcript,
    recover_orphaned_runs,
)
from helm.database import Base
from helm.domain.models import (
    AgentRun,
    AgentRunStatus,
    Message,
    RunEvent,
    RunToolProvenance,
    ToolProvenanceStatus,
    utc_now,
)
from helm.integrations.hermes import (
    HermesRunRejected,
    HermesSessionMissing,
    HermesSubmissionUncertain,
    HermesTranscript,
    get_hermes_client,
)
from helm.main import app
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

HERMES_RUN_ID = "run_0123456789abcdef0123456789abcdef"


class FakeHermes:
    def __init__(
        self,
        *,
        events: list[dict[str, Any]] | None = None,
        submit_error: Exception | None = None,
        status: dict[str, Any] | None = None,
        stop_error: Exception | None = None,
        transcripts: list[HermesTranscript | Exception] | None = None,
    ) -> None:
        self.projected_events = events or []
        self.submit_error = submit_error
        self.snapshot = status or {"status": "running"}
        self.stop_error = stop_error
        self.transcripts = transcripts
        self.submissions: list[tuple[str, str, str, list[dict[str, str]]]] = []
        self.stop_attempts: list[str] = []
        self.stopped: list[str] = []
        self.session_message_calls = 0

    async def submit_run(
        self,
        content: str,
        session_id: str,
        session_key: str,
        history: list[dict[str, str]],
    ) -> str:
        self.submissions.append((content, session_id, session_key, history))
        if self.submit_error is not None:
            raise self.submit_error
        return HERMES_RUN_ID

    async def events(self, run_id: str) -> AsyncIterator[dict[str, Any]]:
        assert run_id == HERMES_RUN_ID
        for event in self.projected_events:
            yield event

    async def session_messages(self, session_id: str) -> HermesTranscript:
        self.session_message_calls += 1
        if self.transcripts is not None:
            transcript = self.transcripts[
                min(self.session_message_calls - 1, len(self.transcripts) - 1)
            ]
            if isinstance(transcript, Exception):
                raise transcript
            return transcript
        if self.session_message_calls == 1:
            raise HermesSessionMissing("new session")
        content = self.submissions[-1][0]
        output = next(
            (
                event.get("output")
                for event in reversed(self.projected_events)
                if event.get("event") == "run.completed"
            ),
            self.snapshot.get("output"),
        )
        messages: list[dict[str, Any]] = [
            {
                "id": 1,
                "role": "user",
                "content": content,
                "tool_call_id": None,
                "tool_calls": None,
                "tool_name": None,
            }
        ]
        if isinstance(output, str):
            messages.append(
                {
                    "id": 2,
                    "role": "assistant",
                    "content": output,
                    "tool_call_id": None,
                    "tool_calls": None,
                    "tool_name": None,
                }
            )
        return HermesTranscript(
            resolved_session_id=session_id,
            messages=tuple(messages),
        )

    async def status(self, run_id: str) -> dict[str, Any]:
        assert run_id == HERMES_RUN_ID
        return self.snapshot

    async def stop(self, run_id: str) -> None:
        self.stop_attempts.append(run_id)
        if self.stop_error is not None:
            error = self.stop_error
            self.stop_error = None
            raise error
        self.stopped.append(run_id)


def create_conversation(api_context) -> UUID:
    response = api_context.client.post(
        f"/workspaces/{api_context.workspace_a}/conversations",
        json={"title": "Hermes projection"},
    )
    assert response.status_code == 201
    return UUID(response.json()["id"])


def seed_run(
    api_context,
    conversation_id: UUID,
    *,
    status: AgentRunStatus = AgentRunStatus.SUCCEEDED,
    event_stream_complete: bool = True,
    events: list[tuple[str, dict[str, Any]]] | None = None,
) -> UUID:
    run_id = uuid4()

    async def seed() -> None:
        now = utc_now()
        active = status in {
            AgentRunStatus.SUBMITTING,
            AgentRunStatus.RUNNING,
            AgentRunStatus.INDETERMINATE,
        }
        run = AgentRun(
            id=run_id,
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            status=status.value,
            input="Persisted run",
            submission_attempted_at=now,
            started_at=now if status != AgentRunStatus.SUBMITTING else None,
            finished_at=None if active else now,
            hermes_run_id=HERMES_RUN_ID if status != AgentRunStatus.SUBMITTING else None,
            hermes_session_id=(
                f"helm:{api_context.workspace_a}:conversation:{conversation_id}"
                if status != AgentRunStatus.SUBMITTING
                else None
            ),
            event_stream_complete=event_stream_complete,
        )
        async with api_context.session_factory() as session:
            session.add(run)
            await session.flush()
            session.add_all(
                [
                    RunEvent(
                        workspace_id=api_context.workspace_a,
                        agent_run_id=run_id,
                        sequence_number=sequence,
                        event_type=event_type,
                        payload=payload,
                    )
                    for sequence, (event_type, payload) in enumerate(events or [])
                ]
            )
            await session.commit()

    asyncio.run(seed())
    return run_id


def test_run_projects_terminal_output(api_context) -> None:
    conversation_id = create_conversation(api_context)
    hermes = FakeHermes(
        events=[
            {"event": "reasoning.available", "text": "must not be stored"},
            {"event": "run.completed", "output": "AAPL.US Apple Inc."},
        ]
    )
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Resolve AAPL"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert response.status_code == 202, response.text
    run_id = UUID(response.json()["id"])

    async def inspect() -> None:
        async with api_context.session_factory() as session:
            run = await session.get(AgentRun, run_id)
            assert run is not None
            assert run.status == AgentRunStatus.SUCCEEDED.value
            assert run.hermes_run_id == HERMES_RUN_ID
            assert run.event_stream_complete is True
            messages = (
                await session.scalars(
                    select(Message)
                    .where(Message.conversation_id == run.conversation_id)
                    .order_by(Message.created_at, Message.id)
                )
            ).all()
            assert [(message.role, message.content) for message in messages] == [
                ("user", "Resolve AAPL"),
                ("assistant", "AAPL.US Apple Inc."),
            ]
            events = (
                await session.scalars(
                    select(RunEvent)
                    .where(RunEvent.agent_run_id == run.id)
                    .order_by(RunEvent.sequence_number)
                )
            ).all()
            assert [event.sequence_number for event in events] == [0, 1, 2, 3]
            assert [event.event_type for event in events] == [
                "run.submitting",
                "run.started",
                "reasoning.available",
                "run.completed",
            ]
            assert events[2].payload == {"available": True}

    asyncio.run(inspect())
    content, session_id, session_key, history = hermes.submissions[0]
    assert content == "Resolve AAPL"
    assert session_id == (
        f"helm:{api_context.workspace_a}:conversation:{conversation_id}"
    )
    assert session_key == f"helm:workspace:{api_context.workspace_a}"
    assert history == []


def test_terminal_run_reconciles_tool_provenance_idempotently(api_context) -> None:
    conversation_id = create_conversation(api_context)
    session_id = f"helm:{api_context.workspace_a}:conversation:{conversation_id}"
    transcript = HermesTranscript(
        resolved_session_id=f"{session_id}:compressed",
        messages=(
            {
                "id": 10,
                "role": "user",
                "content": "Resolve AAPL",
                "tool_call_id": None,
                "tool_calls": None,
                "tool_name": None,
            },
            {
                "id": 11,
                "role": "assistant",
                "content": "",
                "tool_call_id": None,
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {
                            "name": "search_symbol",
                            "arguments": '{"query":"AAPL"}',
                        },
                    }
                ],
                "tool_name": None,
            },
            {
                "id": 12,
                "role": "tool",
                "content": '{"symbol":"AAPL.US"}',
                "tool_call_id": "call_1",
                "tool_calls": None,
                "tool_name": "search_symbol",
            },
            {
                "id": 13,
                "role": "assistant",
                "content": "AAPL.US Apple Inc.",
                "tool_call_id": None,
                "tool_calls": None,
                "tool_name": None,
            },
        ),
    )
    hermes = FakeHermes(
        events=[{"event": "run.completed", "output": "AAPL.US Apple Inc."}],
        transcripts=[
            HermesTranscript(resolved_session_id=session_id, messages=()),
            transcript,
        ],
    )
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Resolve AAPL"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert response.status_code == 202
    run_id = UUID(response.json()["id"])
    base = (
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}"
    )
    detail = api_context.client.get(base)
    provenance = api_context.client.get(f"{base}/provenance")
    foreign = api_context.client.get(
        f"/workspaces/{api_context.workspace_b}/conversations/"
        f"{conversation_id}/runs/{run_id}/provenance"
    )

    assert detail.json()["tool_provenance_status"] == "complete"
    assert detail.json()["tool_provenance_complete"] is True
    assert detail.json()["structured_citations_available"] is False
    assert provenance.json()["status"] == "complete"
    assert provenance.json()["resolved_session_id"] == f"{session_id}:compressed"
    assert provenance.json()["items"] == [
        {
            "sequence_number": 0,
            "call_message_id": 11,
            "result_message_id": 12,
            "tool_call_id": "call_1",
            "tool_name": "search_symbol",
            "arguments": {"query": "AAPL"},
            "result": '{"symbol":"AAPL.US"}',
        }
    ]
    assert provenance.json()["structured_citations_available"] is False
    assert foreign.status_code == 404

    async def retry_and_inspect() -> None:
        await reconcile_run_provenance(
            api_context.session_factory,
            hermes,
            api_context.workspace_a,
            run_id,
        )
        async with api_context.session_factory() as session:
            tools = (
                await session.scalars(
                    select(RunToolProvenance).where(
                        RunToolProvenance.agent_run_id == run_id
                    )
                )
            ).all()
            messages = (
                await session.scalars(
                    select(Message).where(Message.conversation_id == conversation_id)
                )
            ).all()
            events = (
                await session.scalars(
                    select(RunEvent).where(RunEvent.agent_run_id == run_id)
                )
            ).all()
            assert len(tools) == 1
            assert len(messages) == 2
            assert len(events) == 3

    asyncio.run(retry_and_inspect())
    assert hermes.session_message_calls == 2


def test_missing_tool_result_is_partial_without_reconstructing_output(
    api_context,
) -> None:
    conversation_id = create_conversation(api_context)
    session_id = f"helm:{api_context.workspace_a}:conversation:{conversation_id}"
    hermes = FakeHermes(
        events=[{"event": "run.completed", "output": "Evidence is incomplete."}],
        transcripts=[
            HermesTranscript(resolved_session_id=session_id, messages=()),
            HermesTranscript(
                resolved_session_id=session_id,
                messages=(
                    {
                        "id": 1,
                        "role": "user",
                        "content": "Research AAPL",
                        "tool_call_id": None,
                        "tool_calls": None,
                        "tool_name": None,
                    },
                    {
                        "id": 2,
                        "role": "assistant",
                        "content": "",
                        "tool_call_id": None,
                        "tool_calls": [
                            {
                                "id": "call_missing",
                                "type": "function",
                                "function": {
                                    "name": "get_market_data",
                                    "arguments": '{"symbol":"AAPL.US"}',
                                },
                            }
                        ],
                        "tool_name": None,
                    },
                    {
                        "id": 3,
                        "role": "assistant",
                        "content": "Evidence is incomplete.",
                        "tool_call_id": None,
                        "tool_calls": None,
                        "tool_name": None,
                    },
                ),
            ),
        ],
    )
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research AAPL"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    run_id = response.json()["id"]
    provenance = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}/provenance"
    )
    assert provenance.json()["status"] == "partial"
    assert provenance.json()["reason"] == "missing_tool_result"
    assert provenance.json()["items"][0]["result"] is None


def test_tool_activity_after_terminal_output_is_conflicting() -> None:
    reconciliation = reconcile_transcript(
        HermesTranscript(
            resolved_session_id="session",
            messages=(
                {
                    "id": 1,
                    "role": "user",
                    "content": "Research AAPL",
                    "tool_call_id": None,
                    "tool_calls": None,
                    "tool_name": None,
                },
                {
                    "id": 2,
                    "role": "assistant",
                    "content": "Final answer",
                    "tool_call_id": None,
                    "tool_calls": None,
                    "tool_name": None,
                },
                {
                    "id": 3,
                    "role": "assistant",
                    "content": "",
                    "tool_call_id": None,
                    "tool_calls": [
                        {
                            "id": "late_call",
                            "type": "function",
                            "function": {
                                "name": "search_symbol",
                                "arguments": '{"query":"AAPL"}',
                            },
                        }
                    ],
                    "tool_name": None,
                },
                {
                    "id": 4,
                    "role": "tool",
                    "content": '{"symbol":"AAPL.US"}',
                    "tool_call_id": "late_call",
                    "tool_calls": None,
                    "tool_name": "search_symbol",
                },
            ),
        ),
        0,
        "Research AAPL",
        "Final answer",
    )

    assert reconciliation.status == ToolProvenanceStatus.CONFLICTING
    assert reconciliation.reason == "terminal_output_mismatch"


def test_whitespace_tool_call_id_is_conflicting() -> None:
    reconciliation = reconcile_transcript(
        HermesTranscript(
            resolved_session_id="session",
            messages=(
                {
                    "id": 1,
                    "role": "user",
                    "content": "Research AAPL",
                    "tool_call_id": None,
                    "tool_calls": None,
                    "tool_name": None,
                },
                {
                    "id": 2,
                    "role": "assistant",
                    "content": "",
                    "tool_call_id": None,
                    "tool_calls": [
                        {
                            "id": " ",
                            "type": "function",
                            "function": {
                                "name": "search_symbol",
                                "arguments": '{"query":"AAPL"}',
                            },
                        }
                    ],
                    "tool_name": None,
                },
                {
                    "id": 3,
                    "role": "assistant",
                    "content": "Final answer",
                    "tool_call_id": None,
                    "tool_calls": None,
                    "tool_name": None,
                },
            ),
        ),
        0,
        "Research AAPL",
        "Final answer",
    )

    assert reconciliation.status == ToolProvenanceStatus.CONFLICTING
    assert reconciliation.reason == "malformed_or_duplicate_tool_call"


def test_conflicting_or_unavailable_provenance_cannot_create_orders(
    api_context,
) -> None:
    conversation_id = create_conversation(api_context)
    session_id = f"helm:{api_context.workspace_a}:conversation:{conversation_id}"
    duplicate_call = {
        "id": "duplicate",
        "type": "function",
        "function": {
            "name": "search_symbol",
            "arguments": '{"query":"NVDA"}',
        },
    }
    hermes = FakeHermes(
        events=[{"event": "run.completed", "output": "No action taken."}],
        transcripts=[
            HermesTranscript(resolved_session_id=session_id, messages=()),
            HermesTranscript(
                resolved_session_id=session_id,
                messages=(
                    {
                        "id": 1,
                        "role": "user",
                        "content": "Research NVDA",
                        "tool_call_id": None,
                        "tool_calls": None,
                        "tool_name": None,
                    },
                    {
                        "id": 2,
                        "role": "assistant",
                        "content": "",
                        "tool_call_id": None,
                        "tool_calls": [duplicate_call, duplicate_call],
                        "tool_name": None,
                    },
                    {
                        "id": 3,
                        "role": "assistant",
                        "content": "No action taken.",
                        "tool_call_id": None,
                        "tool_calls": None,
                        "tool_name": None,
                    },
                ),
            ),
        ],
    )
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research NVDA"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    run_id = response.json()["id"]
    provenance = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}/provenance"
    )
    assert provenance.json()["status"] == "conflicting"
    assert provenance.json()["items"] == []
    assert "orders" not in Base.metadata.tables
    assert not any(
        "/orders" in path for path in api_context.client.get("/openapi.json").json()["paths"]
    )


def test_pre_submit_session_failure_stays_visibly_unavailable(api_context) -> None:
    conversation_id = create_conversation(api_context)
    hermes = FakeHermes(
        events=[{"event": "run.completed", "output": "Research completed."}],
        transcripts=[httpx.ReadTimeout("Hermes session store unavailable")],
    )
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research MSFT"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    run_id = response.json()["id"]
    provenance = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}/provenance"
    )
    assert provenance.json()["status"] == "unavailable"
    assert provenance.json()["reason"] == "pre_submit_transcript_unavailable"
    assert provenance.json()["items"] == []
    assert hermes.session_message_calls == 1


def test_stale_reconciliation_cannot_downgrade_accepted_provenance(
    api_context,
) -> None:
    conversation_id = create_conversation(api_context)
    run_id = seed_run(api_context, conversation_id)

    async def exercise() -> None:
        async with api_context.session_factory() as session:
            run = await session.get(AgentRun, run_id)
            assert run is not None
            run.tool_provenance_status = ToolProvenanceStatus.COMPLETE.value
            run.tool_provenance_reason = None
            session.add(
                RunToolProvenance(
                    workspace_id=api_context.workspace_a,
                    agent_run_id=run_id,
                    sequence_number=0,
                    call_message_id=1,
                    result_message_id=2,
                    tool_call_id="accepted_call",
                    tool_name="search_symbol",
                    arguments={"query": "AAPL"},
                    result='{"symbol":"AAPL.US"}',
                )
            )
            await session.commit()

        await persist_reconciliation(
            api_context.session_factory,
            api_context.workspace_a,
            run_id,
            Reconciliation(
                ToolProvenanceStatus.CONFLICTING,
                "stale_conflict",
            ),
            resolved_session_id="stale-session",
        )

        async with api_context.session_factory() as session:
            run = await session.get(AgentRun, run_id)
            tools = (
                await session.scalars(
                    select(RunToolProvenance).where(
                        RunToolProvenance.agent_run_id == run_id
                    )
                )
            ).all()
            assert run is not None
            assert run.tool_provenance_status == ToolProvenanceStatus.COMPLETE.value
            assert [tool.tool_call_id for tool in tools] == ["accepted_call"]

    asyncio.run(exercise())


def test_submission_failure_is_audited_without_retry(api_context) -> None:
    conversation_id = create_conversation(api_context)
    hermes = FakeHermes(
        submit_error=HermesSubmissionUncertain("ambiguous upstream timeout"),
    )
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research NVDA"},
        )
        retry = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research NVDA again"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert response.status_code == 202
    assert response.json()["status"] == AgentRunStatus.INDETERMINATE.value
    assert retry.status_code == 409
    assert len(hermes.submissions) == 1

    async def inspect() -> None:
        async with api_context.session_factory() as session:
            run = await session.scalar(
                select(AgentRun).where(AgentRun.conversation_id == conversation_id)
            )
            assert run is not None
            assert run.status == AgentRunStatus.INDETERMINATE.value
            assert run.event_stream_complete is False
            messages = (
                await session.scalars(
                    select(Message).where(Message.conversation_id == conversation_id)
                )
            ).all()
            assert messages == []
            events = (
                await session.scalars(
                    select(RunEvent)
                    .where(RunEvent.agent_run_id == run.id)
                    .order_by(RunEvent.sequence_number)
                )
            ).all()
            assert [event.event_type for event in events] == [
                "run.submitting",
                "run.indeterminate",
            ]
            assert "ambiguous upstream timeout" not in str(events[-1].payload)

    asyncio.run(inspect())


def test_definite_rejection_fails_without_locking_conversation(api_context) -> None:
    conversation_id = create_conversation(api_context)
    hermes = FakeHermes(submit_error=HermesRunRejected("unauthorized"))
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research NVDA"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert response.status_code == 502

    async def inspect() -> None:
        async with api_context.session_factory() as session:
            run = await session.scalar(
                select(AgentRun).where(AgentRun.conversation_id == conversation_id)
            )
            assert run is not None
            assert run.status == AgentRunStatus.FAILED.value
            assert run.finished_at is not None

    asyncio.run(inspect())


def test_active_run_and_workspace_boundaries_fail_closed(api_context) -> None:
    conversation_id = create_conversation(api_context)

    async def seed_active_run() -> None:
        async with api_context.session_factory() as session:
            session.add(
                AgentRun(
                    workspace_id=api_context.workspace_a,
                    conversation_id=conversation_id,
                )
            )
            await session.commit()

    asyncio.run(seed_active_run())
    hermes = FakeHermes()
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        conflict = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Duplicate"},
        )
        foreign = api_context.client.post(
            f"/workspaces/{api_context.workspace_b}/conversations/{conversation_id}/runs",
            json={"content": "Cross workspace"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert conflict.status_code == 409
    assert foreign.status_code == 404
    assert hermes.submissions == []


def test_projection_gap_reconciles_terminal_status(api_context) -> None:
    conversation_id = create_conversation(api_context)
    hermes = FakeHermes(
        status={
            "status": "completed",
            "output": "Recovered final output",
            "usage": {"total_tokens": 5},
        }
    )
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research AMD"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert response.status_code == 202

    async def inspect() -> None:
        async with api_context.session_factory() as session:
            run = await session.scalar(
                select(AgentRun).where(AgentRun.conversation_id == conversation_id)
            )
            assert run is not None
            assert run.status == AgentRunStatus.SUCCEEDED.value
            assert run.event_stream_complete is False

    asyncio.run(inspect())


def test_approval_stop_retries_without_abandoning_stream(api_context) -> None:
    conversation_id = create_conversation(api_context)
    hermes = FakeHermes(
        events=[
            {"event": "approval.request", "choices": ["once", "deny"]},
            {"event": "run.cancelled"},
        ],
        status={"status": "waiting_for_approval"},
        stop_error=httpx.ReadTimeout("ambiguous stop"),
    )
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Unexpected approval"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert response.status_code == 202

    async def inspect() -> None:
        async with api_context.session_factory() as session:
            run = await session.scalar(
                select(AgentRun).where(AgentRun.conversation_id == conversation_id)
            )
            assert run is not None
            assert run.status == AgentRunStatus.CANCELLED.value
            assert run.finished_at is not None

    asyncio.run(inspect())
    assert hermes.stopped == [HERMES_RUN_ID]


def test_projection_database_failure_stops_upstream_and_fails_closed(
    api_context,
    monkeypatch,
) -> None:
    conversation_id = create_conversation(api_context)
    hermes = FakeHermes(
        events=[{"event": "tool.started", "tool": "search_symbol"}],
        status={"status": "running"},
    )
    original = runs_api.persist_projected_event
    failed = False

    async def fail_once(*args, **kwargs) -> None:
        nonlocal failed
        if not failed:
            failed = True
            raise SQLAlchemyError("transient persistence failure")
        await original(*args, **kwargs)

    monkeypatch.setattr(runs_api, "persist_projected_event", fail_once)
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research failure path"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert response.status_code == 202
    assert hermes.stopped == [HERMES_RUN_ID]

    async def inspect() -> None:
        async with api_context.session_factory() as session:
            run = await session.scalar(
                select(AgentRun).where(AgentRun.conversation_id == conversation_id)
            )
            assert run is not None
            assert run.status == AgentRunStatus.INDETERMINATE.value

    asyncio.run(inspect())


def test_correlation_commit_failure_stops_accepted_run(
    api_context,
    monkeypatch,
) -> None:
    conversation_id = create_conversation(api_context)
    hermes = FakeHermes(status={"status": "stopping"})
    original_commit = AsyncSession.commit
    commit_count = 0

    async def fail_second_commit(session) -> None:
        nonlocal commit_count
        commit_count += 1
        if commit_count == 2:
            raise SQLAlchemyError("correlation commit failed")
        await original_commit(session)

    monkeypatch.setattr(AsyncSession, "commit", fail_second_commit)
    app.dependency_overrides[get_hermes_client] = lambda: hermes
    try:
        response = api_context.client.post(
            f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs",
            json={"content": "Research correlation failure"},
        )
    finally:
        app.dependency_overrides.pop(get_hermes_client, None)

    assert response.status_code == 202
    assert response.json()["status"] == AgentRunStatus.INDETERMINATE.value
    assert hermes.stopped == [HERMES_RUN_ID]

    async def inspect() -> None:
        async with api_context.session_factory() as session:
            run = await session.scalar(
                select(AgentRun).where(AgentRun.conversation_id == conversation_id)
            )
            messages = (
                await session.scalars(
                    select(Message).where(Message.conversation_id == conversation_id)
                )
            ).all()
            assert run is not None
            assert run.status == AgentRunStatus.INDETERMINATE.value
            assert run.hermes_run_id == HERMES_RUN_ID
            assert messages == []

    asyncio.run(inspect())


def test_startup_recovery_marks_orphaned_projection_indeterminate(api_context) -> None:
    conversation_id = create_conversation(api_context)
    queued_conversation_id = create_conversation(api_context)

    async def exercise() -> None:
        async with api_context.session_factory() as session:
            run = AgentRun(
                workspace_id=api_context.workspace_a,
                conversation_id=conversation_id,
                status=AgentRunStatus.RUNNING.value,
                input="Interrupted run",
                submission_attempted_at=utc_now(),
                started_at=utc_now(),
                hermes_run_id=HERMES_RUN_ID,
                hermes_session_id=(
                    f"helm:{api_context.workspace_a}:conversation:{conversation_id}"
                ),
            )
            queued = AgentRun(
                workspace_id=api_context.workspace_a,
                conversation_id=queued_conversation_id,
            )
            session.add_all([run, queued])
            await session.commit()
        unresolved = await recover_orphaned_runs(api_context.session_factory)
        assert unresolved == [HERMES_RUN_ID]
        async with api_context.session_factory() as session:
            persisted = await session.get(AgentRun, run.id)
            persisted_queued = await session.get(AgentRun, queued.id)
            assert persisted is not None
            assert persisted_queued is not None
            assert persisted.status == AgentRunStatus.INDETERMINATE.value
            assert persisted.finished_at is None
            assert persisted_queued.status == AgentRunStatus.FAILED.value
            assert persisted_queued.finished_at is not None

    asyncio.run(exercise())


def test_startup_recovery_queues_indeterminate_cleanup_without_network(api_context) -> None:
    conversation_id = create_conversation(api_context)

    async def exercise() -> None:
        async with api_context.session_factory() as session:
            run = AgentRun(
                workspace_id=api_context.workspace_a,
                conversation_id=conversation_id,
                status=AgentRunStatus.INDETERMINATE.value,
                input="Missing upstream run",
                submission_attempted_at=utc_now(),
                started_at=utc_now(),
                hermes_run_id=HERMES_RUN_ID,
                hermes_session_id=f"helm:{api_context.workspace_a}:conversation:{conversation_id}",
            )
            session.add(run)
            await session.commit()
        unresolved = await asyncio.wait_for(
            recover_orphaned_runs(api_context.session_factory),
            timeout=0.5,
        )
        assert unresolved == [HERMES_RUN_ID]
        async with api_context.session_factory() as session:
            persisted = await session.get(AgentRun, run.id)
            assert persisted is not None
            assert persisted.status == AgentRunStatus.INDETERMINATE.value

    asyncio.run(exercise())


def test_run_event_reads_are_scoped_and_resumable(api_context) -> None:
    conversation_id = create_conversation(api_context)
    other_conversation_id = create_conversation(api_context)
    run_id = seed_run(
        api_context,
        conversation_id,
        events=[
            ("run.submitting", {}),
            ("run.started", {"hermes_run_id": HERMES_RUN_ID}),
            ("tool.started", {"tool": "search_symbol"}),
            ("run.completed", {"output": "AAPL.US"}),
        ],
    )
    base = (
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}"
    )

    detail = api_context.client.get(base)
    first_page = api_context.client.get(f"{base}/events", params={"limit": 2})
    second_page = api_context.client.get(
        f"{base}/events",
        params={"after": first_page.json()["next_cursor"], "limit": 2},
    )
    resumed = api_context.client.get(
        f"{base}/events/stream",
        params={"after": 0},
        headers={"Last-Event-ID": "1"},
    )

    assert detail.status_code == 200
    assert detail.json()["event_stream_complete"] is True
    assert detail.json()["projection_gap"] is False
    assert detail.json()["tool_provenance_complete"] is False
    for suffix in ("", "/events", "/events/stream"):
        assert api_context.client.get(
            f"/workspaces/{api_context.workspace_b}/conversations/"
            f"{conversation_id}/runs/{run_id}{suffix}"
        ).status_code == 404
        assert api_context.client.get(
            f"/workspaces/{api_context.workspace_a}/conversations/"
            f"{other_conversation_id}/runs/{run_id}{suffix}"
        ).status_code == 404
    assert [item["sequence_number"] for item in first_page.json()["items"]] == [0, 1]
    assert first_page.json()["next_cursor"] == 1
    assert [item["sequence_number"] for item in second_page.json()["items"]] == [2, 3]
    assert second_page.json()["next_cursor"] is None
    assert second_page.json()["tool_provenance_complete"] is False
    assert resumed.status_code == 200
    assert resumed.headers["content-type"].startswith("text/event-stream")
    assert "id: 0\n" not in resumed.text
    assert "id: 1\n" not in resumed.text
    assert "id: 2\n" in resumed.text
    assert "id: 3\n" in resumed.text
    assert resumed.text.count("event: run-event\n") == 2
    assert '"event_type":"run.completed"' in resumed.text
    assert '"tool_provenance_complete":false' in resumed.text


def test_incomplete_terminal_projection_is_explicit_and_closes(api_context) -> None:
    conversation_id = create_conversation(api_context)
    run_id = seed_run(
        api_context,
        conversation_id,
        status=AgentRunStatus.FAILED,
        event_stream_complete=False,
        events=[
            ("run.started", {"hermes_run_id": HERMES_RUN_ID}),
            ("run.failed", {"error": "projection failed", "projection_gap": True}),
        ],
    )
    base = (
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}"
    )

    detail = api_context.client.get(base)
    events = api_context.client.get(f"{base}/events")
    stream = api_context.client.get(f"{base}/events/stream")

    assert detail.json()["event_stream_complete"] is False
    assert detail.json()["projection_gap"] is True
    assert events.json()["event_stream_complete"] is False
    assert events.json()["projection_gap"] is True
    assert stream.status_code == 200
    assert "id: 1\n" in stream.text
    assert '"projection_gap":true' in stream.text


def test_event_cursors_and_payloads_fail_closed(api_context) -> None:
    conversation_id = create_conversation(api_context)
    oversized = "x" * (runs_api.MAX_EVENT_PAYLOAD_BYTES + 1)
    run_id = seed_run(
        api_context,
        conversation_id,
        events=[
            ("future.event", {"nested": ["preserved", 1]}),
            ("future.large", {"text": oversized}),
        ],
    )
    base = (
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}"
    )

    events = api_context.client.get(f"{base}/events")
    future_cursor = api_context.client.get(f"{base}/events", params={"after": 99})
    oversized_cursor = api_context.client.get(
        f"{base}/events",
        params={"after": runs_api.MAX_SEQUENCE_NUMBER + 1},
    )
    malformed_header = api_context.client.get(
        f"{base}/events/stream",
        headers={"Last-Event-ID": "not-a-sequence"},
    )
    oversized_header = api_context.client.get(
        f"{base}/events/stream",
        headers={"Last-Event-ID": str(runs_api.MAX_SEQUENCE_NUMBER + 1)},
    )

    assert events.status_code == 200
    assert events.json()["items"][0]["payload"] == {"nested": ["preserved", 1]}
    assert events.json()["items"][1]["payload"] == {
        "unavailable": True,
        "reason": "malformed_or_oversized_payload",
    }
    assert future_cursor.status_code == 422
    assert oversized_cursor.status_code == 422
    assert malformed_header.status_code == 422
    assert oversized_header.status_code == 422


def test_persisted_sequence_gap_fails_before_streaming(api_context) -> None:
    conversation_id = create_conversation(api_context)
    run_id = seed_run(
        api_context,
        conversation_id,
        events=[
            ("run.submitting", {}),
            ("run.started", {}),
            ("run.completed", {}),
        ],
    )

    async def remove_middle_event() -> None:
        async with api_context.session_factory() as session:
            await session.execute(
                delete(RunEvent).where(
                    RunEvent.agent_run_id == run_id,
                    RunEvent.sequence_number == 1,
                )
            )
            await session.commit()

    asyncio.run(remove_middle_event())
    base = (
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}"
    )

    assert api_context.client.get(f"{base}/events").status_code == 409
    assert api_context.client.get(f"{base}/events/stream").status_code == 409


@pytest.mark.parametrize(
    "payload",
    [
        {"value": float("nan")},
        {"value": "\ud800"},
        ["not", "an", "object"],
    ],
)
def test_public_event_replaces_malformed_json_payload(payload: Any) -> None:
    event = RunEvent(
        workspace_id=uuid4(),
        agent_run_id=uuid4(),
        sequence_number=0,
        event_type="future.event",
        payload=payload,
        created_at=utc_now(),
    )

    assert runs_api.public_event(event).payload == {
        "unavailable": True,
        "reason": "malformed_or_oversized_payload",
    }


def test_terminal_stream_drains_every_persisted_batch(api_context) -> None:
    conversation_id = create_conversation(api_context)
    event_count = runs_api.EVENT_PAGE_LIMIT + 2
    run_id = seed_run(
        api_context,
        conversation_id,
        events=[
            *[
                ("message.delta", {"delta": str(sequence)})
                for sequence in range(event_count - 1)
            ],
            ("run.completed", {"output": "complete"}),
        ],
    )
    response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/"
        f"{conversation_id}/runs/{run_id}/events/stream"
    )
    delivered = [
        int(line.removeprefix("id: "))
        for line in response.text.splitlines()
        if line.startswith("id: ")
    ]

    assert response.status_code == 200
    assert delivered == list(range(event_count))


def test_projection_rejects_events_after_closed_run(api_context) -> None:
    conversation_id = create_conversation(api_context)
    run_id = seed_run(
        api_context,
        conversation_id,
        status=AgentRunStatus.RUNNING,
        event_stream_complete=False,
    )

    async def exercise() -> None:
        await runs_api.persist_projected_event(
            api_context.session_factory,
            api_context.workspace_a,
            run_id,
            "run.completed",
            {"output": "complete"},
            stream_complete=True,
        )
        await runs_api.persist_projected_event(
            api_context.session_factory,
            api_context.workspace_a,
            run_id,
            "tool.completed",
            {"tool": "late"},
        )
        async with api_context.session_factory() as session:
            events = (
                await session.scalars(
                    select(RunEvent.event_type)
                    .where(RunEvent.agent_run_id == run_id)
                    .order_by(RunEvent.sequence_number)
                )
            ).all()
            assert list(events) == ["run.completed"]

    asyncio.run(exercise())


def test_active_stream_heartbeat_is_only_an_sse_comment(api_context, monkeypatch) -> None:
    conversation_id = create_conversation(api_context)
    run_id = seed_run(
        api_context,
        conversation_id,
        status=AgentRunStatus.RUNNING,
        event_stream_complete=False,
    )
    monkeypatch.setattr(runs_api, "SSE_HEARTBEAT_SECONDS", 0.0)
    monkeypatch.setattr(runs_api, "SSE_POLL_INTERVAL_SECONDS", 0.0)

    class ConnectedRequest:
        async def is_disconnected(self) -> bool:
            return False

    async def read_heartbeat() -> str:
        stream = persisted_event_stream(
            ConnectedRequest(),  # type: ignore[arg-type]
            api_context.session_factory,
            api_context.workspace_a,
            conversation_id,
            run_id,
            -1,
        )
        try:
            return await anext(stream)
        finally:
            await stream.aclose()

    assert asyncio.run(read_heartbeat()) == ": keep-alive\n\n"


def test_postgres_concurrent_projection_closes_with_contiguous_sequences(
    api_context,
) -> None:
    conversation_id = create_conversation(api_context)
    run_id = seed_run(
        api_context,
        conversation_id,
        status=AgentRunStatus.RUNNING,
        event_stream_complete=False,
    )

    async def exercise() -> None:
        async with api_context.session_factory() as session:
            if session.bind is None or session.bind.dialect.name != "postgresql":
                pytest.skip("PostgreSQL row-lock behavior")
        await asyncio.gather(
            runs_api.persist_projected_event(
                api_context.session_factory,
                api_context.workspace_a,
                run_id,
                "tool.started",
                {"tool": "search_symbol"},
            ),
            runs_api.persist_projected_event(
                api_context.session_factory,
                api_context.workspace_a,
                run_id,
                "run.completed",
                {"output": "complete"},
                stream_complete=True,
            ),
            runs_api.persist_projected_event(
                api_context.session_factory,
                api_context.workspace_a,
                run_id,
                "tool.completed",
                {"tool": "late"},
            ),
        )
        async with api_context.session_factory() as session:
            events = (
                await session.execute(
                    select(RunEvent.sequence_number, RunEvent.event_type)
                    .where(RunEvent.agent_run_id == run_id)
                    .order_by(RunEvent.sequence_number)
                )
            ).all()
            assert [sequence for sequence, _ in events] == list(range(len(events)))
            assert events[-1].event_type == "run.completed"

    asyncio.run(exercise())
