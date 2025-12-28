from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TeamResponse(BaseModel):
    id: int
    name: str
    vehicle_weight: Optional[float] = None
    rfid_identifier: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True