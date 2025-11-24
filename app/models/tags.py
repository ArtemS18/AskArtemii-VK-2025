import typing

from sqlalchemy import Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from .base import BaseORM, IDMixin
if typing.TYPE_CHECKING:
    from .questions import QuestionORM

class TagORM(IDMixin, BaseORM):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    popular_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    questions: Mapped[list["QuestionORM"]] = relationship(
        secondary="question_tags", back_populates="tags"
    )
    __table_args__ = (
        Index("idx_popular_count_desc", popular_count.desc()),
    )

