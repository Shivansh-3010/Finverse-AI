"""add support resistance table

Revision ID: 367213c3ca51
Revises: 63442e0448bd
Create Date: 2026-06-13 14:48:53.415537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '367213c3ca51'
down_revision: Union[str, Sequence[str], None] = '63442e0448bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "support_resistance",

        sa.Column(
            "symbol",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "timeframe",
            sa.String(length=10),
            nullable=False,
        ),

        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "nearest_support",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "nearest_resistance",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "signal_level",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "signal",
            sa.String(length=20),
            nullable=True,
        ),

        sa.PrimaryKeyConstraint(
            "symbol",
            "timeframe",
            "timestamp",
        ),
    )


def downgrade() -> None:

    op.drop_table(
        "support_resistance"
    )