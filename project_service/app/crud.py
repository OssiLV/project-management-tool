from sqlalchemy.orm import Session
from .models import Project, ProjectMember
from .schemas import ProjectCreate, ProjectMemberCreate

def create_project(db: Session, project: ProjectCreate, owner_id: int):
    db_project = Project(name=project.name, description=project.description, owner_id=owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    # Automatic add owner like a member for role 'owner'
    owner_member = ProjectMember(project_id=db_project.id, user_id=owner_id, role='owner')
    db.add(owner_member)
    db.commit()
    return db_project

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def add_member(db: Session, project_id: int, member: ProjectMemberCreate):
    # Prevent owner from inviting themselves with any role except 'owner'
    project = db.query(Project).filter(Project.id == project_id).first()
    if project and member.user_id == project.owner_id:
        # Owner already exists as 'owner', cannot invite self with other role
        return None

    # Prevent duplicate member with same role
    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == member.user_id,
        ProjectMember.role == member.role
    ).first()
    if existing:
        return None

    db_member = ProjectMember(project_id=project_id, user_id=member.user_id, role=member.role)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_members(db: Session, project_id: int):
    return db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()

# Update project fields
def update_project(db: Session, project_id: int, update_data: dict):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    for key, value in update_data.items():
        if hasattr(project, key):
            setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

# Delete project
def delete_project(db: Session, project_id: int):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    db.delete(project)
    db.commit()
    return True

# Update project member role
def update_member_role(db: Session, project_id: int, user_id: int, new_role: str):
    member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id).first()
    if not member:
        return None
    member.role = new_role
    db.commit()
    db.refresh(member)
    return member

# Delete project member
def delete_member(db: Session, project_id: int, user_id: int):
    member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id).first()
    if not member:
        return None
    db.delete(member)
    db.commit()
    return True

# Get member role (returns None if not found)
def get_member_role(db: Session, project_id: int, user_id: int):
    member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id).first()
    return member.role if member else None