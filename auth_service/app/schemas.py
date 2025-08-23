from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # Default role can set in crud

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True