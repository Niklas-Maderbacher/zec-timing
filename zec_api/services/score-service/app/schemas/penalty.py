from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PenaltyTypeResponse(BaseModel):
    id: int
    type: str
    amount: int

class PenaltyBase(BaseModel):
    attempt_id: int
    count: int
    penalty_type_id: int

class PenaltyCreate(PenaltyBase):
    pass

class PenaltyUpdate(BaseModel):
    attempt_id: Optional[int] = None
    count: Optional[int] = None
    penalty_type_id: Optional[int] = None

class PenaltyResponse(PenaltyBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
