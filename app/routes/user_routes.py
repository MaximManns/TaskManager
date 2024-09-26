from app import db_models
from app import schemas
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import User

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = db.query(db_models.User).filter(db_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = db_models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list:
    users = db.query(db_models.User).offset(skip).limit(limit).all()
    return users
