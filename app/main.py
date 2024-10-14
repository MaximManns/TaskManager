from app import db_models
from fastapi import FastAPI
from app.database import engine
from app.routes.user_routes import router as user_router
from app.routes.task_routes import router as task_router

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome!": "To the Task Manager"}


app.include_router(user_router, tags=["users"])
app.include_router(task_router, tags=["tasks"])
