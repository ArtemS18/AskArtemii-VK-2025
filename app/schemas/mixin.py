from pydantic import BaseModel
from uuid import UUID
from datetime import datetime, timezone

class DateTimeMixin(BaseModel):
    created_at: datetime = datetime.now(timezone.utc)

class IDMixin(BaseModel):
    id: int

class CSRFMixin(BaseModel):
    csrf_token: UUID
    
    