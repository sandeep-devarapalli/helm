import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any, cast
from uuid import UUID

import httpx
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from helm.database import get_session
from helm.domain.models import (
    AgentRun,
    AgentRunStatus,
    Conversation,
    Message,
    MessageRole,
    RunEvent,
    utc_now,
)
from helm.integrations.hermes import (
    HermesClient,
    HermesError,
    HermesRunMissing,
    HermesRunRejected,
    HermesSubmissionUncertain,
    get_hermes_client,
)

router = APIRouter(prefix="/workspaces/{workspace_id}/conversations", tags=["runs"])
Session = Annotated[AsyncSession, Depends(get_session)]
Hermes = Annotated[HermesClient, Depends(get_hermes_client)]
ACTIVE_STATUSES = {
    AgentRunStatus.QUEUED.value,
    AgentRunStatus.SUBMITTING.value,
    AgentRunStatus.RUNNING.value,
    AgentRunStatus.INDETERMINATE.value,
}
TERMINAL_EVENTS = {"run.completed", "run.failed", "run.cancelled"}
SAFE_EVENT_FIELDS = {
    "message.delta": ("delta",),
    "tool.started": ("tool", "preview"),
    "tool.completed": ("tool", "duration", "error"),
    "reasoning.available": (),
    "approval.request": ("choices",),
    "approval.responded": ("choice", "resolved"),
    "run.completed": ("output", "usage"),
    "run.failed": ("error",),
    "run.cancelled": (),
}


@dataclass(frozen=True)
class StopResolution:
    resolved: bool
    terminal_snapshot: dict[str, Any] | None = None


