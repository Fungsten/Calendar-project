from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class Event(BaseModel):
    name: str
    location: str
    time_start: datetime = None
    time_end: datetime = None
    is_all_day: Optional[bool] = False
    participants: List[str] = []

    