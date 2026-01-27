# ⚡ CIRCUIT BREAKERS — FROM FIRST PRINCIPLES

## Step 0 — The dangerous instinct

When something fails, engineers instinctively think:

> “Retry.”

Retries are good — until they aren’t.

Circuit breakers exist because retries alone can destroy a system.

---

## Step 1 — Feel the failure (this is real)

### Setup

Your EventMetadata service depends on DB.
```
Client
↓
API
↓
DB
```
DB becomes slow (not down, just slow).

---

### What happens WITHOUT a circuit breaker

- Request comes in
- API calls DB
- DB takes 5 seconds
- API times out
- API retries
- More requests come in
- More retries happen
- Threads pile up
- Connection pool exhausts
- API crashes
- Other endpoints fail too

🚨 Your system killed itself trying to recover.

This is called:
- retry storm
- self-inflicted denial of service

---

## Step 2 — The insight behind circuit breakers

> If something is failing consistently, stop calling it for a while.

Just like an electrical circuit breaker:
- detects overload
- cuts power
- prevents fire

---

## Step 3 — What a circuit breaker is (simple)

A circuit breaker is:

A state machine that guards calls to a dependency.

It decides:
- Should I allow the call?
- Or fail fast immediately?

---

## Step 4 — The three states (THIS IS CORE)

### 🟢 CLOSED (normal)
- Requests flow
- Failures are counted

### 🔴 OPEN (tripped)
- Calls are blocked
- Fail fast (no retries, no DB calls)

### 🟡 HALF-OPEN (test mode)
- Allow a few requests
- If they succeed → close
- If they fail → open again

---

## Step 5 — State transitions (feel them)

### CLOSED → OPEN

When:
- error rate exceeds threshold
  or
- N failures in M seconds

Example:
- 10 failures in 30 seconds → OPEN

---

### OPEN → HALF-OPEN

After:
- cooldown period (e.g., 30 seconds)

System says:
- “Let me test if it’s healthy again.”

---

### HALF-OPEN → CLOSED

If:
- test requests succeed

---

### HALF-OPEN → OPEN

If:
- even one test request fails

---

## Step 6 — What circuit breakers actually protect

Circuit breakers protect:
- your service
- your thread pool
- your DB
- your users

They do NOT:
- fix the dependency
- guarantee success

They buy time.

---

## Step 7 — What happens when breaker is OPEN

When OPEN:
- API does not call DB
- API immediately returns an error or fallback

Examples:
- 503 Service Unavailable
- cached or stale response
- partial data

This is intentional degradation.

---

## Step 8 — How this fits in your EventMetadata system

### Example: DB circuit breaker

- Wrap DB calls with a breaker
- If breaker is OPEN:
  - serve cached data if available
  - else return 503

Flow:
```
Client
↓
API
↓
Circuit Breaker
├─ CLOSED → DB
└─ OPEN → fail fast / fallback
```
---

## Step 9 — Why circuit breakers must be per-dependency

Do NOT use:
- one breaker for everything

Use:
- DB breaker
- Redis breaker
- external service breaker

Because:
- each dependency fails independently

---

## Step 10 — Why circuit breakers beat retries

Retries:
- increase load
- amplify failure
- delay response

Circuit breakers:
- reduce load
- isolate failure
- protect latency

---

## 🔒 Golden rule

> Retries handle transient failures. Circuit breakers handle persistent failures.

---

## Step 11 — Circuit breakers + retries (the right combo)

Correct pattern:
- retry a few times (with backoff)
- if failures persist → open breaker
- fail fast
- periodically probe (half-open)

Never:
- infinite retries
- retries without a breaker

---

## Step 12 — Minimal mental pseudo-flow
```
if breaker.is_open():
    raise ServiceUnavailable()

try:
    result = db_call()
    breaker.record_success()
    return result
except Exception:
    breaker.record_failure()
    raise
```

```
pip install fastapi_cb
```

```
from fastapi_cb import CircuitBreaker
from datetime import timedelta

breaker = CircuitBreaker(fail_max=5, reset_timeout=timedelta(seconds=60))

@breaker
async def call_external():
    # call an external service
    ...
```

That’s the essence, There are other circuit breakers as well like pybreaker etc.

---

## Step 13 — One-line mental model (lock this 🔒)

> Circuit breakers stop calling broken dependencies to protect the system.

---

## 🔹 How to explain this clearly (senior-style)

“We wrap calls to the DB with a circuit breaker.
If failures cross a threshold, we open the breaker and fail fast instead of retrying endlessly.
After a cooldown, we allow a few test requests to see if the dependency has recovered.”

---

## 🔒 Final lock-in mental model

