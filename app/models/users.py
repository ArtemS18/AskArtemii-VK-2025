from app.models.mixin import IDMixin, DateTimeMixin
from .base import BasePydantic


class User(IDMixin, DateTimeMixin, BasePydantic):
    login: str
    email: str
    nickname: str
    count: int
    img_url: str | None = None