from pydantic import BaseModel
from typing import Optional

class Person(BaseModel):
    name: str
    email: str