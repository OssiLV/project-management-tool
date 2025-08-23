from sqlalchemy.orm import Session
from .models import User, Role
from .schemas import UserCreate, RoleCreate
import bcrypt

def create_user(db: Session, user: UserCreate):
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(name=user.name, email=user.email, password_hash=hashed_pw.decode('utf-8'), role=user.role)
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

# TODO Add other functions: update user, delete, v.v.