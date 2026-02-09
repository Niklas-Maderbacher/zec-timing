from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TeamResponse(BaseModel):
    id: int
    name: str
    category: str
    vehicle_weight: Optional[float] = None
    rfid_identifier: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)