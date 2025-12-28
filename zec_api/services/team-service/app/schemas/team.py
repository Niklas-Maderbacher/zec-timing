from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeamBase(BaseModel):
    name: str
    mean_power: float
    vehicle_weight: float
    rfid_identifier: float

class TeamCreate(TeamBase):
    created_at: Optional[datetime]

class TeamUpdate(BaseModel):
    id : int 
    name: Optional[str] = None
    vehicle_weight: Optional[float] = None
    mean_power: Optional[float] = None
    rfid_identifier: Optional[str] = None

class TeamResponse(TeamBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
