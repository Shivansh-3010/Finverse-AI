"""add portfolio goals

Revision ID: d558906c8e81
Revises: b71d2b6cb6a2
Create Date: 2026-10-15 16:59:42.474202

"""
"""Add portfolio goals."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd558906c8e81'
down_revision: Union[str, Sequence[str], None] = 'b71d2b6cb6a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "portfolio_goals",
        sa.Column("portfolio_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("goal_type", sa.String(length=50), nullable=False),
        sa.Column(
            "target_amount",
            sa.Numeric(15, 2),
            nullable=False,
        ),
        sa.Column(
            "current_amount",
            sa.Numeric(15, 2),
            server_default="0.00",
            nullable=False,
        ),
        sa.Column(
            "monthly_contribution",
            sa.Numeric(15, 2),
            server_default="0.00",
            nullable=False,
        ),
        sa.Column("target_date", sa.Date(), nullable=False),
        sa.Column(
            "expected_annual_return_pct",
            sa.Numeric(6, 3),
            server_default="7.000",
            nullable=False,
        ),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_portfolio_goals_portfolio_id"),
        "portfolio_goals",
        ["portfolio_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_portfolio_goals_portfolio_id"),
        table_name="portfolio_goals",
    )
    op.drop_table("portfolio_goals")
