🏗️ SYSTEM DESIGN — FROM REAL SCRATCH

(The way engineers actually learn it)

Think of this as “How software runs in the real world”, step by step.

---

## Step 0: What System Design REALLY is (reframe)

System Design is not diagrams.

System Design is answering:

“How does my code behave when it runs outside my laptop,
with real users, real failures, real scale?”

That’s it.

Everything else (APIs, containers, cloud, DevOps) exists only to answer that question.

---

## Step 1: The most basic question (we never skip this)

❓ What happens when you run a backend program?

Let’s start extremely concrete.

You write this code:

```
print("Hello World")
```

On your laptop:

* OS loads Python
* Python runs your code
* Program exits

Now imagine:

```
@app.get("/hello")
def hello():
    return "Hello World"
```

This is not a program that ends.

It:

* starts
* listens forever
* responds to requests

This is called a service.

👉 System design = designing services that run forever.

---

## Step 2: What is a “service”?

A service is just:

* A long-running program that waits for requests and responds.

Example services:

* API server
* background worker
* scheduler

Important realization:

A service is just code + environment + configuration.

---

## Step 3: What is STATE? (this is foundational)

This is where everything starts.

State = information remembered between requests

Example:

```
count = 0

@app.post("/increment")
def inc():
    global count
    count += 1
    return count
```

Here:

* count is state
* It lives in memory
* It survives across requests

Now ask:
❓ What happens if the process restarts?

→ count = 0 again
→ state is lost

This is the core problem system design tries to solve.

---

## Step 4: Stateless vs Stateful (core concept)

### 🟥 Stateful Service

A service is stateful if:

* It keeps important data in memory or local disk
* Restarting the service loses data

Problems:

* Hard to scale
* Hard to recover
* Hard to load-balance

### 🟩 Stateless Service

A service is stateless if:

* Each request is independent
* No important data is stored in memory
* All state is stored elsewhere (DB, cache)

Example:

```
@app.get("/user/{id}")
def get_user(id):
    return db.get_user(id)
```

Here:

* Service remembers nothing
* DB holds state

👉 Stateless services are the default in modern systems.

This single concept will show up everywhere.

---

## Step 5: Why stateless matters (intuition, not theory)

Imagine 3 instances of your service:

```
Client → Load Balancer → Service A
                         Service B
                         Service C
```

If stateless:

* Any request can go to any instance
* You can add/remove instances freely
* Crashes don’t lose data

If stateful:

* Requests must go to the “right” instance
* Scaling is painful
* Failures are dangerous

That’s why people say:

“Push state to storage.”

---

## Step 6: Where does state go then?

There are only 3 places state can live:

* Memory (fast, volatile)
* Disk (local, risky)
* External storage (DB, cache, object store)

System design is mostly about:

Choosing which state goes where.

---

## Step 7: Databases are not “magic boxes”

A database is just:

* Another service that specializes in storing state safely.

Key properties:

* durability
* consistency
* availability

You don’t need internals yet.
Just understand:

DB = state owner.

---

## Step 8: What is an API REALLY?

An API is just:

* A contract between two programs.

Example:

```
GET /users/123
```

Means:

* input shape
* output shape
* error behavior

System design is about:

Designing APIs that are safe, clear, and evolvable.

We’ll go deep into this later.

---

## Step 9: Where containers come in (intuition only)

Right now:

* Your service depends on OS, libraries, configs

A container is:

* A box that bundles code + runtime + dependencies.

It ensures:

“It runs the same everywhere”

Docker doesn’t change what your system is.
It changes how reliably it runs.

---

## 🔒 Lock this in

### 1️⃣ What is state in a service?

State is any information a service depends on that persists beyond a single request.

Examples:

* counters
* user sessions
* auth tokens
* in-progress jobs
* cached values
* configuration loaded at runtime

If losing it breaks correctness → it’s state.

---

### 2️⃣ Why stateless services scale better?

**Example: `/increment` API**

Each time you call the API, it returns how many times it has been called.
So on the 5th call, the response is `5`.

