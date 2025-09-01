from fastapi import FastAPI, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import CommentCreate, CommentUpdate, CommentResponse
from .crud import create_comment, get_comment, get_comments_by_task, update_comment, delete_comment
from .auth import get_current_user

app = FastAPI(
    root_path="/comment_service",
    title="Comment Service API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/edoc",
)

def check_task_permission(task_id: int, user_id: int, token: str):
    # Call board_service to check if user has permission on task (via project)
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"http://board_service:8000/tasks/{task_id}/permission/{user_id}", headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Not authorized for this task")

@app.post("/comments", response_model=CommentResponse)
def create_new_comment(comment: CommentCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check permission (assuming token is obtained from request, simplify)
    check_task_permission(comment.task_id, current_user["id"], "token_here")
    return create_comment(db, comment, current_user["id"])

@app.get("/comments/{comment_id}", response_model=CommentResponse)
def get_comment_detail(comment_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_comment = get_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    check_task_permission(db_comment.task_id, current_user["id"], "token_here")
    return db_comment

@app.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def get_task_comments(task_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    check_task_permission(task_id, current_user["id"], "token_here")
    return get_comments_by_task(db, task_id)

@app.put("/comments/{comment_id}", response_model=CommentResponse)
def update_existing_comment(comment_id: int, update: CommentUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_comment = get_comment(db, comment_id)
    if not db_comment or db_comment.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update")
    return update_comment(db, comment_id, update)

@app.delete("/comments/{comment_id}")
def delete_existing_comment(comment_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_comment = get_comment(db, comment_id)
    if not db_comment or db_comment.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete")
    delete_comment(db, comment_id)
    return {"detail": "Comment deleted"}