from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from app import db_models, schemas
from app.dependencies import get_db

router = APIRouter()


@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = db_models.Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(db_models.Task).offset(skip).limit(limit).all()
    return tasks
