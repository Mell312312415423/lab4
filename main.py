from fastapi import FastAPI, HTTPException, Depends, Request
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Retrieve API Key from environment variables
API_SECRET_KEY = os.getenv("API_KEY")

# API Key Verification Dependency
def authenticate_api_key(request: Request):
    provided_key = request.headers.get("X-API-KEY") or request.query_params.get("api_key")
    if not provided_key or provided_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API Key")
    return provided_key

# Task Management Helper Functions
def find_task_by_id(task_list: list, task_id: int):
    return next((task for task in task_list if task["task_id"] == task_id), None)

def add_task(task_list: list, title: str, description: str):
    new_task = {
        "task_id": len(task_list) + 1,
        "title": title,
        "description": description,
        "completed": False,
    }
    task_list.append(new_task)
    return new_task

def remove_task(task_list: list, task_id: int):
    task = find_task_by_id(task_list, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_list.remove(task)
    return {"message": "Task deleted successfully"}

def modify_task(task_list: list, task_id: int, title: str = None, description: str = None, completed: bool = None):
    task = find_task_by_id(task_list, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if completed is not None:
        task["completed"] = completed
    return {"message": "Task updated successfully", "task": task}

# Sample Task Data Stores
task_store_v1 = [{"task_id": 1, "title": "Learn FastAPI", "description": "Understand the basics", "completed": False}]
task_store_v2 = [{"task_id": 1, "title": "Upgrade API", "description": "Refactor to improve structure", "completed": False}]

# API v1 Endpoints
@app.get("/apiv1/", dependencies=[Depends(authenticate_api_key)])
def api_v1_home():
    return {"message": "Welcome to API v1"}

@app.get("/apiv1/tasks/{task_id}", dependencies=[Depends(authenticate_api_key)])
def fetch_task_v1(task_id: int):
    task = find_task_by_id(task_store_v1, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}

@app.post("/apiv1/tasks/", status_code=201, dependencies=[Depends(authenticate_api_key)])
def add_task_v1(title: str, description: str):
    return {"task": add_task(task_store_v1, title, description)}

@app.delete("/apiv1/tasks/{task_id}", status_code=204, dependencies=[Depends(authenticate_api_key)])
def remove_task_v1(task_id: int):
    return remove_task(task_store_v1, task_id)

@app.patch("/apiv1/tasks/{task_id}", status_code=200, dependencies=[Depends(authenticate_api_key)])
def modify_task_v1(task_id: int, title: str = None, description: str = None, completed: bool = None):
    return modify_task(task_store_v1, task_id, title, description, completed)

# API v2 Endpoints
@app.get("/apiv2/tasks/{task_id}", dependencies=[Depends(authenticate_api_key)])
def fetch_task_v2(task_id: int):
    task = find_task_by_id(task_store_v2, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task": task}

@app.post("/apiv2/tasks/", status_code=201, dependencies=[Depends(authenticate_api_key)])
def add_task_v2(title: str, description: str):
    return {"task": add_task(task_store_v2, title, description)}

@app.delete("/apiv2/tasks/{task_id}", status_code=204, dependencies=[Depends(authenticate_api_key)])
def remove_task_v2(task_id: int):
    return remove_task(task_store_v2, task_id)

@app.patch("/apiv2/tasks/{task_id}", status_code=200, dependencies=[Depends(authenticate_api_key)])
def modify_task_v2(task_id: int, title: str = None, description: str = None, completed: bool = None):
    return modify_task(task_store_v2, task_id, title, description, completed)
