"""expand news provider article id

Revision ID: 512bca479fed
Revises: 106809263507
Create Date: 2026-06-16 16:29:53.482342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '512bca479fed'
down_revision: Union[str, Sequence[str], None] = '106809263507'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.alter_column(
        'news_articles',
        'provider_article_id',
        existing_type=sa.VARCHAR(length=200),
        type_=sa.Text(),
        existing_nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:

    op.alter_column(
        'news_articles',
        'provider_article_id',
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False
    )
    # ### end Alembic commands ###
