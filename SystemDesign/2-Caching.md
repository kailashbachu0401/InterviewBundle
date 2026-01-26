# 🧠 Caching From First Principles (Redis)

## Step 0 — The real problem caching solves

### Why not just hit the DB every time?

Because DB reads are:

- slower than memory
- more expensive (connections, CPU, locks)
- a scaling bottleneck

Even if DB is “fast enough” today, at scale:

- read traffic spikes
- p95 latency increases
- DB becomes the limiting factor

So we introduce a faster layer.

---

## Step 1 — What a cache is (no buzzwords)

A cache is a temporary copy of data stored closer to the code that needs it, to avoid repeating expensive work.

Expensive work can be:

- DB query
- calling another service
- computing something expensive
- rendering something

So caching is not “Redis-only”. Redis is one possible cache.

---

## Step 2 — The core tradeoff (this is the heart)

Caching improves:
✅ performance
✅ scalability
✅ cost

But introduces:
❌ staleness risk
❌ invalidation complexity
❌ extra failure mode

This is the caching contract:

> “Faster reads in exchange for occasionally serving stale data (or doing extra complexity to prevent it).”

---

## Redis: what it really is

Redis is an in-memory key-value store (a service) that can store data fast and supports TTLs and atomic operations.

Key parts to feel:

- memory = fast
- key → value = lookup by key
- TTL = data expires automatically
- atomic ops = safe counters/locks (important later)

---

## Step 3 — The most important caching pattern: Cache-Aside

This is the default pattern you’ll see in most backend teams (likely Eventbrite too).

### Read flow (Cache-Aside)

1. Try cache: `GET key`
2. If hit → return value
3. If miss → read from DB
4. Put into cache with TTL: `SET key value EX 300`
5. Return value

**Why it’s loved:**

- simple
- cache can be down → system still works (falls back to DB)

### Write flow (Cache-Aside)

- Write goes to DB first
- Then either:
  - delete cache key (`DEL key`) ✅ most common
  - or update cache value (works but easy to get wrong)

This is the classic:

**Invalidate on write**

---

## Step 4 — The 2 big questions every cache must answer

### 1) What should be cached?

**Good candidates:**

- read-heavy data
- expensive to compute
- doesn’t change every millisecond

**Examples:**

- user profile
- event metadata
- permissions
- feature flags
- rate limit counters

**Bad candidates:**

- highly volatile data
- huge payloads without clear benefit
- data requiring strict real-time accuracy (unless handled carefully)

### 2) How long can it be stale?

This defines TTL or invalidation strategy.

---

## Step 5 — TTL (Time-To-Live) from scratch

TTL means:

- cache entry expires automatically after time.

Why TTL exists:

- prevents serving ancient data
- bounds memory usage
- avoids needing perfect invalidation

But TTL has tradeoffs:

- too low → cache miss rate high (wasted)
- too high → stale data risk

**Rule of thumb:**

- start with something like 30s–10m depending on staleness tolerance
- observe hit rate + staleness incidents
- adjust

---

## Step 6 — The hardest part of caching: Invalidation

The famous quote:

> “There are only two hard things in Computer Science: cache invalidation and naming things.”

Invalidate means:

- when DB changes, cache must not serve old value

**Most common strategy:**
✅ Delete key on write

- next read repopulates from DB

**Why deletion beats updating:**

- avoids race conditions
- avoids partial updates
- simplest correctness

---

## Step 7 — What can go wrong (real-life failure modes)

### A) Cache stampede (thundering herd)

If a hot key expires:

- thousands of requests miss
- all hit DB at once
- DB gets hammered

**Fixes:**

- lock per key (single-flight)
- jitter TTL (randomize expiration)
- stale-while-revalidate (serve stale briefly while one refreshes)

### B) Hot key problem

One key gets extreme traffic:

- Redis CPU/network becomes bottleneck

**Fixes:**

- shard keys / partition
- local in-process cache (L1 + L2)
- reduce payload size

### C) Cache penetration

Requests for keys that don’t exist (miss forever):

- always hit DB

**Fix:**

- negative caching (cache “not found” briefly)

---

## Step 8 — Caching architectures (L1 / L2)

### L1 (in-process memory)

