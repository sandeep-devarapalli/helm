import asyncio
from collections.abc import AsyncIterator
from typing import Any
from uuid import UUID

import helm.api.runs as runs_api
import httpx
from helm.api.runs import recover_orphaned_runs
from helm.domain.models import AgentRun, AgentRunStatus, Message, RunEvent, utc_now
from helm.integrations.hermes import (
    HermesRunRejected,
    HermesSubmissionUncertain,
    get_hermes_client,
)
from helm.main import app
from sqlalchemy import select
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
    ) -> None:
        self.projected_events = events or []
        self.submit_error = submit_error
        self.snapshot = status or {"status": "running"}
        self.stop_error = stop_error
        self.submissions: list[tuple[str, str, str, list[dict[str, str]]]] = []
        self.stop_attempts: list[str] = []
        self.stopped: list[str] = []

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
