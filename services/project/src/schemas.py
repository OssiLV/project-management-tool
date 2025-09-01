from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class ProjectMemberCreate(BaseModel):
    user_id: int
    role: str  # e.g., 'owner', 'member', 'guest'

class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str

    model_config = ConfigDict(from_attributes=True)
