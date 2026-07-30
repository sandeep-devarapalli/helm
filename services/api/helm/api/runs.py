import asyncio
import json
from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Any, cast
from uuid import UUID

import httpx
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Header,
    HTTPException,
    Query,
    Request,
    status,
)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from helm.api.memory import (
    approved_memory_snapshot,
    memory_snapshot_hash,
    render_memory_instructions,
)
from helm.database import get_session
from helm.domain.models import (
    AgentRun,
    AgentRunStatus,
    Conversation,
    Message,
    MessageRole,
    RunEvent,
    RunToolProvenance,
    ToolProvenanceStatus,
    utc_now,
)
from helm.integrations.hermes import (
    HermesClient,
    HermesError,
    HermesRunMissing,
    HermesRunRejected,
    HermesSessionMissing,
    HermesSubmissionUncertain,
    HermesTranscript,
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
STREAM_CLOSED_STATUSES = {
    AgentRunStatus.INDETERMINATE.value,
    AgentRunStatus.SUCCEEDED.value,
    AgentRunStatus.FAILED.value,
    AgentRunStatus.CANCELLED.value,
}
MAX_EVENT_PAYLOAD_BYTES = 64 * 1024
MAX_TOOL_VALUE_BYTES = 64 * 1024
MAX_SEQUENCE_NUMBER = 2**63 - 1
EVENT_PAGE_LIMIT = 100
SSE_POLL_INTERVAL_SECONDS = 0.25
SSE_HEARTBEAT_SECONDS = 15.0
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
APPROVED_HERMES_TOOLS = frozenset(
    {
        "search_symbol",
        "get_market_data",
        "get_financial_statements",
        "get_stock_profile",
        "get_stock_news",
        "get_sec_filings",
    }
)


@dataclass(frozen=True)
class StopResolution:
    resolved: bool
    terminal_snapshot: dict[str, Any] | None = None


@dataclass(frozen=True)
class ReconciledTool:
    call_message_id: int
    result_message_id: int | None
    tool_call_id: str
    tool_name: str
    arguments: object
    result: str | None


@dataclass(frozen=True)
class Reconciliation:
    status: ToolProvenanceStatus
    reason: str | None
    tools: tuple[ReconciledTool, ...] = ()


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


class RunDetailResponse(RunResponse):
    started_at: datetime | None
    finished_at: datetime | None
    approved_memory_snapshot: list[dict[str, object]]
    approved_memory_snapshot_hash: str
    projection_gap: bool
    tool_provenance_status: str
    tool_provenance_reason: str | None
    tool_provenance_complete: bool
    structured_citations_available: bool = False


class RunEventResponse(BaseModel):
    sequence_number: int
    event_type: str
    payload: dict[str, object]
    created_at: datetime
    tool_provenance_complete: bool = False


class RunEventPage(BaseModel):
    items: list[RunEventResponse]
    next_cursor: int | None
    event_stream_complete: bool
    projection_gap: bool
    tool_provenance_status: str
    tool_provenance_complete: bool


class ToolProvenanceResponse(BaseModel):
    sequence_number: int
    call_message_id: int
    result_message_id: int | None
    tool_call_id: str
    tool_name: str
    arguments: object
    result: str | None


class RunProvenanceResponse(BaseModel):
    status: str
    reason: str | None
    checked_at: datetime | None
    resolved_session_id: str | None
    items: list[ToolProvenanceResponse]
    structured_citations_available: bool = False


def request_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    return cast(async_sessionmaker[AsyncSession], request.app.state.session_factory)


async def scoped_run(
    session: AsyncSession,
    workspace_id: UUID,
    conversation_id: UUID,
    run_id: UUID,
) -> AgentRun:
    run = await session.scalar(
        select(AgentRun).where(
            AgentRun.id == run_id,
            AgentRun.workspace_id == workspace_id,
            AgentRun.conversation_id == conversation_id,
        )
    )
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="run not found")
    return run


