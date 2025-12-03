from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DriverBase(BaseModel):
    name: str
    team_id: Optional[int] = None
    weight: Optional[int] = None


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    team_id: Optional[int] = None
    weight: Optional[int] = None


class DriverResponse(DriverBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
