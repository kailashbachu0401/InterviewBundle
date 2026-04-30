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

from collections import defaultdict, deque

RATE_LIMIT_WINDOW = 10 # seconds
RATE_LIMIT = 3 # per user per endpoint in rolling window

def is_valid_event(event):
    required_fields = {"user", "timestamp", "endpoint"}
    if not required_fields.issubset(event):
        return False

    user = event["user"]
    event_timestamp = event["timestamp"]
    endpoint = event["endpoint"]

    if not isinstance(user, str) or not user:
        return False

    if not isinstance(event_timestamp, int) or event_timestamp < 0:
        return False

    if not isinstance(endpoint, str) or not endpoint:
        return False

    return True

# check
def is_rate_limited(event, recent_allowed):
    user = event["user"]
    endpoint = event["endpoint"]
    key = (user, endpoint)
    timestamps = recent_allowed[key]

    window_start = event["timestamp"] - RATE_LIMIT_WINDOW + 1
    while timestamps and timestamps[0] < window_start:
        timestamps.popleft()

    return len(timestamps) >= RATE_LIMIT

# commit
def record_allowed(event, recent_allowed):
    user = event["user"]
    endpoint = event["endpoint"]
    key = (user, endpoint)
    recent_allowed[key].append(event["timestamp"])

def get_valid_events(events):
    valid_events = [event for event in events if is_valid_event(event)]
    return valid_events

def aggregate_events(events):
    valid_events = get_valid_events(events)

    valid_events.sort(key = lambda x: x["timestamp"])

    request_counts = defaultdict(lambda: defaultdict(int))
    allowed_requests = []
    rejected_requests = []
    recent_allowed = defaultdict(deque)

    for event in valid_events:
        if is_rate_limited(event, recent_allowed):
            rejected_requests.append({
                **event,
                "reason": "rate_limited"
            })
            continue

        record_allowed(event, recent_allowed)
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
✅ How to add a tie-breaker

You extend the key:
- valid_events.sort(key=lambda x: (x["timestamp"], x["user"]))

Now:
- first → timestamp
- second → user (lexicographically)

⚡ More realistic tie-breaker

If multiple fields matter:
- valid_events.sort(key=lambda x: (x["timestamp"], x["user"], x["endpoint"]))

Now it's:
- first → timestamp
- second → user
- third → endpoint
'''
