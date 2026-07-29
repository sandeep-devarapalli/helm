from base64 import urlsafe_b64decode, urlsafe_b64encode
from binascii import Error as Base64Error
from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from helm.database import get_session
from helm.domain.models import Conversation, Workspace

router = APIRouter(prefix="/workspaces/{workspace_id}/conversations", tags=["conversations"])
Session = Annotated[AsyncSession, Depends(get_session)]


class ConversationCreate(BaseModel):
    title: str | None = None

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized or len(normalized) > 200:
            raise ValueError("title must contain between 1 and 200 characters")
        return normalized


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    workspace_id: UUID
    title: str | None
    created_at: datetime


class ConversationPage(BaseModel):
    items: list[ConversationResponse]
    next_cursor: str | None


def encode_cursor(conversation: Conversation) -> str:
    created_at = conversation.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=UTC)
    value = f"{created_at.isoformat()}|{conversation.id}"
    return urlsafe_b64encode(value.encode()).decode().rstrip("=")


def decode_cursor(cursor: str) -> tuple[datetime, UUID]:
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        created_at_raw, conversation_id_raw = (
            urlsafe_b64decode(padded.encode()).decode().rsplit("|", 1)
        )
        created_at = datetime.fromisoformat(created_at_raw)
        if created_at.tzinfo is None:
            raise ValueError
        return created_at, UUID(conversation_id_raw)
    except (Base64Error, UnicodeDecodeError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="invalid conversation cursor",
        ) from error


async def require_workspace(session: AsyncSession, workspace_id: UUID) -> None:
    exists = await session.scalar(select(Workspace.id).where(Workspace.id == workspace_id))
    if exists is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workspace not found")


@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    workspace_id: UUID,
    request: ConversationCreate,
    session: Session,
) -> Conversation:
    await require_workspace(session, workspace_id)
    conversation = Conversation(workspace_id=workspace_id, title=request.title)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


@router.get("", response_model=ConversationPage)
async def list_conversations(
    workspace_id: UUID,
    session: Session,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: str | None = None,
) -> ConversationPage:
    await require_workspace(session, workspace_id)
    statement = select(Conversation).where(Conversation.workspace_id == workspace_id)
    if cursor is not None:
        cursor_created_at, cursor_id = decode_cursor(cursor)
        statement = statement.where(
            or_(
                Conversation.created_at < cursor_created_at,
                and_(
                    Conversation.created_at == cursor_created_at,
                    Conversation.id < cursor_id,
                ),
            )
        )
    conversations = list(
        (
            await session.scalars(
                statement.order_by(
                    Conversation.created_at.desc(),
                    Conversation.id.desc(),
                ).limit(limit + 1)
            )
        ).all()
    )
    has_more = len(conversations) > limit
    items = conversations[:limit]
    return ConversationPage(
        items=[ConversationResponse.model_validate(item) for item in items],
        next_cursor=encode_cursor(items[-1]) if has_more else None,
    )


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    workspace_id: UUID,
    conversation_id: UUID,
    session: Session,
) -> Conversation:
    conversation = await session.scalar(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.workspace_id == workspace_id,
        )
    )
    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="conversation not found",
        )
    return conversation
