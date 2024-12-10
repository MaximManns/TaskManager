from fastapi import FastAPI
from backend.src import db_models
from datetime import datetime
from backend.src.database import engine
from fastapi.middleware.cors import CORSMiddleware
from backend.src.routes.user_routes import router as user_router
from backend.src.routes.task_routes import router as task_router

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"Date and time": datetime.now()}


app.include_router(user_router, tags=["users"])
app.include_router(task_router, tags=["tasks"])
