from .base import BaseModel

class BaseUser(BaseModel):
    nickname: str

class User(BaseUser):
    id: int 
    img_url: str | None = None

class UserForm(BaseUser):
    email: str
    password: str
    password_confirm: str

class UserWrite(BaseUser):
    email: str
    hashed_password: str
    img_url: str | None = None

class UserUpdate(BaseModel):
    email: str | None = None
    nickname: str | None = None
    img_url: str | None = None
