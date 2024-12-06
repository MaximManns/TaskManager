from backend import db_models
from backend import schemas
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas import User
import hashlib

router = APIRouter()


@router.get("/users/{user_id}", response_model=schemas.User)
def get_spefific_user(user_id: int, db: Session = Depends(get_db)) -> User:
    specific_user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not specific_user:
        raise HTTPException(status_code=404, detail="No User with this id registered")
    return specific_user


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> User:
    db_user = db.query(db_models.User).filter(db_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User with this name already registered")
    hashed_password = hashlib.new('sha256')
    hashed_password.update(str.encode(user.password))
    hashed_password.hexdigest()
    new_user = db_models.User(email=user.email, name=user.name, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/", response_model=list[schemas.User])
def get_list_of_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list:
    users = db.query(db_models.User).offset(skip).limit(limit).all()
    return users
