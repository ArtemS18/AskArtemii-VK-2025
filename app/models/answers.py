from app.models.users import User
from .base import BasePydantic
from .mixin import IDMixin, DateTimeMixin

class Answer(IDMixin,DateTimeMixin, BasePydantic):
    text: str 
    author: User
    votes: int 
    is_correct: bool = False


