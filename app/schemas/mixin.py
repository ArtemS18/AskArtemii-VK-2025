from pydantic import BaseModel

from datetime import datetime, timezone

class DateTimeMixin(BaseModel):
    created_at: datetime = datetime.now(timezone.utc)

class IDMixin(BaseModel):
    id: int
    
    