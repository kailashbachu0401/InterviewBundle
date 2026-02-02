# 👁️ OBSERVABILITY — FROM FIRST PRINCIPLES

## Step 0 — The core problem observability solves

Imagine this happens in production:

> “Users are complaining that data is slow or wrong.”

Your system is running.
Nothing is crashed.

But you don’t know:
- where it’s slow
- what’s failing
- whether it’s cache, DB, or queue
- which user is affected
- whether it’s getting worse

Observability exists to answer questions about system behavior from the outside.

---

## Step 1 — Monitoring vs Observability (important distinction)

### Monitoring

Answers:
- “Is the system broken?”

Examples:
- CPU high?
- DB down?
- Service returning 500s?

Good, but shallow.

---

### Observability

Answers:
- “Why is the system behaving this way?”

Examples:
- Why is latency high only for some users?
- Why are retries spiking?
- Why is cache hit rate dropping?
- Why are jobs stuck in RUNNING?

Observability lets you explain behavior, not just detect failure.

---

## Step 2 — The Three Pillars (this is the foundation)

Every observable system is built on three signals:
- Logs – what happened?
- Metrics – how often / how bad?
- Traces – where did time go?

You need all three.

---

## 🧾 1️⃣ Logs — “What happened?”

### What logs really are

Logs are structured records of events.

Bad log:
```
Something failed
```
Good log:
```
{
  "level": "ERROR",
  "service": "event-metadata",
  "event_id": "E123",
  "request_id": "req-789",
  "error": "DB timeout"
}
```

### What logs are good for
- debugging specific failures
- understanding edge cases
- audits

### What logs are bad at
- aggregations
- trends
- alerting

### Logging rules (senior-level)
- Always log with context
  - request_id
  - user_id (if allowed)
  - event_id
- Log errors, not success spam
- Logs must be machine-readable (JSON)

---

## 📊 2️⃣ Metrics — “How bad is it?”

Metrics are numbers over time.

Example metrics:
- request_count
- error_rate
- p95_latency
- cache_hit_rate
- queue_depth

Metrics answer:
- “Is this happening a lot?”

---

### The Golden Signals (you must know these)

Every service should track:
- Latency – how long requests take
- Traffic – how many requests
- Errors – how many failed
- Saturation – how close to capacity

If you only track these four, you’re already strong.

---

### Metric examples (EventMetadata service)

- http_requests_total ``{path="/v1/events/{id}/metadata"}``
- http_request_latency_p95
- cache_hit_ratio
- db_query_latency
- jobs_running_count

---

### Why metrics are better than logs for alerts

Logs:
- too noisy
- too detailed

Metrics:
- aggregated
- stable
- cheap to alert on

---

## 🔗 3️⃣ Traces — “Where did time go?”

Traces show a single request’s journey through the system.

Example trace:
```
GET /events/E123/metadata
 ├─ API Gateway (5ms)
 ├─ EventMetadata Service (20ms)
 │   ├─ Redis GET (2ms)
 │   └─ DB SELECT (15ms)
 └─ Response
```
Without traces:
- you know it’s slow
- you don’t know where

With traces:
- you see exactly where time is spent

---

### What makes tracing work: correlation IDs

Every request gets a unique ID:
```
X-Request-Id: req-abc123
```
This ID is:
- generated at gateway
- passed to all services
- logged everywhere

So logs, metrics, and traces all connect.

### Rule 🔒

If you can’t follow one request end-to-end, you are blind.

---

## Step 3 — Observability in your EventMetadata system

### Logs you should have

On every request:
- request_id
- path
- status_code
- latency

On errors:
- exception
- event_id
- DB / Redis error

---

### Metrics you should track

Service-level:
- request rate
- error rate
- latency p50 / p95 / p99

Cache-level:
- cache_hit_rate
- cache_miss_rate

DB-level:
- query_latency
- connection_errors

Job system:
- jobs_created
- jobs_running
- jobs_failed
- retry_count

---

### Traces you should enable
- gateway → service
- service → redis
- service → db
- service → queue

Even sampling 1–5% is enough.

---

## Step 4 — Alerts (this is where people mess up)

Bad alerts:
- CPU > 80%
- Memory > 70%

Good alerts:
- Error rate > threshold
- Latency SLO violated
- Queue depth growing
- Cache hit rate drops suddenly

---

### Example alert logic

Good:
- “Alert if p95 latency > 500ms for 5 minutes”

Bad:
- “Alert if one request is slow”

---

## Step 5 — Debugging with observability (real flow)

User reports:
- “Event metadata is slow”

You:
- Check metrics → p95 latency up
- Check cache hit rate → dropped
- Check traces → DB calls dominating
- Check logs → Redis timeout errors

Conclusion:
- Redis instability → cache misses → DB overload

Without observability: hours
With observability: minutes

---

## Step 6 — Why observability is not optional

Distributed systems:
- always have partial failures
- always have retries
- always have inconsistency windows

Observability lets you:
- detect
- explain
- fix

without guessing.

---

## Final mental model (lock this 🔒)

Logs tell stories
Metrics tell trends
Traces tell journeys

You need all three to see clearly.
