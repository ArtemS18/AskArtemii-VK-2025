import typing

from sqlalchemy import CheckConstraint, ForeignKey, Index, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Text

from .base import BaseORM, CreatedMixin, IDMixin
if typing.TYPE_CHECKING:
    from .users import UserORM
    from .tags import TagORM
    from .answers import AnswerORM
    from .grade import QuestionGradeORM


class QuestionORM(IDMixin,CreatedMixin, BaseORM):
    __tablename__ = "questions"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    dislike_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    author: Mapped["UserORM"] = relationship(back_populates="questions")
    tags: Mapped[list["TagORM"]] = relationship(
        secondary="question_tags", back_populates="questions"
    )
    answers: Mapped[list["AnswerORM"]] = relationship(
        back_populates="question"
    )
    grade: Mapped[list["QuestionGradeORM"]] = relationship(
        back_populates="question",
        lazy="noload"
    )

    @property
    def answers_count(self) -> int:
        return len(self.answers) if self.answers is not None else 0
    
    @property
    def grade_orm_count(self) -> int:
        return len(self.grade) if self.grade is not None else 0
    
    __table_args__ = (
        Index("indx_grade_count_desc", like_count.desc()),
        CheckConstraint("like_count >= 0", name="check_like_count"),
        CheckConstraint("dislike_count >= 0", name="check_dislike_count")
    )


class QuestionTagsORM(BaseORM):
    __tablename__ = "question_tags"
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
