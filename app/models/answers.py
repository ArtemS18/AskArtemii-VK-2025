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
<<<<<<< HEAD
    # likes: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=None, nullable=True)
=======
    likes_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False, index=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
>>>>>>> 27c9efe6f77bb5e364f5b23bb97f933586ba98d6

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False, index=True)

    author: Mapped["UserORM"] = relationship(back_populates="answers")
    question: Mapped["QuestionORM"] = relationship(back_populates="answers")
    likes: Mapped[list["AnswerLikeORM"]] = relationship(back_populates="answer")

