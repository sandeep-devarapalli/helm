"""Add approval-gated workspace soft preferences.

Revision ID: 20260730_0005
Revises: 20260730_0004
Create Date: 2026-07-30
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260730_0005"
down_revision: str | None = "20260730_0004"
branch_labels: None = None
depends_on: None = None

EMPTY_SNAPSHOT_HASH = (
    "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
)
JSON_TYPE = sa.JSON().with_variant(
    postgresql.JSONB(astext_type=sa.Text()),
    "postgresql",
)
CONTEXT_CHECK = (
    "operating_context in ('individual_self_directed', 'institutional_proprietary')"
)


def upgrade() -> None:
    op.add_column(
        "agent_runs",
        sa.Column(
            "approved_memory_snapshot",
            JSON_TYPE,
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
    )
    op.add_column(
        "agent_runs",
        sa.Column(
            "approved_memory_snapshot_hash",
            sa.Text(),
            server_default=EMPTY_SNAPSHOT_HASH,
            nullable=False,
        ),
    )
    op.create_check_constraint(
        op.f("ck_agent_runs_approved_memory_snapshot_hash_length"),
        "agent_runs",
        "length(approved_memory_snapshot_hash) = 64",
    )
    op.execute(
        """
        CREATE FUNCTION prevent_agent_run_memory_snapshot_mutation()
        RETURNS trigger AS $$
        BEGIN
            IF NEW.approved_memory_snapshot IS DISTINCT FROM OLD.approved_memory_snapshot
               OR NEW.approved_memory_snapshot_hash IS DISTINCT FROM
                  OLD.approved_memory_snapshot_hash THEN
                RAISE EXCEPTION 'agent run memory snapshots are immutable';
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
        """
    )
    op.execute(
        """
        CREATE TRIGGER agent_runs_memory_snapshot_immutable
        BEFORE UPDATE ON agent_runs
        FOR EACH ROW EXECUTE FUNCTION prevent_agent_run_memory_snapshot_mutation()
        """
    )
    op.create_table(
        "memory_change_proposals",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("operating_context", sa.Text(), nullable=False),
        sa.Column("preference_key", sa.Text(), nullable=False),
        sa.Column("proposed_value", sa.Text(), nullable=False),
        sa.Column("evidence", JSON_TYPE, nullable=False),
        sa.Column(
            "proposer_ref",
            sa.Text(),
            server_default="local_user",
            nullable=False,
        ),
        sa.Column("reviewer_ref", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), server_default="pending", nullable=False),
        sa.Column("source_run_id", sa.Uuid(), nullable=True),
        sa.Column("idempotency_key", sa.Text(), nullable=False),
        sa.Column("request_hash", sa.Text(), nullable=False),
        sa.Column("decision_rationale", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "(status = 'pending' and reviewer_ref is null and decided_at is null "
            "and decision_rationale is null) or "
            "(status in ('approved', 'rejected') and reviewer_ref is not null "
            "and decided_at is not null)",
            name=op.f("ck_memory_change_proposals_decision_shape"),
        ),
        sa.CheckConstraint(
            "decision_rationale is null "
            "or length(decision_rationale) between 1 and 1000",
            name=op.f("ck_memory_change_proposals_decision_rationale_length"),
        ),
        sa.CheckConstraint(
            "length(idempotency_key) between 1 and 128",
            name=op.f("ck_memory_change_proposals_idempotency_key_length"),
        ),
        sa.CheckConstraint(
            CONTEXT_CHECK,
            name=op.f("ck_memory_change_proposals_operating_context_allowed"),
        ),
        sa.CheckConstraint(
            "(preference_key = 'communication.response_detail' "
            "and proposed_value in ('concise', 'balanced', 'detailed')) "
            "or (preference_key = 'research.presentation' "
            "and proposed_value in ('narrative', 'bullets', 'table'))",
            name=op.f("ck_memory_change_proposals_preference_allowed"),
        ),
        sa.CheckConstraint(
            "proposer_ref = 'local_user'",
            name=op.f("ck_memory_change_proposals_proposer_ref_allowed"),
        ),
        sa.CheckConstraint(
            "length(request_hash) = 64",
            name=op.f("ck_memory_change_proposals_request_hash_length"),
        ),
        sa.CheckConstraint(
            "reviewer_ref is null or reviewer_ref = 'local_user'",
            name=op.f("ck_memory_change_proposals_reviewer_ref_allowed"),
        ),
        sa.CheckConstraint(
            "status in ('pending', 'approved', 'rejected')",
            name=op.f("ck_memory_change_proposals_status_allowed"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk_memory_change_proposals_workspace_id_workspaces"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id", "source_run_id"],
            ["agent_runs.workspace_id", "agent_runs.id"],
            name=op.f(
                "fk_memory_change_proposals_workspace_id_source_run_id_agent_runs"
            ),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_memory_change_proposals")),
        sa.UniqueConstraint(
            "workspace_id",
            "id",
            name=op.f("uq_memory_change_proposals_workspace_id_id"),
        ),
        sa.UniqueConstraint(
            "workspace_id",
            "idempotency_key",
            name=op.f(
                "uq_memory_change_proposals_workspace_id_idempotency_key"
            ),
        ),
    )
    op.create_index(
        "ix_memory_change_proposals_workspace_created_id",
        "memory_change_proposals",
        ["workspace_id", "created_at", "id"],
    )
    op.create_table(
        "workspace_soft_preferences",
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("preference_key", sa.Text(), nullable=False),
        sa.Column("operating_context", sa.Text(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("source_proposal_id", sa.Uuid(), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            CONTEXT_CHECK,
            name=op.f("ck_workspace_soft_preferences_operating_context_allowed"),
        ),
        sa.CheckConstraint(
            "(preference_key = 'communication.response_detail' "
            "and value in ('concise', 'balanced', 'detailed')) "
            "or (preference_key = 'research.presentation' "
            "and value in ('narrative', 'bullets', 'table'))",
            name=op.f("ck_workspace_soft_preferences_preference_allowed"),
        ),
        sa.CheckConstraint(
            "revision > 0",
            name=op.f("ck_workspace_soft_preferences_revision_positive"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id"],
            ["workspaces.id"],
            name=op.f("fk_workspace_soft_preferences_workspace_id_workspaces"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id", "source_proposal_id"],
            ["memory_change_proposals.workspace_id", "memory_change_proposals.id"],
            name=op.f(
                "fk_workspace_soft_preferences_workspace_id_source_proposal_id_memory_change_proposals"
            ),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "workspace_id",
            "preference_key",
            name=op.f("pk_workspace_soft_preferences"),
        ),
    )
    op.create_table(
        "memory_proposal_events",
        sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("workspace_id", sa.Uuid(), nullable=False),
        sa.Column("proposal_id", sa.Uuid(), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column(
            "actor_ref",
            sa.Text(),
            server_default="local_user",
            nullable=False,
        ),
        sa.Column("operating_context", sa.Text(), nullable=False),
        sa.Column(
            "payload",
            JSON_TYPE,
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "actor_ref = 'local_user'",
            name=op.f("ck_memory_proposal_events_actor_ref_allowed"),
        ),
        sa.CheckConstraint(
            "(sequence_number = 0 and event_type = 'proposed') or "
            "(sequence_number = 1 and event_type in ('approved', 'rejected'))",
            name=op.f("ck_memory_proposal_events_event_shape"),
        ),
        sa.CheckConstraint(
            CONTEXT_CHECK,
            name=op.f("ck_memory_proposal_events_operating_context_allowed"),
        ),
        sa.CheckConstraint(
            "sequence_number in (0, 1)",
            name=op.f("ck_memory_proposal_events_sequence_allowed"),
        ),
        sa.ForeignKeyConstraint(
            ["workspace_id", "proposal_id"],
            ["memory_change_proposals.workspace_id", "memory_change_proposals.id"],
            name=op.f(
                "fk_memory_proposal_events_workspace_id_proposal_id_memory_change_proposals"
            ),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_memory_proposal_events")),
        sa.UniqueConstraint(
            "workspace_id",
            "proposal_id",
            "sequence_number",
            name=op.f(
                "uq_memory_proposal_events_workspace_id_proposal_id_sequence_number"
            ),
        ),
    )
    op.execute(
        """
        CREATE FUNCTION prevent_memory_proposal_event_mutation()
        RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'memory proposal events are append-only';
        END;
        $$ LANGUAGE plpgsql
        """
    )
    op.execute(
        """
        CREATE TRIGGER memory_proposal_events_append_only
        BEFORE UPDATE OR DELETE ON memory_proposal_events
        FOR EACH ROW EXECUTE FUNCTION prevent_memory_proposal_event_mutation()
        """
    )


def downgrade() -> None:
    op.execute(
        "DROP TRIGGER IF EXISTS memory_proposal_events_append_only "
        "ON memory_proposal_events"
    )
    op.execute("DROP FUNCTION IF EXISTS prevent_memory_proposal_event_mutation()")
    op.drop_table("memory_proposal_events")
    op.drop_table("workspace_soft_preferences")
    op.drop_index(
        "ix_memory_change_proposals_workspace_created_id",
        table_name="memory_change_proposals",
    )
    op.drop_table("memory_change_proposals")
    op.execute(
        "DROP TRIGGER IF EXISTS agent_runs_memory_snapshot_immutable ON agent_runs"
    )
    op.execute(
        "DROP FUNCTION IF EXISTS prevent_agent_run_memory_snapshot_mutation()"
    )
    op.drop_constraint(
        op.f("ck_agent_runs_approved_memory_snapshot_hash_length"),
        "agent_runs",
        type_="check",
    )
    op.drop_column("agent_runs", "approved_memory_snapshot_hash")
    op.drop_column("agent_runs", "approved_memory_snapshot")
