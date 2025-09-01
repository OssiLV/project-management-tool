from sqlalchemy.orm import Session
from .models import Board, List, Task, TaskLabel, TaskAttachment
from .schemas import BoardCreate, ListCreate, TaskCreate, TaskLabelCreate, TaskAttachmentCreate, TaskMove

def create_board(db: Session, board: BoardCreate):
    db_board = Board(project_id=board.project_id, name=board.name)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

def get_board(db: Session, board_id: int):
    return db.query(Board).filter(Board.id == board_id).first()

def create_list(db: Session, list_: ListCreate):
    db_list = List(board_id=list_.board_id, name=list_.name, position=list_.position)
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def move_task(db: Session, task_id: int, move: TaskMove):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.list_id = move.new_list_id
        # Logic sắp xếp position nếu cần
        db.commit()
        db.refresh(db_task)
    return db_task

def add_label(db: Session, task_id: int, label: TaskLabelCreate):
    db_label = TaskLabel(task_id=task_id, label=label.label)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

def add_attachment(db: Session, task_id: int, attachment: TaskAttachmentCreate):
    db_attachment = TaskAttachment(task_id=task_id, file_url=attachment.file_url)
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

# Get lists by board
def get_lists_by_board(db: Session, board_id: int):
    return db.query(List).filter(List.board_id == board_id).order_by(List.position).all()

# Get tasks by list
def get_tasks_by_list(db: Session, list_id: int):
    return db.query(Task).filter(Task.list_id == list_id).all()

# Assign task to user
def assign_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    task.assignee_id = user_id
    db.commit()
    db.refresh(task)
    return task

# Update list
def update_list(db: Session, list_id: int, update_data: dict):
    list_ = db.query(List).filter(List.id == list_id).first()
    if not list_:
        return None
    allowed = {"name", "position"}
    for key, value in update_data.items():
        if key in allowed:
            setattr(list_, key, value)
    db.commit()
    db.refresh(list_)
    return list_

# Delete list
def delete_list(db: Session, list_id: int):
    list_ = db.query(List).filter(List.id == list_id).first()
    if not list_:
        return None
    db.delete(list_)
    db.commit()
    return True

# Update task
def update_task(db: Session, task_id: int, update_data: dict):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    allowed = {"title", "description", "assignee_id", "priority", "status", "due_date", "list_id"}
    for key, value in update_data.items():
        if key in allowed:
            setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

# Delete task
def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return None
    db.delete(task)
    db.commit()
    return True