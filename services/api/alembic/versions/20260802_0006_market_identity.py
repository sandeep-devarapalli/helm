"""Add the canonical market identity spine.

Revision ID: 20260802_0006
Revises: 20260730_0005
Create Date: 2026-08-02
"""

import sqlalchemy as sa
from alembic import op

revision: str = "20260802_0006"
down_revision: str | None = "20260730_0005"
branch_labels: None = None
depends_on: None = None


def upgrade() -> None:
    op.create_table(
        "currencies",
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("minor_unit", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "length(code) between 3 and 12 "
            "and code = upper(code) and code not like '% %'",
            name=op.f("ck_currencies_code_shape"),
        ),
        sa.CheckConstraint(
            "minor_unit between 0 and 18",
            name=op.f("ck_currencies_minor_unit_range"),
        ),
        sa.CheckConstraint(
            "length(trim(name)) between 1 and 120",
            name=op.f("ck_currencies_name_length"),
        ),
        sa.PrimaryKeyConstraint("code", name=op.f("pk_currencies")),
    )
    op.create_table(
        "venues",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("mic", sa.Text(), nullable=True),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("timezone", sa.Text(), nullable=False),
        sa.CheckConstraint(
            "length(code) between 2 and 32 "
            "and code = upper(code) and code not like '% %'",
            name=op.f("ck_venues_code_shape"),
        ),
        sa.CheckConstraint(
            "kind in ('securities_exchange', 'crypto_venue')",
            name=op.f("ck_venues_kind_allowed"),
        ),
        sa.CheckConstraint(
            "mic is null or "
            "(length(mic) = 4 and mic = upper(mic) and mic not like '% %')",
            name=op.f("ck_venues_mic_shape"),
        ),
        sa.CheckConstraint(
            "length(trim(name)) between 1 and 160",
            name=op.f("ck_venues_name_length"),
        ),
        sa.CheckConstraint(
            "length(trim(timezone)) between 1 and 64",
            name=op.f("ck_venues_timezone_length"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_venues")),
        sa.UniqueConstraint("code", name=op.f("uq_venues_code")),
        sa.UniqueConstraint("mic", name=op.f("uq_venues_mic")),
    )
    op.create_table(
        "instruments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "kind in ('common_stock', 'etf', 'crypto_asset')",
            name=op.f("ck_instruments_kind_allowed"),
        ),
        sa.CheckConstraint(
            "length(trim(name)) between 1 and 200",
            name=op.f("ck_instruments_name_length"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_instruments")),
    )
    op.create_table(
        "listings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("instrument_id", sa.Uuid(), nullable=False),
        sa.Column("venue_id", sa.Uuid(), nullable=False),
        sa.Column("venue_symbol", sa.Text(), nullable=False),
        sa.Column("quote_currency_code", sa.Text(), nullable=False),
        sa.Column("price_increment", sa.Numeric(38, 18), nullable=False),
        sa.Column("quantity_increment", sa.Numeric(38, 18), nullable=False),
        sa.Column("status", sa.Text(), server_default="active", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "price_increment > 0",
            name=op.f("ck_listings_price_increment_positive"),
        ),
        sa.CheckConstraint(
            "quantity_increment > 0",
            name=op.f("ck_listings_quantity_increment_positive"),
        ),
        sa.CheckConstraint(
            "status in ('active', 'inactive')",
            name=op.f("ck_listings_status_allowed"),
        ),
        sa.CheckConstraint(
            "length(trim(venue_symbol)) between 1 and 64",
            name=op.f("ck_listings_venue_symbol_length"),
        ),
        sa.CheckConstraint(
            "venue_symbol = trim(venue_symbol)",
            name=op.f("ck_listings_venue_symbol_canonical"),
        ),
        sa.ForeignKeyConstraint(
            ("instrument_id",),
            ("instruments.id",),
            name=op.f("fk_listings_instrument_id_instruments"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ("quote_currency_code",),
            ("currencies.code",),
            name=op.f("fk_listings_quote_currency_code_currencies"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ("venue_id",),
            ("venues.id",),
            name=op.f("fk_listings_venue_id_venues"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_listings")),
        sa.UniqueConstraint(
            "venue_id",
            "venue_symbol",
            name=op.f("uq_listings_venue_id_venue_symbol"),
        ),
    )
    op.create_index(
        "ix_listings_instrument_venue",
        "listings",
        ("instrument_id", "venue_id"),
    )


def downgrade() -> None:
    op.drop_index("ix_listings_instrument_venue", table_name="listings")
    op.drop_table("listings")
    op.drop_table("instruments")
    op.drop_table("venues")
    op.drop_table("currencies")
