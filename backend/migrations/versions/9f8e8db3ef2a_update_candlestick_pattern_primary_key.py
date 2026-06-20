"""update_candlestick_pattern_primary_key

Revision ID: 9f8e8db3ef2a
Revises: 64fd05dbf2a2
Create Date: 2026-06-20 11:58:12.157669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f8e8db3ef2a'
down_revision: Union[str, Sequence[str], None] = '64fd05dbf2a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.drop_constraint(
        "candlestick_patterns_pkey",
        "candlestick_patterns",
        type_="primary"
    )

    op.create_primary_key(
        "candlestick_patterns_pkey",
        "candlestick_patterns",
        [
            "symbol",
            "timeframe",
            "timestamp",
            "pattern_name",
        ],
    )


def downgrade() -> None:

    op.drop_constraint(
        "candlestick_patterns_pkey",
        "candlestick_patterns",
        type_="primary"
    )

    op.create_primary_key(
        "candlestick_patterns_pkey",
        "candlestick_patterns",
        [
            "symbol",
            "timeframe",
            "timestamp",
        ],
    )
