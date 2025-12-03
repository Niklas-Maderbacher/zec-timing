from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChallengeBase(BaseModel):
    name: str
    max_attempts: Optional[int] = None
    esp_mac: Optional[str] = None


class ChallengeCreate(ChallengeBase):
    pass


class ChallengeUpdate(BaseModel):
    name: Optional[str] = None
    max_attempts: Optional[int] = None
    esp_mac: Optional[str] = None


class ChallengeResponse(ChallengeBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
