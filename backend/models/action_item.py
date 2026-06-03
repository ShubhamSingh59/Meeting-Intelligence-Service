from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database.session import Base

class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255), nullable=False)
    status = Column(String(50), default="PENDING")
    assignee = Column(String(255), nullable=True)
    due_date = Column(DateTime, nullable=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    
    
