# 🔐 Distributed Locking — From First Principles

## The real problem it solves

You have multiple instances of a service.

They all see the same data.

Now imagine:
> “Only ONE of them should do X.”

Examples:
- only one worker processes a job
- only one instance runs a scheduled task
- only one service updates a shared resource
- cache single-flight
- leader election (next topic)

---

## Why local locks don’t work

In single-process code:
```
lock.acquire()
```
But in distributed systems:
- processes are on different machines
- memory is not shared
- local locks do nothing

So we need a shared lock.

---

## What a distributed lock must guarantee

At minimum:
- Mutual exclusion — only one holder
- Timeout — lock is not held forever
- Ownership — only holder can release

If any of these fail → bugs.

---

## The simplest distributed lock (Redis-based)

This pattern is commonly used, often without naming it.

### Core idea

Use Redis as a shared atomic state.

---

### Lock acquisition

```
lock_id = uuid()
ok = redis.set("lock:event:E123", lock_id, nx=True, ex=5)
```

Meaning:

- `nx=True` → only set if key doesn’t exist
- `ex=5` → auto-expire in 5 seconds

If `ok` is True:

- you hold the lock

If `False`:

- someone else holds it

---

### Lock release (IMPORTANT)

> Only the lock owner should release it.

So you check lock_id before deleting:

```
if redis.get("lock:event:E123") == lock_id:
    redis.delete("lock:event:E123")
```

This prevents:
- one process deleting another process’s lock

---

## Why TTL is mandatory

If a process:
- crashes
- hangs
- gets partitioned

Without TTL:
- lock is stuck forever
- system deadlocks

TTL guarantees eventual recovery.

---

## Failure scenario (feel it)

Two workers: A and B

- A acquires lock
- A crashes
- Lock expires after TTL
- B acquires lock
- Work continues

This is why expiration is non-negotiable.

---

## What Redis locks are good for

- ✅ short-lived coordination
- ✅ best-effort exclusivity
- ✅ cache single-flight
- ✅ job ownership
- ❌ not for long critical sections

Redis locks are pragmatic, not perfect.

---

## What Redis locks are NOT good for

- ❌ long transactions
- ❌ multi-resource atomicity
- ❌ strict fairness guarantees

For those, you need:
- DB locks
- Zookeeper
- etcd

But Redis is enough for most SDE2 use cases.

---

## Where you already used distributed locks

You’ve already seen it:
- cache single-flight
- job lease acquisition

You just didn’t call it that.

---

## One-line mental model 🔒

> A distributed lock is shared state + atomic set + TTL.

---

### All instances must point to the same shared Redis cluster or namespace for the lock key.

Because the lock is just a key in Redis:
- If instance A uses Redis Cluster 1
- and instance B uses Redis Cluster 2

They’ll both think they acquired the lock → lock becomes useless.

So requirement is:
- shared Redis infrastructure (same logical lock store)
- consistent key naming

🔒 Mental model:
> Distributed lock works only if the lock state is shared.

---

### multi-resource atomicity

It means:
- you need to acquire or update multiple resources as one indivisible operation

Example:
- event:E1:metadata
- event:E1:fraud

If you do:
- acquire lock A
- acquire lock B

Failure scenario:
- acquire lock A
- crash before acquiring lock B

Now:
- resource A is locked
- resource B is not locked

System can deadlock or corrupt state.

This is multi-resource coordination.

Atomicity means:
- either all locks are acquired together
- or none are acquired

Redis basic locks don’t give strong guarantees here.

There are patterns:
- lock ordering
- try-lock both and rollback
- specialized systems (etcd, ZooKeeper)

---

## 👑 Leader Election (Conceptual)

## What leader election is

Leader election is basically:

> Pick exactly one instance to perform a shared responsibility.

Examples:
- one scheduler runs cron jobs
- one instance does “outbox publishing”
- one worker coordinates compaction
- one node is “primary” for some shard

---

## Why do we need leader election?

Because if every instance runs the same background job, you get duplicates.

Example:
- You run 10 instances
- each runs “publish outbox every 5 seconds”
- you just published 10x duplicates

So you want:
- ✅ only one instance runs that periodic task

---

## The simplest leader election using Redis lock

Leader election = “keep renewing a lock”.

### Acquire leadership

- Try to acquire lock: leader:publisher
- If you get it → you are leader

### Stay leader

- Periodically extend TTL
- This is called “renewing the lease”

### Lose leadership

- If you crash or stop renewing
- TTL expires
- Someone else acquires leadership

This pattern is also called:
- lease-based leadership

---

## The only 2 tricky points (feel them)

### 1️⃣ Split brain (rare but important)

If the network is weird:
- instance A thinks it’s leader
- instance B also thinks it’s leader

This can happen if:
- lock system is not strongly consistent
- there are network partitions

Mitigation:
- short TTL
- frequent renewal
- verify ownership (token)
- in serious systems: etcd / ZooKeeper

For interviews and SDE2:
- knowing this risk exists is enough

---

### 2️⃣ Leadership ≠ authority forever

Leadership is temporary.

So leader tasks must be:
- idempotent
- safe if run twice
- checkpointed

Because leadership can change mid-job.

---

## Where would you use leader election in your job system?

Earlier example:
- “a background job runs every 30 minutes and enqueues pending jobs”

That background job is a perfect candidate:
- you want only one instance doing it

---

## 1️⃣ Distributed Lock vs Leader Election — clean distinction

### Distributed Lock (scope: an operation)

Purpose:
- ensure only one instance performs a specific operation at a time

Characteristics:
- lock is held briefly
- many instances may acquire it over time

Examples:
- cache single-flight
- updating a shared row
- processing one job
- acquiring a job lease

Mental model:
- “Who can do this operation right now?”

---

### Leader Election (scope: a role)

Purpose:
- ensure only one instance performs a recurring or global task

Characteristics:
- leadership held for a duration
- leader periodically renews lease

Examples:
- cron / scheduler
- outbox publisher
- compaction job
- sweeping stuck jobs

Mental model:
- “Who is responsible for this role right now?”

---

## One-line lock 🔒

Locks protect actions.
Leaders own responsibilities.

This framing is interview gold.

---

## 2️⃣ If the leader crashes, how is a new leader chosen?

- Lease expires
- Another instance acquires it

This is why:
- TTL is mandatory
- leadership must be renewable
- tasks must be idempotent

---

## Correct leader-only examples in your system

- sweeper for stuck jobs
- outbox publisher (if using outbox pattern)
- periodic cleanup tasks
- schema migration coordinator

Refined answer you can say:

“The periodic sweeper that finds stuck RUNNING jobs and re-enqueues them should be leader-only.”

---

## ✅ Leader Election — CLOSED

You now understand:
- why leader election exists
- how it differs from locks
- how Redis leases are used
- where it fits in real systems
