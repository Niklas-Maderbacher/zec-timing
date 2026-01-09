from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DriverBase(BaseModel):
    name: str
    team_id: int
    weight: float

class DriverCreate(DriverBase):
    created_at: Optional[datetime] = datetime.utcnow()

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    team_id: Optional[int] = None
    weight: Optional[float] = None

class DriverResponse(DriverBase):
    id: int
    created_at: datetime
    class ConfigDict:
        from_attributes = True
