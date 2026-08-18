"""add portfolio transactions

Revision ID: 284820fff757
Revises: 9afdfe393480
Create Date: 2026-08-18 10:11:03.221688

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "284820fff757"

down_revision: Union[
    str,
    Sequence[str],
    None
] = "9afdfe393480"

branch_labels: Union[
    str,
    Sequence[str],
    None
] = None

depends_on: Union[
    str,
    Sequence[str],
    None
] = None


def upgrade() -> None:
    """Create portfolio transaction tracking."""

    op.create_table(
        "portfolio_transactions",

        sa.Column(
            "portfolio_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "symbol",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "transaction_type",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "quantity",
            sa.Numeric(
                precision=15,
                scale=4,
            ),
            nullable=True,
        ),

        sa.Column(
            "price",
            sa.Numeric(
                precision=15,
                scale=2,
            ),
            nullable=True,
        ),

        sa.Column(
            "amount",
            sa.Numeric(
                precision=15,
                scale=2,
            ),
            nullable=False,
        ),

        sa.Column(
            "transaction_date",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.Column(
            "reference",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )

    op.create_index(
        op.f("ix_portfolio_transactions_portfolio_id"),
        "portfolio_transactions",
        ["portfolio_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_portfolio_transactions_symbol"),
        "portfolio_transactions",
        ["symbol"],
        unique=False,
    )

    op.create_index(
        op.f("ix_portfolio_transactions_transaction_type"),
        "portfolio_transactions",
        ["transaction_type"],
        unique=False,
    )

    op.create_index(
        op.f("ix_portfolio_transactions_transaction_date"),
        "portfolio_transactions",
        ["transaction_date"],
        unique=False,
    )


def downgrade() -> None:
    """Drop portfolio transaction tracking."""

    op.drop_index(
        op.f("ix_portfolio_transactions_transaction_date"),
        table_name="portfolio_transactions",
    )

    op.drop_index(
        op.f("ix_portfolio_transactions_transaction_type"),
        table_name="portfolio_transactions",
    )

    op.drop_index(
        op.f("ix_portfolio_transactions_symbol"),
        table_name="portfolio_transactions",
    )

    op.drop_index(
        op.f("ix_portfolio_transactions_portfolio_id"),
        table_name="portfolio_transactions",
    )

    op.drop_table(
        "portfolio_transactions"
    )