- Retries → handle brief glitches
- Circuit breakers → handle sustained failures
- Together → resilient systems

---

# 🚢 BULKHEADS — FROM FIRST PRINCIPLES

## Step 0 — Why the name “bulkhead”?

On a ship, bulkheads are walls that divide compartments.

If one compartment floods:
- the whole ship doesn’t sink
- only that compartment is sacrificed

In software:
- bulkheads isolate failures so one part can’t take down everything

---

## Step 1 — Feel the failure bulkheads prevent

Your EventMetadata service has multiple endpoints:
- `GET /events/{id}/metadata` (hot path)
- `POST /metadata/enrich` (background job creation)
- maybe `GET /health`

Now imagine:
- `/metadata/enrich` calls an external fraud service that becomes slow
- those requests pile up
- your thread pool is shared across all endpoints

Result:
- threads are stuck waiting
- even `GET /metadata` becomes slow
- health checks start failing
- load balancer marks instance unhealthy
- traffic shifts → causes more overload
- cascading failure

Even though the hot path might be fine, it gets dragged down by one slow area.

---

## Step 2 — Bulkhead idea (simple)

Give each critical area its own capacity.

So if one area is overloaded, it only consumes its own quota.

---

## Step 3 — What do we isolate in practice?

Most common bulkheads isolate:

---

### 1️⃣ Thread pools / worker pools

Separate pools for:
- external calls
- DB calls
- background tasks
- request handling

---

### 2️⃣ Connection pools

Separate DB pools for:
- read traffic
- write traffic
- admin tasks

---

### 3️⃣ Rate limits / quotas

Cap expensive endpoints separately.

---

## Step 4 — The simplest bulkhead: separate thread pools

### Without bulkhead

- One shared pool
- 100 threads total
- slow endpoint consumes all 100
- everything stalls

---

### With bulkhead

- 70 threads reserved for `GET metadata`
- 30 threads reserved for `POST enrich`

If fraud service hangs:
- it burns its 30 threads
- `GET metadata` still has 70

System remains usable.

---

## Step 5 — Bulkheads are “performance isolation”

Bulkheads aren’t only about failures.

They also protect against:
- latency spikes
- traffic bursts
- noisy neighbors
- expensive queries

---

## Step 6 — Bulkheads + circuit breakers (how they combine)

They solve different problems:

✅ Bulkhead:
- stops resource starvation
- isolates capacity

✅ Circuit breaker:
- stops useless calls to a failing dependency

Together:
- your service stays alive
- downstream systems are protected

---

## Step 7 — Where bulkheads fit in your system

In EventMetadata:

Good places:
- DB calls vs external calls
- hot read endpoints vs heavy write endpoints
- background worker vs API thread pool

Example design:
- dedicated pool for metadata GET path
- separate pool for enrich / signal processing

---

## Step 8 — What bulkheads look like in interviews

Strong answer:

> “We isolate critical workloads using bulkheads — separate thread pools and connection pools — so slow external calls or expensive endpoints can’t starve the core read path.”

---

## Step 9 — One-line mental model 🔒

Bulkheads reserve capacity so one slow or failing area can’t starve the whole service.

---

## ✅ Bulkheads — CLOSED

You now clearly understand:
- Circuit breaker → stop calling something broken
- Bulkhead → stop one thing from starving everything else

Together → service stays alive under stress

---

# 🪫 BACKPRESSURE — FROM FIRST PRINCIPLES

(This is the last core resilience pattern)

Bulkheads protect your service.
Backpressure protects the system as a whole, especially under load.

---

## Step 0 — The real problem

Imagine this:
- Clients send requests faster than you can process
- You keep accepting everything
- Queues grow
- Memory grows
- Latency explodes
- Eventually the process crashes

The system died because it was too polite.

---

## Step 1 — The key insight

If you accept more work than you can handle, you will eventually fail.

So the system must sometimes say:

> “Slow down.”

That’s backpressure.

---

## Step 2 — What backpressure actually is

Backpressure is a mechanism to signal upstream systems to reduce load.

It can be:
- explicit
- implicit

---

## Step 3 — Simple examples (feel it)

---

### Example A — HTTP backpressure

Your API is overloaded.

Instead of:
- accepting request
- queuing it
- waiting forever

You return:
```
429 Too Many Requests
```
or:
```
503 Service Unavailable
Retry-After: 10
```
You’re telling the client:

> “I can’t take this right now.”

This is backpressure.

---

### Example B — Queue backpressure

Worker capacity:
- 10 jobs/sec

Producer sends:
- 100 jobs/sec

If queue grows unbounded → crash.

So you:
- cap queue length
- slow producers
- reject new jobs

That’s backpressure.

