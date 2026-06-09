"""add candlestick patterns table"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f8a9c1d2e3b4"
down_revision: Union[str, Sequence[str], None] = "e6ffbcdc835b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "candlestick_patterns",

        sa.Column(
            "symbol",
            sa.String(length=20),
            nullable=False
        ),

        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.Column(
            "pattern_name",
            sa.String(length=100),
            nullable=False
        ),

        sa.Column(
            "signal",
            sa.String(length=20),
            nullable=False
        ),

        sa.Column(
            "strength",
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            "candlestick_score",
            sa.Float(),
            nullable=False
        ),

        sa.PrimaryKeyConstraint(
            "symbol",
            "timestamp"
        )
    )


def downgrade() -> None:

    op.drop_table(
        "candlestick_patterns"
    )