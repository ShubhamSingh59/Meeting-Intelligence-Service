from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class TranscriptSegment(BaseModel):
    timestamp: str
    speaker: str
    text: str

class MeetingCreate(BaseModel):
    title: str
    participants: List[str]
    meetingDate: datetime
    transcript: List[TranscriptSegment]

class MeetingResponse(BaseModel):
    id: int
    title: str
    meeting_date: datetime
    participants: List[str]
    
    class Config:
        from_attributes = True