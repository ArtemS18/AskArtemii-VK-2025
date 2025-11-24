from .base import BasePydantic
from .mixin import IDMixin
class Tag(IDMixin, BasePydantic):
    name: str 
    popular: int