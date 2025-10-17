from pydantic import BaseModel, ConfigDict

class BasePydantic(BaseModel):
    model_config = ConfigDict(from_attributes=True)