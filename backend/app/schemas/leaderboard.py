from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeaderboardBase(BaseModel):
    team_id: Optional[int] = None
    challenge_id: Optional[int] = None
    best_score: Optional[float] = None


class LeaderboardCreate(LeaderboardBase):
    pass


class LeaderboardUpdate(BaseModel):
    team_id: Optional[int] = None
    challenge_id: Optional[int] = None
    best_score: Optional[float] = None


class LeaderboardResponse(LeaderboardBase):
    id: int
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
