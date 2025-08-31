from fastapi import FastAPI, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import BoardCreate, BoardResponse, ListCreate, ListResponse, TaskCreate, TaskResponse, TaskMove, TaskLabelCreate, TaskLabelResponse, TaskAttachmentCreate, TaskAttachmentResponse
from .crud import create_board, get_board, create_list, create_task, move_task, add_label, add_attachment, get_lists_by_board, get_tasks_by_list, assign_task, update_list, delete_list, update_task, delete_task
from .auth import get_current_user
from .models import List, Task

app = FastAPI(
    root_path="/board_service",
    title="Board Service API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/edoc",
)

def check_project_permission(project_id: int, user_id: int, token: str):
    # Call project_service to check role
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"http://project_service:8000/projects/{project_id}/members/{user_id}", headers=headers)
    if response.status_code != 200 or response.json().get("role") not in ["owner", "member"]:
        raise HTTPException(status_code=403, detail="Not authorized for this project")

@app.post("/boards", response_model=BoardResponse)
def create_new_board(board: BoardCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check role from project_service (need token from request)
    check_project_permission(board.project_id, current_user["id"], current_user.get("token"))
    return create_board(db, board)

@app.get("/boards/{board_id}", response_model=BoardResponse)
def get_board_detail(board_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_board = get_board(db, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    check_project_permission(db_board.project_id, current_user["id"], current_user.get("token"))
    return db_board

# Similar for lists, tasks
@app.post("/lists", response_model=ListResponse)
def create_new_list(list_: ListCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_board = get_board(db, list_.board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    check_project_permission(db_board.project_id, current_user["id"], current_user.get("token"))
    return create_list(db, list_)

@app.post("/tasks", response_model=TaskResponse)
def create_new_task(task: TaskCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check role from list -> board -> project
    db_list = db.query(List).filter(List.id == task.list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    db_board = get_board(db, db_list.board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    check_project_permission(db_board.project_id, current_user["id"], current_user.get("token"))
    return create_task(db, task)

@app.put("/tasks/{task_id}/move", response_model=TaskResponse)
def move_task_position(task_id: int, move: TaskMove, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_list = db.query(List).filter(List.id == db_task.list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    db_board = get_board(db, db_list.board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    check_project_permission(db_board.project_id, current_user["id"], current_user.get("token"))
    return move_task(db, task_id, move)

@app.post("/tasks/{task_id}/labels", response_model=TaskLabelResponse)
def add_task_label(task_id: int, label: TaskLabelCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_list = db.query(List).filter(List.id == db_task.list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    db_board = get_board(db, db_list.board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    check_project_permission(db_board.project_id, current_user["id"], current_user.get("token"))
    return add_label(db, task_id, label)

@app.post("/tasks/{task_id}/attachments", response_model=TaskAttachmentResponse)
def add_task_attachment(task_id: int, attachment: TaskAttachmentCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_list = db.query(List).filter(List.id == db_task.list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    db_board = get_board(db, db_list.board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    check_project_permission(db_board.project_id, current_user["id"], current_user.get("token"))
    return add_attachment(db, task_id, attachment)

# Get lists by board
@app.get("/boards/{board_id}/lists", response_model=list[ListResponse])
def get_lists(board_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_board = get_board(db, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    check_project_permission(db_board.project_id, current_user["id"], current_user["token"])
    return get_lists_by_board(db, board_id)

# Get tasks by list
@app.get("/lists/{list_id}/tasks", response_model=list[TaskResponse])
def get_tasks(list_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_list = db.query(List).filter(List.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    db_board = get_board(db, db_list.board_id)
    check_project_permission(db_board.project_id, current_user["id"], current_user["token"])
    return get_tasks_by_list(db, list_id)

# Assign task to user
@app.put("/tasks/{task_id}/assign/{user_id}", response_model=TaskResponse)
def assign_task_to_user(task_id: int, user_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_list = db.query(List).filter(List.id == db_task.list_id).first()
    db_board = get_board(db, db_list.board_id)
    check_project_permission(db_board.project_id, current_user["id"], current_user["token"])
    task = assign_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or assign failed")
    return task

# Update list
@app.patch("/lists/{list_id}", response_model=ListResponse)
def update_list_route(list_id: int, update_data: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_list = db.query(List).filter(List.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    db_board = get_board(db, db_list.board_id)
    check_project_permission(db_board.project_id, current_user["id"], current_user["token"])
    list_ = update_list(db, list_id, update_data)
    if not list_:
        raise HTTPException(status_code=404, detail="List not found or update failed")
    return list_

# Delete list
@app.delete("/lists/{list_id}", response_model=dict)
def delete_list_route(list_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_list = db.query(List).filter(List.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    db_board = get_board(db, db_list.board_id)
    check_project_permission(db_board.project_id, current_user["id"], current_user["token"])
    result = delete_list(db, list_id)
    if not result:
        raise HTTPException(status_code=404, detail="List not found or delete failed")
    return {"detail": "List deleted"}

# Update task
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task_route(task_id: int, update_data: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_list = db.query(List).filter(List.id == db_task.list_id).first()
    db_board = get_board(db, db_list.board_id)
    check_project_permission(db_board.project_id, current_user["id"], current_user["token"])
    task = update_task(db, task_id, update_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or update failed")
    return task

# Delete task
@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task_route(task_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_list = db.query(List).filter(List.id == db_task.list_id).first()
    db_board = get_board(db, db_list.board_id)
    check_project_permission(db_board.project_id, current_user["id"], current_user["token"])
    result = delete_task(db, task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found or delete failed")
    return {"detail": "Task deleted"}