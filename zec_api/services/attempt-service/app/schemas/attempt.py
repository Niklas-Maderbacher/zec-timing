from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AttemptBase(BaseModel):
    team_id: int
    driver_id: int
    challenge_id: int
    start_time: datetime
    end_time: datetime
    energy_used: float

class AttemptCreate(AttemptBase):
    is_valid: Optional[bool] = True
    penalty_count: Optional[int] = 0
    penalty_type: Optional[int] = None

class AttemptUpdate(BaseModel):
    team_id: Optional[int] = None
    driver_id: Optional[int] = None
    challenge_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    energy_used: Optional[float] = None
    is_valid: Optional[bool] = None

class AttemptResponse(AttemptBase):
    id: int
    created_at: datetime
    is_valid: bool

    model_config = ConfigDict(from_attributes=True)
