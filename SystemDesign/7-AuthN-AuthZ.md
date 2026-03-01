# 🫆 Authentication vs Authorization (from ZERO)

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

> Authentication establishes identity. Authorization enforces permissions.

---

## Where should identity be verified: Gateway or Service?

The correct real-world answer is:

**Authenticate at the API Gateway, authorize in the service.**

Why?

### Real-life Analogy - Entering an Office

- You show your ID at the main entrance, where security/reception verifies who you are, with some protocols.
- Once inside, you don’t re-verify your identity at every floor/department — that would be redundant, and each department doesn’t need to know and handle all the AuthN protocols performed at the reception.
- Being inside the building means you’re **authenticated**.
However, you may not have access to every room — that’s **authorization**.

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
- `X-User-Id`: U123
- `X-Scopes`: `events:read`,`metadata:read`

---

## Why authorization must still happen in the service

- Developers can't access "only staff" rooms. Reception lets both inside but can't know who can access what.
- Access is controlled at departments - Authorization

**Authorization depends on:**
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

**What happens if you only authorize at gateway?**

- Security bugs
- Over-permissive access
- Hard-to-change policies

**What happens if you only authenticate in service?**

- Repeated crypto work
- Inconsistent behavior
- Poor performance

### Lock this rule 🔒

> Gateway answers “who are you?” Service answers “are you allowed?”

---

## Basic Cryptography

### Symmetric encryption

The same secret key is used to encrypt and decrypt data.
```
Plaintext --(Secret Key)--> Ciphertext
Ciphertext --(Same Secret Key)--> Plaintext
```

**Properties**

- Very fast
- Efficient for large data
- Requires secure key sharing

---

### Asymmetric Encryption (Public-Key Cryptography)

Uses two keys:

- Public key → shared openly
- Private key → kept secret

> Encrypt with Public Key → Decrypt with Private Key

**Properties**

- Solves key distribution problem
- Slower than symmetric encryption
- Used for identity and secure key exchange

---

### Hashing

One-way transformation of data into fixed-length output.

```
password → SHA256 → 5e88489...
```

**Properties**

- Not reversible
- Deterministic (same input → same hash)
- Small input change → completely different output

**Used For**

- Password storage
- Data integrity checks
- Digital signatures (hash first, then sign)

---

### Digital Signatures

**Digital signatures use asymmetric cryptography to ensure:**

- Authenticity (who sent it)
- Integrity (data not altered)

**How it Works**

Sender:

- `sign(message, private_key)`:
  - Hashes the message
  - Encrypts the hash using private key → Signature

Receiver:

- Decrypt signature using sender’s public key
- Hash received message
- Compare both hashes
- If equal → valid signature else message is tampered.

---

### How Symmetric and Asymmetric Work Together

- Asymmetric encryption is secure but slow.
- Symmetric encryption is fast but needs secure key exchange.

So real systems combine both with signatures.

Sender:
- Generates symmetric encryption key and encrypts the data
- Encrypts the symmetric key with receiver's public key (Output A)
- Hashes the outut A and encrypts with his private key → Signature
- Sends Output A with signature attached.

Receiver:
- Recives the Output A with signature
- Decrypts the signature with sender's public key → Hash obtained
- Computes Hash of Output A
- If computed and obtained Hash is equal → integrity validated(Output A not tampered)
- Decrypts Output A with his private key → Symmetric key obtained
- Decrypts the data with obtained symmetric key.

Attacker:
- Cannot decrypt Output A(does't have receiver's private key)
- Cannot modify Output A(Output A) ❌ → Hash changes, integrity fails
- Cannot generate signature (does't have sender's private key) ❌

---

### Encoding Vs Encryption

**Encoding**

- Converts data into a different format
- Anyone can decode without a key
- No security

Example:
```
"hello" → Base64 → aGVsbG8=
```

Used for:

- Data transmission formatting
- URLs
- JSON transport

**Encryption**

- Transforms data to keep it secret
- Requires a key to decrypt

Example:
```
"hello" → Encrypted using AES → unreadable ciphertext
```

Used for:

- Secure communication
- Protecting sensitive data

---

## 1. What Is a Token (General Security Meaning)?

### In security terminology:

> A token is a credential or artifact that represents some state, identity, or authority and is to be presented to enable or influence access or behavior.

### When Do We Call Something a Token? (Key idea)?:

