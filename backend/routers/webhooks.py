import os
import hmac
import hashlib
from fastapi import APIRouter, Request, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models.run import WorkflowRun
from backend.metrics import webhook_events_total, webhook_processing_seconds
from datetime import datetime

router = APIRouter()

GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "")

def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    if not signature_header:
        return False
    hash_object = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode("utf-8"),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)

@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None),
    db: Session = Depends(get_db)
):
    # Only process workflow_run events
    if x_github_event != "workflow_run":
        return {"status": "ignored", "reason": "not a workflow_run event"}

    payload_body = await request.body()
    
    if GITHUB_WEBHOOK_SECRET and not verify_signature(payload_body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    with webhook_processing_seconds.time():
        payload = await request.json()
        workflow_run = payload.get("workflow_run", {})
        repository = payload.get("repository", {})

        run_id = workflow_run.get("id")
        if not run_id:
            return {"status": "ignored", "reason": "no run_id"}

        repo_name = repository.get("full_name", "unknown/unknown")
        workflow_name = workflow_run.get("name", "unknown")
        branch = workflow_run.get("head_branch", "unknown")
        
        actor_obj = workflow_run.get("triggering_actor") or workflow_run.get("actor") or {}
        actor = actor_obj.get("login", "unknown")

        status = workflow_run.get("status", "unknown")
        conclusion = workflow_run.get("conclusion")

        started_at_str = workflow_run.get("run_started_at") or workflow_run.get("created_at")
        started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00")) if started_at_str else datetime.utcnow()

        updated_at_str = workflow_run.get("updated_at")
        completed_at = None
        duration_seconds = None

        if status == "completed" and updated_at_str:
            completed_at = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))
            duration_seconds = int((completed_at - started_at).total_seconds())

        # Update metrics
        webhook_events_total.labels(repo=repo_name, conclusion=conclusion or "none").inc()

        # Upsert
        existing_run = db.query(WorkflowRun).filter(WorkflowRun.run_id == run_id).first()
        if existing_run:
            existing_run.status = status
            existing_run.conclusion = conclusion
            existing_run.completed_at = completed_at
            existing_run.duration_seconds = duration_seconds
        else:
            new_run = WorkflowRun(
                repo_name=repo_name,
                workflow_name=workflow_name,
                run_id=run_id,
                branch=branch,
                actor=actor,
                status=status,
                conclusion=conclusion,
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=duration_seconds
            )
            db.add(new_run)
        
        db.commit()

    return {"status": "ok"}