class RunCreate(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def normalize_content(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 20_000:
            raise ValueError("content must contain between 1 and 20000 characters")
        return normalized


class RunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    conversation_id: UUID
    status: str
    hermes_run_id: str | None
    hermes_session_id: str | None
    event_stream_complete: bool
    created_at: datetime


def request_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    return cast(async_sessionmaker[AsyncSession], request.app.state.session_factory)


def safe_event(event: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    event_type = event.get("event")
    if not isinstance(event_type, str) or event_type not in SAFE_EVENT_FIELDS:
        return "hermes.unknown", {}
    payload = {
        key: event[key] for key in SAFE_EVENT_FIELDS[event_type] if key in event
    }
    if event_type == "reasoning.available":
        payload["available"] = True
    return event_type, payload


async def mark_indeterminate(
    session_factory: async_sessionmaker[AsyncSession],
    workspace_id: UUID,
    run_id: UUID,
    reason: str,
    *,
    hermes_run_id: str | None = None,
) -> None:
    async with session_factory() as session:
        run = await session.scalar(
            select(AgentRun)
            .where(AgentRun.id == run_id, AgentRun.workspace_id == workspace_id)
            .with_for_update()
        )
        if run is None or run.finished_at is not None:
            return
        if run.status == AgentRunStatus.INDETERMINATE.value:
            return
        last_sequence = await session.scalar(
            select(func.max(RunEvent.sequence_number)).where(
                RunEvent.workspace_id == workspace_id,
                RunEvent.agent_run_id == run_id,
            )
        )
        session.add(
            RunEvent(
                workspace_id=workspace_id,
                agent_run_id=run_id,
                sequence_number=(last_sequence if last_sequence is not None else -1) + 1,
                event_type="run.indeterminate",
                payload={"reason": reason, "projection_gap": True},
            )
        )
        run.status = AgentRunStatus.INDETERMINATE.value
        run.finished_at = None
        run.event_stream_complete = False
        if run.hermes_run_id is None and hermes_run_id is not None:
            run.hermes_run_id = hermes_run_id
        await session.commit()


async def mark_rejected(
    session_factory: async_sessionmaker[AsyncSession],
    workspace_id: UUID,
    run_id: UUID,
    reason: str,
) -> None:
    async with session_factory() as session:
        run = await session.scalar(
            select(AgentRun)
            .where(AgentRun.id == run_id, AgentRun.workspace_id == workspace_id)
            .with_for_update()
        )
        if run is None or run.finished_at is not None:
            return
        last_sequence = await session.scalar(
            select(func.max(RunEvent.sequence_number)).where(
                RunEvent.workspace_id == workspace_id,
                RunEvent.agent_run_id == run_id,
            )
        )
        session.add(
            RunEvent(
                workspace_id=workspace_id,
                agent_run_id=run_id,
                sequence_number=(last_sequence if last_sequence is not None else -1) + 1,
                event_type="run.rejected",
                payload={"reason": reason},
            )
        )
        run.status = AgentRunStatus.FAILED.value
        run.finished_at = utc_now()
        await session.commit()


async def recover_orphaned_runs(
    session_factory: async_sessionmaker[AsyncSession],
) -> list[str]:
    unresolved_cleanup: list[str] = []
    async with session_factory() as session:
        orphaned = (
            await session.execute(
                select(
                    AgentRun.workspace_id,
                    AgentRun.id,
                    AgentRun.status,
                    AgentRun.hermes_run_id,
                ).where(AgentRun.status.in_(ACTIVE_STATUSES))
            )
        ).all()
    for workspace_id, run_id, run_status, hermes_run_id in orphaned:
        if run_status == AgentRunStatus.QUEUED.value:
            await mark_rejected(
                session_factory,
                workspace_id,
                run_id,
                "Legacy queued run cannot be correlated after restart",
            )
            continue
        if run_status == AgentRunStatus.INDETERMINATE.value:
            if hermes_run_id is not None:
                unresolved_cleanup.append(hermes_run_id)
            continue
        if run_status == AgentRunStatus.RUNNING.value and hermes_run_id is not None:
            unresolved_cleanup.append(hermes_run_id)
        await mark_indeterminate(
            session_factory,
            workspace_id,
            run_id,
            "API restarted before Hermes projection reached a terminal state",
        )
    return unresolved_cleanup


async def persist_projected_event(
    session_factory: async_sessionmaker[AsyncSession],
    workspace_id: UUID,
    run_id: UUID,
    event_type: str,
    payload: dict[str, Any],
    *,
    stream_complete: bool = False,
) -> None:
    async with session_factory() as session:
        run = await session.scalar(
            select(AgentRun)
            .where(AgentRun.id == run_id, AgentRun.workspace_id == workspace_id)
            .with_for_update()
        )
        if run is None or (event_type in TERMINAL_EVENTS and run.finished_at is not None):
            return
        last_sequence = await session.scalar(
            select(func.max(RunEvent.sequence_number)).where(
                RunEvent.workspace_id == workspace_id,
                RunEvent.agent_run_id == run_id,
            )
        )
        session.add(
            RunEvent(
                workspace_id=workspace_id,
                agent_run_id=run_id,
                sequence_number=(last_sequence if last_sequence is not None else -1) + 1,
                event_type=event_type,
                payload=payload,
            )
        )
        if event_type in TERMINAL_EVENTS:
            run.finished_at = utc_now()
            run.event_stream_complete = stream_complete
            if event_type == "run.completed":
                run.status = AgentRunStatus.SUCCEEDED.value
                output = payload.get("output")
                if isinstance(output, str) and output.strip():
                    session.add(
                        Message(
                            workspace_id=workspace_id,
                            conversation_id=run.conversation_id,
                            role=MessageRole.ASSISTANT.value,
                            content=output,
                        )
                    )
            elif event_type == "run.cancelled":
                run.status = AgentRunStatus.CANCELLED.value
            else:
                run.status = AgentRunStatus.FAILED.value
        await session.commit()


async def stop_run_until_resolved(
    hermes: HermesClient,
    hermes_run_id: str,
    *,
    max_attempts: int | None = None,
) -> StopResolution:
    attempts = 0
    while max_attempts is None or attempts < max_attempts:
        attempts += 1
        try:
            await hermes.stop(hermes_run_id)
            return StopResolution(resolved=True)
        except HermesRunMissing:
            return StopResolution(resolved=True)
        except (HermesError, httpx.HTTPError, ValueError):
            try:
                snapshot = await hermes.status(hermes_run_id)
                if snapshot.get("status") in {"completed", "failed", "cancelled"}:
                    return StopResolution(resolved=True, terminal_snapshot=snapshot)
                if snapshot.get("status") == "stopping":
                    return StopResolution(resolved=True)
            except HermesRunMissing:
                return StopResolution(resolved=True)
            except (HermesError, httpx.HTTPError, ValueError):
                pass
            if max_attempts is None or attempts < max_attempts:
                await asyncio.sleep(1)
    return StopResolution(resolved=False)


async def cleanup_upstream_run(
    hermes: HermesClient,
    hermes_run_id: str,
) -> None:
    await stop_run_until_resolved(hermes, hermes_run_id)


async def finalize_projection_failure(
    session_factory: async_sessionmaker[AsyncSession],
    hermes: HermesClient,
    workspace_id: UUID,
    run_id: UUID,
    hermes_run_id: str,
) -> None:
    terminal_snapshot: dict[str, Any] | None = None
    try:
        snapshot = await hermes.status(hermes_run_id)
        if snapshot.get("status") in {"completed", "failed", "cancelled"}:
            terminal_snapshot = snapshot
    except (HermesError, httpx.HTTPError, ValueError):
        pass
    if terminal_snapshot is None:
        resolution = await stop_run_until_resolved(hermes, hermes_run_id)
        terminal_snapshot = resolution.terminal_snapshot
    if terminal_snapshot is not None:
        payload = {
            key: terminal_snapshot[key]
            for key in ("output", "usage", "error")
            if key in terminal_snapshot
        }
        payload["projection_gap"] = True
        try:
            await persist_projected_event(
                session_factory,
                workspace_id,
                run_id,
                f"run.{terminal_snapshot['status']}",
                payload,
            )
            return
        except SQLAlchemyError:
            pass
    while True:
        try:
            await mark_indeterminate(
                session_factory,
                workspace_id,
                run_id,
                "Hermes projection failed before durable terminal state",
            )
            return
        except SQLAlchemyError:
            await asyncio.sleep(1)


async def project_run(
    session_factory: async_sessionmaker[AsyncSession],
    hermes: HermesClient,
    workspace_id: UUID,
    run_id: UUID,
    hermes_run_id: str,
) -> None:
    try:
        async for upstream_event in hermes.events(hermes_run_id):
            event_type, payload = safe_event(upstream_event)
            await persist_projected_event(
                session_factory,
                workspace_id,
                run_id,
                event_type,
                payload,
                stream_complete=event_type in TERMINAL_EVENTS,
            )
            if event_type == "approval.request":
                resolution = await stop_run_until_resolved(hermes, hermes_run_id)
                terminal_snapshot = resolution.terminal_snapshot
                if terminal_snapshot is not None:
                    upstream_status = terminal_snapshot["status"]
                    terminal_payload = {
                        key: terminal_snapshot[key]
                        for key in ("output", "usage", "error")
                        if key in terminal_snapshot
                    }
                    terminal_payload["projection_gap"] = True
                    await persist_projected_event(
                        session_factory,
                        workspace_id,
                        run_id,
                        f"run.{upstream_status}",
                        terminal_payload,
                    )
                    return
            if event_type in TERMINAL_EVENTS:
                return
    except (HermesError, httpx.HTTPError, ValueError, SQLAlchemyError):
        await finalize_projection_failure(
            session_factory,
            hermes,
            workspace_id,
            run_id,
            hermes_run_id,
        )
        return

    try:
        snapshot = await hermes.status(hermes_run_id)
        upstream_status = snapshot.get("status")
        if upstream_status in {"completed", "failed", "cancelled"}:
            payload = {
                key: snapshot[key]
                for key in ("output", "usage", "error")
                if key in snapshot
            }
            payload["projection_gap"] = True
            await persist_projected_event(
                session_factory,
                workspace_id,
                run_id,
                f"run.{upstream_status}",
                payload,
            )
            return
        resolution = await stop_run_until_resolved(hermes, hermes_run_id)
        terminal_snapshot = resolution.terminal_snapshot
        if terminal_snapshot is not None:
            payload = {
                key: terminal_snapshot[key]
                for key in ("output", "usage", "error")
                if key in terminal_snapshot
            }
            payload["projection_gap"] = True
            await persist_projected_event(
                session_factory,
                workspace_id,
                run_id,
                f"run.{terminal_snapshot['status']}",
                payload,
            )
            return
        await mark_indeterminate(
            session_factory,
            workspace_id,
            run_id,
            "Hermes event stream ended while the run was stopping",
        )
    except (HermesError, httpx.HTTPError, ValueError, SQLAlchemyError):
        await finalize_projection_failure(
            session_factory,
            hermes,
            workspace_id,
            run_id,
            hermes_run_id,
        )


@router.post(
    "/{conversation_id}/runs",
    response_model=RunResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_run(
    workspace_id: UUID,
    conversation_id: UUID,
    body: RunCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session,
    hermes: Hermes,
) -> AgentRun:
    session_factory = request_session_factory(request)
    conversation = await session.scalar(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.workspace_id == workspace_id,
        )
    )
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="conversation not found")
    history = [
        {"role": message.role, "content": message.content}
        for message in (
            await session.scalars(
                select(Message)
                .where(
                    Message.workspace_id == workspace_id,
                    Message.conversation_id == conversation_id,
                    Message.role.in_((MessageRole.USER.value, MessageRole.ASSISTANT.value)),
                )
                .order_by(Message.created_at, Message.id)
            )
        ).all()
    ]
    hermes_session_id = f"helm:{workspace_id}:conversation:{conversation_id}"
    hermes_session_key = f"helm:workspace:{workspace_id}"
    run = AgentRun(
        workspace_id=workspace_id,
        conversation_id=conversation_id,
        status=AgentRunStatus.SUBMITTING.value,
        input=body.content,
        submission_attempted_at=utc_now(),
        hermes_session_id=hermes_session_id,
    )
    session.add(run)
    try:
        await session.flush()
        session.add(
            RunEvent(
                workspace_id=workspace_id,
                agent_run_id=run.id,
                sequence_number=0,
                event_type="run.submitting",
                payload={},
            )
        )
        await session.commit()
    except IntegrityError as error:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="conversation already has an active run",
        ) from error
    run_id = run.id

    try:
        hermes_run_id = await hermes.submit_run(
            body.content,
            hermes_session_id,
            hermes_session_key,
            history,
        )
    except HermesRunRejected:
        await mark_rejected(
            session_factory,
            workspace_id,
            run_id,
            "Hermes rejected the run before accepting it",
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Hermes rejected the run submission",
        )
    except (HermesSubmissionUncertain, httpx.HTTPError, ValueError):
        await mark_indeterminate(
            session_factory,
            workspace_id,
            run_id,
            "Hermes submission outcome is uncertain",
        )
        await session.refresh(run)
        return run

    run.hermes_run_id = hermes_run_id
    run.status = AgentRunStatus.RUNNING.value
    run.started_at = utc_now()
    session.add_all(
        [
            Message(
                workspace_id=workspace_id,
                conversation_id=conversation_id,
                role=MessageRole.USER.value,
                content=body.content,
            ),
            RunEvent(
                workspace_id=workspace_id,
                agent_run_id=run.id,
                sequence_number=1,
                event_type="run.started",
                payload={"hermes_run_id": hermes_run_id},
            ),
        ]
    )
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        resolution = await stop_run_until_resolved(
            hermes,
            hermes_run_id,
            max_attempts=1,
        )
        await mark_indeterminate(
            session_factory,
            workspace_id,
            run_id,
            "Hermes accepted the run but durable correlation failed",
            hermes_run_id=hermes_run_id,
        )
        if not resolution.resolved:
            background_tasks.add_task(
                cleanup_upstream_run,
                hermes,
                hermes_run_id,
            )
        persisted_run = await session.get(
            AgentRun,
            run_id,
            populate_existing=True,
        )
        if persisted_run is None:
            raise RuntimeError("Durable Hermes run disappeared during recovery")
        return persisted_run
    background_tasks.add_task(
        project_run,
        session_factory,
        hermes,
        workspace_id,
        run_id,
        hermes_run_id,
    )
    return run
