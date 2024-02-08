import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Możesz tutaj określić konkretne źródła zamiast akceptować wszystkie ("*")
    allow_credentials=True,
    allow_methods=["*"],  # Akceptuj wszystkie metody HTTP
    allow_headers=["*"],  # Akceptuj wszystkie nagłówki
)

class Task(BaseModel):
    id: Optional[int] = None
    name: str
    completed: bool = False

tasks: List[Task] = []

@app.get("/tasks/completed/count")
async def get_completed_tasks_count():
    completed_tasks_count = sum(task.completed for task in tasks)
    return {"completed_tasks_count": completed_tasks_count}

@app.get("/", response_class=HTMLResponse)
async def read_route(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    task.id = len(tasks) + 1
    tasks.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    return tasks

@app.put("/tasks/{task_id}/complete", response_model=Task)
async def complete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(index)
    raise HTTPException(status_code=404, detail="Task not found")
