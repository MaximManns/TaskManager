from backend import db_models
from backend import schemas
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from backend.dependencies import get_db
from backend.schemas import User
from http import HTTPStatus
import hashlib

router = APIRouter()


@router.get("/users/{user_id}", response_model=schemas.User)
def get_spefific_user(user_id: int, db: Session = Depends(get_db)) -> User:
    """Retrieve a specific user by their ID."""
    specific_user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not specific_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="No User with this id registered")
    return specific_user


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> User:
    """Create a new user with a hashed password."""
    db_user = db.query(db_models.User).filter(db_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User with this email already registered")

    # Hash the password using SHA-256
    hashed_password = hashlib.new('sha256')
    hashed_password.update(str.encode(user.password))
    hashed_password = hashed_password.hexdigest()

    new_user = db_models.User(email=user.email, name=user.name, password=hashed_password)

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User with this email or name already exists"
        )


@router.get("/users/", response_model=list[schemas.User])
def get_list_of_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list:
    """Retrieve a list of users."""
    users = db.query(db_models.User).offset(skip).limit(limit).all()
    return users


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by their ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT)
