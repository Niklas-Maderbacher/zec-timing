from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


class DriverBase(BaseModel):
    name: str
    team_id: Optional[int] = None
    weight: Optional[int] = None


class DriverCreate(DriverBase):
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    team_id: Optional[int] = None
    weight: Optional[int] = None


class DriverResponse(DriverBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
