import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union
from models.task import Task
from models.user import User

app = FastAPI()


@app.get("/")
def read_root():
    return{"My" : "Tasks"}