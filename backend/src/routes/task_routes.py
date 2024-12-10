from backend.src import db_models
from backend.src import schemas
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from backend.src.dependencies import get_db
from backend.src.schemas import Task
from http import HTTPStatus

router = APIRouter()


@router.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list:
    """Retrieve a list of tasks from the database."""
    tasks = db.query(db_models.Task).offset(skip).limit(limit).all()
    return tasks


@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)) -> Task:
    """Create a new task associated with an existing user."""
    owner = db.query(db_models.User).filter(db_models.User.id == task.owner_id).first()
    if not owner:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    new_task = db_models.Task(
        title=task.title,
        description=task.description,
        owner_id=task.owner_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task from the database by its ID."""
    task = db.query(db_models.Task).filter(db_models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
