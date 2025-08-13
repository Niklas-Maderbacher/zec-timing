from typing import List, Optional

from pydantic import BaseModel

class Timestamp(BaseModel):
    timestamp: Optional[List[str]] = None