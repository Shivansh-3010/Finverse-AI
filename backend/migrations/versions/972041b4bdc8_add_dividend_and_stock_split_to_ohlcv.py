"""add_dividend_and_stock_split_to_ohlcv

Revision ID: 972041b4bdc8
Revises: 9f8e8db3ef2a
Create Date: 2026-06-20 14:57:36.602662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '972041b4bdc8'
down_revision: Union[str, Sequence[str], None] = '9f8e8db3ef2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "ohlcv_data",
        sa.Column(
            "dividend",
            sa.Float(),
            nullable=False,
            server_default="0"
        )
    )

    op.add_column(
        "ohlcv_data",
        sa.Column(
            "stock_split",
            sa.Float(),
            nullable=False,
            server_default="0"
        )
    )
    # ### end Alembic commands ###


def downgrade() -> None:

    op.drop_column(
        "ohlcv_data",
        "stock_split"
    )

    op.drop_column(
        "ohlcv_data",
        "dividend"
    )
    # ### end Alembic commands ###
