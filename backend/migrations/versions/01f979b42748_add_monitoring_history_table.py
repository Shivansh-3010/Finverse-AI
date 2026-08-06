"""add monitoring history table

Revision ID: 01f979b42748
Revises: cb51d4550f88
Create Date: 2026-08-06 12:01:58.917127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '01f979b42748'
down_revision: Union[str, Sequence[str], None] = 'cb51d4550f88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "monitoring_history",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
        ),

        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "model_name",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "symbol",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "horizon",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "feature_drift",
            sa.Boolean(),
            nullable=False,
        ),

        sa.Column(
            "prediction_drift",
            sa.Boolean(),
            nullable=False,
        ),

        sa.Column(
            "priority",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "recommendation",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "mae",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "rmse",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "mape",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "directional_accuracy",
            sa.Float(),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:

    op.drop_table(
        "monitoring_history"
    )
    # ### end Alembic commands ###
