from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Identity,
    Index,
    Integer,
    Text,
    UniqueConstraint,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from helm.database import Base as Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class OperatingContext(StrEnum):
    INDIVIDUAL_SELF_DIRECTED = "individual_self_directed"
    INSTITUTIONAL_PROPRIETARY = "institutional_proprietary"


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class AgentRunStatus(StrEnum):
    QUEUED = "queued"
    SUBMITTING = "submitting"
    RUNNING = "running"
    INDETERMINATE = "indeterminate"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Workspace(Base):
    __tablename__ = "workspaces"
    __table_args__ = (
        CheckConstraint(
            "operating_context in ('individual_self_directed', 'institutional_proprietary')",
            name="operating_context_allowed",
        ),
        CheckConstraint(
            "length(trim(name)) between 1 and 120",
            name="name_length",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    operating_context: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )


class Conversation(Base):
    __tablename__ = "conversations"
    __table_args__ = (
        UniqueConstraint("workspace_id", "id"),
        CheckConstraint(
            "title is null or length(trim(title)) between 1 and 200",
            name="title_length",
        ),
        Index("ix_conversations_workspace_created_id", "workspace_id", "created_at", "id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    workspace_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        ForeignKeyConstraint(
            ("workspace_id", "conversation_id"),
            ("conversations.workspace_id", "conversations.id"),
            ondelete="CASCADE",
        ),
        CheckConstraint(
            "role in ('user', 'assistant', 'system', 'tool')",
            name="role_allowed",
        ),
        Index(
            "ix_messages_workspace_conversation_created_id",
            "workspace_id",
            "conversation_id",
            "created_at",
            "id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    conversation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )


class AgentRun(Base):
    __tablename__ = "agent_runs"
    __table_args__ = (
        ForeignKeyConstraint(
            ("workspace_id", "conversation_id"),
            ("conversations.workspace_id", "conversations.id"),
            ondelete="CASCADE",
        ),
        UniqueConstraint("workspace_id", "id"),
        CheckConstraint(
            "status in "
            "('queued', 'submitting', 'running', 'indeterminate', "
            "'succeeded', 'failed', 'cancelled')",
            name="status_allowed",
        ),
        CheckConstraint(
            "input is null or length(trim(input)) between 1 and 20000",
            name="input_length",
        ),
        CheckConstraint(
            "status not in ('queued', 'submitting', 'running', 'indeterminate') "
            "or finished_at is null",
            name="active_run_unfinished",
        ),
        CheckConstraint(
            "status not in ('succeeded', 'failed', 'cancelled') "
            "or finished_at is not null",
            name="terminal_run_finished",
        ),
        CheckConstraint(
            "status != 'submitting' or "
            "(input is not null and submission_attempted_at is not null "
            "and started_at is null and hermes_run_id is null "
            "and event_stream_complete = false)",
            name="submitting_shape",
        ),
        CheckConstraint(
            "status != 'running' or "
            "(input is not null and submission_attempted_at is not null "
            "and started_at is not null and hermes_run_id is not null "
            "and hermes_session_id is not null and event_stream_complete = false)",
            name="running_shape",
        ),
        CheckConstraint(
            "status != 'indeterminate' or "
            "(input is not null and submission_attempted_at is not null "
            "and event_stream_complete = false)",
            name="indeterminate_shape",
        ),
        CheckConstraint(
            "event_stream_complete = false "
            "or status in ('succeeded', 'failed', 'cancelled')",
            name="complete_stream_terminal",
        ),
        CheckConstraint(
            "started_at is null or finished_at is null or finished_at >= started_at",
            name="finished_after_started",
        ),
        CheckConstraint(
            "hermes_run_id is null or "
            "(length(hermes_run_id) = 36 and substr(hermes_run_id, 1, 4) = 'run_')",
            name="hermes_run_id_length",
        ),
        CheckConstraint(
            "hermes_session_id is null or length(hermes_session_id) between 1 and 256",
            name="hermes_session_id_length",
        ),
        Index(
            "ix_agent_runs_workspace_conversation_created_id",
            "workspace_id",
            "conversation_id",
            "created_at",
            "id",
        ),
        Index(
            "uq_agent_runs_one_active_per_conversation",
            "workspace_id",
            "conversation_id",
            unique=True,
            postgresql_where=text(
                "status in ('queued', 'submitting', 'running', 'indeterminate')"
            ),
            sqlite_where=text(
                "status in ('queued', 'submitting', 'running', 'indeterminate')"
            ),
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    conversation_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=AgentRunStatus.QUEUED.value,
        server_default=AgentRunStatus.QUEUED.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    input: Mapped[str | None] = mapped_column(Text)
    submission_attempted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    hermes_run_id: Mapped[str | None] = mapped_column(Text)
    hermes_session_id: Mapped[str | None] = mapped_column(Text)
    event_stream_complete: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )


class RunEvent(Base):
    __tablename__ = "run_events"
    __table_args__ = (
        ForeignKeyConstraint(
            ("workspace_id", "agent_run_id"),
            ("agent_runs.workspace_id", "agent_runs.id"),
            ondelete="CASCADE",
        ),
        UniqueConstraint("workspace_id", "agent_run_id", "sequence_number"),
        CheckConstraint("sequence_number >= 0", name="sequence_nonnegative"),
        CheckConstraint(
            "length(trim(event_type)) between 1 and 80",
            name="event_type_length",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        Identity(),
        primary_key=True,
    )
    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    agent_run_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    sequence_number: Mapped[int] = mapped_column(BigInteger, nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict[str, object]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=dict,
        server_default="{}",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )
