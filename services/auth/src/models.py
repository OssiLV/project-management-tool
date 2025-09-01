from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # e.g., 'admin', 'project_manager', 'member', 'guest'
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = soft deleted

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