async def has_projection_gap(
    session: AsyncSession,
    run: AgentRun,
) -> bool:
    if run.status == AgentRunStatus.INDETERMINATE.value:
        return True
    payloads = (
        await session.scalars(
            select(RunEvent.payload).where(
                RunEvent.workspace_id == run.workspace_id,
                RunEvent.agent_run_id == run.id,
                RunEvent.event_type.in_(TERMINAL_EVENTS),
            )
        )
    ).all()
    return any(
        isinstance(payload, dict) and payload.get("projection_gap") is True
        for payload in payloads
    )


def public_event(
    event: RunEvent,
    *,
    tool_provenance_complete: bool = False,
) -> RunEventResponse:
    payload: dict[str, object]
    try:
        encoded = json.dumps(
            event.payload,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
        decoded = json.loads(encoded)
        if len(encoded) > MAX_EVENT_PAYLOAD_BYTES or not isinstance(decoded, dict):
            raise ValueError
        payload = cast(dict[str, object], decoded)
    except (OverflowError, RecursionError, TypeError, UnicodeError, ValueError):
        payload = {
            "unavailable": True,
            "reason": "malformed_or_oversized_payload",
        }
    return RunEventResponse(
        sequence_number=event.sequence_number,
        event_type=event.event_type,
        payload=payload,
        created_at=event.created_at,
        tool_provenance_complete=tool_provenance_complete,
    )


async def validate_event_cursor(
    session: AsyncSession,
    run: AgentRun,
    after: int,
) -> None:
    if after < 0:
        return
    exists = await session.scalar(
        select(RunEvent.id).where(
            RunEvent.workspace_id == run.workspace_id,
            RunEvent.agent_run_id == run.id,
            RunEvent.sequence_number == after,
        )
    )
    if exists is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="event cursor does not exist for this run",
        )


async def validate_persisted_sequence(
    session: AsyncSession,
    run: AgentRun,
) -> None:
    count, first, last = (
        await session.execute(
            select(
                func.count(RunEvent.id),
                func.min(RunEvent.sequence_number),
                func.max(RunEvent.sequence_number),
            ).where(
                RunEvent.workspace_id == run.workspace_id,
                RunEvent.agent_run_id == run.id,
            )
        )
    ).one()
    if count and (first != 0 or last is None or count != last + 1):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="persisted event sequence contains a gap",
        )


def resume_sequence(after: int, last_event_id: str | None) -> int:
    if last_event_id is None:
        return after
    try:
        sequence_number = int(last_event_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Last-Event-ID must be a valid event sequence",
        ) from error
    if sequence_number < 0 or sequence_number > MAX_SEQUENCE_NUMBER:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Last-Event-ID must be a valid event sequence",
        )
    return sequence_number


def sse_frame(event: RunEventResponse) -> str:
    data = json.dumps(event.model_dump(mode="json"), separators=(",", ":"))
    return f"id: {event.sequence_number}\nevent: run-event\ndata: {data}\n\n"


async def persisted_event_stream(
    request: Request,
    session_factory: async_sessionmaker[AsyncSession],
    workspace_id: UUID,
    conversation_id: UUID,
    run_id: UUID,
    after: int,
) -> AsyncIterator[str]:
    cursor = after
    last_activity = asyncio.get_running_loop().time()
    while not await request.is_disconnected():
        async with session_factory() as session:
            run = await session.scalar(
                select(AgentRun).where(
                    AgentRun.id == run_id,
                    AgentRun.workspace_id == workspace_id,
                    AgentRun.conversation_id == conversation_id,
                )
            )
            if run is None:
                return
            events = (
                await session.scalars(
                    select(RunEvent)
                    .where(
                        RunEvent.workspace_id == workspace_id,
                        RunEvent.agent_run_id == run_id,
                        RunEvent.sequence_number > cursor,
                    )
                    .order_by(RunEvent.sequence_number)
                    .limit(EVENT_PAGE_LIMIT)
                )
            ).all()

        if events:
            expected = cursor + 1
            provenance_complete = (
                run.tool_provenance_status == ToolProvenanceStatus.COMPLETE.value
            )
            for event in events:
                if event.sequence_number != expected:
                    return
                yield sse_frame(
                    public_event(
                        event,
                        tool_provenance_complete=provenance_complete,
                    )
                )
                cursor = event.sequence_number
                expected += 1
            last_activity = asyncio.get_running_loop().time()
            continue

        if run.status in STREAM_CLOSED_STATUSES:
            return
        now = asyncio.get_running_loop().time()
        if now - last_activity >= SSE_HEARTBEAT_SECONDS:
            yield ": keep-alive\n\n"
            last_activity = now
        await asyncio.sleep(SSE_POLL_INTERVAL_SECONDS)


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


