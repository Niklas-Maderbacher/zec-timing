from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttemptBase(BaseModel):
    team_id: int
    driver_id: int
    challenge_id: int
    attempt_number: int
    start_time: datetime
    end_time: datetime
    energy_used: float

class AttemptCreate(AttemptBase):
    pass

class AttemptUpdate(BaseModel):
    team_id: Optional[int] = None
    driver_id: Optional[int] = None
    challenge_id: Optional[int] = None
    attempt_number: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    energy_used: Optional[float] = None

class AttemptResponse(AttemptBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
