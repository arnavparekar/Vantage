from sqlalchemy import Column, Integer, String, BigInteger, DateTime, func, Index
from backend.db import Base

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    repo_name = Column(String, index=True, nullable=False)
    workflow_name = Column(String, nullable=False)
    run_id = Column(BigInteger, unique=True, nullable=False, index=True)
    branch = Column(String, index=True, nullable=False)
    actor = Column(String, nullable=False)
    status = Column(String, nullable=False)
    conclusion = Column(String, index=True, nullable=True)
    started_at = Column(DateTime, index=True, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_workflow_runs_repo_branch", "repo_name", "branch"),
    )
