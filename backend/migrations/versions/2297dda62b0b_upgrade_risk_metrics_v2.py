"""upgrade risk metrics v2

Revision ID: 2297dda62b0b
Revises: c422ca671609
Create Date: 2026-07-07 13:55:13.560315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2297dda62b0b'
down_revision: Union[str, Sequence[str], None] = 'c422ca671609'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "risk_metrics",
        sa.Column(
            "volatility_252d",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "volatility_504d",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "drawdown_252d",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "drawdown_504d",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "var95_252d",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "var95_504d",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "expected_shortfall_252d",
            sa.Float(),
            nullable=True
        )
    )

    op.add_column(
        "risk_metrics",
        sa.Column(
            "expected_shortfall_504d",
            sa.Float(),
            nullable=True
        )
    )
    # ### end Alembic commands ###


def downgrade() -> None:

    op.drop_column(
        "risk_metrics",
        "expected_shortfall_504d"
    )

    op.drop_column(
        "risk_metrics",
        "expected_shortfall_252d"
    )

    op.drop_column(
        "risk_metrics",
        "var95_504d"
    )

    op.drop_column(
        "risk_metrics",
        "var95_252d"
    )

    op.drop_column(
        "risk_metrics",
        "drawdown_504d"
    )

    op.drop_column(
        "risk_metrics",
        "drawdown_252d"
    )

    op.drop_column(
        "risk_metrics",
        "volatility_504d"
    )

    op.drop_column(
        "risk_metrics",
        "volatility_252d"
    )
    # ### end Alembic commands ###
