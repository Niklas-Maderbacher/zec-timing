from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeamBase(BaseModel):
    name: str
    mean_power: float
    vehicle_weight: float
    rfid_identifier: str

class TeamCreate(TeamBase):
    created_at: Optional[datetime] = datetime.utcnow()

class TeamUpdate(BaseModel):
    name: Optional[str] = None
    vehicle_weight: Optional[float] = None
    mean_power: Optional[float] = None
    rfid_identifier: Optional[str] = None

class TeamResponse(TeamBase):
    id: int
    created_at: datetime

    class ConfigDict:
        from_attributes = True
