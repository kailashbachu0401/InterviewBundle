# Event Metadata Service — End-to-End Design (Natural Layering)

> New concepts: versioning, opaque cursor pagination, signal dedupe

## What problem are we solving?

We want a service that:

- Stores and serves event metadata fast
- Supports frequent reads (UI, other services)
- Supports updates/enrichment (fraud flags, computed scores, media info)
- Is safe under retries (idempotent writes)
- Can run background enrichments asynchronously

**What this service is NOT**

>It’s not the “source of truth” for the event itself (title, start_time, venue). That lives in the Event service / main DB. This service stores metadata about the event record and related signals.

---

## Data model (what state lives where)

**Metadata entity (keyed by event_id)**

Think of one row per event:

**EventMetadata**

- event_id (PK)
- fraud_risk_level
- is_fraud_suspected
- feature_flags (JSON)
- media_summary (counts, sizes, maybe thumbnail info)
- updated_at

You can store feature_flags either as:

- structured columns (if few and stable), or
- JSON/map (if evolving fast)

**DB is the source of truth** for metadata.

---

## APIs (clean, minimal, scalable)

**Read single metadata (hot path)**

``` GET /events/{event_id}/metadata ```

- Cache-aside
- Returns 200 with metadata
- 404 if not found (or return defaults — but we’ll do 404)

**List - Opaque cursor pagination**

```GET /events/metadata?updated_after=...&limit=...&cursor=...```

- paginate response with opaque cursor (updated_at DESC, event_id DESC)

**Update metadata (write path)**

Two write styles (both useful):

- Full/partial update by trusted producers
  - ``` PATCH /events/{event_id}/metadata ```
  - Internal, Sync
  - Partial update (“set these fields”)
  - Return 200 with updated resource
  - After DB update → invalidate cache key
  - ignore idempotency-key for now, as it just set fields and internal
  - However interanl doesn't mean no retries, internal services still face:
    - timeouts
    - network hiccups
    - restarts
  - so design them to be idempotent in real life.

- Append signals (safer for multiple producers)
  - ``` POST /events/{event_id}/metadata/signals ```
  - Accept signal {source, signal_id, payload, observed_at}
  - Dedupe by (source, signal_id) (domain-level)
  - Merge into EventMetadata (simple mapping)
  - Return 200 with updated resource (or 202 if you make it async later)
  - Invalidate cache

**Async enrichment trigger**

``` POST /events/{event_id}/metadata/enrich ```

- returns 202 with a job_id
- Supports Idempotency-Key (HTTP level)
- uses the job system pattern
- Usual Idempotency-key mapping:
    - ```(key) -> (response + expiry)```
- If designing for multiple endpoints:
    - ```(key + endpoint) -> (response + expiry)```

---

## Read path (make it fast)

This is where Redis fits naturally.

**Cache-aside for reads**

For ``` GET /events/{id}/metadata ``` :

- Check Redis: eventmeta:{event_id}
- If hit → return
- If miss → read DB
- Put into Redis with TTL (e.g., 60–300s)
- Return

**Why TTL + invalidate?**

- TTL protects you from “forgot to invalidate”
- invalidate keeps staleness low

**Stampede protection (for hot events)**

If a key expires and traffic is huge:

- **single-flight lock per key** OR **stale-while-revalidate**
- (Do not over enineer, start with cache-aside and use only if you see stampede in metrics)

That said, if you want a safe simple rule:

> ✅ Single-flight only on cache miss, and only for a short lock TTL (like 1–2 seconds).

Why this is safe:

- Most requests are cache hits → no lock overhead
- Only misses contend
- The lock TTL prevents deadlocks

Hot event detection (if you ever need it):

- count requests per key in a short window (Redis counter)
- or detect repeated misses / high miss QPS

But you don’t need it on day 1.

So: either “no single-flight initially” or “single-flight only on miss for all keys”. Both are reasonable.

---

## ✅ Opaque cursor pagination (how it actually works)

we need cursor to encode the last position in our sorted order.

```ORDER BY updated_at DESC, event_id DESC```

So the cursor must include BOTH:

- last_updated_at
- last_event_id

**What “opaque” means**

Client should treat cursor as a black box:

- not parse it
- just send it back

**Example cursor contents (conceptually)**

```cursor = base64("2026-01-18T09:10:11Z|E123")```

**First page request**

```GET /events/metadata?limit=50```

Response returns:

- 50 items
- next_cursor

**Second page request**

```GET /events/metadata?limit=50&cursor=<next_cursor>```

Server decodes cursor and applies:

> “return rows AFTER this position”

In SQL-ish logic:

```
WHERE (updated_at, event_id) < (cursor.updated_at, cursor.event_id)
ORDER BY updated_at DESC, event_id DESC
LIMIT 50
```

That’s it.

**Why this is better than offset pagination**

