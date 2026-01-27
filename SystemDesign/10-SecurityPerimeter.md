# 🛡️ WAF (Web Application Firewall) — From First Principles

## The core problem a WAF solves

Your public API is exposed to the internet. That means you’ll see:
- normal users
- bots
- scanners
- attackers
- accidental abuse

A WAF exists to stop common web attacks and bad traffic **before** they reach your services.

Think of it as:
- a security filter sitting at the edge, inspecting HTTP requests

---

## Where a WAF sits in the architecture

Typical placement:
```
Client
↓
CDN (optional)
↓
WAF
↓
API Gateway / Load Balancer
↓
Services
```

Sometimes WAF is integrated into:
- the CDN (edge WAF)
- the gateway (gateway WAF)
- the load balancer (LB-attached WAF)

But conceptually, it’s **at the edge**.

---

## What a WAF actually does

A WAF inspects:
- URL path
- query params
- headers
- body (often limited)
- rate / patterns
- IP reputation

And then enforces rules:
- allow
- block
- challenge (captcha)
- log
- throttle

---

## What a WAF protects against (important list)

These are classic web attack patterns.

---

### 1️⃣ SQL injection attempts

Example:
```
GET /search?q=' OR 1=1 --
```
WAF blocks based on known signatures and patterns.

---

### 2️⃣ XSS (script injection)

Example:
```
<script>alert(1)</script>
```
---

### 3️⃣ Path traversal

Example:
```
GET /download?file=../../etc/passwd
```
---

### 4️⃣ Bot / scraping / credential stuffing

- repeated login attempts
- rotating IPs
- aggressive scraping

---

### 5️⃣ Protocol abuse / malformed requests

- huge headers
- weird encodings
- invalid content types

---

## WAF vs Rate Limiting (common confusion)

### Rate limiting
- about fairness & protecting capacity
- “this user can only do X requests per minute”

### WAF
- about blocking malicious patterns
- “this request looks like an attack”

You usually use both:
- WAF blocks obviously malicious traffic
- rate limiting protects from heavy legitimate-ish traffic

---

## WAF vs API Gateway Auth (another confusion)

Auth checks:
- “are you allowed?”

WAF checks:
- “is this request suspicious or malicious?”

Even authorized users can:
- send malicious input
- be compromised

So WAF still matters.

---

## Real-world examples (to feel it)

### Example A: Stop credential stuffing

Attack:
- 100k login attempts from rotating IPs

WAF rules:
- bot detection
- IP reputation
- geo-blocking (if appropriate)
- request fingerprinting

---

### Example B: Block scanning

Attack:
- requesting random paths:
  - /wp-admin
  - /phpmyadmin
  - /actuator

WAF:
- blocks known scanner patterns

---

## What a WAF does NOT solve

A WAF is not magic.

It does NOT replace:
- input validation in your app
- authentication
- authorization
- secure coding
- parameterized SQL

Think:
- WAF reduces noise and blocks common attacks
- your app must still be secure

---

## WAF “rules” — the only 2 types you need to know

### 1️⃣ Managed rules
- prebuilt
- block common known patterns
- good baseline
- most companies start here

---

### 2️⃣ Custom rules
Your own logic, for example:
- block a specific path
- block certain payload lengths
- allow only from certain IPs for admin endpoints

---

## How to talk about WAF in system design

A strong SDE2 explanation:

> “For public APIs, we use WAF at the edge (often integrated with CDN or gateway) with managed OWASP rules and a few custom rules for our endpoints. It blocks common injection and bot patterns before traffic reaches our services, and pairs with rate limiting to protect capacity.”

That’s enough.

---

## 1️⃣ Why still WAF if you already have auth + rate limiting?

Authentication and rate limiting control:
- who
- how much

WAF controls:
- what the request looks like

Even:
- authenticated users
- within rate limits

can send:
- SQL injection payloads
- XSS
- malformed requests
- bot-driven abuse

WAF filters request shape, not identity.

---

## 2️⃣ Example of request WAF blocks

Examples you can say confidently:
```
GET /search?q=' OR 1=1 --
```
or
```
POST /login
{ "username": "admin", "password": "' OR '1'='1" }
```