- It is issued by someone/authority.
- It represents something (like an identiy or authorization).
- It is meant to be presented.
- It has lifecycle (expiry, scope).
- It may be short-lived.
- It can be verified.

### Analogy - Passport can act as a token:
- It represents my authority and identiy
- Issued by trusted entity(government)
- Verified by my signature
- Presented at Airport to get access.

### Examples (We'll dive into below deeper):

- Session token (represents session)
- CSRF token (prevents CSRF)
- Access token (grants access to protected resource)
- Refresh token (grants new access token)
- ID token (represents identity)
- Password reset token
- OAuth token
- Auth token
- JWT
- Bearer token

These are issued dynamically.

---

## 2. What Is a Key?

### A key is typically:

> A secret/password used to create/verify trust or encrypt/verify data.

### Analogy:
- My signature on passport is kinda key, it proves my identity on passport. Without it, my identity or details on passport can't be trusted or passport(token) not valid.
- Signature is valuable, you don't sign everything randomly

### We usually call something a key when:

- Secrets and Stored securely
- Long-lived
- Not meant to be passed around casually
- Used to create or verify tokens
- It is not derived from a delegation flow.

### Examples:

- RSA private key signs JWT
- HMAC secret signs JWT
- Encryption key

---

## 3. The Conceptual Difference - Key Vs Token

### 🔐 Key

> Used to create or verify trust.

### 🎫 Token

> Used to present proof of trust.

### The Cleanest Mental Model

Keys

- Cryptographic keys
- Used to sign/verify
- Used to encrypt/decrypt
- Long-lived
- Secret

Tokens

- Issued artifacts
- Represent identity or authority
- Meant to be presented
- Often short-lived
- Verified using keys

**In most modern systems:**

> Keys create trust. Tokens carry trust.

That’s the clean separation.

However:
- Across different credentials, the line of key vs token is blurred a bit.
- The credential should be called a key or token based on the main purpose it serves.

Example:

Refresh token:
- A credential that allows a client to obtain a new access token.
- If valid → you get a new access token.

Why is it a token?:
- It is a credential
- It represents authority
  - Authority to obtain new access tokens.
- It is presented to a system
  - It is sent to the authorization server.
It influences behavior
  - If valid → system issues new access token.

That fits the general definition of token.

Refresh token checks few boxes of a key too:

- Long-lived
- Stored securely
- Cannot be leaked
- Highly sensitive
- If stolen → attacker can mint new access tokens.

> But its main purpose to represent authority to get new token, not create/verify trust or encrypt data, hence token

Similary ID token:
- does not grant to resources
- but represents identity of user or service
- meant to presented, and influences beahavior
  - App logs the user in
  - creates the session etc.
- issued by auth service

This satisfies the definition of token.

---

## 4. API Keys

Its behaviour is closer to a token(Access token), but its still called a key.

### What is it?
- A random string
- `X-API-Key`: abc123
- No embedded identity encoded, just a random string

### What it represents:
- It identifies an application, Not a user (usually)
- "This request is from Application X.”

### Client-side:
-  Adds below in the request header
- `Authorization: Bearer <API key>`

### Server-side (API Service):
- Receives the request, and looks up API key in DB
- `api_key → (account_id, scopes, rate_limit, status, expiry etc.)`
- If key not existing, immediately reject request
- If existing, calling app is valid and identified from the DB record.

### What it means:
- If you have this key, you’re trusted and can access the resource(API usually)
- You issue an API key to Application A so it can access your APIs.
- Anyone trying to impersonate Application A would need that key — which is why API keys are secrets and must never be exposed.

> In short, when an API key is presented, it’s verified and grants access to the resource. So it technically acts like a token, but it’s historically called a “key” because of its properties.

### Properties
- Long-lived
- secret
- Static
- Manually issued
- It is not derived dynamically from another trust chain
- It identifies an application

### Pros:
- Simple
- Easy to generate
- Easy to revoke(Just delete API key from DB)
- Used for rate limiting & Billing
- Bearer-style (possession = authority)

### Cons
- No embedded identity
- No expiry (unless managed separately)
- Must be checked against DB or cache
- if leaked → High risk as long lived.

### Use cases
- Internal services
- Low-risk APIs
- Server-to-server access

---

## 5. What Is a “Claim”?

### In security terminology:

A claim is a statement about an entity.

