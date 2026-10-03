from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.database import create_task, get_task, init_db, list_tasks


app = FastAPI(title="FlyRank A3 Task API")


class TaskCreate(BaseModel):
    title: str
    done: bool = False


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "FlyRank A3 Task API is running"}


@app.get("/tasks")
def get_tasks():
    return list_tasks()


@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    task = get_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.post("/tasks", status_code=201)
def post_task(task: TaskCreate):
    return create_task(task.title, task.done)