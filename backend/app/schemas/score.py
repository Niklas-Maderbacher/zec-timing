from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScoreBase(BaseModel):
    attempt_id: Optional[int] = None
    value: Optional[float] = None


class ScoreCreate(ScoreBase):
    pass


class ScoreUpdate(BaseModel):
    attempt_id: Optional[int] = None
    value: Optional[float] = None


class ScoreResponse(ScoreBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
