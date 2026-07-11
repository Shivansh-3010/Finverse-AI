"""upgrade support resistance historical

Revision ID: cb51d4550f88
Revises: 428e0f4395ed
Create Date: 2026-07-07 22:46:13.569442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cb51d4550f88'
down_revision: Union[str, Sequence[str], None] = '428e0f4395ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "support_resistance",
        sa.Column(
            "distance_to_support_pct",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "support_resistance",
        sa.Column(
            "distance_to_resistance_pct",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "support_resistance",
        sa.Column(
            "support_strength",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "support_resistance",
        sa.Column(
            "resistance_strength",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "support_resistance",
        sa.Column(
            "breakout_zone_lower",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "support_resistance",
        sa.Column(
            "breakout_zone_upper",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "support_resistance",
        sa.Column(
            "breakdown_zone_lower",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "support_resistance",
        sa.Column(
            "breakdown_zone_upper",
            sa.Float(),
            nullable=True
        )
    )
    # ### end Alembic commands ###


def downgrade():

    op.drop_column(
        "support_resistance",
        "breakdown_zone_upper"
    )

    op.drop_column(
        "support_resistance",
        "breakdown_zone_lower"
    )

    op.drop_column(
        "support_resistance",
        "breakout_zone_upper"
    )

    op.drop_column(
        "support_resistance",
        "breakout_zone_lower"
    )

    op.drop_column(
        "support_resistance",
        "resistance_strength"
    )

    op.drop_column(
        "support_resistance",
        "support_strength"
    )

    op.drop_column(
        "support_resistance",
        "distance_to_resistance_pct"
    )

    op.drop_column(
        "support_resistance",
        "distance_to_support_pct"
    )    # ### end Alembic commands ###