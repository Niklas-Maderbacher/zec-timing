from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChallengeBase(BaseModel):
    name: str
    max_attempts: Optional[int] = None
    esp_mac_start1: Optional[str] = None
    esp_mac_start2: Optional[str] = None
    esp_mac_finish1: Optional[str] = None
    esp_mac_finish2: Optional[str] = None

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    max_attempts: Optional[int] = None
    esp_mac_start1: Optional[str] = None
    esp_mac_start2: Optional[str] = None
    esp_mac_finish1: Optional[str] = None
    esp_mac_finish2: Optional[str] = None

class ChallengeResponse(ChallengeBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
