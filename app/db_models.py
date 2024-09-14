from sqlalchemy import Columnm, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "User"
    id = Columnm(Integer, primary_key=True, index=True)
    first_name = Columnm(String(30), index=True)
    last_name = Columnm(String(30), index=True)
    email = Columnm(String(50), unique=True, index=True)
    task = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "Task"
    id = Columnm(Integer, primary_key=True, index=True)
    title = Columnm(String(30), index=True)
    description = Columnm(String(100), index=True)
    owner_id = Columnm(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="Task")