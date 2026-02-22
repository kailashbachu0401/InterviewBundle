'''
FastAPI Job system - skeleton (Learning version)

APIs
- POST /jobs              -> create async job (202 Accepted)
- GET  /jobs/{job_id}     -> fetch job status/details
- GET  /jobs              -> list jobs with filters + cursor pagination
- Idempotency-Key support -> retries won't create duplicate jobs


Try:
  curl -X POST "http://127.0.0.1:8000/jobs" \
    -H "Content-Type: application/json" \
    -H "Idempotency-Key: abc123" \
    -d '{"type":"generate_report","payload":{"event_id":"E1"},"user_id":"U1"}'
'''

from typing import Dict, Optional, Any, List
from uuid import uuid4
from pydantic import BaseModel, Field
from fastapi import FastAPI, Header, Query
from fastapi import status
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
from fastapi import HTTPException

app = FastAPI(title = "Background Job Processing System", version = "0.1.0")

# -----------------------------
# First create the models (API contracts)
# -----------------------------

class JobStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"

@dataclass
class JobRow:
    job_id: str
    status: JobStatus
    type: str
    created_at: datetime
    updated_at: datetime
    attempt_count: int
    user_id: Optional[str]
    payload: Dict[str, Any]
    lease_expires_at: Optional[datetime] = None
    last_err: Optional[str] = None

# tables
JOBS: Dict[str, JobRow] = {}
LEASE_DURATION_SECONDS = 10 * 60 # 10 minutes
# idempotency_key -> (job_id, expires_at)
IDEMPOTENCY: Dict[str, tuple[str, datetime]] = {}
IDEMPOTENCY_TTL_SECONDS = 2 * 60 * 60 # 2 hours

def cleanup_expired_idempotency_keys():
    utc_now = datetime.now(timezone.utc)
    expired_keys = [key for key, (_, exp) in IDEMPOTENCY.items() if exp <= utc_now]
    for key in expired_keys:
        IDEMPOTENCY.pop(key, None)

class CreateJobRequest(BaseModel):
    user_id: Optional[str] = Field(default = None, examples = ["123"])
    type: str = Field(..., min_length = 1, examples = ["generate_report"])
    payload: Dict[str, Any] = Field(default_factory = dict)

class CreateJobResponse(BaseModel):
    job_id: str
    status: JobStatus

class JobView(BaseModel):
    job_id: str
    status: JobStatus
    type: str
    created_at: datetime
    updated_at: datetime
    attempt_count: int
    user_id: Optional[str]
    payload: Dict[str, Any]
    lease_expires_at: Optional[datetime] = None
    last_err: Optional[str] = None

def to_job_view(job: JobRow) -> JobView:
    return JobView(
        job_id = job.job_id,
        status = job.status,
        type = job.type,
        created_at = job.created_at,
        updated_at = job.updated_at,
        attempt_count = job.attempt_count,
        user_id = job.user_id,
        payload = job.payload,
        lease_expires_at = job.lease_expires_at,
        last_err = job.last_err,
    )

class ListJobsResponse(BaseModel):
    jobs: List[JobView]
    next_cursor: Optional[str] = None

# -------------------------------------------------------------
# 2nd - Start creating APIs, implement the functions as you go
# -------------------------------------------------------------
@app.post("/jobs", response_model = CreateJobResponse, status_code = status.HTTP_202_ACCEPTED)
def create_job(
    req: CreateJobRequest,
    idempotency_key: Optional[str] = Header(default = None, alias = "Idempotency-Key", convert_underscores = False)
    ) -> CreateJobResponse:

    cleanup_expired_idempotency_keys()

    if idempotency_key and idempotency_key in IDEMPOTENCY:
        job_id, _ = IDEMPOTENCY[idempotency_key]
        if job_id in JOBS:
            return CreateJobResponse(job_id = job_id, status = JOBS[job_id].status)

    utc_now = datetime.now(timezone.utc)

    job = JobRow(
        job_id = str(uuid4()),
        status = JobStatus.PENDING,
        type = req.type,
        created_at = utc_now,
        updated_at = utc_now,
        attempt_count = 0,
        user_id = req.user_id,
        payload = req.payload,
    )

    JOBS[job.job_id] = job

    # enqueue job

    if idempotency_key:
        IDEMPOTENCY[idempotency_key] = (job.job_id, utc_now + timedelta(seconds = IDEMPOTENCY_TTL_SECONDS))

    return CreateJobResponse(job_id = job.job_id, status = job.status)

@app.get("/jobs/{id}", response_model = JobView)
def get_job(id: str) -> JobView:
    job = JOBS.get(id)
    if not job:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Job {id} not found")
    return to_job_view(job)

@app.get("/jobs", response_model = ListJobsResponse)
def list_jobs(
    user_id: Optional[str] = Query(default = None),
    status_filter: Optional[JobStatus] = Query(default = None, alias = "status"),
    cursor: Optional[str] = Query(default = None),
    limit: int = Query(default = 20, ge = 1, le = 100)
    ) -> ListJobsResponse:

    """
    List jobs with simple filters + cursor pagination.

    Cursor design (learning):
    - cursor is the last job_id from previous page (stable enough for in-memory demo)
    - real systems use created_at + id or opaque cursors
    """

    # order_by created_at DESC
    jobs = sorted(JOBS.values(), key = lambda job: (job.created_at, job.job_id), reverse = True)

    if user_id:
        jobs = [job for job in jobs if job.user_id == user_id]
    if status_filter:
        jobs = [job for job in jobs if job.status == status_filter]

    start_idx = 0
    if cursor:
        for i, j in enumerate(jobs):
            if j.job_id == cursor:
                start_idx = i + 1
                break

    page = jobs[start_idx:start_idx + limit]
    next_cursor = jobs[-1].job_id if len(page) == limit else None

    return ListJobsResponse(jobs = [to_job_view(job) for job in page], next_cursor = next_cursor)

# -----------------------------
# Optional: a tiny "worker" simulator endpoint (for learning)
# -----------------------------
class UpdateJobRequest(BaseModel):
    status: JobStatus
    last_error: Optional[str] = None


@app.post("/jobs/{job_id}/_simulate", response_model=JobView)
def simulate_worker_update(job_id: str, req: UpdateJobRequest) -> JobView:
    """
    Learning-only endpoint to simulate the worker updating job state.
    In real systems, workers update DB directly; you wouldn't expose this publicly.
    """
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")

    job.status = req.status
    job.last_err = req.last_error if req.last_error else None
    job.updated_at = datetime.now(timezone.utc)

    return to_job_view(job)

# -----------------------------
'''
Quick test commands

Create job (with idempotency):

curl -X POST "http://127.0.0.1:8000/jobs" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: abc123" \
  -d '{"type":"generate_report","payload":{"event_id":"E1"},"user_id":"U1"}'


Retry the same request (same key) → you should get the same job_id:

curl -X POST "http://127.0.0.1:8000/jobs" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: abc123" \
  -d '{"type":"generate_report","payload":{"event_id":"E1"},"user_id":"U1"}'


Fetch job:

curl "http://127.0.0.1:8000/jobs/<JOB_ID>"


List jobs (filters + cursor):

curl "http://127.0.0.1:8000/jobs?user_id=U1&status=PENDING&limit=10"


Simulate worker finishing:

curl -X POST "http://127.0.0.1:8000/jobs/<JOB_ID>/_simulate" \
  -H "Content-Type: application/json" \
  -d '{"status":"DONE","result":{"url":"s3://bucket/report.pdf"}}'
'''