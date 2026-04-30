events = [
    {"user": "alice", "timestamp": 5, "endpoint": "/charges"},
    {"user": "alice", "timestamp": 1, "endpoint": "/charges"},
    {"user": "alice", "timestamp": 9, "endpoint": "/charges"},
    {"user": "alice", "timestamp": 10, "endpoint": "/charges"},
    {"user": "alice", "timestamp": 12, "endpoint": "/charges"},
    {"user": "bob", "timestamp": 3, "endpoint": "/refunds"},
    {"user": "bob", "timestamp": 8, "endpoint": "/refunds"},
    {"user": "bob", "timestamp": 14, "endpoint": "/refunds"},
    {"user": "bob", "timestamp": 15, "endpoint": "/refunds"},
    {"user": "charlie", "timestamp": 7, "endpoint": "/charges"},
    {"user": "charlie", "timestamp": 16, "endpoint": "/charges"},

    # invalid events
    {"user": "david", "timestamp": "20", "endpoint": "/charges"},   # invalid timestamp type
    {"user": "erin", "endpoint": "/charges"},                       # missing timestamp
    {"user": "frank", "timestamp": 4, "endpoint": 123},            # invalid endpoint type
    {"user": "", "timestamp": 6, "endpoint": "/charges"},          # invalid user
]

from collections import defaultdict

RATE_LIMIT_WINDOW = 10 # seconds
RATE_LIMIT = 3 # per user per endpoint requests per time window
RATE_LIMIT_TRACKER = defaultdict(int)

def is_valid_event(event):
    required_fields = {"user", "timestamp", "endpoint"}
    if not required_fields.issubset(event): # this just checks if these fields are existing bsaically truthiness and not actually validate them
        return False

    user = event["user"]
    event_timestamp = event["timestamp"]
    endpoint = event["endpoint"]

    # Explicit validation for fields
    if not isinstance(user, str) or not user:
        return False

    if not isinstance(event_timestamp, int) or event_timestamp < 0:
        return False

    if not isinstance(endpoint, str) or not endpoint:
        return False

    return True

def is_rate_limited(event):
    user = event["user"]
    endpoint = event["endpoint"]
    timestamp = event["timestamp"]
    bucket = timestamp // RATE_LIMIT_WINDOW
    key = f"{user}:{endpoint}:{bucket}"


    RATE_LIMIT_TRACKER[key] += 1

    if RATE_LIMIT_TRACKER[key] > RATE_LIMIT:
        return True
    # We are coupling check and commit in the same fun above
    # If the request is not allowed/rate limited, then it has already corrupted the state
    # this corrupted state can impact future decisions.
    # It works in this case as new key is generated everytime, however in general it is nt recommended
    # Try keeping check and commit separate

    return False

def filter_invalid_events(events):
    valid_events = []
    for event in events:
        if is_valid_event(event):
            valid_events.append(event)
    return valid_events

def aggregate_events(events):
    valid_events = filter_invalid_events(events)

    valid_events.sort(key = lambda x: x["timestamp"])

    request_counts = defaultdict(lambda: defaultdict(int))
    allowed_requests = []
    rejected_requests = []

    for event in valid_events:
        if is_rate_limited(event):
            event["reason"] = "rate_limited"
            rejected_requests.append(event)
            continue

        allowed_requests.append(event)

        user = event["user"]
        endpoint = event["endpoint"]
        request_counts[user][endpoint] += 1

    return {
        "allowed_requests": allowed_requests,
        "rejected_requests": rejected_requests,
        "counts": {
            user: dict(endpoints)
            for user, endpoints in request_counts.items()
        }
    }


print(aggregate_events(events))

'''

Third issue: global mutable state

This is bad:

RATE_LIMIT_TRACKER = defaultdict(int)

and then:

RATE_LIMIT_TRACKER[key] += 1

Problems:

state leaks across test runs
calling aggregate_events twice will produce wrong results unless you manually reset it
hidden coupling makes testing harder
not thread-safe
bad interview hygiene

In interview code, global mutable state is usually a smell unless the prompt explicitly asks for an object-oriented long-lived limiter.

Here, the tracker should be local to the processing function.

Fourth issue: mutating input events

You do this:

event["reason"] = "rate_limited"
rejected_requests.append(event)

That mutates the original input event dict.

This is risky because:

side effects leak outside your function
same object may appear in allowed/rejected analysis later
makes debugging harder

Safer:

rejected_requests.append({
    "user": event["user"],
    "timestamp": event["timestamp"],
    "endpoint": event["endpoint"],
    "reason": "rate_limited",
})

In interviews, input mutation should be deliberate, not accidental.

Fifth issue: is_rate_limited both checks and updates state

This function does two things:

RATE_LIMIT_TRACKER[key] += 1

if RATE_LIMIT_TRACKER[key] > RATE_LIMIT:
    return True

So it:

updates tracker
answers rate-limit question

That is not ideal because:

if rejected, it has already polluted the tracker
check and commit are mixed together
harder to extend later

For rolling-window logic, you want something more like:

clean old timestamps
inspect current active allowed timestamps
decide if new request can be allowed
only then append current timestamp if allowed

That separation is cleaner and more correct.


'''
