from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy import select, update, case, text
from sqlalchemy.orm import Session
from schemas.schemas import TaskCreate, TaskResponse, UserCreate, UserResponse, UserTaskResponse
from models.models import Task, User
from base import SessionLocal, engine
from apis.prompt import get_Query

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/get-Query/")
def get_query(user_prompt: str = Body(...), db: Session = Depends(get_db)):
    try:
        message = get_Query(user_prompt)
        result = db.execute(text(message))
        rows = result.fetchall()
        column_names = result.keys()
        output = [dict(zip(column_names, row)) for row in rows]
        return {"message": message, "data": output}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Query execution failed: {str(e)}")

@router.get("/users/", response_model=list[UserResponse])
def get_users(db : Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/users/", response_model=UserResponse)
def create_user(user : UserCreate, db : Session = Depends(get_db)):
    new_user = User(username = user.username, email = user.email, password = user.password)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400)

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.username = user.username
    existing_user.email = user.email
    existing_user.password = user.password
    db.commit()
    db.refresh(existing_user)
    return existing_user

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.get("/tasks/", response_model=list[TaskResponse])
def get_tasks(db : Session = Depends(get_db)):
    return db.query(Task).all()

@router.post("/tasks/", response_model=TaskResponse)
def create_task(task : TaskCreate, db : Session = Depends(get_db)):
    new_task = Task(todo=task.todo, status=task.status, user_id = task.user_id)
    db.add(new_task)
    try:
        db.commit()
        db.refresh(new_task)
        return new_task
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id : int, db : Session = Depends(get_db)):
    new_task = db.query(Task).filter(task_id == Task.task_id).first()
    if not new_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if new_task.status == "Completed":
        new_task.status = "Pending"
    elif new_task.status == "Pending":
        new_task.status = "Completed"
    db.commit()
    db.refresh(new_task)
    return new_task

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id : int, db : Session = Depends(get_db)):
    new_task = db.query(Task).filter(task_id == Task.task_id).first()
    if not new_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if new_task.isExist:
        new_task.isExist = False
        db.commit()
        return {"message" : "Task deleted successfully"}
    return {"message" : "Task is already deleted"}

@router.get("/user_tasks/{user_id}")
def get_tasks_of_user(user_id : int, db : Session = Depends(get_db)):
    stmt = (
        select(User, Task)
        .join(Task, Task.user_id == User.user_id, isouter=True)  # Use an outer join
        .filter(User.user_id == user_id)
    )
    results = db.execute(stmt).all()
    if not results:
        raise HTTPException(status_code=404, detail="User not found")
    user = results[0][0]
    tasks = [row[1] for row in results if row[1] is not None]

    # Return the response
    return {
        "user_id": user.user_id,
        "username": user.username,
        "usermail" : user.email,
        "tasks": tasks  # Empty list if no tasks are assigned
    }

@router.put("/usesr_tasks_update/{user_id}", response_model = list[TaskResponse])
def update_tasks_of_user(user_id : int, db : Session = Depends(get_db)):
    task_new = db.query(Task).filter(Task.user_id == user_id).all()
    for task in task_new:
        if task.status == "Completed":
            task.status = "Pending"
        elif task.status == "Pending":
            task.status = "Completed"
        db.commit()
        db.refresh(task)
    return task_new

@router.delete("/user_tasks/{user_id}", response_model=dict)
def delete_tasks_of_user(user_id : int, db : Session = Depends(get_db)):
    db.query(Task).filter(user_id == Task.user_id).update({Task.isExist: False})
    db.commit()
    return {"message" : "Tasks succesfully deleted "}