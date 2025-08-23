from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # To map from ORM

class ProjectMemberCreate(BaseModel):
    user_id: int
    role: str  # e.g., 'member', 'guest'

class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str

    class Config:
        from_attributes = True