# Authentication vs Authorization (lock this)

## Authentication (AuthN)

**Who are you?**

Examples:
- “This is user U123”
- “This is service A”
- “This is an anonymous user”

## Authorization (AuthZ)

**What are you allowed to do?**

Examples:
- “User U123 can read event E1”
- “Service A can update metadata”
- “User cannot delete event”

## One-liner to remember

Authentication establishes identity.
Authorization enforces permissions.

---

## 2️⃣ Where should identity be verified: Gateway or Service?

The correct real-world answer is:

**Authenticate at the API Gateway, authorize in the service.**

Let’s explain why.

### Why authenticate at the API Gateway

Authentication is:
- expensive (crypto, token parsing)
- repetitive (every request)
- identical across services

So doing it once at the gateway:
- avoids duplication
- reduces load on services
- gives consistent behavior

Gateway verifies:
- token is valid
- token not expired
- token signed by trusted issuer

Then it forwards:
- identity context to services

Example headers:
- X-User-Id: U123
- X-Scopes: events:read,metadata:read

### Why authorization must still happen in the service

Authorization depends on:
- business rules
- data ownership
- domain logic

Example:
- “User U123 can read event E1 but not E2”

The gateway cannot know this, because:
- it doesn’t know your DB
- it shouldn’t embed business logic

So:
- Gateway authenticates
- Service authorizes

### What happens if you only authorize at gateway?

- Security bugs
- Over-permissive access
- Hard-to-change policies

### What happens if you only authenticate in service?

- Repeated crypto work
- Inconsistent behavior
- Poor performance

### Lock this rule 🔒

Gateway answers “who are you?”
Service answers “are you allowed?”

---

## 3️⃣ API Keys vs JWTs — from first principles

## API Keys (simplest form)

### What is it?

A random string:
- X-API-Key: abc123

### What it means

“If you have this key, you’re trusted.”

### Pros
- Simple
- Easy to generate
- Easy to revoke

### Cons
- No embedded identity
- No expiry (unless managed separately)
- Must be checked against DB or cache
- Weak if leaked

### Use cases
- Internal services
- Low-risk APIs
- Server-to-server access

---

## JWT (JSON Web Token)

### What is it?

A signed blob containing claims:
```
{
"sub": "U123"
"scopes": ["metadata:read"]
"exp": 1700000000
}
```
Signed by:
- auth service
- identity provider

### What it means

“This identity was verified, and here are its permissions.”

### Pros
- Self-contained
- No DB lookup required to validate
- Has expiry
- Can carry roles/scopes

### Cons
- Harder to revoke immediately
- Larger payload
- Requires key rotation

### Use cases
- User-facing APIs
- Multi-service systems
- OAuth-based auth

---

## One-liner comparison (remember this)

API key = “password for an app”
JWT = “verifiable identity card with permissions”

### Why JWTs are often stronger
- Include identity + claims
- Expire automatically
- Can be verified cryptographically
- Scale better (no DB lookup per request)

But API keys are still valid in many contexts.

---

## If Service A calls Service B on behalf of a user, should Service A forward the user’s JWT to Service B? Why or why not?

### Why forwarding user JWTs is dangerous in practice

### 🔴 Problem 1: Token scope leakage

User JWTs often contain:
- broad scopes
- long-lived permissions
- access intended only for public-facing APIs

If Service B trusts that JWT:
- any internal service holding it can impersonate the user
- blast radius increases dramatically

You lose least privilege.

---

### 🔴 Problem 2: Trust boundary violation

User JWTs are issued for:
- client → gateway
- client → API

They are not issued for internal service-to-service trust.

If Service B accepts user JWTs:
- it must understand user auth logic
- rotate public keys
- validate token audience
- enforce expiry
- handle revocation

Now every service becomes an auth service ❌

---

### 🔴 Problem 3: Auditing & accountability

If Service B sees a user JWT:
- did the user call B directly?
- or did Service A call B?

You lose clarity.

---

## ✅ The correct real-world pattern

Service A authenticates the user.
Service A calls Service B as itself, and passes user context explicitly.

So instead of:
```
Service A → Service B
Authorization: Bearer <user_jwt>
```
You do:
```
Service A → Service B
Authorization: Bearer <service_A_token>
X-User-Id: U123
X-User-Scopes: metadata:read
```
Now:
- Service B authenticates Service A
- Service B authorizes based on:
  - service identity
  - user context passed explicitly

This is called delegation, not impersonation.

---

## 🔒 Lock this rule (very important)

> User identity is authenticated at the edge. Internal services authenticate each other using service credentials.

Or even simpler:

> User tokens stop at the gateway.

---

## When is forwarding user JWT acceptable?

