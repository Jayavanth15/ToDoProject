from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr

class TaskCreate(BaseModel):
    todo : str
    status : str
    user_id : int

class TaskResponse(BaseModel):
    task_id : Optional[int]
    todo : Optional[str]
    createdAt : Optional[datetime]
    status : Optional[str]
    isExist : Optional[bool]
    user_id : Optional[int]

class UserTaskResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    task : Optional[list[TaskResponse]] = []
    class Config:
        orm_mode = True