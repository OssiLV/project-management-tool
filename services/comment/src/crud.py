from sqlalchemy.orm import Session
from .models import Comment
from .schemas import CommentCreate, CommentUpdate

def create_comment(db: Session, comment: CommentCreate, user_id: int):
    db_comment = Comment(task_id=comment.task_id, user_id=user_id, content=comment.content)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_comments_by_task(db: Session, task_id: int):
    return db.query(Comment).filter(Comment.task_id == task_id).all()

def update_comment(db: Session, comment_id: int, update: CommentUpdate):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        if update.content is not None:
            db_comment.content = update.content
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = get_comment(db, comment_id)
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment