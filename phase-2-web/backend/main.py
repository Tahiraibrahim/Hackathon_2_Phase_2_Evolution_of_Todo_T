from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from db import create_db_and_tables, get_session
from models import Task, Priority
from auth import get_current_user, router as auth_router
from agents.task_orchestrator import TaskOrchestrator 

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
task_orchestrator = TaskOrchestrator()

# Include auth router
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[Priority] = Priority.MEDIUM
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    priority: Optional[Priority] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/todos", response_model=List[Task])
def list_todos(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session),
    search: Optional[str] = Query(None, description="Search tasks by title or description"),
    priority: Optional[Priority] = Query(None, description="Filter tasks by priority"),
    sort_by: Optional[str] = Query("id", description="Sort by field (id, title, priority, due_date, created_at)")
):
    """
    List all tasks for the authenticated user.

    Uses TaskOrchestrator to:
    - Retrieve tasks from database
    - Apply search filters
    - Apply priority filters
    - Sort results
    """
    result = task_orchestrator.list_tasks(
        session=session,
        user_id=user_id,
        search=search,
        priority=priority,
        sort_by=sort_by,
    )

    return result["tasks"]

@app.post("/api/todos", response_model=Task, status_code=201)
def create_todo(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Uses TaskOrchestrator to:
    - Validate task title and category
    - Create task in database
    """
    result = task_orchestrator.create_task(
        session=session,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        category=task_data.category,
        due_date=task_data.due_date,
        is_recurring=task_data.is_recurring,
    )

    if not result["success"]:
        # Determine appropriate status code based on error
        if "cannot be empty" in result["error"]:
            status_code = 400
        else:
            status_code = 422
        raise HTTPException(status_code=status_code, detail=result["error"])

    return result["task"]

@app.put("/api/todos/{task_id}", response_model=Task)
def update_todo(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.

    Uses TaskOrchestrator to:
    - Verify task ownership
    - Validate updated fields
    - Update task in database
    """
    result = task_orchestrator.update_task(
        session=session,
        task_id=task_id,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed,
        priority=task_data.priority,
        category=task_data.category,
        due_date=task_data.due_date,
        is_recurring=task_data.is_recurring,
    )

    if not result["success"]:
        # Determine appropriate status code based on error
        if result["error"] == "Task not found":
            status_code = 404
        elif "cannot be empty" in result["error"]:
            status_code = 400
        else:
            status_code = 422
        raise HTTPException(status_code=status_code, detail=result["error"])

    return result["task"]

@app.delete("/api/todos/{task_id}", status_code=204)
def delete_todo(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task.

    Uses TaskOrchestrator to:
    - Verify task ownership
    - Delete task from database
    """
    result = task_orchestrator.delete_task(
        session=session,
        task_id=task_id,
        user_id=user_id,
    )

    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["error"])

    return None