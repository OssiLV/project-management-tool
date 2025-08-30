import os
import requests
from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import ProjectCreate, ProjectResponse, ProjectMemberCreate, ProjectMemberResponse
from .crud import create_project, get_project, add_member, get_members, get_member_role, update_project, delete_project, update_member_role, delete_member
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
    # Check user_id exists in auth_service
    auth_url = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8000")
    headers = {"Authorization": f"Bearer {current_user['token']}"} if current_user['token'] else {}
    user_resp = requests.get(f"{auth_url}/users/{member.user_id}", headers=headers)
    if user_resp.status_code != 200:
        return JSONResponse(status_code=user_resp.status_code, content=user_resp.json())
    db_member = add_member(db, project_id, member)
    if db_member is None:
        raise HTTPException(status_code=400, detail="Cannot invite owner as member or duplicate member/role")
    return db_member        

@app.get("/projects/{project_id}/members", response_model=list[ProjectMemberResponse])
def get_project_members(project_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check role: from member role and above
    role = get_member_role(db, project_id, current_user["id"])
    if not role:
        raise HTTPException(status_code=403, detail="Not authorized")
    return get_members(db, project_id)

# Update project (owner only)
@app.patch("/projects/{project_id}", response_model=ProjectResponse)
def update_project_route(project_id: int, update_data: dict = Body(...), current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    role = get_member_role(db, project_id, current_user["id"])
    if role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can update project")
    project = update_project(db, project_id, update_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Delete project (owner only)
@app.delete("/projects/{project_id}", response_model=dict)
def delete_project_route(project_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    role = get_member_role(db, project_id, current_user["id"])
    if role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can delete project")
    result = delete_project(db, project_id)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted"}

# Update member role (owner only)
@app.patch("/projects/{project_id}/members/{user_id}", response_model=ProjectMemberResponse)
def update_member_role_route(project_id: int, user_id: int, new_role: str = Body(..., embed=True), current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    role = get_member_role(db, project_id, current_user["id"])
    if role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can update member role")
    member = update_member_role(db, project_id, user_id, new_role)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# Delete member (owner only, cannot remove self)
@app.delete("/projects/{project_id}/members/{user_id}", response_model=dict)
def delete_member_route(project_id: int, user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    role = get_member_role(db, project_id, current_user["id"])
    if role != "owner":
        raise HTTPException(status_code=403, detail="Only owner can delete member")
    if user_id == current_user["id"]:
        raise HTTPException(status_code=400, detail="Owner cannot remove self")
    result = delete_member(db, project_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"detail": "Member deleted"}