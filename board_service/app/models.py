from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from .database import Base
from datetime import datetime

class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)  # Từ project_db, không ForeignKey
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class List(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True, index=True)
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    name = Column(String(255), nullable=False)
    position = Column(Integer, default=0)  # To sort

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("lists.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    assignee_id = Column(Integer)  # user_id from auth_db
    priority = Column(String(50))  # e.g., 'high', 'medium', 'low'
    status = Column(String(50), default='todo')
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class TaskLabel(Base):
    __tablename__ = "task_labels"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    label = Column(String(100), nullable=False)

class TaskAttachment(Base):
    __tablename__ = "task_attachments"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    file_url = Column(String(512), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)