But this count is stored in the instance’s memory.

Because of that:

* You can’t route the request to another instance during high load, since a new instance starts with count `0`.
* You can’t restart the instance either, because the memory (and count) is lost.

So if the load increases or the instance has issues, you can’t scale or restart it
because the API depends on in-memory state that you can’t afford to lose.

We naturally touched all the right pain points with Stateful services:

* sticky routing
* inability to restart
* inability to add instances
* risk during crashes

This is exactly how real engineers understand statelessness.

One sentence summary:

Stateless services don’t care where a request goes — stateful ones do.

That single property unlocks:

* horizontal scaling
* safe restarts
* rolling deployments
* auto-scaling

---

### 3️⃣ Where should long-term state live?

Long-term state should live in a system whose job is to manage state reliably.

That can be:

* databases
* caches (Redis) — semi-state
* object storage
* message queues (for transient state)

But not inside your service memory.

---

Now that you understand state, the next natural questions are:

* How do services get configured?
* How do we run the same service in:

  * dev
  * staging
  * prod
* How do we package a service so it runs the same everywhere?

This leads us to:

👉 Configuration & Environment
👉 Containers (what they really solve)

Not Docker commands yet.
Concepts first.

---

## Step 10: Configuration (from scratch)

Question:

How does a service know:

* which DB to talk to?
* which port to listen on?
* which environment it’s in?

Hardcoding is bad:

```
db = connect("prod-db.internal")
```

Because:

* breaks local dev
* breaks testing
* dangerous for prod

So we externalize config.

Configuration = state too (important)

Config is:

* also state
* but not business data

Examples:

* DB URL
* credentials
* feature flags
* timeouts

Rule:

Code stays the same. Config changes per environment.

---

### How config is usually passed (conceptually)

Three main ways:

* Environment variables
* Config files
* Config services (advanced)

We’ll start with environment variables because they are universal.

Example:

```
DB_HOST=prod-db.internal
SERVICE_PORT=8080
```

Service reads:

```
os.getenv("DB_HOST")
```

Why env vars are loved:

* no code changes
* safe for containers
* easy to override
* standard across platforms

---

### 1️⃣ Why config should not be hardcoded

Code should not know which environment it is running in.
Environment should tell the code how to behave.

Hardcoding config causes:

* fragile deployments
* risky prod changes
* branching logic in code (if prod else test)
* mistakes that are hard to detect

External config avoids all of this.

---

### 2️⃣ Why config is “state” but not business data

Let’s lock the distinction clearly:

**Business data**

* belongs to users
* correctness-critical
* must be durable
* e.g. users, files, metadata

**Config**

* belongs to the service
* controls how the service runs
* not user-visible
* still persistent across requests

So your line:

“metadata which my customer don't need to care about”

is exactly right.

One-liner to remember:

Business state answers “what”, config answers “how”.

---

### 3️⃣ What happens if prod code uses wrong env vars

* prod service talking to test DB
* cross-environment data corruption
* “things get messy”

That’s not hypothetical — that’s how incidents happen.

This is why:

* env separation
* config discipline

are taken very seriously in real systems.

---

🚀 Now the next natural step: CONTAINERS (from first principles)

Everything you understand so far leads directly to this question:

If code is stateless
and config is external
how do we package and run this service consistently?

That’s where containers come in.

---

## 🧱 What is a Container? (no Docker yet)

Forget Docker commands.
Forget images.
Forget YAML.

Conceptually:

A container is a packaged environment that contains:

* your code
* runtime (Python, Java, etc.)
* libraries
* OS-level dependencies

So that:

Your service runs the same way everywhere.

---

### The problem containers solve (very important)

Before containers:

“Works on my machine”

* Different OS versions
* Different library versions
* Different Python/Java versions

This caused:

* bugs only in prod
* painful debugging
* manual setup per server

---

### Container mindset (this is the shift)

Instead of saying:

“Install Python 3.10, then install these libraries, then run this command”

You say:

“Here is a box that already has everything needed to run my service.”

That box = container image.

---

### How containers fit your mental model so far

