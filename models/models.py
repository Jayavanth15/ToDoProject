from sqlalchemy import Column, Integer, Boolean, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    assigned_task = relationship("Task", back_populates="assigned_user")

class Task(Base):
    __tablename__ = "Tasks"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    todo = Column(String(255), nullable=False)
    createdAt = Column(DateTime, default = func.now())
    status = Column(String(255), nullable=False)
    isExist = Column(Boolean, default = True, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.user_id"))

    assigned_user = relationship("User", back_populates="assigned_task")