WAF blocks these before they ever hit your app.

---

## 3️⃣ Where to place WAF?

At the edge, in front of the gateway.

Reason:
> WAF should block malicious traffic as early as possible to reduce load and attack surface for downstream systems

That’s why WAF is often:
- integrated with CDN
- or attached to API Gateway at the edge

---

## ✅ WAF — CLOSED

You now understand:
- what WAF does
- what it doesn’t do
- how it complements auth & rate limiting
- where it sits in architecture

---

# 🔐 Secrets Management — From First Principles

## The real problem secrets management solves

Your service needs secrets:
- DB password
- Redis password
- API keys
- JWT signing keys
- OAuth client secrets

Naively, people put them in:
- source code ❌
- git ❌
- config files ❌
- Docker images ❌

Once leaked:
- attackers get full access
- rotation is painful
- audit is hard

---

## What is a “secret” really?

Any value that grants access if known.

Not just passwords:
- tokens
- private keys
- certificates
- encryption keys

---

## What secrets management aims to guarantee

- Secrets are not in code
- Secrets can be rotated
- Access to secrets is controlled
- Secrets are auditable
- Secrets are injected at runtime

---

## The simplest correct baseline

### Environment variables

Examples:
- `DB_PASSWORD`
- `REDIS_PASSWORD`
- `JWT_PRIVATE_KEY`

Why env vars are good:
- not in code
- easy to override per environment
- supported everywhere

But env vars alone have limits.

---

## The problem with env vars alone

- hard to rotate automatically
- visible to any process with access
- often copied into logs accidentally
- not encrypted at rest by default

So at scale, teams use secret stores.

---

## Secret stores (conceptually)

Examples:
- AWS Secrets Manager
- HashiCorp Vault
- Kubernetes Secrets

Conceptually, they all:
- store secrets encrypted
- control who can read them
- log access
- support rotation

---

## How services actually get secrets (flow)

- Service starts
- Authenticates to secret store (machine identity)
- Fetches secrets
- Keeps them in memory
- Periodically refreshes or reloads

Secrets never touch:
- git
- docker image
- logs

---

## Why rotation matters (feel it)

Imagine:
- DB password leaked
- attacker connects

If you can rotate:
- generate new password
- update DB
- update secret store
- services reload

You recover.

If not:
- redeploy everything
- downtime
- panic

---

## Secret rotation vs key rotation (connect the dots)

- JWT key rotation → rotate signing keys
- API key rotation → replace keys
- DB credential rotation → change passwords

All are forms of secrets rotation.

---

## What not to do (interview red flags)

❌ “We store secrets in config files”
❌ “We commit .env files”
❌ “Secrets are baked into Docker image”

Correct answer:
- “Secrets are injected at runtime from a secure store.”

---

## One-line mental model 🔒

Secrets should be stored centrally, injected at runtime, and rotated safely.

---

## 1️⃣ Why is storing secrets in code dangerous even for private repos?

Because in real life:
- repos get cloned to laptops
- access permissions drift over time
- contractors / ex-employees retain copies
- CI logs sometimes print env or config
- backups exist forever
- code gets forked or shared accidentally

Once a secret is in git:
- assume it is compromised forever
- deleting it later doesn’t help (history exists)

🔒 Rule
> Anything committed to git should be treated as public.

---

## 2️⃣ Why is rotation a core requirement, not a nice-to-have?

Secrets will leak. Rotation limits the blast radius.

Without rotation:
- one leak = permanent compromise
- attacker has unlimited time

With rotation:
- leak window is bounded
- damage is contained
- recovery is possible without redeploying everything

> 🔒 Security is not about preventing leaks; it’s about surviving them.

---

## 3️⃣ Where should secrets live relative to Docker images?

Docker images must be secret-free.

Secrets are injected at runtime via:
- environment variables (simple)
- mounted files
- fetched from a secret store (best)

Docker images should be:
- build-once
- run-anywhere
- secret-less

---

## ✅ Secrets Management — CLOSED

You now understand:
- what secrets are
- why env vars are a baseline
- why secret stores exist
- why rotation matters
- how secrets relate to containers

This completes the Security Perimeter part.

---