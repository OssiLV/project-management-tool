from sqlalchemy.orm import Session
from .models import User, Role
from .schemas import UserCreate, RoleCreate
import bcrypt

def create_user(db: Session, user: UserCreate):
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(name=user.name, email=user.email, password_hash=hashed_pw.decode('utf-8'), role=user.role, is_active=1)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_role(db: Session, role: RoleCreate):
    db_role = Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()

# Flexible update user fields
def update_user(db: Session, user_id: int, update_data: dict):
    user = db.query(User).filter(User.id == user_id, User.is_active == 1).first()
    if not user:
        return None
    for key, value in update_data.items():
        if key == "password":
            value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            setattr(user, "password_hash", value)
        elif key in {"name", "email", "role"}:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

# Soft delete user (mark as inactive)
def soft_delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id, User.is_active == 1).first()
    if not user:
        return None
    user.is_active = 0
    db.commit()
    db.refresh(user)
    return user

# Hard delete user (remove from DB)
def hard_delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    db.delete(user)
    db.commit()
    return True

# Reactivate a soft-deleted user
def reactivate_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id, User.is_active == 0).first()
    if not user:
        return None
    user.is_active = 1
    db.commit()
    db.refresh(user)
    return user