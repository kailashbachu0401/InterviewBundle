from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel, Field
from dataclasses import dataclass
from fastapi import HTTPException, status, Query, Header
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime, timedelta, timezone
import base64

app = FastAPI(title="Event MetaData System", version="0.1.0")

# -----------------------------
# Helpers
# -----------------------------

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def b64_encode(s: str) -> str:
    return base64.urlsafe_b64encode(s.encode("utf-8")).decode("utf-8")

def b64_decode(s: str) -> str:
    return base64.urlsafe_b64decode(s.encode("utf-8")).decode("utf-8")

def make_cursor(updated_at: datetime, event_id: str) -> str:
    return b64_encode(f"{updated_at.isoformat()}|{event_id}")

def parse_cursor(cursor: str) -> Tuple[datetime, str]:
    raw = b64_decode(cursor)
    ts_str, event_id = raw.split("|", 1) # Split atmost once
    return datetime.fromisoformat(ts_str), event_id



# -----------------------------
# Domain Models
# -----------------------------

class FraudRisk(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class EventMetaDataView(BaseModel):
    event_id: str
    fraud_risk_level: Optional[FraudRisk] = None
    is_fraud_suspected: Optional[bool] = None
    feature_flags: Dict[str, Any] = Field(default_factory = dict)
    media_summary: Dict[str, Any] = Field(default_factory = dict)
    updated_at: datetime

class EventMetaDataPatch(BaseModel):
    fraud_risk_level: Optional[FraudRisk] = None
    is_fraud_suspected: Optional[bool] = None
    feature_flags: Dict[str, Any] = Field(default_factory = dict)
    media_summary: Dict[str, Any] = Field(default_factory = dict)

class SignalRequest(BaseModel):
    source: str = Field(..., min_length = 1, description = "The source of the signal")
    signal_id: str = Field(..., min_length = 1, description = "The id of the signal")
    payload: Optional[Dict[str, Any]] = Field(default_factory = dict)
    observed_at: Optional[datetime] = None

class ListMetadataResponse(BaseModel):
    events: List[EventMetaDataView]
    next_cursor: Optional[str] = None

# -----------------------------
# DB
# -----------------------------

@dataclass
class EventMetaDataRow:
    event_id: str
    fraud_risk_level: Optional[FraudRisk]
    is_fraud_suspected: Optional[bool]
    feature_flags: Dict[str, Any]
    media_summary: Dict[str, Any]
    updated_at: datetime

# event_id -> EventMetaDataRow
EVENT_METADATA: Dict[str, EventMetaDataRow] = {}

# (event_id, source, signal_id) -> True  (dedupe + audit stub)
SIGNALS: Dict[Tuple[str, str, str], bool] = {}

# idempotency: (scope, key) -> (response, expires_at)
IDEMP: Dict[Tuple[str, str], Tuple[Dict[str, Any], datetime]] = {}
IDEMPOTENCY_TTL_SECONDS = 2 * 60 * 60 # 2 hours

# cache: event_id -> (response, expires_at)
CACHE: Dict[str, Tuple[Dict[str, Any], datetime]] = {}
CACHE_TTL_SECONDS = 120

def cleanup_idemp():
    now = utc_now()

    for key in IDEMP.keys():
        _, exp = IDEMP[key]
        if exp <= now:
            IDEMP.pop(key, None)

def to_view(row: EventMetaDataRow) -> EventMetaDataView:
    return EventMetaDataView(
        event_id = row.event_id,
        fraud_risk_level = row.fraud_risk_level,
        is_fraud_suspected = row.is_fraud_suspected,
        feature_flags = row.feature_flags,
        media_summary = row.media_summary,
        updated_at = row.updated_at
    )

def cache_get(key: str) -> Optional[Dict[str, Any]]:
    now = utc_now()
    cached = CACHE.get(key)
    if not cached:
        return None

    response, exp = cached
    if exp <= now:
        CACHE.pop(key, None)
        return None

    return response

def cache_set(key: str, response: Dict[str, Any]) -> None:
    now = utc_now()
    CACHE[key] = (response, now + timedelta(seconds = CACHE_TTL_SECONDS))

def cache_delete(key: str) -> None:
    CACHE.pop(key, None)


# -----------------------------
# API
# -----------------------------

@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "timestamp": utc_now().isoformat()
    }

