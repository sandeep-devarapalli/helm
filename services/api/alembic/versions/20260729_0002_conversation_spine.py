"""Persist the conversation spine.

Revision ID: 20260729_0002
Revises: 20260713_0001
Create Date: 2026-07-29
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260729_0002"
down_revision: str | None = "20260713_0001"
branch_labels: None = None
depends_on: None = None


def upgrade() -> None:
    op.create_table(
        "workspaces",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("operating_context", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "operating_context in ('individual_self_directed', 'institutional_proprietary')",
            name=op.f("ck_workspaces_operating_context_allowed"),
        ),
        sa.CheckConstraint(
            "length(trim(name)) between 1 and 120",
            name=op.f("ck_workspaces_name_length"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_workspaces")),
    )
    op.create_table(
        "conversations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "title is null or length(trim(title)) between 1 and 200",
            name=op.f("ck_conversations_title_length"),
        ),
        sa.ForeignKeyConstraint(
            ("workspace_id",),
            ("workspaces.id",),
            name=op.f("fk_conversations_workspace_id_workspaces"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_conversations")),
        sa.UniqueConstraint(
            "workspace_id",
            "id",
            name=op.f("uq_conversations_workspace_id_id"),
        ),
    )
    op.create_index(
        "ix_conversations_workspace_created_id",
        "conversations",
        ("workspace_id", "created_at", "id"),
    )
    op.create_table(
        "messages",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("conversation_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "role in ('user', 'assistant', 'system', 'tool')",
            name=op.f("ck_messages_role_allowed"),
        ),
        sa.ForeignKeyConstraint(
            ("workspace_id", "conversation_id"),
            ("conversations.workspace_id", "conversations.id"),
            name=op.f("fk_messages_workspace_id_conversation_id_conversations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_messages")),
    )
    op.create_index(
        "ix_messages_workspace_conversation_created_id",
        "messages",
        ("workspace_id", "conversation_id", "created_at", "id"),
    )
    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("conversation_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.Text(), server_default="queued", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status in ('queued', 'running', 'succeeded', 'failed', 'cancelled')",
            name=op.f("ck_agent_runs_status_allowed"),
        ),
        sa.CheckConstraint(
            "started_at is null or finished_at is null or finished_at >= started_at",
            name=op.f("ck_agent_runs_finished_after_started"),
        ),
        sa.ForeignKeyConstraint(
            ("workspace_id", "conversation_id"),
            ("conversations.workspace_id", "conversations.id"),
            name=op.f("fk_agent_runs_workspace_id_conversation_id_conversations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_agent_runs")),
        sa.UniqueConstraint(
            "workspace_id",
            "id",
            name=op.f("uq_agent_runs_workspace_id_id"),
        ),
    )
    op.create_index(
        "ix_agent_runs_workspace_conversation_created_id",
        "agent_runs",
        ("workspace_id", "conversation_id", "created_at", "id"),
    )
    op.create_table(
        "run_events",
        sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("agent_run_id", sa.Uuid(), nullable=False),
        sa.Column("sequence_number", sa.BigInteger(), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("payload", postgresql.JSONB(), server_default="{}", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "length(trim(event_type)) between 1 and 80",
            name=op.f("ck_run_events_event_type_length"),
        ),
        sa.CheckConstraint(
            "sequence_number >= 0",
            name=op.f("ck_run_events_sequence_nonnegative"),
        ),
        sa.ForeignKeyConstraint(
            ("workspace_id", "agent_run_id"),
            ("agent_runs.workspace_id", "agent_runs.id"),
            name=op.f("fk_run_events_workspace_id_agent_run_id_agent_runs"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_run_events")),
        sa.UniqueConstraint(
            "workspace_id",
            "agent_run_id",
            "sequence_number",
            name=op.f("uq_run_events_workspace_id_agent_run_id_sequence_number"),
        ),
    )


def downgrade() -> None:
    op.drop_table("run_events")
    op.drop_index(
        "ix_agent_runs_workspace_conversation_created_id",
        table_name="agent_runs",
    )
    op.drop_table("agent_runs")
    op.drop_index(
        "ix_messages_workspace_conversation_created_id",
        table_name="messages",
    )
    op.drop_table("messages")
    op.drop_index(
        "ix_conversations_workspace_created_id",
        table_name="conversations",
    )
    op.drop_table("conversations")
    op.drop_table("workspaces")