That’s it.

**A claim is just:**

> Some information asserted about something.

### Simple Examples of Claims

If I say:

- “Alex’s user id is 123” → that’s a claim
- “This token expires at 5PM” → that’s a claim
- “This request has scope design:read” → that’s a claim
- “Issuer is Google” → that’s a claim

A claim is just a key-value statement.

- They are just assertions, no guarantee that they can be trusted.
- When these assertions come from a verifyable trusted entity, they can be trusted.
- **Claim ≠ Guaranteed Truth**

---

## 6. JWT (JSON Web Token)

### What is it?
- A compact, URL-safe, cryptographically signed JSON blob of claims.
- Signed by Auth Service or Identity provider

JWT does not define:

- Authentication
- Authorization
- OAuth
- Sessions

It is only a **format** for securely transmitting claims between parties.

**JWT = Signed Claims Container.**

---

### Structure of a JWT

A JWT consists of three parts:

`base64url(header).base64url(payload).signature`

Example:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjMiLCJleHAiOjE3MDAwMDAwMDB9.
Qk3kdf93jf93jf93jf93jf93jf93jf93jf
```

**Header**

Contains metadata about the token.

Example:
```
{
  "alg": "RS256",
  "typ": "JWT"
}
```
Common fields:

- alg → signing algorithm (HS256, RS256, etc.)
- typ → token type (JWT)

**Payload (Claims)**

The payload contains claims.

Example:
```
{
  "sub": "user123",
  "iss": "https://auth.example.com",
  "aud": "designhub-api",
  "exp": 1700000000,
  "scope": "design:read"
}
```
Each field is a claim.

JWT does not define what claims must exist (except the above standard ones).

| Claim | Meaning                        |
| ----- | ------------------------------ |
| `iss` | Issuer                         |
| `sub` | Subject (who token represents) |
| `aud` | Audience (intended recipient)  |
| `exp` | Expiration time                |
| `iat` | Issued at                      |
| `nbf` | Not valid before               |

These are conventions, not mandatory.

**Signature**

The signature ensures integrity.

It is computed as:
```
Sign(
  base64url(header) + "." + base64url(payload),
  <private_key of Auth service>
)
```

When JWT is received, signature is verified:
- Decrypt the signature with public key of Auth Service → Hash obtained
- Compute the Hash from `base64url(header).base64url(payload)`
- If computed and obtained Hash match → msg integrity and identity of Auth service verified ✅

If payload changes, signature becomes invalid.

---

### Important: JWT Is Not Encryption, but Encoding

JWT is:

- Base64 encoded (not encrypted)
- Readable by anyone who has it
- Protected against tampering via signature

> Anyone can decode the payload. But no one can modify it without breaking the signature.

---

### What JWT Represents

> JWT represents claims, not necessarily identity.

These Cliams can represent:

- A user
- A service
- A device
- A session
- A transaction
- Any signed statement

JWT does not inherently mean:

- Claims can be trusted
- A user is logged in
- Authentication happened
- Authorization is granted

Those meanings depend on context.

---

### Types of Claims

- Registered Claims – Standard names (sub, exp, etc.)
- Public Claims – Publicly agreed-upon custom fields (scope, roles)
- Private Claims – Application-specific fields(feature_flags etc.)

JWT is flexible — claims are arbitrary JSON.

---

### How JWT Is Verified

To trust a JWT:

- Verify signature.
- Verify iss (issuer).
- Verify aud (audience).
- Check exp (expiry).
- Optionally check scopes/roles.

**Now the claims can be trusted**

**Never trust a JWT without verifying signature.**

---

### JWT and Identity

JWT are often used in auth systems to carry identity information of a user/service via claims like:
```
{
  "sub": "user123",
  "email": "bachu@example.com"
}
```

- But JWT itself is neutral.
- It carries claims.
- Identity is just a type of claim.
- A token just has to represent seomthing, it doesn't have to be only identity.

---

### Pros
- Self-contained
- No DB lookup required to validate like API keys
- Expires automatically
- Can carry roles/scopes
- Scale better as no DB required

### Cons
- Harder to revoke immediately
- Larger payload
- Requires signing and key rotation
- You must need an Auth service to use JWTs

### Use cases
- User-facing APIs
- Multi-service systems
- OAuth-based auth

---

## 7. Bearer token

Bearer means:

> Whoever bears (holds) this token can use it.

There is no extra proof required.

If you have:

- `Authorization: Bearer abc123`

API assumes:

- You are authorized, because you possess token

It does NOT check:

- IP
- Device
- Password

Just possession.

That’s bearer.

> You can use API keys & JWTs in bearer style

---

## 8. Stateful Authentication

### What Is a Session? (From Absolute Zero)

You walk into a hotel, At reception:

- You show ID
- They verify you
- They give you a room key card

After that:

- You don’t show ID every time.
- You just show the key card.

That’s a session.

**In Web Terms**

When you log into Canva:

- You send username + password (or Google login)
- Canva verifies identity
- Canva creates a server-side record:
```
session_id = S12345
user_id = 789
expires = 2 hours
```
This record lives on Canva’s server.

That record is called a session.

---

### What Is a Cookie?

Now Canva needs your browser to remember:

> “You are session S12345”

So Canva sends back:
```
Set-Cookie: session_id=S12345; HttpOnly; Secure
```

Your browser stores this.

Now every request to canva.com automatically includes:

`Cookie: session_id=S12345`

That’s a **cookie**.

So:

- Session = server-side state
- Cookie = browser storage mechanism that carries session ID

---

### Traditional Session-Based Auth

Flow:

- Login
- Server creates session
- Browser stores session_id in cookie
- Each request:
  - Browser sends session_id
  - Server looks up session
  - Gets user_id
  - Executes request

Server must store sessions in:

- Memory
- Redis
- Database

This is called **stateful authentication**.

---

## 9. Stateless Authentication

Now enter JWT-based systems.

> Instead of storing session on server, server gives you a **self-contained token**.

Example JWT:
```
{
  "sub": "User",
  "email": "bachu@example.com",
  "exp": 1740000000
}
```
**Signed**.

Now server does NOT need session storage.

On each request:
```
Authorization: Bearer eyJhbGciOi...
```

Server:

- Verifies signature
- Reads user_id
- Checks expiry
- Done

This is called **stateless authentication**.
- No DB lookup.

---

## Token Vs Auth token Vs OAuth token V Access token

Token:
- Its an umbrella
- Any credential whose purpose satisfies the conditions of token are tokens
- There are different types of tokens

Auth token:
- Authentication token
- usually refers to a token that proves identity.
- Often a JWT
- It can authenticate anything, representing identity of user, service, session etc.
- Often used vaguely in context of session toke, ID token, JWT for login etc.

OAuth Token(we'll dive deep into this):
- Used in OAuth flows
- Delegated authorization token (OAuth Access tokens)
- A service, on behalf of user, can perform this action on a service
- delegation can be service -> service also

Access token:
- Grants access to protected resource like API, if valid
- can be JWT or opaque like API keys

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

### ✅ The correct real-world pattern

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

### 🔒 Lock this rule (very important)

> User identity is authenticated at the edge. Internal services authenticate each other using service credentials.

Or even simpler:

> User tokens stop at the gateway.

---

### Interview-Ready Answer

If asked:

- Should Service A forward user JWT to Service B?

You say:

> “In most real-world microservice architectures, forwarding user JWTs is discouraged because it causes scope leakage and expands blast radius. The user token typically contains broad scopes and is issued for public APIs. Instead, Service A should validate the user JWT and generate a downscoped internal token targeted specifically for Service B, preserving least privilege and proper trust boundaries.”

That’s senior-level security thinking.

---

### When is forwarding user JWT acceptable?

Only in very limited cases:
- tightly coupled services
- same trust boundary
- same auth domain
- explicitly designed for it

But as a default mental model: don’t forward user JWTs.

---

## OAuth from First Principles — Sign in with Google

### The real problem OAuth solves

You want:
- User to prove identity
- Without sharing password
- With limited access
- Across different apps

Example:
- “Canva wants to know who you are, but should not know your Google password.”

---

### Actors in OAuth

There are always four parties:
- User (you)
- Client App (Canva)
- Authorization Server (Google)
- Resource Server (Google APIs)

---

### What happens when you click “Sign in with Google”

Let’s walk the flow slowly, end to end, with the *why* behind every step.

---

### Step 1: Redirect to Google (Authorization Request)

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

### Step 2: User authenticates at Google

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

### Step 3: Google gives Canva an Authorization Code

Google redirects your browser back to Canva:

```https://canva.com/callback?code=abc123```

