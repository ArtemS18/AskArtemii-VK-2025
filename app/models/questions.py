import typing

from sqlalchemy import ForeignKey, Index, Table, Column
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
    likes_count: Mapped[int] = mapped_column(Integer, default=0)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    author: Mapped["UserORM"] = relationship(back_populates="questions")
    tags: Mapped[list["TagORM"]] = relationship(
        secondary="question_tags", back_populates="questions"
    )
    answers: Mapped[list["AnswerORM"]] = relationship(
        back_populates="question"
    )
    likes: Mapped[list["QuestionLikeORM"]] = relationship(
        back_populates="question"
    )

    @property
    def answers_count(self) -> int:
        return len(self.answers) if self.answers is not None else 0
    
    @property
    def likes_orm_count(self) -> int:
        return len(self.likes) if self.likes is not None else 0
    
    __table_args__ = (
        Index("indx_likes_count_desc", likes_count.desc()),
    )


class QuestionTagsORM(BaseORM):
    __tablename__ = "question_tags"
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
