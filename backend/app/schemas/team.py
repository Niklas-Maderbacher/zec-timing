from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


class TeamBase(BaseModel):
    name: str
    vehicle_weight: Optional[float] = None
    rfid_identifier: Optional[str] = None


class TeamCreate(TeamBase):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TeamUpdate(BaseModel):
    id : int 
    name: Optional[str] = None
    vehicle_weight: Optional[float] = None
    rfid_identifier: Optional[str] = None


class TeamResponse(TeamBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
