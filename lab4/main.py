from fastapi import FastAPI, HTTPException, Depends, Request
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# API Key 
API_KEY = os.getenv("my_api_key")

# Dependency 
def verify_api_key(request: Request):
    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


# Database
task_db_v1 = [
    {"task_id": 1, "task_title": "Test 1", "task_desc": "Complete FastAPI basics", "is_finished": False}
]

task_db_v2 = [
    {"task_id": 1, "task_title": "Test 2", "task_desc": "Revise To-Do API", "is_finished": False}
]


# API 
@app.get("/apiv1/", dependencies=[Depends(verify_api_key)])
def apiv1_root():
    return {"message": "Welcome to API v1"}


@app.get("/apiv1/tasks/")
def get_tasks_v1():
    if not task_db_v1:
        raise HTTPException(status_code=204, detail="No tasks available")
    return {"status": "ok", "tasks": task_db_v1}


@app.get("/apiv1/tasks/{task_id}")
def get_task_by_id_v1(task_id: int):
    task = next((task for task in task_db_v1 if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok", "task": task}


@app.post("/apiv1/tasks/", status_code=201)
def create_task_v1(task_title: str, task_desc: str):
    new_task = {"task_id": len(task_db_v1) + 1, "task_title": task_title, "task_desc": task_desc, "is_finished": False}
    task_db_v1.append(new_task)
    return {"status": "ok", "task": new_task}


@app.delete("/apiv1/tasks/{task_id}", status_code=204)
def delete_task_v1(task_id: int):
    task = next((task for task in task_db_v1 if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db_v1.remove(task)
    return {"status": "ok", "message": "Task deleted successfully"}


@app.patch("/apiv1/tasks/{task_id}", status_code=204)
def update_task_v1(task_id: int, task_title: str = None, task_desc: str = None, is_finished: bool = None):
    task = next((task for task in task_db_v1 if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_title is not None:
        task["task_title"] = task_title
    if task_desc is not None:
        task["task_desc"] = task_desc
    if is_finished is not None:
        task["is_finished"] = is_finished
    return {"status": "ok", "task": task}


# API 
@app.get("/apiv2/", dependencies=[Depends(verify_api_key)])
def apiv2_root():
    return {"message": "Welcome to API v2"}


@app.get("/apiv2/tasks/")
def get_tasks_v2():
    if not task_db_v2:
        raise HTTPException(status_code=204, detail="No tasks available")
    return {"status": "ok", "tasks": task_db_v2}


@app.get("/apiv2/tasks/{task_id}")
def get_task_by_id_v2(task_id: int):
    task = next((task for task in task_db_v2 if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok", "task": task}


@app.post("/apiv2/tasks/", status_code=201)
def create_task_v2(task_title: str, task_desc: str):
    new_task = {"task_id": len(task_db_v2) + 1, "task_title": task_title, "task_desc": task_desc, "is_finished": False}
    task_db_v2.append(new_task)
    return {"status": "ok", "task": new_task}


@app.delete("/apiv2/tasks/{task_id}", status_code=204)
def delete_task_v2(task_id: int):
    task = next((task for task in task_db_v2 if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db_v2.remove(task)
    return {"status": "ok", "message": "Task deleted successfully"}


@app.patch("/apiv2/tasks/{task_id}", status_code=204)
def update_task_v2(task_id: int, task_title: str = None, task_desc: str = None, is_finished: bool = None):
    task = next((task for task in task_db_v2 if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_title is not None:
        task["task_title"] = task_title
    if task_desc is not None:
        task["task_desc"] = task_desc
    if is_finished is not None:
        task["is_finished"] = is_finished
    return {"status": "ok", "task": task}