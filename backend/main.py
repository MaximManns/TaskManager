from backend import db_models
from fastapi import FastAPI
from backend.database import engine
from datetime import datetime
from backend.routes.user_routes import router as user_router
from backend.routes.task_routes import router as task_router

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Date and time": datetime.now()}


app.include_router(user_router, tags=["users"])
app.include_router(task_router, tags=["tasks"])
