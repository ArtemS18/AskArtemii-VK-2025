from datetime import datetime, timezone
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import BigInteger, DateTime


class BaseORM(DeclarativeBase):
    pass
    

class IDMixin(BaseORM):
    __abstract__ = True
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)

class CreatedMixin(BaseORM):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), server_default=func.now())