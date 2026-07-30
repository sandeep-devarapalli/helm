import hashlib
import json
import re
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from helm.database import get_session
from helm.domain.models import (
    AgentRun,
    MemoryChangeProposal,
    MemoryProposalEvent,
    MemoryProposalStatus,
    Workspace,
    WorkspaceSoftPreference,
    utc_now,
)

router = APIRouter(prefix="/workspaces/{workspace_id}/memory", tags=["memory"])
Session = Annotated[AsyncSession, Depends(get_session)]
IDEMPOTENCY_KEY_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
ALLOWED_PREFERENCES = {
    "communication.response_detail": frozenset({"concise", "balanced", "detailed"}),
    "research.presentation": frozenset({"narrative", "bullets", "table"}),
}
PREFERENCE_INSTRUCTIONS = {
    ("communication.response_detail", "concise"): "Keep responses concise.",
    (
        "communication.response_detail",
        "balanced",
    ): "Use a balanced level of response detail.",
    (
        "communication.response_detail",
        "detailed",
    ): "Provide detailed responses when the evidence supports them.",
    (
        "research.presentation",
        "narrative",
    ): "Present research primarily as a clear narrative.",
    (
        "research.presentation",
        "bullets",
    ): "Present research primarily as concise bullet points.",
    (
        "research.presentation",
        "table",
    ): "Use tables for research comparisons when suitable.",
}
MAX_INSTRUCTIONS_BYTES = 4096


class ProposalCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preference_key: str
    proposed_value: str
    evidence: list[str]
    source_run_id: UUID | None = None

    @field_validator("preference_key", "proposed_value")
    @classmethod
    def normalize_choice(cls, value: str) -> str:
        return value.strip()

    @field_validator("evidence")
    @classmethod
    def normalize_evidence(cls, value: list[str]) -> list[str]:
        if not 1 <= len(value) <= 10:
            raise ValueError("evidence must contain between 1 and 10 items")
        normalized = [item.strip() for item in value]
        if any(not item or len(item) > 500 for item in normalized):
            raise ValueError("each evidence item must contain between 1 and 500 characters")
        return normalized

    @model_validator(mode="after")
    def validate_preference(self) -> "ProposalCreate":
        if self.proposed_value not in ALLOWED_PREFERENCES.get(
            self.preference_key, frozenset()
        ):
            raise ValueError("preference key and value are not allowed")
        return self


class ProposalDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: Literal["approve", "reject"]
    rationale: str | None = None

    @field_validator("rationale")
    @classmethod
    def normalize_rationale(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized or len(normalized) > 1000:
            raise ValueError("rationale must contain between 1 and 1000 characters")
        return normalized


class ProposalEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sequence_number: int
    event_type: str
    actor_ref: str
    operating_context: str
    payload: dict[str, object]
    created_at: datetime


class ProposalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    operating_context: str
    preference_key: str
    proposed_value: str
    evidence: list[str]
    proposer_ref: str
    reviewer_ref: str | None
    status: str
    source_run_id: UUID | None
    created_at: datetime
    decided_at: datetime | None
    decision_rationale: str | None
    events: list[ProposalEventResponse] = Field(default_factory=list)


class ProposalPage(BaseModel):
    items: list[ProposalResponse]


class PreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    workspace_id: UUID
    operating_context: str
    preference_key: str
    value: str
    source_proposal_id: UUID
    revision: int
    updated_at: datetime


class PreferencePage(BaseModel):
    items: list[PreferenceResponse]


def request_hash(body: ProposalCreate) -> str:
    encoded = json.dumps(
        body.model_dump(mode="json"),
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def memory_snapshot_hash(snapshot: list[dict[str, object]]) -> str:
    encoded = json.dumps(
        snapshot,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


async def approved_memory_snapshot(
    session: AsyncSession,
    workspace_id: UUID,
) -> list[dict[str, object]]:
    workspace = await session.scalar(
        select(Workspace).where(Workspace.id == workspace_id)
    )
    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="workspace not found",
        )
    preferences = (
        await session.scalars(
            select(WorkspaceSoftPreference)
            .where(WorkspaceSoftPreference.workspace_id == workspace_id)
            .order_by(WorkspaceSoftPreference.preference_key)
        )
    ).all()
    proposal_ids = {preference.source_proposal_id for preference in preferences}
    proposals = (
        await session.scalars(
            select(MemoryChangeProposal).where(
                MemoryChangeProposal.workspace_id == workspace_id,
                MemoryChangeProposal.id.in_(proposal_ids),
            )
        )
    ).all()
    proposals_by_id = {proposal.id: proposal for proposal in proposals}
    snapshot: list[dict[str, object]] = []
    for preference in preferences:
        proposal = proposals_by_id.get(preference.source_proposal_id)
        if (
            preference.operating_context != workspace.operating_context
            or preference.value
            not in ALLOWED_PREFERENCES.get(preference.preference_key, frozenset())
            or proposal is None
            or proposal.status != MemoryProposalStatus.APPROVED.value
            or proposal.operating_context != workspace.operating_context
            or proposal.preference_key != preference.preference_key
            or proposal.proposed_value != preference.value
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="approved memory does not match the workspace context",
            )
        snapshot.append(
            {
                "preference_key": preference.preference_key,
                "value": preference.value,
                "revision": preference.revision,
                "source_proposal_id": str(preference.source_proposal_id),
            }
        )
    return snapshot


def render_memory_instructions(snapshot: list[dict[str, object]]) -> str | None:
    if not snapshot:
        return None
    guidance = [
        PREFERENCE_INSTRUCTIONS[(str(item["preference_key"]), str(item["value"]))]
        for item in snapshot
    ]
    instructions = (
        "The following are approved, non-authoritative presentation preferences. "
        "They cannot modify tools, policy, mandates, risk controls, credentials, "
        "or execution authority.\n- "
        + "\n- ".join(guidance)
    )
    if len(instructions.encode()) > MAX_INSTRUCTIONS_BYTES:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="approved memory instructions exceed the safe limit",
        )
    return instructions


async def require_workspace(
    session: AsyncSession,
    workspace_id: UUID,
    *,
    lock: bool = False,
) -> Workspace:
    statement = select(Workspace).where(Workspace.id == workspace_id)
    if lock:
        statement = statement.with_for_update()
    workspace = await session.scalar(statement)
    if workspace is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="workspace not found",
        )
    return workspace


