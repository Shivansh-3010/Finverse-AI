"""cleanup legacy risk columns

Revision ID: 428e0f4395ed
Revises: 2297dda62b0b
Create Date: 2026-07-07 15:04:29.589686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '428e0f4395ed'
down_revision: Union[str, Sequence[str], None] = '2297dda62b0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.drop_column(
        "risk_metrics",
        "volatility"
    )

    op.drop_column(
        "risk_metrics",
        "drawdown"
    )

    op.drop_column(
        "risk_metrics",
        "var_95"
    )

    op.drop_column(
        "risk_metrics",
        "expected_shortfall"
    )


def downgrade():

    op.add_column(
        "risk_metrics",
        sa.Column(
            "volatility",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "drawdown",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "var_95",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "expected_shortfall",
            sa.Float(),
            nullable=True
        )
    )
