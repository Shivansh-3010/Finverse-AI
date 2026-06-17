"""add prediction evaluations table

Revision ID: 64fd05dbf2a2
Revises: 753f9420c6e8
Create Date: 2026-06-17 11:10:31.401143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64fd05dbf2a2'
down_revision: Union[str, Sequence[str], None] = '753f9420c6e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "prediction_evaluations",

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
            "predicted_return",
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            "actual_return",
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            "absolute_error",
            sa.Float(),
            nullable=False
        ),

        sa.Column(
            "directional_correct",
            sa.Float(),
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
        "prediction_evaluations"
    )