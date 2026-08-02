import asyncio
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from helm.domain.models import (
    AgentRun,
    AgentRunStatus,
    Conversation,
    Message,
    MessageRole,
    RunEvent,
    Workspace,
    utc_now,
)
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError


def test_conversation_persists_and_is_isolated(api_context) -> None:
    response = api_context.client.post(
        f"/workspaces/{api_context.workspace_a}/conversations",
        json={"title": "  NVDA versus AMD  "},
    )

    assert response.status_code == 201
    conversation = response.json()
    assert conversation["workspace_id"] == str(api_context.workspace_a)
    assert conversation["title"] == "NVDA versus AMD"

    detail = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/{conversation['id']}"
    )
    assert detail.status_code == 200
    assert detail.json() == conversation

    foreign_detail = api_context.client.get(
        f"/workspaces/{api_context.workspace_b}/conversations/{conversation['id']}"
    )
    assert foreign_detail.status_code == 404

    own_list = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations"
    ).json()
    foreign_list = api_context.client.get(
        f"/workspaces/{api_context.workspace_b}/conversations"
    ).json()
    assert [item["id"] for item in own_list["items"]] == [conversation["id"]]
    assert foreign_list == {"items": [], "next_cursor": None}


def test_conversation_creation_validates_workspace_and_title(
    api_context,
) -> None:
    missing_workspace = api_context.client.post(
        "/workspaces/00000000-0000-0000-0000-000000000000/conversations",
        json={"title": "Research"},
    )
    blank_title = api_context.client.post(
        f"/workspaces/{api_context.workspace_a}/conversations",
        json={"title": "   "},
    )

    assert missing_workspace.status_code == 404
    assert blank_title.status_code == 422


def test_conversation_list_uses_cursor_without_duplicates(
    api_context,
) -> None:
    async def create_same_time_conversations() -> set[str]:
        created_at = datetime(2026, 7, 29, 12, 0, tzinfo=UTC)
        conversations = [
            Conversation(
                workspace_id=api_context.workspace_a,
                title=title,
                created_at=created_at,
            )
            for title in ("First", "Second", "Third")
        ]
        async with api_context.session_factory() as session:
            session.add_all(conversations)
            await session.commit()
        return {str(conversation.id) for conversation in conversations}

    created_ids = asyncio.run(create_same_time_conversations())

    first_response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations",
        params={"limit": 2},
    )
    first_page = first_response.json()
    second_response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations",
        params={"limit": 2, "cursor": first_page["next_cursor"]},
    )
    second_page = second_response.json()
    returned_ids = {
        item["id"] for item in first_page["items"] + second_page["items"]
    }

    assert first_response.status_code == 200, first_response.text
    assert second_response.status_code == 200, second_response.text
    assert first_page["next_cursor"] is not None
    assert second_page["next_cursor"] is None
    assert returned_ids == created_ids


def test_invalid_conversation_cursor_is_rejected(api_context) -> None:
    response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations",
        params={"cursor": "not-a-cursor"},
    )

    assert response.status_code == 422


def test_messages_are_chronological_paginated_and_workspace_scoped(api_context) -> None:
    conversation = api_context.client.post(
        f"/workspaces/{api_context.workspace_a}/conversations",
        json={"title": "Persisted transcript"},
    ).json()
    conversation_id = UUID(conversation["id"])

    async def seed_messages() -> list[str]:
        created_at = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)
        user = Message(
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            role=MessageRole.USER.value,
            content="Compare NVDA and AMD.",
            created_at=created_at,
        )
        assistant = Message(
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT.value,
            content="I will gather evidence first.",
            created_at=created_at,
        )
        follow_up = Message(
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            role=MessageRole.USER.value,
            content="Show the evidence quality.",
            created_at=created_at,
        )
        system = Message(
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            role=MessageRole.SYSTEM.value,
            content="Internal instruction",
            created_at=created_at,
        )
        tool = Message(
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            role=MessageRole.TOOL.value,
            content="Internal tool result",
            created_at=created_at,
        )
        async with api_context.session_factory() as session:
            session.add_all([user, assistant, follow_up, system, tool])
            await session.commit()
        return [
            str(message.id)
            for message in sorted((user, assistant, follow_up), key=lambda item: item.id)
        ]

    expected_ids = asyncio.run(seed_messages())
    first_response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/{conversation['id']}/messages",
        params={"limit": 2},
    )
    first_page = first_response.json()
    second_response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/{conversation['id']}/messages",
        params={"limit": 2, "cursor": first_page["next_cursor"]},
    )
    second_page = second_response.json()
    foreign_response = api_context.client.get(
        f"/workspaces/{api_context.workspace_b}/conversations/{conversation['id']}/messages"
    )

    assert first_response.status_code == 200, first_response.text
    assert second_response.status_code == 200, second_response.text
    assert foreign_response.status_code == 404
    assert first_page["next_cursor"] is not None
    assert second_page["next_cursor"] is None
    items = first_page["items"] + second_page["items"]
    assert [item["id"] for item in items] == expected_ids
    assert {item["role"] for item in items} == {
        MessageRole.USER.value,
        MessageRole.ASSISTANT.value,
    }
    assert {item["content"] for item in items}.isdisjoint(
        {"Internal instruction", "Internal tool result"}
    )


