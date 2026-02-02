# 🔄 CONSISTENCY MODELS — FROM FIRST PRINCIPLES

## Step 0 — The uncomfortable truth

In a distributed system, this is unavoidable:

Different parts of the system do not see the same data at the same time.

Once you accept this, consistency models stop feeling scary and start feeling practical.

---

## Step 1 — The core question consistency answers

Whenever data is written:

-  WRITE happens at time T

Consistency asks:

- Who can see this write, and when?

That’s it. Every consistency model is just a different answer to that question.

---

## Step 2 — The baseline: Single-machine consistency

Imagine:
- One process
- One DB
- One thread

If you write:

x = 5

And immediately read:

read(x)

You always see 5.

This is:
- Strong consistency (by default)

But this breaks the moment you add:
- replicas
- caches
- networks

---

## Step 3 — Why consistency breaks in real systems

Consider your real architecture:
```
Client
↓
Service
↓
Redis Cache
↓
DB Primary → DB Replica
```
Now imagine:
- You update metadata in DB primary
- Cache invalidation happens
- Replica hasn’t caught up yet

Now different readers may see:
- old value
- new value

depending on path.

This is not a bug.
This is physics (network + replication delay).

---

## Step 4 — Strong Consistency (what it really means)

### Definition (simple)

Once a write completes, all future reads see that write.

This means:
- no stale reads
- no surprises

### Cost
- higher latency
- lower availability
- coordination overhead

### How it’s achieved
- single leader
- synchronous replication
- locks / transactions

### Where it’s used
- payments
- inventory
- money movement
- security decisions

---

## Step 5 — Eventual Consistency (the default in distributed systems)

### Definition

Writes propagate asynchronously; reads may see stale data temporarily, but the system converges.

This is what:
- caches
- read replicas
- queues

naturally give you.

### Important clarification

Eventual consistency does NOT mean:
- random
- wrong forever

It means:
- temporarily inconsistent

---

## Step 6 — Why eventual consistency exists (feel it)

If you demand strong consistency everywhere:
- every read waits for all replicas
- network hiccups block reads
- availability drops

Eventual consistency trades:
- Immediate correctness
for:
- scalability and availability

This tradeoff is intentional.

---

## Step 7 — Consistency guarantees that actually matter

Most systems don’t say “strong vs eventual”.

They say:
- “What guarantees do we promise to clients?”

These are the important ones.

---

## 1️⃣ Read-Your-Writes (RYW)

If you write something, you should see it on your next read.

Example:
- User updates metadata
- Immediately fetches metadata
- Must see their update

How systems ensure it:
- read from primary
- bypass cache briefly
- sticky session
- version checks

RYW is extremely important for user experience.

---

## 2️⃣ Monotonic Reads

Once you see a new value, you should never see an older one.

Bad behavior:
- First read: fraud_risk = HIGH
- Second read: fraud_risk = LOW

This feels broken to users.

---

## 3️⃣ Writes-Follow-Reads (WFR)

If you read a value, then write based on it, the write shouldn’t be lost.

This prevents silent overwrites.

---

## Step 8 — Writes-Follow-Reads (deep, feel it)

### The bug WFR prevents

You read something, act on it, but your action is based on stale state and gets lost.

This is a very real bug class.

### Concrete story

Initial state:
- event_id = E1
- fraud_risk_level = LOW
- version = 5

Step 1 — You READ
- fraud_risk = LOW
- version = 5

You assume:
- “This is the current truth.”

Step 2 — Someone else updates
- fraud_risk = HIGH
- version = 6

Step 3 — You WRITE based on what you read
- fraud_risk = MEDIUM

If WFR is not enforced, DB might do:
- fraud_risk = MEDIUM
- version = 7

🚨 The HIGH update is LOST.

You:
- never saw version 6
- still overwrote it

This feels wrong.

### What WFR guarantees

If you write based on a read, the system must ensure your write is applied on top of what you read — or fail.

So the system says:
- “You read version 5, but current version is 6 — retry.”

---

## How systems enforce WFR

Optimistic locking (most common):

When you READ:
- version = 5

When you WRITE:

UPDATE event_metadata
SET fraud_risk = 'MEDIUM', version = version + 1
WHERE event_id = 'E1' AND version = 5;

If 0 rows updated:
- someone else wrote first
- your write is rejected
- you must re-read and retry

✅ No silent overwrite

### Why WFR matters

Without it:
- concurrent updates clobber each other
- state becomes unpredictable
- bugs are very hard to detect

WFR is why:
- version columns exist
- updated_at preconditions exist
- ETags exist in HTTP

### One-line lock 🔒

Writes-Follow-Reads prevents you from overwriting data you never saw.

---

## Step 9 — Where inconsistencies show up (your system)

### Cache
- stale reads after write
- fixed by invalidate-on-write

### Read replicas
- lag causes stale reads
- fixed by reading from primary or accepting staleness

### Async jobs
- eventual updates
- fixed by user messaging (“processing…”), polling

---

## Step 🔟 — Partition Tolerance (feel it)

### What is a partition?

Some machines cannot talk to other machines.

Not everything is down — just the network between parts.

Caused by:
- network issues
- AZ outages
- firewall misconfig
- packet loss
- cloud hiccups

This will happen.

---

### The uncomfortable truth

In a distributed system, partitions are inevitable.

So you don’t choose whether to tolerate partitions —
you choose how to behave when they happen.

---

### The CAP intuition

During a partition, you must choose:

Option A — Consistency
- Don’t return stale or conflicting data
- Some requests must fail

Option B — Availability
- Always respond
- Responses may be stale

You cannot do both simultaneously.

---

### Concrete story

Setup:
- DB primary in AZ-1
- DB replica in AZ-2
- Service in AZ-2 reads from replica

Partition happens:
- AZ-2 cannot reach AZ-1
- Replica is stuck with old data

Request arrives.

Choice 1 — Be consistent (CP):
- Return 503
- System is consistent but unavailable

Choice 2 — Be available (AP):
- Serve stale data
- System is available but inconsistent

---

### Why systems choose partition tolerance

Because:
- partitions are unavoidable
- pretending otherwise is lying

So systems are designed as:
- CP for writes
- AP for reads

---

## Step 11 — CAP theorem (very lightly)

In presence of partitions, you can’t have all three:
- Consistency
- Availability
- Partition tolerance

Most real systems are:
- AP for reads
- CP for writes

---

## Step 12 — Practical rules you should remember

Strong consistency where correctness matters.
Eventual consistency where performance matters.

Examples:

Area | Consistency
 --- | ---------
Payments | Strong
Metadata | Eventual
UI read models | Eventual
Auth decisions | Strong
Caches | Eventual

---

## Step 13 — How to talk about consistency (senior-style)

Instead of:
- “We use eventual consistency”

Say:
- “Reads may be stale briefly due to caching and replica lag, but writes are strongly consistent and the system guarantees read-your-writes for the user.”

This shows intentional design.

---

## Final mental model (lock this 🔒)

Consistency is not binary.
It’s a set of promises you make — and must keep.

---

## Final mental summary (keep this)

- Caching ⇒ eventual consistency
- RYW ⇒ user trust
- Writes-Follow-Reads ⇒ no lost updates
- Partition tolerance ⇒ system survives reality

You are already designing with consistency models — even if you didn’t call them that.
