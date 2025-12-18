from typing import List, Optional
import typing

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String

from .base import BaseORM, CreatedMixin, IDMixin
if typing.TYPE_CHECKING:
    from .questions import QuestionORM
    from .answers import AnswerORM
    from .grade import AnswerGradeORM, QuestionGradeORM


class UserORM(IDMixin,CreatedMixin, BaseORM):
    __tablename__ = "users"

    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    # login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    popular_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    profile: Mapped["UserProfileORM"] = relationship(
        back_populates="user", 
        uselist=False
    )
    questions: Mapped[List["QuestionORM"]] = relationship(back_populates="author")
    answers: Mapped[List["AnswerORM"]] = relationship(back_populates="author")
    answer_grade: Mapped[List["AnswerGradeORM"]] = relationship(back_populates="user")
    question_grade: Mapped[List["QuestionGradeORM"]] = relationship(back_populates="user")
    __table_args__ = (
        Index("indx_popular_count_desc", popular_count.desc()),
    )

class UserProfileORM(IDMixin, BaseORM):
    __tablename__ = "user_profiles"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)
    img_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    nickname: Mapped[str] = mapped_column(String(100), nullable=True,)

    user: Mapped["UserORM"] = relationship(
        back_populates="profile", 
        foreign_keys=[user_id],
        remote_side=[UserORM.id]
    )