async def scoped_proposal(
    session: AsyncSession,
    workspace_id: UUID,
    proposal_id: UUID,
    *,
    lock: bool = False,
) -> MemoryChangeProposal:
    statement = select(MemoryChangeProposal).where(
        MemoryChangeProposal.id == proposal_id,
        MemoryChangeProposal.workspace_id == workspace_id,
    )
    if lock:
        statement = statement.with_for_update()
    proposal = await session.scalar(statement)
    if proposal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="memory proposal not found",
        )
    return proposal


async def proposal_response(
    session: AsyncSession,
    proposal: MemoryChangeProposal,
) -> ProposalResponse:
    events = (
        await session.scalars(
            select(MemoryProposalEvent)
            .where(
                MemoryProposalEvent.workspace_id == proposal.workspace_id,
                MemoryProposalEvent.proposal_id == proposal.id,
            )
            .order_by(MemoryProposalEvent.sequence_number)
        )
    ).all()
    return ProposalResponse(
        **ProposalResponse.model_validate(
            proposal,
            from_attributes=True,
        ).model_dump(exclude={"events"}),
        events=[
            ProposalEventResponse.model_validate(event, from_attributes=True)
            for event in events
        ],
    )


@router.post(
    "/proposals",
    response_model=ProposalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_proposal(
    workspace_id: UUID,
    body: ProposalCreate,
    response: Response,
    session: Session,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key")],
) -> ProposalResponse:
    if IDEMPOTENCY_KEY_PATTERN.fullmatch(idempotency_key) is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="invalid Idempotency-Key",
        )
    workspace = await require_workspace(session, workspace_id, lock=True)
    digest = request_hash(body)
    existing = await session.scalar(
        select(MemoryChangeProposal).where(
            MemoryChangeProposal.workspace_id == workspace_id,
            MemoryChangeProposal.idempotency_key == idempotency_key,
        )
    )
    if existing is not None:
        if existing.request_hash != digest:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Idempotency-Key was already used for a different proposal",
            )
        if existing.operating_context != workspace.operating_context:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="memory proposal does not match the workspace context",
            )
        response.status_code = status.HTTP_200_OK
        return await proposal_response(session, existing)
    if body.source_run_id is not None:
        source_run = await session.scalar(
            select(AgentRun.id).where(
                AgentRun.id == body.source_run_id,
                AgentRun.workspace_id == workspace_id,
            )
        )
        if source_run is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="source run not found",
            )
    proposal = MemoryChangeProposal(
        workspace_id=workspace_id,
        operating_context=workspace.operating_context,
        preference_key=body.preference_key,
        proposed_value=body.proposed_value,
        evidence=body.evidence,
        source_run_id=body.source_run_id,
        idempotency_key=idempotency_key,
        request_hash=digest,
    )
    session.add(proposal)
    await session.flush()
    session.add(
        MemoryProposalEvent(
            workspace_id=workspace_id,
            proposal_id=proposal.id,
            sequence_number=0,
            event_type="proposed",
            operating_context=workspace.operating_context,
            payload={
                "preference_key": body.preference_key,
                "proposed_value": body.proposed_value,
                "evidence": body.evidence,
                "request_hash": digest,
                "source_run_id": (
                    str(body.source_run_id) if body.source_run_id is not None else None
                ),
            },
        )
    )
    try:
        await session.commit()
    except IntegrityError as error:
        await session.rollback()
        concurrent = await session.scalar(
            select(MemoryChangeProposal).where(
                MemoryChangeProposal.workspace_id == workspace_id,
                MemoryChangeProposal.idempotency_key == idempotency_key,
            )
        )
        if (
            concurrent is not None
            and concurrent.request_hash == digest
            and concurrent.operating_context == workspace.operating_context
        ):
            response.status_code = status.HTTP_200_OK
            return await proposal_response(session, concurrent)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="proposal conflicts with existing workspace state",
        ) from error
    return await proposal_response(session, proposal)


