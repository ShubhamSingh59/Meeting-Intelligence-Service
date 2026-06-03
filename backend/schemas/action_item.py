from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal, List, Optional


class ActionItemCreate(BaseModel):
    task: str
    assignee: EmailStr
    due_date: datetime
    meeting_id: int


# We separate the update schema because users can ONLY update the status
class ActionItemUpdateStatus(BaseModel):
    status: Literal["PENDING", "IN PROGRESS", "COMPLETED"]


class ActionItemResponse(BaseModel):
    id: int
    task: str
    assignee: str
    status: str
    due_date: datetime
    meeting_id: int

    class Config:
        from_attributes = True