---

### Example C — Thread pool saturation

Thread pool is full.

Instead of:
- creating more threads
- letting memory blow up

You:
- reject new work
- block briefly
- shed load

Again: backpressure.

---

## Step 4 — Backpressure vs rate limiting (important distinction)

### Rate limiting
- proactive
- per user / per key
- fairness

### Backpressure
- reactive
- system-level
- survival

You often use both.

---

## Step 5 — Backpressure in your EventMetadata system

### 1️⃣ API layer

- Thread pool full → return `503`
- Rate limit exceeded → `429`

---

### 2️⃣ Job creation

- Queue depth too large → reject new jobs
- Or return `202` but delay enqueue (less common)

---

### 3️⃣ Worker side

- If DB is slow → stop pulling more jobs
- Let queue build temporarily

---

## Step 6 — Why backpressure beats buffering

Bad design:
- “Let’s just buffer more”
- bigger queues
- more memory

Good design:
- bound queues
- reject excess
- recover gracefully

---

## Step 7 — Where backpressure interacts with circuit breakers & bulkheads

They work together:

- Circuit breaker → stop calling broken dependencies
- Bulkhead → isolate capacity
- Backpressure → stop accepting new load

These three form a resilience triangle.

---

## Step 8 — What interviewers want to hear

Strong SDE2 answer:

> “When the system is overloaded, we apply backpressure by rejecting or slowing incoming requests rather than letting queues grow unbounded. This protects latency and avoids cascading failures.”

---

## Step 9 — One-line mental model 🔒

Backpressure prevents overload by refusing excess work instead of buffering it forever.

---

# 🎯 SLOs / SLIs — FROM FIRST PRINCIPLES (Capstone)

This ties together:
- observability
- backpressure
- circuit breakers
- bulkheads
- retries
- product expectations

Once this clicks, system design is complete.

---

## Step 0 — The uncomfortable truth

Your system will:
- fail sometimes
- be slow sometimes
- return errors sometimes

So the real question is NOT:
- “Can we make it never fail?”

The real question is:
- “How much failure is acceptable?”

SLOs answer that.

---

## Step 1 — What is an SLI?

SLI (Service Level Indicator) is a measurable signal of service behavior.

Examples:
- request success rate
- p95 latency
- job completion time
- cache hit rate

SLIs are metrics.

---

## Step 2 — What is an SLO?

SLO (Service Level Objective) is a target for an SLI.

Examples:
- “99.9% of requests should succeed”
- “p95 latency < 300ms”

SLOs are goals, not guarantees.

---

## Step 3 — What SLOs are NOT

❌ Not SLAs (legal contracts)
❌ Not “100% uptime”
❌ Not internal wishful thinking

SLOs exist to:
- guide engineering tradeoffs

---

## Step 4 — Why SLOs matter (feel it)

Without SLOs:
- every error feels like a crisis
- engineers overreact
- systems become brittle
- velocity dies

With SLOs:
- small failures are acceptable
- focus shifts to user impact
- resilience patterns make sense

---

## Step 5 — Error budgets (THIS IS KEY)

Error budget = how much failure is allowed.

If SLO is:
- 99.9% success

Then error budget is:
- 0.1%

Meaning:
- some failures are allowed
- you don’t panic until the budget is exhausted

This is why:
- retries
- circuit breakers
- backpressure

exist.

They protect the error budget.

---

## Step 6 — SLOs in your EventMetadata system

### API availability SLO
- SLI: successful GET requests / total GET requests
- SLO: 99.9%

### Latency SLO
- SLI: p95 latency
- SLO: < 300ms

### Job processing SLO
- SLI: jobs completed within 5 minutes
- SLO: 99%

### Cache SLO (supporting)
- SLI: cache hit ratio
- Target: > 90%

---

## Step 7 — How SLOs guide design decisions

### Example 1 — Redis down

- Cache hit rate drops
- Latency increases
- Success rate still > 99.9%

→ No paging alert
→ Acceptable degradation

---

### Example 2 — DB slow

- Latency SLO violated
- Error budget burning fast

→ Trigger:
- circuit breaker
- backpressure
- incident response

---

## Step 8 — Alerting based on SLOs (important)

Bad alert:
- CPU > 80%

Good alert:
- Error budget burn rate > threshold

Meaning:
- “We are violating user expectations.”

This keeps teams sane.

---

## Step 9 — SLOs & deployment safety

Before deploying:
- check remaining error budget

If low:
- freeze risky deploys

This prevents:
- cascading outages
- reckless changes

---

## Step 10 — One-line mental model 🔒

SLIs measure behavior.
SLOs define acceptable behavior.
Error budgets fund reliability work.

---
