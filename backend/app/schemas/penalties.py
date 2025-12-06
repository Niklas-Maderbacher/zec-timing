from typing import List, Optional
from pydantic import BaseModel

from app.models.penalties import PenaltyType

class Penalty(BaseModel):
    id: int
    penalty_amount: float
    type: PenaltyType