| Concept        | Where it lives               |
| -------------- | ---------------------------- |
| Code           | inside container             |
| Runtime        | inside container             |
| Libraries      | inside container             |
| Config         | outside container (env vars) |
| Business state | outside container (DB)       |

This separation is intentional and powerful.

---

## 🔑 VERY IMPORTANT RULE (lock this in)

Containers should be immutable.
State should never live inside them.

If a container dies:

* you restart it
* nothing important is lost

Because:

* config is external
* state is external

---

## 🍱 Real-life analogy: Cooking & Restaurants

Scenario:

You want to open a restaurant chain.

You have:

* a recipe (your code)
* ingredients (libraries)
* cooking tools (runtime)
* kitchen setup (OS dependencies)

---

## 🧾 What Git is (important)

Git is just the recipe book.

It contains:

* instructions (code)
* steps (logic)

But:

* it does NOT include ingredients
* it does NOT include kitchen tools
* it does NOT guarantee the dish tastes the same everywhere

If I give you my recipe:

* your kitchen might not have the same oven
* ingredients might differ
* outcome changes

👉 Git alone cannot guarantee reproducibility.

---

## 🧱 What a Dockerfile is (this is the click)

A Dockerfile is the kitchen blueprint + recipe combined.

It answers:

“Exactly what kitchen, tools, and ingredients are needed to cook this dish?”

Real-life equivalent:

* type of stove
* exact oven temperature
* ingredient brands
* preparation steps

So instead of saying:

“Please install Python, install these libraries, set this up…”

You say:

“Here is the entire kitchen setup + recipe.”

That’s a Dockerfile.

---

## 🔑 Key feeling

Dockerfile = instructions to build an identical kitchen anywhere

This is something Git cannot do.

---

### ❓ What problem does Dockerfile solve that Git cannot?

👉 Git tracks source code.
Dockerfile defines the execution environment.

Without Dockerfile:

* “works on my machine” problem
* setup drift
* environment mismatch

With Dockerfile:

* reproducible runtime
* same behavior everywhere
* fewer production surprises

---

## 🧩 What is docker-compose? (new analogy)

You don’t run just ONE thing.

A real restaurant needs:

* kitchen
* storage
* delivery
* billing system

In software terms:

* API service
* Database
* Cache
* Background worker

Running them manually is painful.

---

### What docker-compose is

docker-compose is the restaurant opening plan.

It says:

* which kitchens exist
* how they talk to each other
* which ingredients/config each gets
* start everything together

Real-life:

“Open the kitchen, fridge room, billing desk, and delivery desk together.”

It’s coordination, not execution.

---

### Key difference (lock this in)

| Concept        | What it is                        |
| -------------- | --------------------------------- |
| Dockerfile     | How to build one service          |
| docker-compose | How to run many services together |

---

## 🧠 Back to software (now it clicks)

**Dockerfile** defines:

* runtime
* libraries
* how your service starts

Used in:

* dev
* staging
* prod

**docker-compose** defines:

* API service
* DB service
* Redis service

Mostly used for:

* local development
* testing
* integration environments

In production, orchestration is done by:

* Kubernetes
* ECS
* Nomad

…but the idea is the same.

---

## 🔒 Core system-design rule you just learned

Code + Runtime + Dependencies must be versioned together.
Configuration and state must stay outside.

That’s the entire container philosophy.

---

## 1️⃣ What is a Dockerfile really?

A Dockerfile is a reproducible recipe that defines the exact runtime environment required to run a service.

It specifies:

* base OS/runtime
* libraries & dependencies
* how the service starts

Very important nuance:

Dockerfile does not run the service.
It defines how to build something that can run the service.

Think:

* Dockerfile = blueprint
* Container = actual running instance built from that blueprint

---

## 2️⃣ When would you use docker-compose?

docker-compose is used to define and run multiple related services together in one environment.

It answers:

* Which services exist?
* How do they connect?
* What config does each service get?
* How do I start/stop everything together?

Important clarification:

Each service still has its own Dockerfile.

