"""Add portfolio snapshots

Revision ID: b71d2b6cb6a2
Revises: 284820fff757
Create Date: 2026-08-19 22:20:39.815598

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b71d2b6cb6a2'
down_revision: Union[str, Sequence[str], None] = '284820fff757'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "portfolio_snapshots",
        sa.Column(
            "portfolio_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "snapshot_time",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "portfolio_value",
            sa.Numeric(
                precision=15,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "cash",
            sa.Numeric(
                precision=15,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "invested_value",
            sa.Numeric(
                precision=15,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "return_value",
            sa.Numeric(
                precision=15,
                scale=2,
            ),
            nullable=False,
        ),
        sa.Column(
            "risk_score",
            sa.Numeric(
                precision=10,
                scale=4,
            ),
            nullable=True,
        ),
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
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
        op.f("ix_portfolio_snapshots_portfolio_id"),
        "portfolio_snapshots",
        ["portfolio_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_portfolio_snapshots_snapshot_time"),
        "portfolio_snapshots",
        ["snapshot_time"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_portfolio_snapshots_snapshot_time"),
        table_name="portfolio_snapshots",
    )

    op.drop_index(
        op.f("ix_portfolio_snapshots_portfolio_id"),
        table_name="portfolio_snapshots",
    )

    op.drop_table("portfolio_snapshots")
    # ### end Alembic commands ###