Only in very limited cases:
- tightly coupled services
- same trust boundary
- same auth domain
- explicitly designed for it

But as a default mental model: don’t forward user JWTs.

---

## OAuth from First Principles — Deep, Combined Explanation (lock this)

## What is OAuth? (and “Sign in with Google”)

Let’s strip this down to first principles.

---

## The real problem OAuth solves

You want:
- User to prove identity
- Without sharing password
- With limited access
- Across different apps

Example:
- “Canva wants to know who you are, but should not know your Google password.”

---

## Actors in OAuth

There are always four parties:
- User (you)
- Client App (Canva)
- Authorization Server (Google)
- Resource Server (Google APIs)

---

## What happens when you click “Sign in with Google”

Let’s walk the flow slowly, end to end, with the *why* behind every step.

---

## Step 1: Redirect to Google (Authorization Request)

Canva redirects you to Google with:
- client_id (Canva’s ID)
- requested scopes (profile, email)
- redirect URL
- response_type=code

Meaning:
- “Google, can you authenticate this user and tell me who they are?”
- “And ask them if they consent to sharing this data with me.”

📌 Important:
- Canva is NOT asking for a token yet.
- It is asking for an authorization decision.

---

## Step 2: User authenticates at Google

Now:
- You enter password / biometrics
- Canva never sees this

Google confirms:
- “Yes, this is user ```alice@gmail.com```”

Then Google asks:
- “Can Canva access your profile and email?”

You click Allow.

📌 Up to now:
- Canva has nothing
- Google only knows the user authenticated and consented

---

## Step 3: Google gives Canva an Authorization Code

Google redirects your browser back to Canva:

```https://canva.com/callback?code=abc123```

This is a temporary one-time code.

### What is this “authorization code”?

The authorization code is:
- NOT a token
- NOT a JWT
- NOT usable to call Google APIs

It is simply:
- Proof that the user authenticated and consented

Think of it as:
- “User approved. Canva is allowed to ask for tokens.”

### Why not send tokens directly here?

Because:
- This redirect goes through the browser
- URLs can be logged
- URLs can leak via referrers
- URLs can be intercepted

So Google sends a temporary, useless-by-itself code instead.

📌 Key properties:
- short-lived
- single-use
- meaningless without Canva’s secret

---

## Step 4: Canva exchanges the code for tokens (SERVER TO SERVER)

Now Canva’s backend does this:

POST ```https://oauth2.googleapis.com/token```

With:
- code = abc123
- client_id = canva_id
- client_secret = canva_secret

📌 This is server-to-server:
- No browser
- No user
- Secure channel

Now Google can verify:
- The code is valid
- The code was issued to this Canva
- Canva knows the secret (proof of identity)

This solves:
- “Is the user really the user?”
- “Is the app really Canva?”

At the same time:
- User password never reaches Canva
- Tokens never travel through the browser

---

## Step 5: Google sends TOKENS to Canva

Google returns:

### 1️⃣ ID Token (JWT) — Identity proof

This answers:
- Who is the user?

Example:
- sub: user ID
- email
- issuer
- audience
- expiry

This token is:
- cryptographically signed
- verifiable by Canva
- proof of identity

Canva uses this to:
- trust Google’s identity assertion
- log you in
- create or find your user account
- create its own session / JWT

📌 Canva does NOT use Google tokens for internal authentication.

---

### 2️⃣ Access Token — Permission token

This answers:
- What can Canva do on behalf of the user at Google?

Used to call Google APIs:
- Authorization: Bearer <access_token>

Canva uses this token to:
- fetch profile info
- fetch email
- fetch other allowed data

📌 This token is scoped, limited, and short-lived.

---

### 3️⃣ (Optional) Refresh Token

Used to:
- get new access tokens
- without asking the user to log in again

Stored securely:
- server-side only

---

## The roles summarized cleanly

| Thing | What it is | Who uses it | Purpose |
| ----- | ---------- | ------------| --------|
| Authorization Code | One-time proof | Canva backend | Exchange for tokens |
| ID Token (JWT) | Identity proof | Canva | Log user in |
| Access Token | Permission token | Canva → Google APIs | Fetch user data |
| Refresh Token | Long-lived token | Canva backend | Renew access |

---

### OAuth must guarantee ALL of this at once:

- The user is really you
- The app is really Canva
- The password never leaves Google
- Tokens don’t leak via URLs
- Access is limited
- Access is revocable

This is why OAuth has **two steps**, not one.

---

## Why OAuth MUST have two steps (core insight 🔑)

If Google sent tokens directly in the redirect:
- tokens would appear in URLs
- tokens would be logged
- tokens could be stolen

So:
- Authorization Code travels via browser
- Tokens travel via backend only

