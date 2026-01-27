# 🗄️ DATABASE SCALING — FROM FIRST PRINCIPLES

---

## Step 0 — What a database really does

A database is just a service that:

- stores state durably
- answers queries
- enforces correctness (constraints, transactions)

So scaling a DB means:

- handling more reads, more writes, or more data
- without breaking correctness

---

## Step 1 — The first scaling wall (feel it)

Imagine this simple system:

Service → Database

Everything works fine until:

- traffic increases
- DB CPU spikes
- queries slow down
- connections exhaust

At this point, your service is fine — **DB is the bottleneck**.

So the question becomes:

> “Which type of load is hurting us?”

This determines the scaling strategy.

---

## 🔍 Step 2 — Identify the bottleneck

There are 3 fundamentally different problems:

1️⃣ Too many reads
2️⃣ Too many writes
3️⃣ Too much data

Each has a different solution.

---

## Step 3 — Read scaling (the easiest one)

### Observation

Most systems are:

- read-heavy
- same data requested repeatedly

So why hit the same DB for the same data?

### ✅ Solution: Read Replicas

**Idea**

- One primary DB (writes)
- Multiple replicas (reads)

Service behavior:

- writes → Primary DB
- reads → Replica DBs

### What this gives you

- Reads scale horizontally
- Primary DB protected
- Low risk

### Tradeoff (VERY IMPORTANT)

Replicas are usually:

- eventually consistent

Meaning:

- write happens
- replica catches up later

So:

- you may read slightly stale data

For many use cases:

- profiles
- metadata
- events

This is totally fine.

### Rule of thumb

**Scale reads first. Always.**

This is the first DB scaling step in real systems.

---

## Step 4 — Write scaling (this is harder)

Writes are harder because:

- correctness matters
- conflicts happen
- ordering matters

You cannot just “add replicas” for writes.

So what do we do?

### ❌ What doesn’t work

- Multiple primaries writing same data without coordination
- “Just shard randomly” without rules

These break consistency.

---

## Step 5 — Vertical scaling (the naive approach)

First instinct:

> “Let’s use a bigger DB machine.”

This is called **vertical scaling**.

### Pros

- Simple
- No code change

### Cons

- Hard limit
- Expensive
- Eventually fails

This buys time — **not a solution**.

---

## Step 6 — Sharding (horizontal write scaling)

### What is sharding?

Split data across multiple independent databases.

Instead of:

- one DB with all data

You have:

- DB shard 1 → users 1–1M
- DB shard 2 → users 1M–2M
- DB shard 3 → users 2M–3M

Each shard:

- handles its own reads & writes
- reduces load per DB

### Key idea

Each piece of data has **exactly one owner shard**.

This avoids conflicts.

---

## Step 7 — How do you choose shards? (this is critical)

You must choose a **shard key**.

### Good shard keys

- evenly distributed
- frequently queried
- immutable

Examples:

- user_id
- account_id
- tenant_id

### Bad shard keys

- timestamp (hotspot)
- country (skewed)
- mutable fields

---

## Step 8 — Sharding tradeoffs (feel the pain)

Sharding gives scale, but costs:

- ❌ Cross-shard queries become hard
- ❌ Transactions across shards are complex
- ❌ Re-sharding later is painful

So we follow this rule:

**Shard only when you must.**

Before sharding, always try:

- caching
- read replicas
- query optimization

---

Example usecase for sharding:

> Blinkit processes millions of orders per seconds, but their DB is stable. They shard orders table based on state: all Delhi orders go to a shard, and similarly Pune, Andhra etc.

This is a location-based shard key.

Let’s analyze why it works and when it doesn’t.

### Why location-based sharding works for Blinkit

Key properties of a good shard key:

- 1️⃣ High cardinality
    - Many cities / regions
    - Load spread across shards

- 2️⃣ Write locality
    -Orders for Delhi mostly accessed together
    -Inventory checks local

- 3️⃣ Query alignment

    - Most queries are “orders in this city”
    - Cross-city queries are rare

So:
```
shard_key = city_id
```

is a domain-aligned shard key.

### When this would NOT work

If:

- Delhi generates 10× traffic of other cities
- One shard becomes a hotspot

Then:

- that shard becomes bottleneck
- system loses balance

This is called **shard skew**.

---

### Important sharding pitfalls (VERY IMPORTANT)

**❌ Bad shard key: time**

Example:
```
shard by day
```

Why bad:

- “today” shard gets all writes
- hotspot guaranteed

---

**❌ Bad shard key: low cardinality**

Example:
```
shard by country (IN, US)
```

Too few shards → uneven load.

---

**❌ Bad shard key: frequently queried across shards**

Example:
```
shard by user_id
```

But queries are:
```
“all orders today”
```

Now every query hits all shards.

This defeats sharding.

---

### The 3 questions to decide a shard key (memorize)

Before sharding, always ask:

- What grows the fastest? (writes or data)
- What do queries look like?
- Can most queries be answered by ONE shard?

