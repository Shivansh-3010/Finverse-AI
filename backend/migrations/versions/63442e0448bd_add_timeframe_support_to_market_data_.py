"""add timeframe support to market data tables"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "63442e0448bd"
down_revision: Union[str, Sequence[str], None] = "f8a9c1d2e3b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.drop_table("candlestick_patterns")
    op.drop_table("technical_indicators")
    op.drop_table("ohlcv_data")

    op.create_table(
        "ohlcv_data",

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

        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.BigInteger(), nullable=False),

        sa.PrimaryKeyConstraint(
            "symbol",
            "timeframe",
            "timestamp",
        ),
    )

    op.create_table(
        "technical_indicators",

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

        sa.Column("rsi", sa.Float(), nullable=False),
        sa.Column("mfi", sa.Float(), nullable=False),

        sa.Column("sma_20", sa.Float(), nullable=False),
        sa.Column("ema_20", sa.Float(), nullable=False),

        sa.Column("macd", sa.Float(), nullable=False),
        sa.Column("macd_signal", sa.Float(), nullable=False),

        sa.Column("adx", sa.Float(), nullable=False),

        sa.Column("atr", sa.Float(), nullable=False),

        sa.Column("obv", sa.Float(), nullable=False),
        sa.Column("vwap", sa.Float(), nullable=False),

        sa.Column("bb_upper", sa.Float(), nullable=False),
        sa.Column("bb_middle", sa.Float(), nullable=False),
        sa.Column("bb_lower", sa.Float(), nullable=False),

        sa.PrimaryKeyConstraint(
            "symbol",
            "timeframe",
            "timestamp",
        ),
    )

    op.create_table(
        "candlestick_patterns",

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
            "pattern_name",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "signal",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "strength",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "confidence",
            sa.Float(),
            nullable=False,
        ),

        sa.Column(
            "candlestick_score",
            sa.Float(),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint(
            "symbol",
            "timeframe",
            "timestamp",
        ),
    )


def downgrade() -> None:
    pass