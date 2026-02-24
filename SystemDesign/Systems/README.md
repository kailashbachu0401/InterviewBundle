# Info & Setup

In this repo, we build systems with FastAPI(Python)

## What's happening here (important)

```
app = FastAPI()

@app.get("/hello")
def hello():
    return "Hello, World!"
```

- app = FastAPI() → creates the service
- `@app.get("/hello")` → route mapping
- `hello()` → function called per request
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
   cd SystemDesign/Systems
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

   Installs
   - FastAPI and related
   - Redis

4. **Run the server:**
   ```bash
   cd <into whatever system you wanna run>
   uvicorn main:app --reload
   ```

5. **Visit:** http://127.0.0.1:8000/docs

---

## Connecting FastAPI to what you already know

| Concept |	FastAPI |
| ------- | ------- |
| Stateless service |	default behavior |
| Listening on port |	uvicorn |
| API contract |	path + method |
| Config | env vars |
| Business logic | Python functions |



