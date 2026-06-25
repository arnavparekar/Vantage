from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class WorkflowRunBase(BaseModel):
    repo_name: str
    workflow_name: str
    run_id: int
    branch: str
    actor: str
    status: str
    conclusion: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None

class WorkflowRunCreate(WorkflowRunBase):
    pass

class WorkflowRunResponse(WorkflowRunBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SummaryResponse(BaseModel):
    total_runs: int
    success_rate: float
    avg_duration_seconds: Optional[float]
    mttr_seconds: Optional[float]

class TrendDataPoint(BaseModel):
    date: str
    avg_duration_seconds: float

class FailureRateDataPoint(BaseModel):
    date: str
    failure_rate: float

class FlakyWorkflow(BaseModel):
    workflow_name: str
    flakiness_score: float
