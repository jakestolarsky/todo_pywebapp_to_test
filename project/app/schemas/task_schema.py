from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    id: Optional[int] = None
    name: str
    completed: bool = False