If answer to #3 is “no”, rethink shard key.

---

### Common shard key patterns (real-world)

| Pattern |	Example | When it works |
| -- | -- | -- |
Tenant-based | tenant_id |	SaaS apps
Geography-based |	city_id |	Local services
User-based |	user_id |	User-centric apps
Hash-based |	hash(id) |	Uniform load, simple queries

---

### Hash-based sharding (important fallback)

Instead of:
```
shard = city_id
```

You do:
```
shard = hash(order_id) % N
```

**Pros:**

- perfect distribution

**Cons:**

- no locality
- cross-shard queries common

**Used when:**

- uniform access > locality

---

### Re-sharding (the hard truth)

Re-sharding is:

- expensive
- risky
- operationally complex

That’s why:

> You delay sharding until absolutely necessary.

And when you do shard:

- pick shard key carefully
- think long-term growth

---

### One-line mental model 🔒

> Sharding trades simplicity for scalability — choose shard keys based on query patterns, not intuition.

---

## Step 9 — Transactions & consistency (important intuition)

### Single DB

- ACID transactions are easy

### Sharded DB

- ACID across shards is expensive or impossible

Systems move toward:

- eventual consistency
- application-level coordination

This is why:

Many large systems sacrifice strict consistency for scale.

---

## Step 10 — Indexing (the forgotten hero)

Before scaling infrastructure, always ask:

> “Is the query fast?”

Indexes:

- dramatically reduce read time
- reduce CPU
- reduce IO

Bad indexing often causes:

- unnecessary “scaling” efforts

### Senior habit

**Profile queries before scaling databases.**

---

## Step 11 — Putting it all together (mental hierarchy)

When DB struggles, think in this order:

1. Can I cache?
2. Can I add read replicas?
3. Can I optimize queries/indexes?
4. Can I vertically scale temporarily?
5. Do I really need sharding?

This order matters.

---

## 🧠 One-page DB Scaling Mental Model

| Problem            | Solution                     |
|--------------------|------------------------------|
| Too many reads     | Cache, read replicas         |
| Too many writes    | Sharding                     |
| Too much data      | Sharding                     |
| Slow queries       | Indexing                     |
| Stale reads        | Accept or design around      |
| Strict consistency | Avoid sharding or redesign   |

---

## 1️⃣ Why is read scaling easier than write scaling?

Let’s lock the deeper reason:

**Reads can be safely duplicated. Writes cannot.**

Why:

- Multiple replicas can serve the same data
- Reads don’t need coordination
- No ordering or conflict resolution needed

Writes, on the other hand:

- change state
- must be ordered
- must be consistent
- may conflict with other writes

So:

Reads scale horizontally by copying data.
Writes require coordination, which limits scale.

That’s the core reason.

---

## 2️⃣ Why does sharding complicate transactions?

> Transactions require atomicity and consistency across multiple resources.

In a single DB:

- one transaction manager
- easy rollback
- ACID guarantees

Across shards:

- each shard is an independent DB
- no single authority
- partial failure possible

To make it work, you need:

- two-phase commit
- distributed locks
- compensation logic

All of which:

- are slow
- are failure-prone
- hurt availability

That’s why most large systems:

**Avoid cross-shard transactions entirely.**

---

## 3️⃣ When should you NOT shard a database? (important correction)

The correct rule is:

> You should NOT shard when your data set or write load can still be handled by a single database instance.

Sharding is not primarily about consistency — it’s about operational complexity.

You avoid sharding when:

- DB fits on one machine
- writes are manageable
- queries often need joins
- strong transactions are important
- team complexity should be low

Even systems that can compromise consistency often still avoid sharding until absolutely necessary.

So the better phrasing:

**Don’t shard until you are forced to by scale.**

Consistency tradeoffs come after that decision.

---

## 🔒 One-line DB scaling rule

**Sharding is a last resort. Cache and replicas come first.**

---

## 🔗 Applying DB Scaling to a Job System (Real World)

This is the payoff.

---

## Job system DB usage (realistic)

### Reads

- GET /jobs/{id}
- polling job status
- dashboards

➡️ Read-heavy
➡️ Easy to scale with:

- cache
- read replicas

### Writes

- job creation
- status updates
- lease updates

➡️ Write-sensitive
➡️ Usually manageable on single primary DB

So:

**Job systems rarely need sharding early.**

That’s a real-world insight.

---

## Where caching fits (connecting topics)

For job status:

- cache job:{job_id}:status
- TTL = short (e.g., 5–10 seconds)
- invalidate on write

This:

- reduces DB polling load
- improves UX
- avoids stale results for long

---

## Where sharding might come later

If:

- millions of jobs per second
- multi-tenant system
- very large tables

Then shard by:

- tenant_id
- account_id

But not before.

---

## 🧠 You now have the FULL mental stack

You’ve built, from scratch:

- Services (stateless)
- Config
- Containers
- Load balancers
- Sync vs async
- Queues
- Idempotency
- Job processing
- Caching
- DB scaling

**This is real system design.**
