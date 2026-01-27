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

   Installs
   - FastAPI and related
   - Redis

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

## Rate limiting – from first principles

What problem does rate limiting solve?

- Prevent abuse
- Protect downstream systems
- Ensure fairness

First-principles definition

> Rate limiting limits how often a client can perform an action in a time window.

Simplest mental model

> “Allow at most N requests per key per time window.”

Keys can be:

- user_id
- API key
- IP address

**Redis-based rate limiting (core idea)**
```
key = rate:{user_id}:{current_minute}
count = INCR(key)
if count == 1:
    EXPIRE key 60
if count > LIMIT:
    reject
```

**Skeleton code**
```
def allow_request(user_id):
    key = f"rate:{user_id}:{current_minute()}"
    count = redis.incr(key)
    if count == 1:
        redis.expire(key, 60)
    return count <= LIMIT
```
Interview-level explanation

> “We use Redis counters with TTL to enforce per-user rate limits.”

That’s enough.

---

## ETags (HTTP) — from first principles

ETags are a perfect starting point because they are:
- small
- concrete
- directly build on caching & consistency

---

## ❓ The real problem ETags solve

Imagine this flow:

Client fetches metadata:
```
GET /events/E1/metadata
```
Server returns metadata.

Client fetches again 2 seconds later.

Question:
- How does the server know whether the client already has the latest version?

Without help:
- server recomputes response
- sends full payload again
- wastes bandwidth & CPU

ETags exist to answer:
- “Has this resource changed since the last time you saw it?”

---

## 🧠 What an ETag really is

An ETag is a fingerprint of a resource’s current version.

Example response:
```
ETag: "v123"
```
That value could be:
- hash of content
- version number
- timestamp-based token

---

## 🔄 How ETags work (step-by-step)

### Step 1 — Client fetches resource

Request:
```
GET /events/E1/metadata
```
Response:
```
200 OK
ETag: "abc123"

{ ...metadata... }
```

Client stores:
- response body
- ETag "abc123"

---

### Step 2 — Client fetches again (conditional request)

Request:
```
GET /events/E1/metadata
If-None-Match: "abc123"
```
Client is saying:
- “Only send me the data if it changed.”

---

### Step 3 — Server compares ETag

If current ETag is still "abc123":
```
304 Not Modified
```
- no response body

If changed:
```
200 OK
ETag: "def456"

{ new metadata }

```
---

## Why this is powerful

- Saves bandwidth
- Saves CPU
- Reduces latency
- Works beautifully with caches & CDNs

---

## How this fits with Redis caching

Cache stores:
- metadata
- ETag

Server compares:
- client ETag
- cached ETag

Can return:
- 304 without touching DB

---

## Strong mental model 🔒

ETags are “versions for HTTP resources”.

---

## One concrete example (EventMetadata service)

If updated_at changes → new ETag

ETag could be:
- hash(event_id + updated_at)

Or even:
- updated_at
(for learning purposes)

---

## What ETags do not solve

- Authorization
- Data correctness
- Write conflicts

They are about:
- read efficiency
- freshness

not writes.

---

### 1️⃣ Why is 304 Not Modified useful?

> 304 lets the server avoid sending the response body when the client already has the latest version.

Benefits:

- saves bandwidth
- saves serialization cost
- saves CPU
- often avoids DB access (if cache/ETag available)

Important nuance:

- DB avoidance depends on whether ETag is computed from cache/version
- even if DB is touched, response body is skipped → still a win

---

### 2️⃣ How are ETags different from Redis caching?

Redis caching

- Server-side optimization
- Stores data close to service
- Helps the server avoid DB calls
- Client is unaware

ETags

- Client-side / protocol-level optimization
- Client participates in freshness check
- Helps avoid sending data over the network
- Works even without server-side cache

One-line lock 🔒

> Redis avoids recomputing data. ETags avoid resending data.

They complement each other — not replacements.

---

