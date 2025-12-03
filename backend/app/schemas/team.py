from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TeamBase(BaseModel):
    name: str
    vehicle_weight: Optional[float] = None
    rfid_identifier: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = None
    vehicle_weight: Optional[float] = None
    rfid_identifier: Optional[str] = None


class TeamResponse(TeamBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
