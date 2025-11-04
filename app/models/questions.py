import typing

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Text

from .base import BaseORM, CreatedMixin, IDMixin
if typing.TYPE_CHECKING:
    from .users import UserORM
    from .tags import TagORM
    from .answers import AnswerORM
    from .likes import QuestionLikeORM


class QuestionORM(IDMixin,CreatedMixin, BaseORM):
    __tablename__ = "questions"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    author: Mapped["UserORM"] = relationship(back_populates="questions")
    tags: Mapped[list["TagORM"]] = relationship(
        secondary="question_tags", back_populates="questions"
    )
    answers: Mapped[list["AnswerORM"]] = relationship(
        back_populates="question"
    )
    likes: Mapped[list["QuestionLikeORM"]] = relationship(
        secondary="question_likes", back_populates="question"
    )

    @property
    def answers_count(self) -> int:
        return len(self.answers) if self.answers is not None else 0

question_tags = Table(
    "question_tags",
    BaseORM.metadata,
    Column("question_id", ForeignKey("questions.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