### 3️⃣ Where do ETags shine most?

Why public APIs & CDNs benefit most:

- many clients
- repeated GETs
- same resources requested often
- bandwidth & latency matter a lot

ETags + CDN:

- CDN can respond 304 at the edge
- origin is never hit
- massive scalability win

Internal APIs

- fewer clients
- lower repetition
- Redis/cache is usually enough

---

### 4️⃣ “How does ETag work even without server-side cache?”

### 🔹 What an ETag fundamentally represents

An ETag is a version identifier for a resource.

That version can be derived from:
- DB state
- metadata stored alongside the resource
- a precomputed value
- or a cached copy

ETag does NOT magically avoid DB access.
It avoids sending the response body when unchanged.

---

### 🔹 ETag WITHOUT server-side cache (still useful)

Imagine this setup:
- No Redis
- No in-memory cache
- Just DB

### Request flow

Client sends:
- GET /events/E1/metadata
- If-None-Match: "v123"

Server does:
- Query DB for lightweight version info only
  (updated_at, version, row_hash)
- Compare with "v123"

If equal:
- 304 Not Modified

→ No response body
→ No JSON serialization
→ No large payload

If different:
- 200 OK
- ETag: "v124"
- full metadata

### What did we save?
- Bandwidth
- Serialization cost
- Network latency

Even though DB was touched, the response is much cheaper.

---

### 🔹 ETag WITH server-side cache (best case)

Now add Redis.

Cache stores:
- metadata
- ETag (or updated_at)

Flow:
- Compare client ETag with cached ETag
- If same → 304 without DB
- If different or cache miss → DB

So yes:
- Redis makes ETags far more powerful
- but ETags are still valid without it

---

### 🔒 Key mental model (lock this in)

ETags optimize network transfer first.
Caches optimize computation and DB access.

They solve different problems and stack nicely.

---

## Backward Compatibility (API evolution)

This is huge for senior engineers, and it connects directly to:
- versioning (/v1, /v2)
- adding / removing fields
- rolling deployments
- zero-downtime changes

---

## ❓ The real problem backward compatibility solves

Imagine this situation:
- You have 100 clients
- You deploy a server change
- 30 clients are still on old code

Question:
- How do you change APIs without breaking existing clients?

Backward compatibility answers that.

---

## The golden rule (memorize this)

Servers must be backward compatible.
Clients can be forward compatible, but not required to be.

Why?
- You control server deployment
- You don’t control when clients upgrade

---

## What breaks backward compatibility?

❌ Removing a field
- Old clients expect it → crash

❌ Changing field meaning
- Same name, different semantics → subtle bugs

❌ Tightening validation
- Requests that used to work now fail

---

## What is usually safe?

✅ Adding a new field
- Old clients ignore it

✅ Adding a new endpoint
- No one is forced to use it

✅ Making a field optional
- If default behavior is preserved

---

## Concrete example (EventMetadata)

### Old response (v1)
```
{
  "event_id": "E1",
  "fraud_risk_level": "LOW"
}
```

### New response (still v1, backward compatible)
```
{
  "event_id": "E1",
  "fraud_risk_level": "LOW",
  "fraud_score": 0.12
}
```

Old clients:
- don’t know fraud_score
- ignore it
- still work

---

## When you need a new version

Introduce a new version when:
- response meaning changes
- field types change
- behavior changes
- you remove fields

Example:
- v1: ```fraud_risk_level: "LOW"```
- v2: ```fraud: { risk: "LOW", score: 0.12 }```

That’s a breaking change → new version.

---

## Versioning strategies (quick)

- Path versioning: ```/v1/...``` (most common)
- Header versioning: ```Accept: application/vnd...```

---

## How backward compatibility ties to deployments

Because:
- servers deploy gradually
- old and new versions run together
- clients hit different instances

So APIs must tolerate:
- mixed versions
- partial rollouts

---

## One-line mental model 🔒

