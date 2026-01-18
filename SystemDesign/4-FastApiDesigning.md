# 🧠 What an API server REALLY is (re-grounding)

An API server is just:

A long-running process that:
- listens on a port
- receives HTTP requests
- runs code
- returns responses

FastAPI just makes this clean and explicit in Python.

---

## What's happening here (important)

```
app = FastAPI()

@app.get("/hello")
def hello():
    return "Hello, World!"
```

- app = FastAPI() → creates the service
- @app.get("/hello") → route mapping
- hello() → function called per request
- return value → JSON response

No magic. Just Python functions.

---

## You don't "run" this file like a script.

You start a server:
```
uvicorn main:app --reload
```
Meaning:

- main → file name
- app → FastAPI object
- --reload → auto restart on code change

Now:

- service listens on localhost:8000
- /hello is reachable
- This is your service lifecycle.

---

## Setup

1. **Create a virtual environment:**
   ```bash
   cd <into SystemDesign>
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate  # On Mac/Linux
   # or
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Visit:** http://127.0.0.1:8000/docs

---

## Step 3️⃣ Connecting FastAPI to what you already know

Let’s map concepts:

| Concept |	FastAPI |
| ------- | ------- |
| Stateless service |	default behavior |
| Listening on port |	uvicorn |
| API contract |	path + method |
| Config | env vars |
| Business logic | Python functions |

---

## ✅ Path param = identity (which resource?)

Use a path param when the value identifies the thing you’re operating on.

Examples:

- GET /jobs/{job_id} → you’re asking for one specific job
- GET /events/{event_id}
- PUT /users/{user_id}
- DELETE /orders/{order_id}

Rule of thumb

> If changing the value changes which resource you’re talking about, it belongs in the path.

---

## ✅ Query param = options (how do you want it?)

Use query params for:

- filtering
- sorting
- pagination
- searching
- optional modifiers

Examples:

- GET /jobs?status=RUNNING&limit=20
- GET /events?city=delhi&start_after=2026-01-01
- GET /search?q=music
- GET /events/{id}?expand=venue (optional “how much info” option)

Rule of thumb

> If changing the value changes how you fetch/list/format results (but not the identity), it’s a query param.

---

### Quick “feel” test

If you can say:

- “Give me job 123” → path
- “Give me jobs where status=RUNNING” → query
- “Give me job 123 but with extra details” → query option (expand=...)

---

## Connecting path/query params to our Job System

### Option A — /users/{user_id}/jobs

What it means conceptually

> “Show me the jobs that belong to this specific user.”

Here:

- user is the primary resource
- jobs are owned by the user
- jobs are subordinate to user
This reads very naturally.

*When A is the better choice ?*

Choose A when:

- jobs clearly belong to a user
- user context is central
- you expect more user-scoped endpoints

Example:

- /users/{id}
- /users/{id}/jobs
- /users/{id}/settings
- /users/{id}/notifications

This models a hierarchy.

---

### Option B — /jobs?user_id={user_id}

What it means conceptually

> “Show me jobs, filtered by user.”

Here:

- jobs are the primary resource
- user_id is just one of many possible filters
- This treats jobs as a global collection.

*When B is the better choice*

Choose B when:

- jobs can be filtered by many dimensions
- user is just one filter among many

Example:

- /jobs?user_id=123
- /jobs?status=RUNNING
- /jobs?type=report
- /jobs?created_after=...

This is very flexible and common in real systems.

---

Are we identifying a single resource, or filtering a collection?

- GET /jobs/{job_id} → identifies one job
- GET /jobs?user_id=123 → filters many jobs

So:

path params identify a specific resource

query params filter collections

---

### which is “more correct” here?

For a job system, most teams choose:

> 👉 B) GET /jobs?user_id={user_id}

Why?

- jobs are a global resource
- user is just one filter
- easy to extend later

But…

A) is still valid if:

- you want strong domain hierarchy
- your API is user-centric
- you prefer clearer ownership semantics

Senior-level takeaway (THIS is what matters)

> Path params express identity. Query params express filtering.

Both are correct — choose based on clarity

---
