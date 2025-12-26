from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AttemptBase(BaseModel):
    team_id: Optional[int] = None
    driver_id: Optional[int] = None
    challenge_id: Optional[int] = None
    attempt_number: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    average_power: Optional[float] = None
    energy_used: Optional[float] = None

class AttemptCreate(AttemptBase):
    pass

class AttemptUpdate(BaseModel):
    id : int
    team_id: Optional[int] = None
    driver_id: Optional[int] = None
    challenge_id: Optional[int] = None
    attempt_number: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    average_power: Optional[float] = None
    energy_used: Optional[float] = None

class AttemptResponse(AttemptBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