def test_invalid_message_cursor_is_rejected(api_context) -> None:
    conversation = api_context.client.post(
        f"/workspaces/{api_context.workspace_a}/conversations",
        json={"title": "Invalid transcript cursor"},
    ).json()

    response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/{conversation['id']}/messages",
        params={"cursor": "not-a-cursor"},
    )

    assert response.status_code == 422


def test_latest_run_supports_refresh_without_browser_state(api_context) -> None:
    conversation = api_context.client.post(
        f"/workspaces/{api_context.workspace_a}/conversations",
        json={"title": "Refresh state"},
    ).json()
    conversation_id = UUID(conversation["id"])
    latest_before_run = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/{conversation['id']}/runs/latest"
    )

    async def seed_runs() -> str:
        created_at = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)
        completed_id = uuid4()
        active_id = uuid4()
        if active_id > completed_id:
            completed_id, active_id = active_id, completed_id
        completed = AgentRun(
            id=completed_id,
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            status=AgentRunStatus.SUCCEEDED.value,
            created_at=created_at,
            finished_at=created_at + timedelta(minutes=1),
        )
        active = AgentRun(
            id=active_id,
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            status=AgentRunStatus.QUEUED.value,
            created_at=created_at,
        )
        async with api_context.session_factory() as session:
            session.add_all([completed, active])
            await session.commit()
        return str(active.id)

    active_run_id = asyncio.run(seed_runs())
    latest_response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/{conversation['id']}/runs/latest"
    )
    foreign_response = api_context.client.get(
        f"/workspaces/{api_context.workspace_b}/conversations/{conversation['id']}/runs/latest"
    )
    latest = latest_response.json()["run"]

    assert latest_before_run.status_code == 200
    assert latest_before_run.json() == {"run": None}
    assert latest_response.status_code == 200, latest_response.text
    assert foreign_response.status_code == 404
    assert latest["id"] == active_run_id
    assert latest["status"] == AgentRunStatus.QUEUED.value
    assert latest["event_stream_complete"] is False
    assert latest["projection_gap"] is False
    assert latest["approval_blocked"] is False
    assert latest["tool_provenance_complete"] is False
    assert "approved_memory_snapshot" not in latest
    assert "hermes_run_id" not in latest


def test_latest_run_marks_approval_blocked(api_context) -> None:
    conversation = api_context.client.post(
        f"/workspaces/{api_context.workspace_a}/conversations",
        json={"title": "Approval boundary"},
    ).json()
    conversation_id = UUID(conversation["id"])

    async def seed_cancelled_run() -> None:
        run = AgentRun(
            workspace_id=api_context.workspace_a,
            conversation_id=conversation_id,
            status=AgentRunStatus.CANCELLED.value,
            finished_at=utc_now(),
        )
        async with api_context.session_factory() as session:
            session.add(run)
            await session.flush()
            session.add(
                RunEvent(
                    workspace_id=api_context.workspace_a,
                    agent_run_id=run.id,
                    sequence_number=0,
                    event_type="approval.request",
                    payload={"choices": ["once", "deny"]},
                )
            )
            await session.commit()

    asyncio.run(seed_cancelled_run())
    response = api_context.client.get(
        f"/workspaces/{api_context.workspace_a}/conversations/{conversation_id}/runs/latest"
    )

    assert response.status_code == 200, response.text
    assert response.json()["run"]["status"] == AgentRunStatus.CANCELLED.value
    assert response.json()["run"]["approval_blocked"] is True


