from pydantic import BaseModel, ConfigDict


# Task
class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    owner_id: int


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: str


# User
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    task: list[Task] | None = None
