from datetime import UTC, datetime
from decimal import Decimal
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
    Numeric,
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


class VenueKind(StrEnum):
    SECURITIES_EXCHANGE = "securities_exchange"
    CRYPTO_VENUE = "crypto_venue"


class InstrumentKind(StrEnum):
    COMMON_STOCK = "common_stock"
    ETF = "etf"
    CRYPTO_ASSET = "crypto_asset"


class ListingStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


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


class ToolProvenanceStatus(StrEnum):
    PENDING = "pending"
    COMPLETE = "complete"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"
    CONFLICTING = "conflicting"


class MemoryProposalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


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


class Currency(Base):
    __tablename__ = "currencies"
    __table_args__ = (
        CheckConstraint(
            "length(code) between 3 and 12 and code = upper(code) and code not like '% %'",
            name="code_shape",
        ),
        CheckConstraint(
            "length(trim(name)) between 1 and 120",
            name="name_length",
        ),
        CheckConstraint("minor_unit between 0 and 18", name="minor_unit_range"),
    )

    code: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    minor_unit: Mapped[int] = mapped_column(Integer, nullable=False)


class Venue(Base):
    __tablename__ = "venues"
    __table_args__ = (
        UniqueConstraint("code"),
        UniqueConstraint("mic"),
        CheckConstraint(
            "length(code) between 2 and 32 and code = upper(code) and code not like '% %'",
            name="code_shape",
        ),
        CheckConstraint(
            "mic is null or (length(mic) = 4 and mic = upper(mic) and mic not like '% %')",
            name="mic_shape",
        ),
        CheckConstraint(
            "kind in ('securities_exchange', 'crypto_venue')",
            name="kind_allowed",
        ),
        CheckConstraint(
            "length(trim(name)) between 1 and 160",
            name="name_length",
        ),
        CheckConstraint(
            "length(trim(timezone)) between 1 and 64",
            name="timezone_length",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    mic: Mapped[str | None] = mapped_column(Text)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    timezone: Mapped[str] = mapped_column(Text, nullable=False)


class Instrument(Base):
    __tablename__ = "instruments"
    __table_args__ = (
        CheckConstraint(
            "kind in ('common_stock', 'etf', 'crypto_asset')",
            name="kind_allowed",
        ),
        CheckConstraint(
            "length(trim(name)) between 1 and 200",
            name="name_length",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    kind: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )


class Listing(Base):
    __tablename__ = "listings"
    __table_args__ = (
        UniqueConstraint("venue_id", "venue_symbol"),
        CheckConstraint(
            "length(trim(venue_symbol)) between 1 and 64",
            name="venue_symbol_length",
        ),
        CheckConstraint("price_increment > 0", name="price_increment_positive"),
        CheckConstraint(
            "quantity_increment > 0",
            name="quantity_increment_positive",
        ),
        CheckConstraint(
            "status in ('active', 'inactive')",
            name="status_allowed",
        ),
        Index("ix_listings_instrument_venue", "instrument_id", "venue_id"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    instrument_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("instruments.id", ondelete="RESTRICT"),
        nullable=False,
    )
    venue_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("venues.id", ondelete="RESTRICT"),
        nullable=False,
    )
    venue_symbol: Mapped[str] = mapped_column(Text, nullable=False)
    quote_currency_code: Mapped[str] = mapped_column(
        Text,
        ForeignKey("currencies.code", ondelete="RESTRICT"),
        nullable=False,
    )
    price_increment: Mapped[Decimal] = mapped_column(Numeric(38, 18), nullable=False)
    quantity_increment: Mapped[Decimal] = mapped_column(
        Numeric(38, 18),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=ListingStatus.ACTIVE.value,
        server_default=ListingStatus.ACTIVE.value,
    )
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
        CheckConstraint(
            "hermes_message_cursor is null or hermes_message_cursor >= 0",
            name="hermes_message_cursor_nonnegative",
        ),
        CheckConstraint(
            "hermes_resolved_session_id is null "
            "or length(hermes_resolved_session_id) between 1 and 256",
            name="hermes_resolved_session_id_length",
        ),
        CheckConstraint(
            "tool_provenance_status in "
            "('pending', 'complete', 'partial', 'unavailable', 'conflicting')",
            name="tool_provenance_status_allowed",
        ),
        CheckConstraint(
            "tool_provenance_reason is null "
            "or length(tool_provenance_reason) between 1 and 120",
            name="tool_provenance_reason_length",
        ),
        CheckConstraint(
            "length(approved_memory_snapshot_hash) = 64",
            name="approved_memory_snapshot_hash_length",
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
    hermes_message_cursor: Mapped[int | None] = mapped_column(BigInteger)
    hermes_resolved_session_id: Mapped[str | None] = mapped_column(Text)
    event_stream_complete: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )
    tool_provenance_status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=ToolProvenanceStatus.PENDING.value,
        server_default=ToolProvenanceStatus.PENDING.value,
    )
    tool_provenance_reason: Mapped[str | None] = mapped_column(Text)
    tool_provenance_checked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    approved_memory_snapshot: Mapped[list[dict[str, object]]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
        default=list,
        server_default="[]",
    )
    approved_memory_snapshot_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        server_default="4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
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


class RunToolProvenance(Base):
    __tablename__ = "run_tool_provenance"
    __table_args__ = (
        ForeignKeyConstraint(
            ("workspace_id", "agent_run_id"),
            ("agent_runs.workspace_id", "agent_runs.id"),
            ondelete="CASCADE",
        ),
        UniqueConstraint("workspace_id", "agent_run_id", "sequence_number"),
        UniqueConstraint("workspace_id", "agent_run_id", "tool_call_id"),
        CheckConstraint("sequence_number >= 0", name="sequence_nonnegative"),
        CheckConstraint("call_message_id > 0", name="call_message_id_positive"),
        CheckConstraint(
            "result_message_id is null or result_message_id > call_message_id",
            name="result_after_call",
        ),
        CheckConstraint(
            "length(trim(tool_call_id)) between 1 and 256",
            name="tool_call_id_length",
        ),
        CheckConstraint(
            "length(trim(tool_name)) between 1 and 200",
            name="tool_name_length",
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
    call_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    result_message_id: Mapped[int | None] = mapped_column(BigInteger)
    tool_call_id: Mapped[str] = mapped_column(Text, nullable=False)
    tool_name: Mapped[str] = mapped_column(Text, nullable=False)
    arguments: Mapped[object] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
    )
    result: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )


class MemoryChangeProposal(Base):
    __tablename__ = "memory_change_proposals"
    __table_args__ = (
        UniqueConstraint("workspace_id", "id"),
        UniqueConstraint("workspace_id", "idempotency_key"),
        ForeignKeyConstraint(
            ("workspace_id", "source_run_id"),
            ("agent_runs.workspace_id", "agent_runs.id"),
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "operating_context in ('individual_self_directed', 'institutional_proprietary')",
            name="operating_context_allowed",
        ),
        CheckConstraint(
            "(preference_key = 'communication.response_detail' "
            "and proposed_value in ('concise', 'balanced', 'detailed')) "
            "or (preference_key = 'research.presentation' "
            "and proposed_value in ('narrative', 'bullets', 'table'))",
            name="preference_allowed",
        ),
        CheckConstraint(
            "status in ('pending', 'approved', 'rejected')",
            name="status_allowed",
        ),
        CheckConstraint(
            "length(idempotency_key) between 1 and 128",
            name="idempotency_key_length",
        ),
        CheckConstraint("length(request_hash) = 64", name="request_hash_length"),
        CheckConstraint("proposer_ref = 'local_user'", name="proposer_ref_allowed"),
        CheckConstraint(
            "reviewer_ref is null or reviewer_ref = 'local_user'",
            name="reviewer_ref_allowed",
        ),
        CheckConstraint(
            "(status = 'pending' and reviewer_ref is null and decided_at is null "
            "and decision_rationale is null) or "
            "(status in ('approved', 'rejected') and reviewer_ref is not null "
            "and decided_at is not null)",
            name="decision_shape",
        ),
        CheckConstraint(
            "decision_rationale is null "
            "or length(decision_rationale) between 1 and 1000",
            name="decision_rationale_length",
        ),
        Index(
            "ix_memory_change_proposals_workspace_created_id",
            "workspace_id",
            "created_at",
            "id",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    workspace_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="RESTRICT"),
        nullable=False,
    )
    operating_context: Mapped[str] = mapped_column(Text, nullable=False)
    preference_key: Mapped[str] = mapped_column(Text, nullable=False)
    proposed_value: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[list[str]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
    )
    proposer_ref: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="local_user",
        server_default="local_user",
    )
    reviewer_ref: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=MemoryProposalStatus.PENDING.value,
        server_default=MemoryProposalStatus.PENDING.value,
    )
    source_run_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True))
    idempotency_key: Mapped[str] = mapped_column(Text, nullable=False)
    request_hash: Mapped[str] = mapped_column(Text, nullable=False)
    decision_rationale: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class WorkspaceSoftPreference(Base):
    __tablename__ = "workspace_soft_preferences"
    __table_args__ = (
        ForeignKeyConstraint(
            ("workspace_id", "source_proposal_id"),
            ("memory_change_proposals.workspace_id", "memory_change_proposals.id"),
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "operating_context in ('individual_self_directed', 'institutional_proprietary')",
            name="operating_context_allowed",
        ),
        CheckConstraint(
            "(preference_key = 'communication.response_detail' "
            "and value in ('concise', 'balanced', 'detailed')) "
            "or (preference_key = 'research.presentation' "
            "and value in ('narrative', 'bullets', 'table'))",
            name="preference_allowed",
        ),
        CheckConstraint("revision > 0", name="revision_positive"),
    )

    workspace_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="RESTRICT"),
        primary_key=True,
    )
    preference_key: Mapped[str] = mapped_column(Text, primary_key=True)
    operating_context: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    source_proposal_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )


class MemoryProposalEvent(Base):
    __tablename__ = "memory_proposal_events"
    __table_args__ = (
        ForeignKeyConstraint(
            ("workspace_id", "proposal_id"),
            ("memory_change_proposals.workspace_id", "memory_change_proposals.id"),
            ondelete="RESTRICT",
        ),
        UniqueConstraint("workspace_id", "proposal_id", "sequence_number"),
        CheckConstraint("sequence_number in (0, 1)", name="sequence_allowed"),
        CheckConstraint(
            "(sequence_number = 0 and event_type = 'proposed') or "
            "(sequence_number = 1 and event_type in ('approved', 'rejected'))",
            name="event_shape",
        ),
        CheckConstraint("actor_ref = 'local_user'", name="actor_ref_allowed"),
        CheckConstraint(
            "operating_context in ('individual_self_directed', 'institutional_proprietary')",
            name="operating_context_allowed",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(Integer, "sqlite"),
        Identity(),
        primary_key=True,
    )
    workspace_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    proposal_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    actor_ref: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="local_user",
        server_default="local_user",
    )
    operating_context: Mapped[str] = mapped_column(Text, nullable=False)
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
