from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class Event(BaseModel):
    name: str
    location: str
    start_time: datetime = None
    end_time: datetime = None
    is_all_day: Optional[bool] = False
    participants: List[str] = []

    