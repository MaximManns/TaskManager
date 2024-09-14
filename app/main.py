import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from app.db_models import User, Task

app = FastAPI()


@app.get("/")
def read_root():
    return{"My" : "Tasks"}