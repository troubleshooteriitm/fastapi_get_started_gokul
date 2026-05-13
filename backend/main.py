from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="TaskFlow API")

# ── CORS – allow any origin (wildcard cannot be used with allow_credentials=True) ─
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # Must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── In-memory store ────────────────────────────────────────────────────────
tasks: dict[str, dict] = {}


# ── Schemas ────────────────────────────────────────────────────────────────
class TaskCreate(BaseModel):
    text: str
    priority: str = "medium"   # low | medium | high
    category: Optional[str] = "personal"
    due: Optional[str] = None  # ISO date string "YYYY-MM-DD"


class TaskUpdate(BaseModel):
    text: Optional[str] = None
    done: Optional[bool] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due: Optional[str] = None


# ── Routes ─────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"message": "TaskFlow API is running 🚀"}


@app.get("/tasks")
async def get_tasks():
    """Return all tasks ordered newest-first."""
    return sorted(tasks.values(), key=lambda t: t["createdAt"], reverse=True)


@app.post("/tasks", status_code=201)
async def create_task(body: TaskCreate):
    """Create a new task and return it."""
    import time
    task_id = str(uuid.uuid4())
    task = {
        "id":        task_id,
        "text":      body.text,
        "done":      False,
        "priority":  body.priority,
        "category":  body.category,
        "due":       body.due,
        "createdAt": int(time.time() * 1000),   # ms timestamp like JS Date.now()
    }
    tasks[task_id] = task
    return task


@app.patch("/tasks/{task_id}")
async def update_task(task_id: str, body: TaskUpdate):
    """Partially update a task (text, done, priority, category, due)."""
    task = tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = body.model_dump(exclude_unset=True)
    task.update(updates)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Delete a task by id."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]