from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.penalty import PenaltyType

class PenaltyBase(BaseModel):
    attempt_id: int
    penalty_amount: float
    type: PenaltyType

class PenaltyCreate(PenaltyBase):
    pass

class PenaltyUpdate(BaseModel):
    attempt_id: Optional[int] = None
    penalty_amount: Optional[float] = None
    type: Optional[PenaltyType] = None

class PenaltyResponse(PenaltyBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
