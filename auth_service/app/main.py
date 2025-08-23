from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import bcrypt
from .database import get_db
from .schemas import UserCreate, UserResponse, Token, RoleCreate, RoleResponse
from .crud import create_user, get_user_by_email, create_role, get_roles, get_user_by_id
from .auth import create_access_token, get_current_user

app = FastAPI()

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(user_id=user.id, email=user.email, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if admin or self
    if current_user["id"] != user_id and current_user.get("role") != "admin":  # JWT include role
        raise HTTPException(status_code=403, detail="Not authorized")
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/roles", response_model=RoleResponse)
def create_new_role(role: RoleCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Chỉ admin
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return create_role(db, role)

@app.get("/roles", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return get_roles(db)

# TODO
# Add routes: update/delete user (admin only), v.v.