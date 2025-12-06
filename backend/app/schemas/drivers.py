from typing import List, Optional

from pydantic import BaseModel

class Driver(BaseModel):
    id: int
    driver_name: str
    team_id: int