- fastest
- per instance
- not shared
- gets wiped on restart

### L2 (Redis)

- shared across instances
- centralized cache
- still fast

**Common design:**

1. check L1
2. then Redis
3. then DB

---

## Step 9 — Write patterns (when cache-aside isn’t enough)

### Write-through

- write to cache and DB together (cache always updated)
- simpler reads (always hit cache)
- but write latency increases and coupling increases

### Write-behind (write-back)

- write to cache first
- DB updated async later
- fast writes but risky for correctness (data loss if cache dies)
- used in special cases, not default

For most business systems:
✅ **Cache-aside + invalidate is the safe default.**

---

## Step 10 — Redis is not a database (important feeling)

Redis can persist, but you should treat it as:

> “fast, disposable layer”

Meaning:

- if Redis flushes, system must still be correct
- DB remains source of truth (unless you explicitly design otherwise)

---

## ✅ Quick “Redis caching checklist” (notes)

When you introduce caching, decide:

- **Key design**
  - What’s the key? (`user:{id}`, `event:{id}`, `permissions:{user}:{event}`)

- **TTL**
  - How stale is acceptable?

- **Invalidation**
  - On which writes do we delete/update keys?

- **Failure behavior**
  - If Redis down → fallback to DB? (usually yes)

- **Stampede protection**
  - lock / jitter / stale-while-revalidate?

- **Negative caching**
  - cache “not found” briefly?

---

## 🔥 Why these “cache fixes” exist (the core problem)

Caching introduces one new failure mode that DB-only systems don’t have:

Many requests can miss the cache at the same time.

DBs are designed to handle concurrency carefully.
Caches are fast but dumb.

So we need guardrails.

---

## 1️⃣ Lock per key (Single-flight)

### The problem (feel it)

Imagine:

- Event E123 is super popular
- Redis key event:E123 expires at 10:00:00
- At 10:00:01 → 10,000 users hit GET /events/E123

What happens without protection?

- All 10,000 requests miss cache
- All 10,000 hit DB
- DB melts

This is called a cache stampede.

---

### The fix: Lock per key

**Idea:**

Only ONE request should go to DB.
Others should wait.

**How it feels:**

- Request A sees cache miss
- Request A acquires lock lock:event:E123
- Request A hits DB and populates cache
- Request A releases lock
- Requests B–Z read from cache

**Redis-style flow:**

- If cache miss
- If lock acquired
  - Read from DB
  - Set cache
  - Release lock
- Else
  - Wait or retry cache

**Why it’s called “single-flight”**

Only one flight goes to DB.

---

## 2️⃣ Jitter TTL (randomized expiration)

### The problem

Imagine:

- You cache 1 million events
- You set TTL = 5 minutes for all keys
- All keys expire at the same second

Result:

- Massive simultaneous cache miss
- DB spike

---

### The fix: Jitter TTL

**Idea:**

Don’t let all keys expire at the same time.

Instead of:

- TTL = 300s

Do:

- TTL = 300s ± random(0–60s)

Now:

- Keys expire gradually
- Load spreads over time
- DB stays healthy

**Feeling:**

“Let things die slowly, not all at once.”

---

## 3️⃣ Stale-While-Revalidate (serve stale briefly)

### The problem

Sometimes:

- Cache entry expires
- But DB is slow
- User waits (bad UX)

---

### The fix: Serve stale, refresh in background

**Idea:**

Slightly stale data is better than slow responses.

**Flow:**

- Cache entry expires
- First request:
  - returns stale value
  - triggers background refresh
- Next requests:
  - get fresh data

This works when:

- data is eventually consistent
- small staleness is acceptable

**Example:**

- Event name, description
- Not payment status

**Feeling:**

“Give users something now, fix it quietly.”

---

## 4️⃣ Shard keys / partition (hot key problem)

### The problem

One event becomes extremely popular:

- event:E123 gets 90% of traffic
- Redis CPU/network saturates
- Even cache becomes bottleneck

---

### The fix: Key sharding

Instead of:

- event:E123

Use:

- event:E123:shard1
- event:E123:shard2

Requests randomly choose shard.

This spreads:

- CPU
- network
- lock contention

**Feeling:**

“Don’t let one celebrity crush the party.”

---