This is a temporary one-time code.

**What is this “authorization code”?**

The authorization code is:
- NOT a token
- NOT a JWT
- NOT usable to call Google APIs

It is simply:
- Proof that the user authenticated and consented

Think of it as:
- “User approved. Canva is allowed to ask for tokens.”

**Why not send tokens directly here?**

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

### Step 4: Canva exchanges the code for tokens (SERVER TO SERVER)

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

### Step 5: Google sends TOKENS to Canva

Google returns:

**1️⃣ ID Token (JWT) — Identity proof**

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

**2️⃣ Access Token — Permission token**

This answers:
- What can Canva do on behalf of the user at Google?

Used to call Google APIs:
- Authorization: Bearer `<access_token>`

Canva uses this token to:
- fetch profile info
- fetch email
- fetch other allowed data

📌 This token is scoped, limited, and short-lived.

---

**3️⃣ (Optional) Refresh Token**

Used to:
- get new access tokens
- without asking the user to log in again

Stored securely:
- server-side only

---

### The roles summarized cleanly

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

### Why OAuth MUST have two steps (core insight 🔑)

If Google sent tokens directly in the redirect:
- tokens would appear in URLs
- tokens would be logged
- tokens could be stolen

So:
- Authorization Code travels via browser
- Tokens travel via backend only

