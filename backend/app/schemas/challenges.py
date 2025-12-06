from typing import List, Optional, Dict

from pydantic import BaseModel

class Challenge(BaseModel):
    id: int
    name: str
    esp_mac_start1: str
    esp_mac_start2: str
    esp_mac_finish1: str
    esp_mac_finish2: str