docker-compose does not replace Dockerfile.
docker-compose orchestrates services built from Dockerfiles.

Relationship:

* Dockerfile → how to build ONE service
* docker-compose → how to run MANY services together

---

## 3️⃣ Why should business data NEVER be inside a container?

Containers are disposable. Business data is not.

If business data lives inside a container:

* container restart = data loss
* scaling = inconsistent data
* rollback = corruption risk

This breaks:

* reliability
* availability
* safety

---

🚀 You’ve crossed an important line

At this point, you now understand the WHY behind:

* stateless services
* containers
* config separation
* orchestration

Now the next unavoidable questions are:

* How does a service start and listen for requests?
* How does traffic reach the container?
* How do services talk to each other?
* What happens when I run multiple instances?

This leads us to:

👉 Ports, Networking, and Service-to-Service Communication

---

## Step 11 — How a service is reachable (from scratch)

Very simple starting question:

If I have a service running in a container,
how does the outside world talk to it?

To answer that, we need to understand:

* ports
* networking
* load balancing (later)

---

### Quick mental model (no commands)

Inside a container:

* your service listens on a port (e.g. 8080)

Outside:

* requests come from clients
* something must route traffic to that port

Mapping:

Client → Port → Service

---

### 1️⃣ What does it mean for a service to “listen on a port”?

Correct mental model:

“My process has opened a socket on this port and is waiting for incoming network connections.”

So in:

```
@app.get("/files")
```

* `/files` is application-level routing
* Port (e.g. 8080) is network-level routing

Full picture:

Client → IP + PORT → Service process → /files handler

---

### 2️⃣ Why can two containers both listen on port 8080 without conflict?

❌ Not because of GET vs POST
HTTP methods have nothing to do with ports.

✅ The real reason:

Each container has its own network namespace.

That means:

* Each container has its own IP address
* Ports are scoped per IP

Valid:

```
Container A: 172.17.0.2:8080
Container B: 172.17.0.3:8080
```

No conflict because:

(IP, PORT) pair is unique.

---

### 🔑 Lock this in

Ports belong to an IP, not globally to the machine.

---

### 3️⃣ Why do we need something outside the container to route traffic?

Containers are:

* ephemeral
* scaled up/down
* replaced during deploys

Direct container access breaks clients.

Solution: external routing layer.

```
Client
  ↓
Load Balancer / Gateway
  ↓
Containers
```

Senior-level one-liner:

Clients should never depend on individual service instances — only on stable endpoints.

---

### Putting it all together

* Service listens on a port
* Container has its own IP
* External router/load balancer routes traffic

This is the backbone of cloud services.

---

## 🚦 NEXT NATURAL STEP: LOAD BALANCERS (FROM FIRST PRINCIPLES)

Why load balancers exist:

* many containers
* stateless services
* freedom to restart, scale, deploy

Clients want:

* one stable endpoint
* no failures

So we insert a middleman.

```
Client
  ↓
Load Balancer
  ↓
Service Instances
```

---

### What a Load Balancer REALLY is

A load balancer is:

* a network component that receives requests
* forwards them to one of many backends

It:

* does NOT store business data
* does NOT understand business logic

---

### Core responsibilities

1️⃣ Stable entry point
2️⃣ Health checks
3️⃣ Traffic distribution
4️⃣ Failure isolation

---

### Load balancer + stateless services

Because services are stateless:

* any request can go anywhere
* retries are safe
* scaling is easy

---

### Where load balancers live

* Outside containers
* Managed or software-based

---

### What load balancers are NOT

They are NOT:

* databases
* caches
* queues

---

### 🔒 Lock-in rule

Load balancers work best when they can be dumb.
Stateless services allow that.

---

## 🧩 Full picture (final)

```
Client
  ↓
DNS
  ↓
Load Balancer
  ↓
Stateless Service Containers
  ↓
Database / Cache / Storage
```

Properties:

* containers can die → OK
* traffic spikes → OK
* deploy new version → OK
* failures isolated → OK

This is the minimum viable cloud architecture.

Everything else in system design builds on this.
