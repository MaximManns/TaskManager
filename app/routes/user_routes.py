import app
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app import db_models, schemas
from app.main import get_db


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(db_models.User).filter(db_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = db_models.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(db_models.User).offset(skip).limit(limit).all()
    return users