This separation is the entire point of OAuth.

---

## What Canva actually does with each thing

### Authorization Code
- Immediately exchanges it
- Discards it forever

### ID Token
- Validates signature
- Extracts user identity
- Creates Canva session / JWT

### Access Token
- Calls Google APIs
- Fetches profile/email
- May discard after use

### Refresh Token
- Stored securely (server-side)
- Used to refresh access tokens

---

## 🔑 Key insight about OAuth

OAuth is not “login”.
OAuth is delegated authorization.

Login is just a common use case.

---

## Why OAuth matters for system design

Because:
- tokens have scopes
- tokens expire
- trust is delegated
- auth is centralized

This is why modern systems use:
- OAuth
- OpenID Connect (OIDC)

---

## One-sentence mental model (lock this 🔒)

Authorization Code = permission receipt
Token = actual access

Or even simpler:

Code proves consent.
Token grants access.

---

## SAML — Just Enough to Understand It

## What problem SAML solves

Same core problem as OAuth:
- Single Sign-On (SSO) across organizations

Example:
- You work at Company A
- You access Tool B (Jira, Confluence, Workday)
- You don’t want separate passwords

---

## The core idea (strip it down)

SAML lets one system assert a user’s identity to another system using signed XML.

That’s it.

---

## The players (3 things only)

- User (Browser)

- Identity Provider (IdP)
  → company login system (Okta, Azure AD, ADFS)

- Service Provider (SP)
  → app you’re trying to access (Jira, Salesforce)

---

## High-level flow (feel it)

- User tries to access Service Provider
- SP says: “I don’t know who you are — go to your IdP”
- User authenticates at IdP
- IdP sends back a SAML Assertion (signed XML) via browser
- SP verifies signature and logs user in

---

## What is a SAML Assertion?

It’s a signed statement that says:

- “This user (alice@company.com) authenticated successfully at time T
  and has these attributes.”

Properties:
- Digitally signed
- Short-lived
- Cannot be forged

---

## Why SAML feels painful

- XML (verbose)
- Browser redirects + POSTs
- Hard to debug
- Less flexible than OAuth/JWT

But it’s:
- very secure
- very standardized
- deeply entrenched in enterprises

---

## SAML vs OAuth (quick comparison)

Aspect | SAML | OAuth / OIDC
- Format | XML | JSON / JWT
- Transport | Browser redirects | Browser + API
- Typical use | Enterprise SSO | Web + mobile + APIs
- Flexibility | Low | High
- Popular today | Legacy / Enterprise | Modern default

---

## One-liner to remember

SAML = enterprise SSO with signed XML assertions.

That’s enough. You’ll recognize it if it comes up, and you won’t be scared.

---

## Service-to-Service Authentication (lock this)

## The real problem

You have:

Service A → Service B → Service C

No user involved.

Questions:
- How does B know the caller is really A?
- How does B know A is allowed to call this endpoint?
- How do we rotate credentials safely?

---

## What service-to-service auth is NOT

❌ User JWT forwarding
❌ Hardcoded passwords
❌ Long-lived API keys in config files

---

## The 3 real patterns (you must know these)

We’ll go in increasing maturity.

---

## 1️⃣ API Keys (baseline, weakest)

### How it works

Service A sends:
- Authorization: ApiKey abc123

Service B:
- looks up key
- checks permissions

### Pros
- Simple
- Easy to implement

### Cons
- Long-lived secrets
- Hard to rotate
- If leaked → bad day

### When acceptable
- Low risk
- Internal tools
- Temporary systems

---

## 2️⃣ Service JWTs (most common modern pattern)

### How it works

- Each service has an identity
- An auth system issues short-lived JWTs for services

Service A sends:
- Authorization: Bearer <service_A_jwt>

JWT claims:
- iss: auth.internal
- sub: service-A
- aud: service-B
- exp: …

Service B:
- verifies signature
- checks audience
- authorizes based on service identity

### Pros
- Short-lived
- No DB lookup
- Scales well
- Clear identity

### Cons
- Need auth infrastructure
- Key rotation needed

This is the default choice in many modern systems.

---

## 3️⃣ Mutual TLS (mTLS) — strongest, infra-heavy

### How it works

- Each service has a client certificate
- TLS handshake proves identity
- No tokens in headers

Service B trusts:
- “Only services with valid certs can connect”

### Pros
- Very strong security
- Identity verified at network level
- No token handling in app

### Cons
- Operationally complex
- Cert rotation, trust stores
- Needs strong infra support

Used in:
- high-security environments
- service meshes (Istio, Linkerd)

---

## How authorization works for services

Authentication answers:
- “Who is calling?”

Authorization answers:
- “Is this service allowed to call this endpoint?”

