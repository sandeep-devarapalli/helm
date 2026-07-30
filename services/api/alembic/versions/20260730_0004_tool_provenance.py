"""Add bounded Hermes tool provenance.

Revision ID: 20260730_0004
Revises: 20260729_0003
Create Date: 2026-07-30
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260730_0004"
down_revision: str | None = "20260729_0003"
branch_labels: None = None
depends_on: None = None


def upgrade() -> None:
    op.add_column(
        "agent_runs",
        sa.Column("hermes_message_cursor", sa.BigInteger(), nullable=True),
    )
    op.add_column(
        "agent_runs",
        sa.Column("hermes_resolved_session_id", sa.Text(), nullable=True),
    )
    op.add_column(
        "agent_runs",
        sa.Column(
            "tool_provenance_status",
            sa.Text(),
            server_default="pending",
            nullable=False,
        ),
    )
    op.add_column(
        "agent_runs",
        sa.Column("tool_provenance_reason", sa.Text(), nullable=True),
    )
    op.add_column(
        "agent_runs",
        sa.Column(
            "tool_provenance_checked_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            """
            UPDATE agent_runs
            SET tool_provenance_status = 'unavailable',
                tool_provenance_reason = CASE
                    WHEN status = 'indeterminate'
                        THEN 'run_state_indeterminate'
                    ELSE 'predates_message_cursor'
                END
            WHERE status IN ('succeeded', 'failed', 'cancelled')
               OR status = 'indeterminate'
            """
        )
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_hermes_message_cursor_nonnegative"),
        "agent_runs",
        "hermes_message_cursor is null or hermes_message_cursor >= 0",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_hermes_resolved_session_id_length"),
        "agent_runs",
        "hermes_resolved_session_id is null "
        "or length(hermes_resolved_session_id) between 1 and 256",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_tool_provenance_status_allowed"),
        "agent_runs",
        "tool_provenance_status in "
        "('pending', 'complete', 'partial', 'unavailable', 'conflicting')",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_tool_provenance_reason_length"),
        "agent_runs",
        "tool_provenance_reason is null "
        "or length(tool_provenance_reason) between 1 and 120",
    )
    op.create_table(
        "run_tool_provenance",
        sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("agent_run_id", sa.Uuid(), nullable=False),
        sa.Column("sequence_number", sa.BigInteger(), nullable=False),
        sa.Column("call_message_id", sa.BigInteger(), nullable=False),
        sa.Column("result_message_id", sa.BigInteger(), nullable=True),
        sa.Column("tool_call_id", sa.Text(), nullable=False),
        sa.Column("tool_name", sa.Text(), nullable=False),
        sa.Column(
            "arguments",
            sa.JSON().with_variant(postgresql.JSONB(astext_type=sa.Text()), "postgresql"),
            nullable=False,
        ),
        sa.Column("result", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "call_message_id > 0",
            name=op.f("ck_run_tool_provenance_call_message_id_positive"),
        ),
        sa.CheckConstraint(
            "result_message_id is null or result_message_id > call_message_id",
            name=op.f("ck_run_tool_provenance_result_after_call"),
        ),
        sa.CheckConstraint(
            "sequence_number >= 0",
            name=op.f("ck_run_tool_provenance_sequence_nonnegative"),
        ),
        sa.CheckConstraint(
            "length(trim(tool_call_id)) between 1 and 256",
            name=op.f("ck_run_tool_provenance_tool_call_id_length"),
        ),
        sa.CheckConstraint(
            "length(trim(tool_name)) between 1 and 200",
            name=op.f("ck_run_tool_provenance_tool_name_length"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id", "agent_run_id"],
            ["agent_runs.workspace_id", "agent_runs.id"],
            name=op.f(
                "fk_run_tool_provenance_workspace_id_agent_run_id_agent_runs"
            ),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_run_tool_provenance")),
        sa.UniqueConstraint(
            "workspace_id",
            "agent_run_id",
            "sequence_number",
            name=op.f(
                "uq_run_tool_provenance_workspace_id_agent_run_id_sequence_number"
            ),
        ),
        sa.UniqueConstraint(
            "workspace_id",
            "agent_run_id",
            "tool_call_id",
            name=op.f(
                "uq_run_tool_provenance_workspace_id_agent_run_id_tool_call_id"
            ),
        ),
    )


def downgrade() -> None:
    op.drop_table("run_tool_provenance")
    for constraint in (
        "tool_provenance_reason_length",
        "tool_provenance_status_allowed",
        "hermes_resolved_session_id_length",
        "hermes_message_cursor_nonnegative",
    ):
        op.drop_constraint(
            op.f(f"ck_agent_runs_{constraint}"),
            "agent_runs",
            type_="check",
        )
    op.drop_column("agent_runs", "tool_provenance_checked_at")
    op.drop_column("agent_runs", "tool_provenance_reason")
    op.drop_column("agent_runs", "tool_provenance_status")
    op.drop_column("agent_runs", "hermes_resolved_session_id")
    op.drop_column("agent_runs", "hermes_message_cursor")
