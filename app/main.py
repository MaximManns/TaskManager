from fastapi import FastAPI
from app import db_models
from app.database import SessionLocal, engine

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