Example:
- Service A → allowed to READ metadata
- Service C → allowed to WRITE metadata

This logic usually lives:
- in the service
- sometimes partially in the gateway

---

## The correct mental model (lock this 🔒)

Users authenticate at the edge.
Services authenticate to each other internally.
Never mix the two.

---

## Putting it all together (big picture)

User
↓
CDN
↓
API Gateway (auth user)
↓
Service A (authorize user)
↓
Service B (auth service A, authorize action)

Each hop has:
- its own identity
- its own trust boundary

---

## Final one-sentence takeaway

OAuth / SAML are about users.
Service-to-service auth is about machines proving who they are.

---

# JWT key rotation — what key are we rotating?

In this JWT:

- iss: auth.internal
- sub: service-A
- aud: service-B
- exp: 1700000000

👉 This JSON is NOT the key.
The key is used to SIGN this JWT, not inside it.

---

## What actually signs a JWT

When the auth service issues a JWT:

JWT = sign(payload, SIGNING_KEY)

The JWT looks like:
- header.payload.signature

The signature is created using the signing key.

Service B verifies the JWT by:
- recomputing the signature
- checking it matches

---

## So what key are we rotating?

👉 The JWT signing key (private key / secret) used by the auth service.

---

## Two common signing setups

### 🔹 Symmetric signing (HS256)

- One shared secret
- Auth service signs
- Services verify with same secret

SIGNING_KEY = "abc123"

---

### 🔹 Asymmetric signing (RS256) — most common

- Auth service has private key
- Services have public key

Private key → signs
Public key → verifies

---

## What does “key rotation” mean?

Changing the signing key periodically **without breaking the system**.

Why:
- Keys can leak
- Keys can be compromised
- Security best practice

---

## Small concrete JWT rotation example (RS256)

### Before rotation

Auth service uses:
- PrivateKey_v1
- PublicKey_v1

Service B trusts:
- PublicKey_v1

JWTs signed with v1 are valid.

---

### During rotation (important part)

Auth service now has:
- PrivateKey_v1 (old)
- PrivateKey_v2 (new)

It publishes:
- PublicKey_v1
- PublicKey_v2

Service B:
- accepts JWTs signed with either key
- checks JWT header kid

JWT header example:
- alg: RS256
- kid: key-v2

Now:
- new tokens use v2
- old tokens (not expired) use v1
- everything keeps working

---

### After rotation completes

- Old tokens expire naturally
- Auth service removes v1
- Services remove PublicKey_v1

✅ Zero downtime
✅ No forced logout
✅ Secure

---

## Why this matters in real life

If you don’t rotate keys:
- leaked key = full system compromise
- attackers mint valid JWTs
- every service trusts them

That’s catastrophic.

---

## One-liner to remember 🔒

JWT key rotation = rotating the signing keys, not the token contents.

---

# API key rotation — what is rotated and why it’s hard

API keys are usually:
- stored in DB or secret store
- looked up on each request (or cached)

Example table:
- key
- service_name
- permissions
- status

---

## What does “rotate an API key” mean?

Replace an old key with a new one without breaking clients.

---

## Why API key rotation is hard

### 🔴 Problem 1: Long-lived secrets

API keys usually:
- never expire automatically
- are hardcoded in configs
- live in many places

Rotation means:
- generate new key
- update every client
- deploy everywhere
- revoke old key later

---

### 🔴 Problem 2: No self-describing identity

API keys are just random strings.

They don’t contain:
- expiry
- audience
- issuer

So:
- DB lookup every time
- manual revocation

---

### 🔴 Problem 3: Revocation is painful

If a key leaks:
- disable it immediately
- clients break instantly
- no graceful transition

---

## JWTs solve these problems

JWTs:
- expire automatically
- are short-lived
- don’t require DB lookup
- can coexist during rotation

That’s why JWTs scale better for service-to-service auth.

---

## Small API key rotation example (feel the pain)

Service A uses:
- API_KEY = key_v1

Rotation:
- Create key_v2
- Deploy Service A with key_v2
- Wait until all instances updated
- Disable key_v1

If deployment is partial:
- some instances break
- some still work
- debugging pain

---

## One-liner to remember 🔒

API keys are easy to start with, hard to rotate safely.
JWTs are harder to set up, easier to operate at scale.

---

## Final comparison (lock this in)

Aspect | API Keys | JWTs
- Stored in DB | Yes | No
- Self-contained | No | Yes
- Expiry | Manual | Built-in
- Rotation | Hard | Smooth
- Scale | Limited | Excellent
- Best for | Simple internal | Modern systems

---

You now understand:
- what keys are
- what rotation means
- why security systems are designed this way
