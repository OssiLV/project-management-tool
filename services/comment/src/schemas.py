from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    task_id: int
    content: str

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)