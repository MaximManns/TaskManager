from pydantic import BaseModel


# Task
class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    owner_id: int


class Task(TaskBase):
    id: int
    title: str

    class Config:
        orm_mode = True


# User
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    password: str


class User(UserBase):
    id: int
    tasks: list[Task] | None = None

    class Config:
        orm_mode = True
