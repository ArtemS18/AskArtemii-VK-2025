"""add check

Revision ID: 051e48bf356b
Revises: 8e590272304e
Create Date: 2025-12-19 02:08:39.753023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '051e48bf356b'
down_revision: Union[str, Sequence[str], None] = '8e590272304e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем CHECK constraints для существующей таблицы
    op.create_check_constraint(
        "check_like_count",
        "questions",
        sa.text("like_count >= 0"),
    )
    op.create_check_constraint(
        "check_dislike_count",
        "questions",
        sa.text("dislike_count >= 0"),
    )


def downgrade() -> None:
    # Важно: для Postgres нужен type_="check"
    op.drop_constraint("check_dislike_count", "questions", type_="check")
    op.drop_constraint("check_like_count", "questions", type_="check")