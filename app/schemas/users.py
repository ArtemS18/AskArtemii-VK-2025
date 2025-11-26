# from app.schemas.mixin import IDMixin, DateTimeMixin
# from .base import BasePydantic


# class User(IDMixin, DateTimeMixin, BasePydantic):
#     login: str
#     email: str
#     nickname: str
#     count: int
#     img_url: str | None = None


# class UserCreate(BasePydantic):
#     email: str
#     password: str
#     password_confirm: str
#     nickname: str