from sqlalchemy import Column, Integer, Text, DateTime
from .database import Base
from datetime import datetime

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False)  # From board_db, not ForeignKey
    user_id = Column(Integer, nullable=False)  # From auth_db
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)