Offset breaks when rows are inserted/updated between pages.
Cursor pagination remains consistent.

---

## Write path (correctness first)

For ```PATCH``` / ```POST signals```:

**Steps**

- Validate input
- Idempotency check (Idempotency-Key)
- Update DB (transaction)
- Invalidate cache: DEL eventmeta:{event_id}
- Return response (200/204)

**Why invalidate (DEL) instead of update cache?**

Deletion avoids race conditions like:

- writer updates DB, but cache update loses some fields
- concurrent writers overwrite each other in cache

Deletion is simplest and safest.

---

## Idempotency keys (where they live)

You already learned this well:

- Client generates key per intent
- Server stores mapping: ```(idempotency_key → response)``` with TTL

For updates, idempotency prevents:

- double applying the same signal
- duplicate writes due to retries/timeouts

**Idempotency applies to writes**, not reads.

---

## Async enrichment (use the job system)

Some metadata is **computed**, not directly written:

- fraud scoring
- media inspection
- derived flags
- cross-service aggregations

So: ```POST /events/{id}/metadata/enrich``` does:

- create job row
- enqueue job_id
- return 202 + job_id

Worker:

- reads upstream sources
- computes metadata
- writes metadata in DB
- invalidates cache key

This gives you:

- non-blocking UI
- resilience
- retry-safe processing

---

## Failure scenarios (the “feel” checklist)

**Redis down**

- reads fall back to DB
- writes still go to DB
✅ system remains correct (slower)

**Queue duplicates job_id**

- worker must be idempotent
- check job state / lease ownership

**Producer retries update**

- Idempotency-Key prevents double write

**DB slow**

- cache hit rate becomes critical
- read replicas can help for read-heavy endpoints
- writes remain on primary

---

## Scaling story (when traffic doubles)

**Scales easily**

- stateless API: add instances behind LB
- reads: cache + read replicas

**Risky**

- writes if they grow a lot (might need partitioning later)
- hot keys in Redis (one event dominating traffic)
- stampede on TTL expiry (solve with lock/jitter/stale-while-revalidate)

---

## The clean mental model

- Read path: Cache → DB
- Write path: DB → Invalidate cache
- Expensive computation: Job → Queue → Worker → DB → Invalidate cache
- Retries everywhere: require idempotency (API + worker)

This is a complete, real cloud service.

---

## Versioning (simple and practical)

> Versioning exists because APIs are **contracts**.

When you change:

- response fields
- meaning of fields
- status codes
- pagination style
- auth rules

…you risk breaking clients.

So teams create /v2, /v3 so:

- old clients keep working
- new clients get new behavior
- migration can happen gradually

**Example of a “breaking change”**

- v2 returns fraud_risk: "HIGH"
- v3 returns fraud: { "risk_level": "HIGH", "score": 0.92 }

If you changed v2 directly:

- clients parsing string would break
- So you release v3 while keeping v2.

✅ Versioning is basically “multiple API contracts supported at once”.

Start with:

```/v1/...``` in the path

Most teams do path versioning because it’s obvious.

So you’d have:

```/v1/events/{id}/metadata```

Version when you:

- break response shape
- change semantics
- remove fields

Adding fields is usually backwards compatible.

---

## Contracts: status codes and semantics

```GET /events/{id}/metadata```

- 200 OK with metadata
- 404 if event metadata not found (or you can auto-create defaults; your choice)

```PATCH /events/{id}/metadata```

- 200 OK with updated resource or
- 204 No Content if you don’t return body

Good practice: return 200 with updated metadata so callers can immediately see final state.

```POST /events/{id}/metadata/signals```

- 202 Accepted if processing signal async
- 200 OK if applied immediately
Choose based on implementation.

```POST /events/{id}/metadata/enrich```

- 202 Accepted with { job_id }

---

## Dedupe for signals: idempotency key vs signal_id

**Best practice:**

- Idempotency-Key is for API request retries
- signal_id (or (source, signal_id)) is for domain-level dedupe

Because the fraud pipeline might legitimately send:

- different signals for the same event with different meaning

And idempotency keys are typically:

- generated per HTTP request
- TTL bounded
- not always stable across pipeline retries unless designed carefully

✅ So the best field inside the signal payload is:

- signal_id (unique per signal)
- plus source (namespacing)

---

## Let’s lock your v1 API spec (clean and minimal)

**Reads**

- GET /v1/events/{event_id}/metadata

**Updates (sync)**

- PATCH /v1/events/{event_id}/metadata
- POST /v1/events/{event_id}/metadata/signals (sync, dedupe via source + signal_id)

**Async enrich (job)**

- POST /v1/events/{event_id}/metadata/enrich (202 + job_id, supports Idempotency-Key)

**List (for pagination practice)**

- GET /v1/events/metadata?updated_after=...&limit=...&cursor=...