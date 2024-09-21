from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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


@app.get("/")
def read_root():
    return {"message": "Task Manager API is working!"}


@app.get("/check-db")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        # Test the connection by querying the User table
        users = db.query(db_models.User).all()
        return {"message": "Database connection successful!", "users_in_db": len(users)}
    except Exception as e:
        # Return the detailed error message to help with debugging
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
