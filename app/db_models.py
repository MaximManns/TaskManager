from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    email = Column(String(50), unique=True, index=True)
    task = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "Task"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(30), index=True)
    description = Column(String(100), index=True)
    owner_id = Column(Integer, ForeignKey("User.id"))

    owner = relationship("User", back_populates="Task")