@app.get("/v1/events/{event_id}/metadata") # versioning -> v1
def get_metadata(event_id: str) -> EventMetaDataView:
    # check cache first
    cache_key = f"eventmeta:{event_id}" # incase we wanna store multiple domains in same cache
    cached = cache_get(cache_key)
    if cached:
        return EventMetaDataView(**cached)

    # not in cache, read from db
    row = EVENT_METADATA.get(event_id)
    if not row:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Event {event_id} not found")

    # cache the result
    view = to_view(row)
    cache_set(cache_key, view.model_dump()) # model_dump() converts to dict
    return view

@app.patch("/v1/events/{event_id}/metadata", response_model = EventMetaDataView)
def patch_metadata(event_id: str, req: EventMetaDataPatch) -> EventMetaDataView:
    cache_key = f"eventmeta:{event_id}"
    metedata = EVENT_METADATA.get(event_id)
    if not metedata:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Event {event_id} not found")

    # update the metadata
    metedata.fraud_risk_level = req.fraud_risk_level
    metedata.is_fraud_suspected = req.is_fraud_suspected
    metedata.feature_flags = req.feature_flags
    metedata.media_summary = req.media_summary
    metedata.updated_at = utc_now()

    # invalidate the cache
    cache_delete(cache_key)

    # return the updated metadata
    return to_view(metedata)

@app.post("/v1/events/{event_id}/metadata/signals", response_model = EventMetaDataView)
def post_signal(event_id: str, sig: SignalRequest) -> EventMetaDataView:
    sig_key = (event_id, sig.source, sig.signal_id)

    cache_key = f"eventmeta:{event_id}"
    row = EVENT_METADATA.get(event_id)
    if not row:
        EVENT_METADATA[event_id] = EventMetaDataRow(
            event_id = event_id,
            updated_at = utc_now(),
            fraud_risk_level = None,
            is_fraud_suspected = None,
            feature_flags = {},
            media_summary = {}
        )
        row = EVENT_METADATA[event_id]

    if sig_key in SIGNALS:
        # signal already applied -> idempotent
        return to_view(row)

    # new signal -> apply it
    SIGNALS[sig_key] = True

    # update the metadata
    payload = sig.payload

    if "fraud_risk_level" in payload:
        row.fraud_risk_level = FraudRisk(payload["fraud_risk_level"])
    if "is_fraud_suspected" in payload:
        row.is_fraud_suspected = bool(payload["is_fraud_suspected"])
    if "feature_flags" in payload and isinstance(payload["feature_flags"], dict):
        row.feature_flags.update(payload["feature_flags"])
    if "media_summary" in payload and isinstance(payload["media_summary"], dict):
        row.media_summary.update(payload["media_summary"])

    row.updated_at = utc_now()

    # invalidate the cache
    cache_delete(cache_key)

@app.post("/v1/events/{event_id}/metadata/enrich", status_code = status.HTTP_202_ACCEPTED)
def enrich(
    event_id: str,
    idempotency_key: Optional[str] = Header(default = None, alias = "Idempotency-Key", convert_underscores = False)
    ) -> Dict[str, Any]:

    """
    Async trigger. In real system: create job + enqueue.
    Here: we return a fake job_id.
    """

    cleanup_idemp()

    scope = f"POST:/v1/events/{event_id}/metadata/enrich"
    if idempotency_key and (scope, idempotency_key) in IDEMP:
        response, _exp = IDEMP[(scope, idempotency_key)]
        return response

    job_id = f"job_{event_id}_{utc_now().isoformat()}"
    response = { "job_id": job_id, "status": "ACCEPTED"}

    IDEMP[(scope, idempotency_key)] = (response, utc_now() + timedelta(seconds = IDEMPOTENCY_TTL_SECONDS))
    return response

@app.get("/v1/events/metadata", response_model = ListMetadataResponse)
def list_metadata(
    updated_after: Optional[datetime] = Query(default = None),
    limit: int = Query(default = 5, ge = 1, le = 100),
    cursor: Optional[str] = Query(default = None)
    ) -> ListMetadataResponse:

    rows = list(EVENT_METADATA.values())

    if updated_after:
        rows = [row for row in rows if row.updated_at > updated_after]

    rows.sort(key = lambda r:(r.updated_at, r.event_id), reverse = True)
    if cursor:
        updated_at, event_id = parse_cursor(cursor)
        rows = [row for row in rows if (row.updated_at, row.event_id) < (updated_at, event_id)]

    page = rows[:limit]
    next_cursor = make_cursor(page[-1].updated_at, page[-1].event_id) if len(page) == limit else None

    return ListMetadataResponse(events = [to_view(row) for row in page], next_cursor = next_cursor)
