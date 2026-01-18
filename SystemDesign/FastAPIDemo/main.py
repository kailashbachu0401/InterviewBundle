# Minimal FastAPI app
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import status

app = FastAPI(title="Event API Demo", description="A simple event API", version="0.1.0")

class Event(BaseModel):
    id: int
    name: str

# Stateless Service
@app.get("/hello")
def hello():
    return "Hello, World!"

# Global variable (module-level)
count = 0

# Stateful Service
@app.get("/increment")
def increment():
    global count  # Tell Python: "I want to modify the global 'count', not create a local one"
    count += 1
    return {
        "message": "Incremented",
        "count": count
    }

# Path Param
@app.get("/event/{id}")
def get_event(id: str):
    return {
        "event_id": id,
    }

# Query Param
# http://localhost:8000/event?id=1&name=sample
@app.get("/event")
def get_event(id: int, name: str):
    return {
        "event_id": id,
        "event_name": name
    }

# Req body
# 202 Accepted - used for Async operations
@app.post("/event", status_code=status.HTTP_202_ACCEPTED)
def create_event(event: Event):
    return {
        "event_id": event.id,
        "event_name": event.name
    }