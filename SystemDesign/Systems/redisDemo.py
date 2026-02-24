import redis
from typing import Optional, Dict, Any
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
print("Redis connection successful:", r.ping())  # True

# Pluggedin to EventMetaDataSystem/main.py
def cache_get_json(key: str) -> Optional[Dict[str, Any]]:
    s = r.get(key)
    return json.loads(s) if s else None

def cache_set_json(key: str, value: Dict[str, Any], ttl_seconds: int) -> None:
    r.set(key, json.dumps(value), ex=ttl_seconds)

def cache_delete(key: str) -> None:
    r.delete(key)

'''
That's enough to implement:

- cache-aside
- TTL
- invalidate on write
'''

'''
Single-flight hook (stampede protection) — minimal & correct

We only do this on cache miss.

Flow:

- cache miss
- try to acquire lock
- if lock acquired:
    - read DB
    - set cache
    - release lock
- else: wait briefly and retry cache
'''

import time

def db_fetch_somehow() -> Dict[str, Any]:
    return {"id": "123", "name": "Test Event"}

def get_with_singleflight(cache_key: str, lock_ttl: int = 2):
    # 1) cache first
    cached = cache_get_json(cache_key)
    if cached:
        return cached

    lock_key = f"lock:{cache_key}"

    # 2) acquire lock (atomic)
    got_lock = r.set(lock_key, "1", nx=True, ex=lock_ttl)
    if got_lock:
        try:
            # Double-check cache after lock (reduces DB hits)
            cached2 = cache_get_json(cache_key)
            if cached2:
                return cached2

            # 3) fetch from DB here
            value = db_fetch_somehow()

            cache_set_json(cache_key, value, ttl_seconds=120)
            return value
        finally:
            r.delete(lock_key)
    else:
        # 4) someone else is fetching. wait a bit and retry cache.
        time.sleep(0.02)  # 20ms
        cached3 = cache_get_json(cache_key)
        if cached3:
            return cached3

        # Worst case fallback: DB (or wait-and-retry loop)
        return db_fetch_somehow()

'''
Why lock TTL matters

If the process dies while holding lock, TTL ensures lock disappears quickly.
'''

# Pluggedin to EventMetaDataSystem/main.py
def allow_request(user_id: str, limit: int = 100, window_seconds: int = 60) -> bool:
    # Example: per-minute window
    # time.time() returns the number of seconds since the Unix epoch
    # // is integer division
    # window_seconds = 60, current_time = seconds_since_epoch = 60010
    # bucket = 60010 // 60 = 1000
    # Meaning:
    # This request falls in window #1000
    # Which covers: seconds 60000 → 60059

    bucket = int(time.time() // window_seconds)
    key = f"rate:{user_id}:{bucket}"

    count = r.incr(key)          # atomic
    if count == 1:
        r.expire(key, window_seconds)  # set TTL once

    return count <= limit
