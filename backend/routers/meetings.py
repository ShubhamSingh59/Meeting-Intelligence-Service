from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from models.meeting import Meeting
from schemas.meeting import MeetingCreate, MeetingResponse
from services.ai_service import analysis_service
from core.security import current_user

router = APIRouter()

## Create a new meeting
@router.post("/api/meetings")
def create_meeting(request: Request, meeting: MeetingCreate, db: Session = Depends(get_db), current_user: str= Depends(current_user)):
    try:
        new_meeting = Meeting(
            title=meeting.title,
            meeting_date=meeting.meetingDate,
            participants=meeting.participants,
            transcript=[segment.model_dump() for segment in meeting.transcript]
        )
        
        db.add(new_meeting)
        db.commit()
        db.refresh(new_meeting)
        
        return {
            "traceId": request.state.trace_id,
            "success": True,
            "data": new_meeting
        }
        
    except Exception as e:
        db.rollback()
        return {
            "traceId": request.state.trace_id,
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }
        }
        
## Get list of all meetings
@router.get("/api/meetings")
def list_meetings(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    meetings = db.query(Meeting).offset(skip).limit(limit).all()
    return {
        "traceId": request.state.trace_id,
        "success": True,
        "data": meetings
    }
    
## Details ablut a specific meeting
@router.get("/api/meetings/{meeting_id}")
def get_meeting(request: Request, meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        return {
            "traceId": request.state.trace_id,
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Meeting not found"
            }
        }
        
        
    return {
        "traceId": request.state.trace_id,
        "success": True,
        "data": meeting
    }
    
    

## Analyze a meeting transcript
@router.post("/api/meetings/{meeting_id}/analyze")
def analyze_meeting(request: Request, meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    if not meeting:
        return {
            "traceId": request.state.trace_id,
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Meeting not found"
            }
        }
    
    if not meeting.transcript or len(meeting.transcript) == 0:
        return {
            "traceId": request.state.trace_id,
            "success": False,
            "error": {
                "code": "BAD_REQUEST",
                "message": "No transcript available for analysis"
            }
        }
        
    try:
        analysis_result = analysis_service.analyze_transcript(meeting.transcript)
        
        return {
            "traceId": request.state.trace_id,
            "success": True,
            "data": analysis_result
        }
        
    except Exception as e:
        return {
            "traceId": request.state.trace_id,
            "success": False,
            "error": {
                "code": "GENERATION_FAILED",
                "message": str(e)
            }
        }