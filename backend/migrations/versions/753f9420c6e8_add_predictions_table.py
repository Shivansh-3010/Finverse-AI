"""add predictions table

Revision ID: 753f9420c6e8
Revises: 512bca479fed
Create Date: 2026-06-17 00:42:57.032905

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '753f9420c6e8'
down_revision: Union[str, Sequence[str], None] = '512bca479fed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "predictions",

        sa.Column(
            "symbol",
            sa.String(length=20),
            nullable=False
        ),

        sa.Column(
            "timeframe",
            sa.String(length=10),
            nullable=False
        ),

        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False
        ),

        sa.Column(
            "model_name",
            sa.String(length=50),
            nullable=False
        ),

        sa.Column(
            "prediction",
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            "confidence",
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            "horizon",
            sa.String(length=20),
            nullable=False
        ),

        sa.PrimaryKeyConstraint(
            "symbol",
            "timeframe",
            "timestamp",
            "model_name"
        )
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table(
        "predictions"
    )