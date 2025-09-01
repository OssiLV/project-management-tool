import pytest
from src.schemas import BoardCreate, ListCreate, TaskCreate
from src.crud import create_board, create_list, create_task, get_board, get_lists_by_board, get_tasks_by_list, update_list, delete_list, update_task, delete_task

def test_create_board(db_session):
    board_data = BoardCreate(project_id=1, name="Test Board")
    board = create_board(db_session, board_data)
    assert board.id is not None
    assert board.name == "Test Board"

def test_create_list(db_session):
    board_data = BoardCreate(project_id=1, name="Board for List")
    board = create_board(db_session, board_data)
    list_data = ListCreate(board_id=board.id, name="List 1", position=1)
    list_ = create_list(db_session, list_data)
    assert list_.id is not None
    assert list_.name == "List 1"
    assert list_.board_id == board.id

def test_create_task(db_session):
    board_data = BoardCreate(project_id=1, name="Board for Task")
    board = create_board(db_session, board_data)
    list_data = ListCreate(board_id=board.id, name="List for Task", position=1)
    list_ = create_list(db_session, list_data)
    task_data = TaskCreate(list_id=list_.id, title="Task 1", description="Desc", assignee_id=1, priority="high")
    task = create_task(db_session, task_data)
    assert task.id is not None
    assert task.title == "Task 1"
    assert task.list_id == list_.id

def test_get_lists_by_board(db_session):
    board_data = BoardCreate(project_id=1, name="Board for Lists")
    board = create_board(db_session, board_data)
    create_list(db_session, ListCreate(board_id=board.id, name="List A", position=1))
    create_list(db_session, ListCreate(board_id=board.id, name="List B", position=2))
    lists = get_lists_by_board(db_session, board.id)
    assert len(lists) == 2
    assert lists[0].name == "List A"
    assert lists[1].name == "List B"

def test_get_tasks_by_list(db_session):
    board_data = BoardCreate(project_id=1, name="Board for Tasks")
    board = create_board(db_session, board_data)
    list_data = ListCreate(board_id=board.id, name="List for Tasks", position=1)
    list_ = create_list(db_session, list_data)
    create_task(db_session, TaskCreate(list_id=list_.id, title="Task X", description="Desc X", assignee_id=1, priority="low"))
    create_task(db_session, TaskCreate(list_id=list_.id, title="Task Y", description="Desc Y", assignee_id=2, priority="high"))
    tasks = get_tasks_by_list(db_session, list_.id)
    assert len(tasks) == 2
    assert tasks[0].title == "Task X"
    assert tasks[1].title == "Task Y"

def test_update_list(db_session):
    board_data = BoardCreate(project_id=1, name="Board for Update List")
    board = create_board(db_session, board_data)
    list_data = ListCreate(board_id=board.id, name="List to Update", position=1)
    list_ = create_list(db_session, list_data)
    updated = update_list(db_session, list_.id, {"name": "Updated List", "position": 2})
    assert updated.name == "Updated List"
    assert updated.position == 2

def test_delete_list(db_session):
    board_data = BoardCreate(project_id=1, name="Board for Delete List")
    board = create_board(db_session, board_data)
    list_data = ListCreate(board_id=board.id, name="List to Delete", position=1)
    list_ = create_list(db_session, list_data)
    result = delete_list(db_session, list_.id)
    assert result is True
    lists = get_lists_by_board(db_session, board.id)
    assert len(lists) == 0

def test_update_task(db_session):
    board_data = BoardCreate(project_id=1, name="Board for Update Task")
    board = create_board(db_session, board_data)
    list_data = ListCreate(board_id=board.id, name="List for Update Task", position=1)
    list_ = create_list(db_session, list_data)
    task_data = TaskCreate(list_id=list_.id, title="Task to Update", description="Desc", assignee_id=1, priority="medium")
    task = create_task(db_session, task_data)
    updated = update_task(db_session, task.id, {"title": "Updated Task", "priority": "high"})
    assert updated.title == "Updated Task"
    assert updated.priority == "high"

def test_delete_task(db_session):
    board_data = BoardCreate(project_id=1, name="Board for Delete Task")
    board = create_board(db_session, board_data)
    list_data = ListCreate(board_id=board.id, name="List for Delete Task", position=1)
    list_ = create_list(db_session, list_data)
    task_data = TaskCreate(list_id=list_.id, title="Task to Delete", description="Desc", assignee_id=1, priority="low")
    task = create_task(db_session, task_data)
    result = delete_task(db_session, task.id)
    assert result is True
    tasks = get_tasks_by_list(db_session, list_.id)
    assert len(tasks) == 0