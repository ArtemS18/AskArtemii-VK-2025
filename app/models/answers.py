import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Boolean, BigInteger, Text


from .base import BaseORM, CreatedMixin, IDMixin
if typing.TYPE_CHECKING:
    from .users import UserORM
    from .questions import QuestionORM
    from .likes import AnswerLikeORM



class AnswerORM(IDMixin, CreatedMixin, BaseORM):
    __tablename__ = "answers"

    text: Mapped[str] = mapped_column(Text, nullable=False)
    # likes: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=None, nullable=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)

    author: Mapped["UserORM"] = relationship(back_populates="answers")
    question: Mapped["QuestionORM"] = relationship(back_populates="answers")
    likes: Mapped[list["AnswerLikeORM"]] = relationship(back_populates="answer")

