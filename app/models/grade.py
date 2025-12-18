import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base import BaseORM, CreatedMixin
if typing.TYPE_CHECKING:
    from .questions import QuestionORM
    from .answers import AnswerORM
    from app.models.users import UserORM


class QuestionGradeORM(CreatedMixin, BaseORM):
    __tablename__ = "question_grade"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False, primary_key=True)
    is_like: Mapped[bool]

    question: Mapped["QuestionORM"] = relationship(
        back_populates="grade"
    )
    user: Mapped["UserORM"] = relationship(
        back_populates="question_grade"
    )

class AnswerGradeORM(CreatedMixin, BaseORM):
    __tablename__ = "answer_grade"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, primary_key=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"), nullable=False, primary_key=True)

    answer: Mapped["AnswerORM"] = relationship(
        back_populates="grade"
    )
    user: Mapped["UserORM"] = relationship(
        back_populates="answer_grade"
    )

