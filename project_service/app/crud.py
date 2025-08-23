from sqlalchemy.orm import Session
from .models import Project, ProjectMember
from .schemas import ProjectCreate, ProjectMemberCreate

def create_project(db: Session, project: ProjectCreate, owner_id: int):
    db_project = Project(name=project.name, description=project.description, owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    # Automatic add owner like member for role 'owner'
    owner_member = ProjectMember(project_id=db_project.id, user_id=owner_id, role='owner')
    db.add(owner_member)
    db.commit()
    return db_project

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def add_member(db: Session, project_id: int, member: ProjectMemberCreate):
    db_member = ProjectMember(project_id=project_id, user_id=member.user_id, role=member.role)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_members(db: Session, project_id: int):
    return db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()

# TODO: update, delete project/member, check role
def get_member_role(db: Session, project_id: int, user_id: int):
    member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id).first()
    return member.role if member else None