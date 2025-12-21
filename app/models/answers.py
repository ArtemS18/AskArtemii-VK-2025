import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, Integer, Text


from .base import BaseORM, CreatedMixin, IDMixin
if typing.TYPE_CHECKING:
    from .users import UserORM
    from .questions import QuestionORM
    from .grade import AnswerGradeORM



class AnswerORM(IDMixin, CreatedMixin, BaseORM):
    __tablename__ = "answers"

    text: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    dislike_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False, index=True)

    author: Mapped["UserORM"] = relationship(back_populates="answers", lazy="noload")
    question: Mapped["QuestionORM"] = relationship(back_populates="answers", lazy="noload")
    grade: Mapped[list["AnswerGradeORM"]] = relationship(back_populates="answer", lazy="noload")