def encoded_size(value: object) -> int:
    return len(
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def reconcile_transcript(
    transcript: HermesTranscript,
    cursor: int,
    expected_input: str,
    terminal_output: str | None,
) -> Reconciliation:
    suffix = [message for message in transcript.messages if message["id"] > cursor]
    if not suffix:
        return Reconciliation(
            ToolProvenanceStatus.UNAVAILABLE,
            "no_messages_after_cursor",
        )
    user_indexes = [
        index for index, message in enumerate(suffix) if message["role"] == "user"
    ]
    if (
        not user_indexes
        or any(message["role"] != "system" for message in suffix[: user_indexes[0]])
        or suffix[user_indexes[0]]["content"] != expected_input
    ):
        return Reconciliation(
            ToolProvenanceStatus.CONFLICTING,
            "turn_boundary_mismatch",
        )
    turn_end = user_indexes[1] if len(user_indexes) > 1 else len(suffix)
    turn = suffix[user_indexes[0] : turn_end]

    calls: dict[str, ReconciledTool] = {}
    results: dict[str, tuple[int, str, str]] = {}
    for message in turn:
        if message["role"] == "assistant":
            tool_calls = message.get("tool_calls") or []
            for raw_call in tool_calls:
                if not isinstance(raw_call, dict):
                    return Reconciliation(
                        ToolProvenanceStatus.CONFLICTING,
                        "malformed_tool_call",
                    )
                function = raw_call.get("function")
                call_id = raw_call.get("id")
                if (
                    raw_call.get("type") != "function"
                    or not isinstance(function, dict)
                    or not isinstance(call_id, str)
                    or not 1 <= len(call_id) <= 256
                    or not call_id.strip()
                    or call_id in calls
                ):
                    return Reconciliation(
                        ToolProvenanceStatus.CONFLICTING,
                        "malformed_or_duplicate_tool_call",
                    )
                tool_name = function.get("name")
                raw_arguments = function.get("arguments")
                if (
                    not isinstance(tool_name, str)
                    or tool_name not in APPROVED_HERMES_TOOLS
                    or not isinstance(raw_arguments, str)
                ):
                    return Reconciliation(
                        ToolProvenanceStatus.CONFLICTING,
                        "unapproved_or_malformed_tool_call",
                    )
                try:
                    arguments = json.loads(raw_arguments)
                    if not isinstance(arguments, dict):
                        raise ValueError
                    if encoded_size(arguments) > MAX_TOOL_VALUE_BYTES:
                        raise OverflowError
                except (
                    OverflowError,
                    RecursionError,
                    TypeError,
                    UnicodeError,
                    ValueError,
                ):
                    return Reconciliation(
                        ToolProvenanceStatus.CONFLICTING,
                        "invalid_or_oversized_tool_arguments",
                    )
                calls[call_id] = ReconciledTool(
                    call_message_id=message["id"],
                    result_message_id=None,
                    tool_call_id=call_id,
                    tool_name=tool_name,
                    arguments=arguments,
                    result=None,
                )
        elif message["role"] == "tool":
            call_id = message.get("tool_call_id")
            tool_name = message.get("tool_name")
            result = message["content"]
            if (
                not isinstance(call_id, str)
                or not call_id
                or not call_id.strip()
                or call_id in results
                or not isinstance(tool_name, str)
                or tool_name not in APPROVED_HERMES_TOOLS
                or len(result.encode("utf-8")) > MAX_TOOL_VALUE_BYTES
            ):
                return Reconciliation(
                    ToolProvenanceStatus.CONFLICTING,
                    "malformed_or_duplicate_tool_result",
                )
            results[call_id] = (message["id"], tool_name, result)

    if set(results) - set(calls):
        return Reconciliation(
            ToolProvenanceStatus.CONFLICTING,
            "orphan_tool_result",
        )

    reconciled: list[ReconciledTool] = []
    missing_result = False
    for call in calls.values():
        result = results.get(call.tool_call_id)
        if result is None:
            missing_result = True
            reconciled.append(call)
            continue
        result_message_id, result_tool_name, result_content = result
        if (
            result_tool_name != call.tool_name
            or result_message_id <= call.call_message_id
        ):
            return Reconciliation(
                ToolProvenanceStatus.CONFLICTING,
                "tool_result_mismatch",
            )
        reconciled.append(
            ReconciledTool(
                call_message_id=call.call_message_id,
                result_message_id=result_message_id,
                tool_call_id=call.tool_call_id,
                tool_name=call.tool_name,
                arguments=call.arguments,
                result=result_content,
            )
        )

    if terminal_output is not None:
        final_messages = [
            message
            for message in turn
            if message["role"] == "assistant"
            and not message.get("tool_calls")
            and message["content"]
        ]
        if (
            not final_messages
            or final_messages[-1]["content"] != terminal_output
            or final_messages[-1]["id"] != turn[-1]["id"]
        ):
            return Reconciliation(
                ToolProvenanceStatus.CONFLICTING,
                "terminal_output_mismatch",
            )

    if missing_result:
        return Reconciliation(
            ToolProvenanceStatus.PARTIAL,
            "missing_tool_result",
            tuple(reconciled),
        )
    return Reconciliation(
        ToolProvenanceStatus.COMPLETE,
        None,
        tuple(reconciled),
    )


async def persist_reconciliation(
    session_factory: async_sessionmaker[AsyncSession],
    workspace_id: UUID,
    run_id: UUID,
    reconciliation: Reconciliation,
    *,
    resolved_session_id: str | None,
) -> None:
    async with session_factory() as session:
        run = await session.scalar(
            select(AgentRun)
            .where(AgentRun.id == run_id, AgentRun.workspace_id == workspace_id)
            .with_for_update()
        )
        if run is None or run.status not in {
            AgentRunStatus.SUCCEEDED.value,
            AgentRunStatus.FAILED.value,
            AgentRunStatus.CANCELLED.value,
        }:
            return
        if run.tool_provenance_status in {
            ToolProvenanceStatus.COMPLETE.value,
            ToolProvenanceStatus.PARTIAL.value,
            ToolProvenanceStatus.CONFLICTING.value,
        }:
            return
        await session.execute(
            delete(RunToolProvenance).where(
                RunToolProvenance.workspace_id == workspace_id,
                RunToolProvenance.agent_run_id == run_id,
            )
        )
        for sequence_number, tool in enumerate(reconciliation.tools):
            session.add(
                RunToolProvenance(
                    workspace_id=workspace_id,
                    agent_run_id=run_id,
                    sequence_number=sequence_number,
                    call_message_id=tool.call_message_id,
                    result_message_id=tool.result_message_id,
                    tool_call_id=tool.tool_call_id,
                    tool_name=tool.tool_name,
                    arguments=tool.arguments,
                    result=tool.result,
                )
            )
        run.hermes_resolved_session_id = resolved_session_id
        run.tool_provenance_status = reconciliation.status.value
        run.tool_provenance_reason = reconciliation.reason
        run.tool_provenance_checked_at = utc_now()
        await session.commit()


async def reconcile_run_provenance(
    session_factory: async_sessionmaker[AsyncSession],
    hermes: HermesClient,
    workspace_id: UUID,
    run_id: UUID,
) -> None:
    async with session_factory() as session:
        row = (
            await session.execute(
                select(
                    AgentRun.hermes_session_id,
                    AgentRun.hermes_message_cursor,
                    AgentRun.input,
                    AgentRun.tool_provenance_status,
                    RunEvent.event_type,
                    RunEvent.payload,
                )
                .join(
                    RunEvent,
                    (RunEvent.workspace_id == AgentRun.workspace_id)
                    & (RunEvent.agent_run_id == AgentRun.id),
                )
                .where(
                    AgentRun.id == run_id,
                    AgentRun.workspace_id == workspace_id,
                    RunEvent.event_type.in_(TERMINAL_EVENTS),
                )
                .order_by(RunEvent.sequence_number.desc())
                .limit(1)
            )
        ).one_or_none()
    if row is None:
        return
    (
        session_id,
        cursor,
        run_input,
        provenance_status,
        terminal_event,
        terminal_payload,
    ) = row
    if provenance_status in {
        ToolProvenanceStatus.COMPLETE.value,
        ToolProvenanceStatus.PARTIAL.value,
        ToolProvenanceStatus.CONFLICTING.value,
    }:
        return
    if session_id is None or cursor is None or run_input is None:
        await persist_reconciliation(
            session_factory,
            workspace_id,
            run_id,
            Reconciliation(
                ToolProvenanceStatus.UNAVAILABLE,
                "pre_submit_transcript_unavailable",
            ),
            resolved_session_id=None,
        )
        return
    try:
        transcript = await hermes.session_messages(session_id)
    except (HermesError, httpx.HTTPError, ValueError):
        await persist_reconciliation(
            session_factory,
            workspace_id,
            run_id,
            Reconciliation(
                ToolProvenanceStatus.UNAVAILABLE,
                "session_unavailable",
            ),
            resolved_session_id=None,
        )
        return
    terminal_output = None
    if terminal_event == "run.completed":
        output = terminal_payload.get("output")
        terminal_output = output if isinstance(output, str) else ""
    await persist_reconciliation(
        session_factory,
        workspace_id,
        run_id,
        reconcile_transcript(transcript, cursor, run_input, terminal_output),
        resolved_session_id=transcript.resolved_session_id,
    )


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
        run.tool_provenance_status = ToolProvenanceStatus.UNAVAILABLE.value
        run.tool_provenance_reason = "run_state_indeterminate"
        run.tool_provenance_checked_at = utc_now()
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
        run.tool_provenance_status = ToolProvenanceStatus.UNAVAILABLE.value
        run.tool_provenance_reason = "run_not_accepted"
        run.tool_provenance_checked_at = utc_now()
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
        if run is None or run.status != AgentRunStatus.RUNNING.value:
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
            run.tool_provenance_status = ToolProvenanceStatus.UNAVAILABLE.value
            run.tool_provenance_reason = "reconciliation_pending"
            run.tool_provenance_checked_at = None
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
            await reconcile_run_provenance(
                session_factory,
                hermes,
                workspace_id,
                run_id,
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
                    await reconcile_run_provenance(
                        session_factory,
                        hermes,
                        workspace_id,
                        run_id,
                    )
                    return
            if event_type in TERMINAL_EVENTS:
                await reconcile_run_provenance(
                    session_factory,
                    hermes,
                    workspace_id,
                    run_id,
                )
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
            await reconcile_run_provenance(
                session_factory,
                hermes,
                workspace_id,
                run_id,
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
            await reconcile_run_provenance(
                session_factory,
                hermes,
                workspace_id,
                run_id,
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


@router.get(
    "/{conversation_id}/runs/{run_id}",
    response_model=RunDetailResponse,
)
async def get_run(
    workspace_id: UUID,
    conversation_id: UUID,
    run_id: UUID,
    session: Session,
) -> RunDetailResponse:
    run = await scoped_run(session, workspace_id, conversation_id, run_id)
    return RunDetailResponse(
        **RunResponse.model_validate(run).model_dump(),
        started_at=run.started_at,
        finished_at=run.finished_at,
        approved_memory_snapshot=run.approved_memory_snapshot,
        approved_memory_snapshot_hash=run.approved_memory_snapshot_hash,
        projection_gap=await has_projection_gap(session, run),
        tool_provenance_status=run.tool_provenance_status,
        tool_provenance_reason=run.tool_provenance_reason,
        tool_provenance_complete=(
            run.tool_provenance_status == ToolProvenanceStatus.COMPLETE.value
        ),
    )


@router.get(
    "/{conversation_id}/runs/{run_id}/provenance",
    response_model=RunProvenanceResponse,
)
async def get_run_provenance(
    workspace_id: UUID,
    conversation_id: UUID,
    run_id: UUID,
    session: Session,
) -> RunProvenanceResponse:
    run = await scoped_run(session, workspace_id, conversation_id, run_id)
    tools = (
        await session.scalars(
            select(RunToolProvenance)
            .where(
                RunToolProvenance.workspace_id == workspace_id,
                RunToolProvenance.agent_run_id == run_id,
            )
            .order_by(RunToolProvenance.sequence_number)
        )
    ).all()
    return RunProvenanceResponse(
        status=run.tool_provenance_status,
        reason=run.tool_provenance_reason,
        checked_at=run.tool_provenance_checked_at,
        resolved_session_id=run.hermes_resolved_session_id,
        items=[
            ToolProvenanceResponse.model_validate(tool, from_attributes=True)
            for tool in tools
        ],
    )


@router.get(
    "/{conversation_id}/runs/{run_id}/events",
    response_model=RunEventPage,
)
async def list_run_events(
    workspace_id: UUID,
    conversation_id: UUID,
    run_id: UUID,
    session: Session,
    after: Annotated[int, Query(ge=-1, le=MAX_SEQUENCE_NUMBER)] = -1,
    limit: Annotated[int, Query(ge=1, le=EVENT_PAGE_LIMIT)] = EVENT_PAGE_LIMIT,
) -> RunEventPage:
    run = await scoped_run(session, workspace_id, conversation_id, run_id)
    await validate_persisted_sequence(session, run)
    await validate_event_cursor(session, run, after)
    events = (
        await session.scalars(
            select(RunEvent)
            .where(
                RunEvent.workspace_id == workspace_id,
                RunEvent.agent_run_id == run_id,
                RunEvent.sequence_number > after,
            )
            .order_by(RunEvent.sequence_number)
            .limit(limit + 1)
        )
    ).all()
    page = events[:limit]
    expected = after + 1
    for event in page:
        if event.sequence_number != expected:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="persisted event sequence contains a gap",
            )
        expected += 1
    return RunEventPage(
        items=[
            public_event(
                event,
                tool_provenance_complete=(
                    run.tool_provenance_status
                    == ToolProvenanceStatus.COMPLETE.value
                ),
            )
            for event in page
        ],
        next_cursor=page[-1].sequence_number if len(events) > limit else None,
        event_stream_complete=run.event_stream_complete,
        projection_gap=await has_projection_gap(session, run),
        tool_provenance_status=run.tool_provenance_status,
        tool_provenance_complete=(
            run.tool_provenance_status == ToolProvenanceStatus.COMPLETE.value
        ),
    )


@router.get("/{conversation_id}/runs/{run_id}/events/stream")
async def stream_run_events(
    workspace_id: UUID,
    conversation_id: UUID,
    run_id: UUID,
    request: Request,
    after: Annotated[int, Query(ge=-1, le=MAX_SEQUENCE_NUMBER)] = -1,
    last_event_id: Annotated[str | None, Header(alias="Last-Event-ID")] = None,
) -> StreamingResponse:
    session_factory = request_session_factory(request)
    resume_after = resume_sequence(after, last_event_id)
    async with session_factory() as session:
        run = await scoped_run(session, workspace_id, conversation_id, run_id)
        await validate_persisted_sequence(session, run)
        await validate_event_cursor(session, run, resume_after)
    return StreamingResponse(
        persisted_event_stream(
            request,
            session_factory,
            workspace_id,
            conversation_id,
            run_id,
            resume_after,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
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
    memory_snapshot = await approved_memory_snapshot(session, workspace_id)
    approved_snapshot_hash = memory_snapshot_hash(memory_snapshot)
    memory_instructions = render_memory_instructions(memory_snapshot)
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
    try:
        transcript = await hermes.session_messages(hermes_session_id)
        hermes_message_cursor = (
            transcript.messages[-1]["id"] if transcript.messages else 0
        )
    except HermesSessionMissing:
        hermes_message_cursor = 0
    except (HermesError, httpx.HTTPError, ValueError):
        hermes_message_cursor = None
    run = AgentRun(
        workspace_id=workspace_id,
        conversation_id=conversation_id,
        status=AgentRunStatus.SUBMITTING.value,
        input=body.content,
        submission_attempted_at=utc_now(),
        hermes_session_id=hermes_session_id,
        hermes_message_cursor=hermes_message_cursor,
        approved_memory_snapshot=memory_snapshot,
        approved_memory_snapshot_hash=approved_snapshot_hash,
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
            memory_instructions,
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
