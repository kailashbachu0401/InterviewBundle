# Minimal FastAPI app
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import status
from fastapi import Depends
from fastapi import Query
from fastapi.responses import JSONResponse

app = FastAPI(title="Event API Demo", description="A simple event API", version="0.1.0")

# Pydantic Model
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
def get_event(id: str, name: str): # name is query param
    # raise EventNotFoundException(id)
    return {
        "event_id": id,
        "event_name": name
    }

# Query Param
# http://localhost:8000/event?id=1&name=sample
@app.get("/event")
def get_event(event: Event = Depends()): # Pydantic model in fun params is treated as request body and expects JSON, Depends() tells FastApi to serialize the model from query params
    return {
        "event_id": event.id,
        "event_name": event.name
    }

# Req body
# 202 Accepted - used for Async operations
@app.post("/event", status_code=status.HTTP_202_ACCEPTED)
def create_event(event: Event, extra: str): # extra is query param
    return {
        "event_id": event.id,
        "event_name": event.name,
        "extra": extra
    }

class EventNotFoundException(Exception):
    def __init__(self, event_id: str):
        self.event_id = event_id

@app.exception_handler(EventNotFoundException)
def event_not_found_exc_handler(req, exc: EventNotFoundException):
    return JSONResponse(
        status_code = status.HTTP_404_NOT_FOUND,
        content = {
            "error_code": "EVENT_NOT_FOUND",
            "error_message": f"event {exc.event_id} not found"
        }
    )