This separation is the entire point of OAuth.

---

### What Canva actually does with each thing

**Authorization Code**
- Immediately exchanges it
- Discards it forever

**ID Token**
- Validates signature
- Extracts user identity
- Creates Canva session / JWT

**Access Token**
- Calls Google APIs
- Fetches profile/email
- May discard after use

**Refresh Token**
- Stored securely (server-side)
- Used to refresh access tokens

---

### 🔑 Key insight about OAuth

OAuth is not “login”.
OAuth is delegated authorization.

Login is just a common use case.

---

### Why OAuth matters for system design

Because:
- tokens have scopes
- tokens expire
- trust is delegated
- auth is centralized

This is why modern systems use:
- OAuth
- OpenID Connect (OIDC)

---

### One-sentence mental model (lock this 🔒)

- Authorization Code = permission receipt
- Token = actual access

Or even simpler:

Code proves consent.
Token grants access.

---

## SAML — Signed XML

### What problem SAML solves

Same core problem as OAuth:
- Single Sign-On (SSO) across organizations

Example:
- You work at Company A
- You access Tool B (Jira, Confluence, Workday)
- You don’t want separate passwords

---

### The core idea (strip it down)

SAML lets one system assert a user’s identity to another system using signed XML.

That’s it.

---

### The players (3 things only)

- User (Browser)

- Identity Provider (IdP)
  → company login system (Okta, Azure AD, ADFS)

- Service Provider (SP)
  → app you’re trying to access (Jira, Salesforce)

---

### High-level flow (feel it)

- User tries to access Service Provider (JIRA)
- SP says: “I don’t know who you are — go to your IdP”
- User authenticates at IdP
- IdP sends back a SAML Assertion (signed XML) via browser
- SP verifies signature and logs user in

---

### What is a SAML Assertion?

It’s a signed statement that says:

- “This user (`alice@company.com`) authenticated successfully at time T
  and has these attributes.”

Properties:
- Digitally signed
- Short-lived
- Cannot be forged

---

### Why SAML feels painful

- XML (verbose)
- Browser redirects + POSTs
- Hard to debug
- Less flexible than OAuth/JWT

But it’s:
- very secure
- very standardized
- deeply entrenched in enterprises

---

### SAML vs OAuth (quick comparison)

| Aspect | SAML | OAuth / OIDC |
| ------ | ---- | ------------ |
Format | XML | JSON / JWT |
Transport | Browser redirects | Browser + API
Typical use | Enterprise SSO | Web + mobile + APIs
Flexibility | Low | High
Popular today | Legacy / Enterprise | Modern default

---

### One-liner to remember

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
```
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
```
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

| Aspect | API Keys | JWTs |
| ------ | -------- | ---- |
Stored in DB | Yes | No
Self-contained | No | Yes
Expiry | Manual | Built-in
Rotation | Hard | Smooth
Scale | Limited | Excellent
Best for | Simple internal | Modern systems

---

You now understand:
- what keys are
- what rotation means
- why security systems are designed this way
