from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base
from datetime import datetime

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, nullable=False)  # user_id from auth_db, no ForeignKey because cross-DB
    created_at = Column(DateTime, default=datetime.utcnow)

class ProjectMember(Base):
    __tablename__ = "project_members"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    role = Column(String(50), nullable=False)  # e.g., 'owner', 'member', 'guest'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(String(50))  # e.g., admin, member
    created_at = Column(DateTime, default=datetime.utcnow)