from fastapi import FastAPI, APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from models.action_item import ActionItem
from datetime import datetime
from schemas.action_item import (
    ActionItemCreate,
    ActionItemResponse,
    ActionItemUpdateStatus,
)
from typing import Optional

router = APIRouter()


## Create a new action item
@router.post("/api/action-items")
def create_action_item(
    request: Request, action_item: ActionItemCreate, db: Session = Depends(get_db)
):
    try:
        new_action_item = ActionItem(
            task=action_item.task,
            assignee=action_item.assignee,
            due_date=action_item.due_date,
            meeting_id=action_item.meeting_id,
            status="PENDING",  # Default status while creating an action item
        )

        db.add(new_action_item)
        db.commit()
        db.refresh(new_action_item)

        return {
            "traceId": request.state.trace_id,
            "success": True,
            "data": new_action_item,
        }

    except Exception as e:
        db.rollback()
        return {
            "traceId": request.state.trace_id,
            "success": False,
            "error": {"code": "INTERNAL_SERVER_ERROR", "message": str(e)},
        }


## Update status of an action item
@router.patch("/api/action-items/{item_id}/status")
def update_action_item_status(
    request: Request,
    item_id: int,
    status_update: ActionItemUpdateStatus,
    db: Session = Depends(get_db),
):
    action_item = db.query(ActionItem).filter(ActionItem.id == item_id).first()

    if not action_item:
        return {
            "traceId": request.state.trace_id,
            "success": False,
            "error": {"code": "NOT_FOUND", "message": "Action item not found"},
        }

    try:
        action_item.status = status_update.status
        db.commit()
        db.refresh(action_item)

        return {
            "traceId": request.state.trace_id,
            "success": True,
            "data": action_item,
        }

    except Exception as e:
        db.rollback()
        return {
            "traceId": request.state.trace_id,
            "success": False,
            "error": {"code": "INTERNAL_SERVER_ERROR", "message": str(e)},
        }


## Get the list of action items
@router.get("/api/action-items")
def get_action_items(
    request: Request,
    status: Optional[str] = None,
    assignee: Optional[str] = None,
    meeting_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    query = db.query(ActionItem)

    if status:
        query = query.filter(ActionItem.status == status)
    if assignee:
        query = query.filter(ActionItem.assignee == assignee)
    if meeting_id:
        query = query.filter(ActionItem.meeting_id == meeting_id)

    action_items = query.all()

    return {
        "traceId": request.state.trace_id,
        "success": True,
        "data": action_items,
    }


## Overdue endpoint
@router.get("/api/action-items/overdue")
def get_overdue_action_items(request: Request, db: Session = Depends(get_db)):
    current_time = datetime.utcnow()
    overdue_items = (
        db.query(ActionItem).filter(
            ActionItem.due_date < current_time, 
            ActionItem.status != "COMPLETED"
            ).all()
    )

    return {
        "traceId": request.state.trace_id,
        "success": True,
        "data": overdue_items,
    }