Additive changes are safe.
Breaking changes require a new version.

---

## Why different error responses on retries are a problem

## 1️⃣ Client behavior becomes unpredictable

If retries return different errors:

- First retry: 500 Internal Server Error
- Second retry: 400 Bad Request
- Third retry: 409 Conflict

The client cannot decide:
- should I retry again?
- should I fix my request?
- should I stop completely?

So the client logic breaks down.

---

## 2️⃣ Retries may make things worse

Retries are usually automated.

If errors are inconsistent:
- client might retry on an error that is not retryable
- client might stop retrying on an error that was transient

This leads to:
- retry storms
- partial failures
- cascading issues

---

## 3️⃣ Observability becomes useless

From logs and metrics:
- you see multiple error types
- no clear pattern
- hard to aggregate or alert

This makes debugging much harder.

---
### This leads us to the core idea:
## 🔴 Error Contracts & Consistency (core idea)

## What is an error contract?

An error contract defines how errors are:
- represented
- categorized
- repeated

It ensures:
- same error → same response
- retryable vs non-retryable is clear
- clients can reason about behavior

---

### What makes a good error contract?

---

### 1️⃣ Stable error shape

Always return errors in the same structure.

Example:
```
{
  "error": {
    "code": "METADATA_NOT_FOUND",
    "message": "Metadata for event E123 not found",
    "details": {
      "event_id": "E123"
    }
  }
}
```

Never return:
- sometimes plain text
- sometimes JSON
- sometimes different fields

---

### 2️⃣ Stable error codes (THIS IS KEY)

Error codes must be:
- machine-readable
- stable over time
- independent of wording

Examples:
- `METADATA_NOT_FOUND`
- `RATE_LIMIT_EXCEEDED`
- `INVALID_SIGNAL`
- `IDEMPOTENCY_CONFLICT`

The message can change.
The code must not.

---

### 3️⃣ Same error for the same failure (idempotency)

If the same request fails twice:
- the error response should be the same

This is especially important for:
- idempotent POSTs
- retries after timeouts

Example:
- Retrying a request with the same Idempotency-Key
- Should return the same error code & message

---

## Retryability — the most important distinction

Every error must fall into one of these buckets.

---

### ❌ Non-retryable (client must fix request)

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict (sometimes)

---

### ⚠️ Retryable (client may retry)

- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable
- 504 Gateway Timeout
- 429 Too Many Requests (with backoff)

---

## Golden rule 🔒

Same error → same retry decision.

---

## Error consistency in your EventMetadata system

### GET /events/{id}/metadata

| Scenario | Status | Error Code |
| -------- | ------ | ---------- |
Metadata not found | 404 | METADATA_NOT_FOUND
Redis down (fallback works) | 200 | —
DB down | 503 | SERVICE_UNAVAILABLE

---

### POST /metadata/signals

Scenario | Status | Error Code
-------- | ------ | ---------
Duplicate signal | 200 | — (idempotent success)
Invalid payload | 400 | INVALID_SIGNAL
DB error | 503 | SERVICE_UNAVAILABLE

---

### POST /metadata/enrich

Scenario | Status | Error Code
-- | - | --
Duplicate Idempotency-Key | 202 | same job_id
Queue down | 503 | QUEUE_UNAVAILABLE

---

## Why this matters for retries & idempotency

Now everything connects:
- Idempotency → same request = same result
- Error contract → same failure = same error
- Retries → client can safely retry only retryable errors
- Observability → metrics aggregate cleanly

This is professional-grade API design.

---

## One-line mental model (lock this 🔒)

Clients retry logic depends on error consistency.
Inconsistent errors break distributed systems.

---

## API Design Deep Dive — OFFICIALLY CLOSED ✅

You’ve now covered:
- resources & semantics
- idempotency
- pagination
- versioning
- ETags
- rate limiting
- error contracts
- retries & consistency

That’s a complete API design toolkit.