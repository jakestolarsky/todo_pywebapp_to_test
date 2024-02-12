from typing import List
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from config import templates
from app.models.task_model import tasks
from app.schemas.task_schema import Task



router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})

@router.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    return task

@router.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks

@router.put("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.get("/tasks/completed/count")
async def get_completed_tasks_count():
    completed_tasks_count = sum(task.completed for task in tasks)
    return {"completed_tasks_count": completed_tasks_count}

@router.put("/tasks/{task_id}/update", response_model=Task)
async def update_task_name(task_id: int, task: Task):
    for existing_task in tasks:
        if existing_task.id == task_id:
            existing_task.name = task.name
            return existing_task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(index)
    raise HTTPException(status_code=404, detail="Task not found")