## 5️⃣ Local in-process cache (L1 + L2)

### The problem

Even Redis:

- is network call
- adds latency
- can be overloaded

---

### The fix: Two-level cache

Service structure:

- L1: in-memory dict (per instance)
- L2: Redis
- DB

**Flow:**

- Check L1 (super fast)
- If miss → Redis
- If miss → DB

**L1 properties:**

- fastest
- wiped on restart
- not shared

**L2 properties:**

- shared
- slower than memory
- survives instance restarts

**Feeling:**

“Remember things locally before asking the world.”

---

## 6️⃣ Reduce payload size

### The problem

Even cache hits can be slow if:

- payload is huge
- serialization is expensive
- network transfer dominates

---

### The fix

Cache:

- only what you need
- not entire objects

**Example:**

- cache event summary
- not full description + images + nested objects

**Feeling:**

“Don’t carry the whole house when you need the keys.”

---

## 7️⃣ Negative caching (“not found”)

### The problem

Requests for non-existent data:

- GET /events/does-not-exist

Every time:

- cache miss
- DB hit
- DB hit
- DB hit

Attackers can abuse this.

---

### The fix: Cache the absence

Cache:

- event:does-not-exist → NOT_FOUND (TTL 30s)

Now:

- future requests don’t hit DB
- TTL ensures eventual correctness

**Feeling:**

“Remember that something doesn’t exist.”

---

## 🧠 Big picture — what you now understand

You now understand caching at engineering depth:

- why caching exists
- why it fails
- how to fix failures
- when to add complexity
- how Redis fits in

This is way beyond interview-only knowledge.

---

## Single Flight key - concept and skeleton code
```
GET /events/E123/metadata

1. Check cache
2. Miss
3. Try to acquire lock: lock:event:E123
4. If lock acquired:
     - Read DB
     - Set cache
     - Release lock
     - Return
   Else:
     - Wait briefly / retry cache
```

**skeleton code**

```
def get_event_metadata(event_id):
    key = f"eventmeta:{event_id}"
    lock_key = f"lock:{key}"

    value = redis.get(key)
    if value:
        return value

    if redis.setnx(lock_key, "1"):
        redis.expire(lock_key, 2)  # safety TTL
        try:
            value = db.fetch(event_id)
            redis.set(key, value, ex=120)
            return value
        finally:
            redis.delete(lock_key)
    else:
        # Someone else is fetching; wait and retry cache
        sleep(20ms)
        return redis.get(key) or db.fetch(event_id)
```

When to mention in interview

Say:

> “We can add single-flight locking on cache miss if we see stampedes on hot keys.”

You don’t need to implement it unless asked.

---

## Run Redis locally with Docker
```
docker run --name redis-dev -p 6379:6379 -d redis:7
```

Check it’s running:
```
docker ps
```

(Optional) open Redis CLI inside container:
```
docker exec -it redis-dev redis-cli
```

Try:
```
PING
# -> PONG
```

---

## Redis basics you must know (SDE2 level)

Redis is an in-memory key-value store. Common types:

- String (most used)
- Hash, Set, Sorted Set, List (useful later)

For caching we mostly use String values, often JSON.

Key concepts:

- TTL: key expires automatically
- Atomic operations: SET NX, INCR are atomic (super important for locks & rate limiting)

---

## Install Python Redis client
```
pip install redis
```

Test connection (Python REPL):

```
import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.ping()  # True
```

**Important option**

```decode_responses=True``` → you get strings not bytes (simplifies JSON)

---

## Redis commands & terminology (what “setnx” means)

SETNX (Set if Not eXists)

**Old Redis command:**

- ```SETNX key value```
- returns 1 if it set, 0 if key already exists

**In modern Redis, preferred form is SET with NX:**

- ```SET key value NX EX 2```

Meaning:

- NX = only set if key doesn’t exist
- EX 2 = expire in 2 seconds

In redis-py, that’s:

```r.set("lock:key", "1", nx=True, ex=2)```

That line is the “setnx + expire” combo in one atomic command.

---

## Rate limiting (Redis INCR + EXPIRE) — terminology + code

Redis INCR key atomically increments an integer value.

Pattern:

- increment counter
- if it was first increment → set expiry window
- block if counter exceeds limit