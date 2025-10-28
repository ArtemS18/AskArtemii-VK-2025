from app.entities.users import User
from app.entities.base import BasePydantic
from app.entities.mixin import IDMixin, DateTimeMixin


class Answer(IDMixin, DateTimeMixin, BasePydantic):
    text: str
    author: User
    votes: int
    is_correct: bool = False
