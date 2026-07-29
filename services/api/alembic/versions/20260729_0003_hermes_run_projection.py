"""Add Hermes run correlation and projection state.

Revision ID: 20260729_0003
Revises: 20260729_0002
Create Date: 2026-07-29
"""

import sqlalchemy as sa
from alembic import op

revision: str = "20260729_0003"
down_revision: str | None = "20260729_0002"
branch_labels: None = None
depends_on: None = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM agent_runs
                    WHERE status IN ('queued', 'running')
                    GROUP BY workspace_id, conversation_id
                    HAVING count(*) > 1
                ) THEN
                    RAISE EXCEPTION
                        'Resolve duplicate queued/running agent runs before upgrade';
                END IF;
            END $$;
            """
        )
    )
    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM agent_runs
                    WHERE status = 'running'
                       OR (
                           status = 'queued'
                           AND (started_at IS NOT NULL OR finished_at IS NOT NULL)
                       )
                       OR (
                           status IN ('succeeded', 'failed', 'cancelled')
                           AND finished_at IS NULL
                       )
                ) THEN
                    RAISE EXCEPTION
                        'Resolve legacy agent-run lifecycle state before upgrade';
                END IF;
            END $$;
            """
        )
    )

    op.drop_constraint(
        op.f("ck_agent_runs_status_allowed"),
        "agent_runs",
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_status_allowed"),
        "agent_runs",
        "status in "
        "('queued', 'submitting', 'running', 'indeterminate', "
        "'succeeded', 'failed', 'cancelled')",
    )
    op.add_column("agent_runs", sa.Column("input", sa.Text(), nullable=True))
    op.add_column(
        "agent_runs",
        sa.Column("submission_attempted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column("agent_runs", sa.Column("hermes_run_id", sa.Text(), nullable=True))
    op.add_column("agent_runs", sa.Column("hermes_session_id", sa.Text(), nullable=True))
    op.add_column(
        "agent_runs",
        sa.Column(
            "event_stream_complete",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False,
        ),
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_input_length"),
        "agent_runs",
        "input is null or length(trim(input)) between 1 and 20000",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_active_run_unfinished"),
        "agent_runs",
        "status not in ('queued', 'submitting', 'running', 'indeterminate') "
        "or finished_at is null",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_terminal_run_finished"),
        "agent_runs",
        "status not in ('succeeded', 'failed', 'cancelled') "
        "or finished_at is not null",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_submitting_shape"),
        "agent_runs",
        "status != 'submitting' or "
        "(input is not null and submission_attempted_at is not null "
        "and started_at is null and hermes_run_id is null "
        "and event_stream_complete = false)",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_running_shape"),
        "agent_runs",
        "status != 'running' or "
        "(input is not null and submission_attempted_at is not null "
        "and started_at is not null and hermes_run_id is not null "
        "and hermes_session_id is not null and event_stream_complete = false)",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_indeterminate_shape"),
        "agent_runs",
        "status != 'indeterminate' or "
        "(input is not null and submission_attempted_at is not null "
        "and event_stream_complete = false)",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_complete_stream_terminal"),
        "agent_runs",
        "event_stream_complete = false "
        "or status in ('succeeded', 'failed', 'cancelled')",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_hermes_run_id_length"),
        "agent_runs",
        "hermes_run_id is null or "
        "(length(hermes_run_id) = 36 and substr(hermes_run_id, 1, 4) = 'run_')",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_hermes_session_id_length"),
        "agent_runs",
        "hermes_session_id is null or length(hermes_session_id) between 1 and 256",
    )
    op.create_index(
        "uq_agent_runs_one_active_per_conversation",
        "agent_runs",
        ("workspace_id", "conversation_id"),
        unique=True,
        postgresql_where=sa.text(
            "status in ('queued', 'submitting', 'running', 'indeterminate')"
        ),
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM agent_runs
                    WHERE status IN ('submitting', 'indeterminate')
                ) THEN
                    RAISE EXCEPTION
                        'Resolve submitting/indeterminate agent runs before downgrade';
                END IF;
            END $$;
            """
        )
    )

    op.drop_index(
        "uq_agent_runs_one_active_per_conversation",
        table_name="agent_runs",
        postgresql_where=sa.text(
            "status in ('queued', 'submitting', 'running', 'indeterminate')"
        ),
    )
    for constraint in (
        "complete_stream_terminal",
        "indeterminate_shape",
        "running_shape",
        "submitting_shape",
        "terminal_run_finished",
        "active_run_unfinished",
    ):
        op.drop_constraint(
            op.f(f"ck_agent_runs_{constraint}"),
            "agent_runs",
            type_="check",
        )
    op.drop_constraint(
        op.f("ck_agent_runs_hermes_session_id_length"),
        "agent_runs",
        type_="check",
    )
    op.drop_constraint(
        op.f("ck_agent_runs_hermes_run_id_length"),
        "agent_runs",
        type_="check",
    )
    op.drop_constraint(
        op.f("ck_agent_runs_input_length"),
        "agent_runs",
        type_="check",
    )
    op.drop_column("agent_runs", "event_stream_complete")
    op.drop_column("agent_runs", "hermes_session_id")
    op.drop_column("agent_runs", "hermes_run_id")
    op.drop_column("agent_runs", "submission_attempted_at")
    op.drop_column("agent_runs", "input")
    op.drop_constraint(
        op.f("ck_agent_runs_status_allowed"),
        "agent_runs",
        type_="check",
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_status_allowed"),
        "agent_runs",
        "status in ('queued', 'running', 'succeeded', 'failed', 'cancelled')",
    )
