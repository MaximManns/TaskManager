from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    owner_email: str


class Task(TaskBase):
    id: int
    title: str
    owner_email: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    items: list[Task] = []

    class Config:
        orm_mode = True