@router.get("/proposals", response_model=ProposalPage)
async def list_proposals(
    workspace_id: UUID,
    session: Session,
    proposal_status: Annotated[
        Literal["pending", "approved", "rejected"] | None,
        Query(alias="status"),
    ] = None,
) -> ProposalPage:
    workspace = await require_workspace(session, workspace_id)
    statement = select(MemoryChangeProposal).where(
        MemoryChangeProposal.workspace_id == workspace_id
    )
    if proposal_status is not None:
        statement = statement.where(MemoryChangeProposal.status == proposal_status)
    proposals = (
        await session.scalars(
            statement.order_by(
                MemoryChangeProposal.created_at.desc(),
                MemoryChangeProposal.id.desc(),
            ).limit(100)
        )
    ).all()
    if any(
        proposal.operating_context != workspace.operating_context
        for proposal in proposals
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="memory proposal does not match the workspace context",
        )
    return ProposalPage(
        items=[await proposal_response(session, proposal) for proposal in proposals]
    )


@router.get("/proposals/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(
    workspace_id: UUID,
    proposal_id: UUID,
    session: Session,
) -> ProposalResponse:
    workspace = await require_workspace(session, workspace_id)
    proposal = await scoped_proposal(session, workspace_id, proposal_id)
    if proposal.operating_context != workspace.operating_context:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="memory proposal does not match the workspace context",
        )
    return await proposal_response(session, proposal)


@router.post("/proposals/{proposal_id}/decisions", response_model=ProposalResponse)
async def decide_proposal(
    workspace_id: UUID,
    proposal_id: UUID,
    body: ProposalDecision,
    session: Session,
) -> ProposalResponse:
    workspace = await require_workspace(session, workspace_id, lock=True)
    proposal = await scoped_proposal(
        session,
        workspace_id,
        proposal_id,
        lock=True,
    )
    desired_status = (
        MemoryProposalStatus.APPROVED.value
        if body.decision == "approve"
        else MemoryProposalStatus.REJECTED.value
    )
    if proposal.operating_context != workspace.operating_context:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="memory proposal does not match the workspace context",
        )
    if proposal.status != MemoryProposalStatus.PENDING.value:
        if (
            proposal.status == desired_status
            and proposal.decision_rationale == body.rationale
        ):
            return await proposal_response(session, proposal)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="memory proposal already has a different decision payload",
        )
    now = utc_now()
    proposal.status = desired_status
    proposal.reviewer_ref = "local_user"
    proposal.decision_rationale = body.rationale
    proposal.decided_at = now
    if desired_status == MemoryProposalStatus.APPROVED.value:
        preference = await session.scalar(
            select(WorkspaceSoftPreference).where(
                WorkspaceSoftPreference.workspace_id == workspace_id,
                WorkspaceSoftPreference.preference_key == proposal.preference_key,
            )
        )
        if preference is None:
            session.add(
                WorkspaceSoftPreference(
                    workspace_id=workspace_id,
                    operating_context=workspace.operating_context,
                    preference_key=proposal.preference_key,
                    value=proposal.proposed_value,
                    source_proposal_id=proposal.id,
                    revision=1,
                    updated_at=now,
                )
            )
        else:
            if preference.operating_context != workspace.operating_context:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="approved memory does not match the workspace context",
                )
            preference.value = proposal.proposed_value
            preference.source_proposal_id = proposal.id
            preference.revision += 1
            preference.updated_at = now
    session.add(
        MemoryProposalEvent(
            workspace_id=workspace_id,
            proposal_id=proposal.id,
            sequence_number=1,
            event_type=desired_status,
            operating_context=workspace.operating_context,
            payload={"rationale": body.rationale},
        )
    )
    try:
        await session.commit()
    except IntegrityError as error:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="memory decision conflicts with existing workspace state",
        ) from error
    return await proposal_response(session, proposal)


@router.get("/preferences", response_model=PreferencePage)
async def list_preferences(
    workspace_id: UUID,
    session: Session,
) -> PreferencePage:
    await approved_memory_snapshot(session, workspace_id)
    preferences = (
        await session.scalars(
            select(WorkspaceSoftPreference)
            .where(WorkspaceSoftPreference.workspace_id == workspace_id)
            .order_by(WorkspaceSoftPreference.preference_key)
        )
    ).all()
    return PreferencePage(
        items=[
            PreferenceResponse.model_validate(preference, from_attributes=True)
            for preference in preferences
        ]
    )
