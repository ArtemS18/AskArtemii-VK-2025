from typing import List, Optional
import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String

from .base import BaseORM, CreatedMixin, IDMixin
if typing.TYPE_CHECKING:
    from .questions import QuestionORM
    from .answers import AnswerORM
    from .likes import AnswerLikeORM, QuestionLikeORM


class UserORM(IDMixin,CreatedMixin, BaseORM):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False)
    popular_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    img_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    questions: Mapped[List["QuestionORM"]] = relationship(back_populates="author")
    answers: Mapped[List["AnswerORM"]] = relationship(back_populates="author")
    answer_likes: Mapped[List["AnswerLikeORM"]] = relationship(back_populates="answer_likes")
    question_likes: Mapped[List["QuestionLikeORM"]] = relationship(back_populates="question_likes")

