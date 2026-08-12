"""add horizon to prediction evaluations

Revision ID: 9afdfe393480
Revises: 01f979b42748
Create Date: 2026-08-11 14:34:43.391824

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "9afdfe393480"

down_revision: Union[
    str,
    Sequence[str],
    None
] = "01f979b42748"

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
    """Upgrade schema."""

    # Add the column as nullable first so existing
    # evaluation records can be backfilled safely.
    op.add_column(
        "prediction_evaluations",
        sa.Column(
            "horizon",
            sa.String(length=20),
            nullable=True,
        ),
    )

    # Existing evaluation records were generated for
    # the current 1d prediction pipeline.
    op.execute(
        sa.text(
            """
            UPDATE prediction_evaluations
            SET horizon = '1d'
            WHERE horizon IS NULL
            """
        )
    )

    # Horizon is required for all future evaluation records.
    op.alter_column(
        "prediction_evaluations",
        "horizon",
        existing_type=sa.String(length=20),
        nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "prediction_evaluations",
        "horizon",
    )