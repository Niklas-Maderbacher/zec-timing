from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ScoreBase(BaseModel):
    attempt_id: Optional[int] = None
    challenge_id: Optional[int] = None
    value: Optional[float] = None

class ScoreCreate(BaseModel):
    attempt_id: int

class ScoreUpdate(BaseModel):
    value: float

class ScoreResponse(ScoreBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
