from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class BoardCreate(BaseModel):
    project_id: int
    name: str

class BoardResponse(BaseModel):
    id: int
    project_id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

class ListCreate(BaseModel):
    board_id: int
    name: str
    position: Optional[int] = 0

class ListResponse(BaseModel):
    id: int
    board_id: int
    name: str
    position: int

    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    list_id: int
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    list_id: int
    title: str
    description: Optional[str]
    assignee_id: Optional[int]
    priority: Optional[str]
    status: str
    due_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class TaskLabelCreate(BaseModel):
    label: str

class TaskLabelResponse(BaseModel):
    id: int
    task_id: int
    label: str

    class Config:
        from_attributes = True

class TaskAttachmentCreate(BaseModel):
    file_url: str

class TaskAttachmentResponse(BaseModel):
    id: int
    task_id: int
    file_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class TaskMove(BaseModel):
    new_list_id: int
    new_position: Optional[int] = None