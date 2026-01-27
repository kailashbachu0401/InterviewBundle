# 🚨 Failure Scenarios Workshop

*(Event Metadata Service)*

We’ll walk through **realistic failures**, one by one, and answer **four questions each time**:

- What exactly fails?
- What happens immediately?
- What does the system do?
- Why correctness is still preserved (or what degrades)

This is how senior engineers think.

---

## 🧩 Baseline Architecture (recap)

```
Client
  ↓
Load Balancer
  ↓
FastAPI (stateless)
  ↓
Redis (cache, rate limit)
  ↓
SQLite / DB (source of truth)
  ↓
(Async jobs via Queue + Worker)
```

---

## Scenario 1️⃣ — Redis is DOWN

### What fails?

- Cache reads/writes
- Rate limiting
- Single-flight locks

### Immediate effect

- Cache GET returns nothing / throws error
- Cache SET / DEL fails

### What should the system do?

- Fall back to DB
- Treat cache as best-effort
- Correct handling pattern

```
try:
    cached = cache_get(key)
except RedisError:
    cached = None
```

Then:

- Read from DB
- Serve correct data (slower)

### What degrades?

- Latency ↑
- DB load ↑

### What stays correct?

- Data correctness
- API behavior
- Idempotency
- Writes

### Why this is okay

> Cache is an optimization, not a dependency.

This is why DB is the source of truth.

---

## Scenario 2️⃣ — Redis rate limiter fails

### What fails?

- Rate limiting enforcement

### What happens?

- Users may exceed limits

### Correct decision

- Fail open, not closed
- Let requests through

### Why?

> Blocking all traffic because rate limiting infra is down is worse.

### Senior line:

> “Rate limiting is a protection mechanism, not a correctness mechanism.”

---

## Scenario 3️⃣ — Cache stampede on hot event

### What fails?

- Cache key expires
- Thousands of concurrent cache misses

### Without protection

- DB gets hammered

### With protections

- TTL jitter
- Optional single-flight lock

### If protections fail?

- DB load spike
- Possibly slower responses

### What stays correct?

- Data correctness
- Eventually cache repopulates

### Lesson

> You add stampede protection only when metrics show the need.

---

## Scenario 4️⃣ — DB is SLOW (but not down)

### What fails?

- Query latency increases
- API responses slow

### What should happen?

- Timeouts kick in
- API returns errors for slow paths
- Cache hit rate becomes critical

### Mitigations

- Cache
- Read replicas
- Query optimization

### What degrades?

- Latency
- Throughput

### What stays correct?

- Writes still correct
- No data corruption

---

### Scenario 5️⃣ — DB is DOWN

### What fails?

- Reads
- Writes
- Updates

### What should the system do?

- Fail fast
- Return 5xx
- Do not pretend success

### Why?

**Because:**

> You cannot guarantee correctness without DB

- Lying to the client is worse

### Senior principle:

> “If you can’t be correct, fail loudly.”

---

## Scenario 6️⃣ — Duplicate SIGNAL submissions

### What fails?

- Fraud pipeline retries
- Same signal arrives twice

### What prevents corruption?

- Unique constraint (event_id, source, signal_id)
- Transactional insert

### Result

- Second insert fails safely
- Metadata not updated twice

### Lesson

> Use the DB to enforce invariants.

---

## Scenario 7️⃣ — Two PATCH requests race

### What fails?

- Concurrent updates

### What happens?

- Last write wins (unless you add version checks)

### Is this acceptable?

- Often yes for metadata
- If not, add:
    - updated_at precondition
    - optimistic locking (version column)

### Senior framing

> “We accept last-write-wins unless business semantics demand stricter control.”

---

## Scenario 8️⃣ — Enrich job duplicated

### What fails?

- Client retries POST /enrich
- Two jobs created

### What prevents this?

- Idempotency-Key
- Stored response returned on retry

### Result

- Only one job runs
- Client sees consistent job_id

---

## Scenario 9️⃣ — Worker crashes mid-enrichment

### What fails?

- Job stuck in RUNNING

### What recovers it?

- Queue visibility timeout
- Lease expiration
- Retry

### What stays correct?

- Metadata eventually updated
- Cache invalidated after write

---

## Scenario 🔟 — Wrong pagination cursor sent

### What fails?

- Client sends stale or invalid cursor

### Correct behavior

- Return empty page
- Or 400 invalid cursor

### Why?

> Pagination is best-effort navigation, not correctness-critical.

---

## 🔒 Big invariants you preserved (THIS is the goal)

### Across all failures:

- DB is the source of truth
- Cache never corrupts data
- Retries never duplicate effects
- Async jobs
- System fails safely under stress

**This is production-grade correctness.**

### What interviewers look for in failure discussions

**They don’t want:**

- perfect uptime
- zero errors

**They want:**

- clear thinking
- correct fallbacks
- graceful degradation
- invariants preserved

You now have that.