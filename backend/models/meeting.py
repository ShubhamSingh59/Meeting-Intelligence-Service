from sqlalchemy import Column, Integer, String, DateTime, JSON
from database.session import Base
from datetime import datetime

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    meeting_date = Column(DateTime, default=datetime.utcnow)
    participants = Column(JSON, nullable=False)
    transcript = Column(JSON, nullable=True)
    

