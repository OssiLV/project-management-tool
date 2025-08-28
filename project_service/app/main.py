from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import ProjectCreate, ProjectResponse, ProjectMemberCreate, ProjectMemberResponse
from .crud import create_project, get_project, add_member, get_members, get_member_role
from .auth import get_current_user

app = FastAPI(
    root_path="/project_service",
    title="Project Service API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/edoc",
)

@app.post("/projects", response_model=ProjectResponse)
def create_new_project(project: ProjectCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_project(db, project, owner_id=current_user["id"])

@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project_detail(project_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_project = get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    # Check role: user must be member role
    role = get_member_role(db, project_id, current_user["id"])
    if not role:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db_project

@app.post("/projects/{project_id}/members", response_model=ProjectMemberResponse)
def invite_member(project_id: int, member: ProjectMemberCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if current_user is owner
    role = get_member_role(db, project_id, current_user["id"])
    if role != 'owner':
        raise HTTPException(status_code=403, detail="Only owner can invite members")
    # TODO: Check user_id tồn tại bằng gọi auth_service (e.g., requests.get("http://auth_service:8000/users/{member.user_id}", headers={"Authorization": f"Bearer {token}"}))
    return add_member(db, project_id, member)

@app.get("/projects/{project_id}/members", response_model=list[ProjectMemberResponse])
def get_project_members(project_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check role: from member role and above
    role = get_member_role(db, project_id, current_user["id"])
    if not role:
        raise HTTPException(status_code=403, detail="Not authorized")
    return get_members(db, project_id)

# TODO
# Add other routes: update project, delete, v.v.