from app.entities.answers import Answer
from app.entities.mixin import IDMixin, DateTimeMixin
from app.entities.users import User
from .base import BasePydantic
from .tags import Tag


class Question(IDMixin, DateTimeMixin, BasePydantic):
    title: str 
    text: str
    #user_id: int 
    author: User
    likes: int
    tags: list[Tag]
    answers_count: int
    answers :list[Answer]