def test_event_order_and_workspace_constraints(api_context) -> None:
    async def exercise() -> None:
        async with api_context.session_factory() as session:
            conversation = Conversation(
                workspace_id=api_context.workspace_a,
                title="Persistence graph",
            )
            session.add(conversation)
            await session.flush()
            run = AgentRun(
                workspace_id=api_context.workspace_a,
                conversation_id=conversation.id,
            )
            session.add(run)
            await session.flush()
            session.add_all(
                [
                    Message(
                        workspace_id=api_context.workspace_a,
                        conversation_id=conversation.id,
                        role=MessageRole.USER.value,
                        content="Valid message",
                    ),
                    RunEvent(
                        workspace_id=api_context.workspace_a,
                        agent_run_id=run.id,
                        sequence_number=2,
                        event_type="completed",
                    ),
                    RunEvent(
                        workspace_id=api_context.workspace_a,
                        agent_run_id=run.id,
                        sequence_number=1,
                        event_type="started",
                    ),
                ]
            )
            await session.commit()

        async with api_context.session_factory() as session:
            sequences = list(
                (
                    await session.scalars(
                        select(RunEvent.sequence_number)
                        .where(
                            RunEvent.workspace_id == api_context.workspace_a,
                            RunEvent.agent_run_id == run.id,
                        )
                        .order_by(RunEvent.sequence_number)
                    )
                ).all()
            )
            assert sequences == [1, 2]

            session.add(
                RunEvent(
                    workspace_id=api_context.workspace_a,
                    agent_run_id=run.id,
                    sequence_number=1,
                    event_type="duplicate",
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()

        async with api_context.session_factory() as session:
            session.add(
                Message(
                    workspace_id=api_context.workspace_b,
                    conversation_id=conversation.id,
                    role=MessageRole.USER.value,
                    content="Cross-workspace attachment",
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()

        async with api_context.session_factory() as session:
            session.add(
                AgentRun(
                    workspace_id=api_context.workspace_b,
                    conversation_id=conversation.id,
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()

        async with api_context.session_factory() as session:
            session.add(
                RunEvent(
                    workspace_id=api_context.workspace_b,
                    agent_run_id=run.id,
                    sequence_number=3,
                    event_type="foreign-workspace",
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()

        async with api_context.session_factory() as session:
            persisted_run = await session.get(AgentRun, run.id)
            assert persisted_run is not None
            persisted_run.status = AgentRunStatus.SUCCEEDED.value
            persisted_run.finished_at = utc_now()
            await session.commit()

        async with api_context.session_factory() as session:
            second_run = AgentRun(
                workspace_id=api_context.workspace_a,
                conversation_id=conversation.id,
            )
            session.add(second_run)
            await session.flush()
            session.add(
                RunEvent(
                    workspace_id=api_context.workspace_a,
                    agent_run_id=second_run.id,
                    sequence_number=1,
                    event_type="started",
                )
            )
            await session.commit()

        async with api_context.session_factory() as session:
            persisted_run = await session.get(AgentRun, second_run.id)
            assert persisted_run is not None
            persisted_run.status = AgentRunStatus.INDETERMINATE.value
            persisted_run.input = "Analyze this symbol."
            persisted_run.submission_attempted_at = utc_now()
            await session.commit()

        async with api_context.session_factory() as session:
            session.add(
                AgentRun(
                    workspace_id=api_context.workspace_a,
                    conversation_id=conversation.id,
                )
            )
            with pytest.raises(IntegrityError):
                await session.commit()

        async with api_context.session_factory() as session:
            await session.execute(
                delete(Workspace).where(Workspace.id == api_context.workspace_a)
            )
            await session.commit()
            remaining = {
                model.__tablename__: await session.scalar(
                    select(func.count()).select_from(model)
                )
                for model in (Conversation, Message, AgentRun, RunEvent)
            }
            assert remaining == {
                "conversations": 0,
                "messages": 0,
                "agent_runs": 0,
                "run_events": 0,
            }

    asyncio.run(exercise())
