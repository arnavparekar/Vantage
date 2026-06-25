from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, func, case
from typing import List, Optional
from datetime import datetime, timedelta

from backend.db import get_db
from backend.models.run import WorkflowRun
from backend.schemas.run import WorkflowRunResponse, SummaryResponse, TrendDataPoint, FailureRateDataPoint, FlakyWorkflow

router = APIRouter()

@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    repo: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    cutoff = datetime.utcnow() - timedelta(days=days)
    base_query = db.query(WorkflowRun).filter(WorkflowRun.started_at >= cutoff)
    if repo:
        base_query = base_query.filter(WorkflowRun.repo_name == repo)
    
    total_runs = base_query.count()
    if total_runs == 0:
        return SummaryResponse(total_runs=0, success_rate=0.0, avg_duration_seconds=0.0, mttr_seconds=None)
    
    success_runs = base_query.filter(WorkflowRun.conclusion == "success").count()
    success_rate = (success_runs / total_runs) * 100.0

    avg_duration = base_query.filter(WorkflowRun.duration_seconds.isnot(None)).with_entities(func.avg(WorkflowRun.duration_seconds)).scalar()
    
    # MTTR using raw SQL
    mttr_query = text("""
        WITH failed_runs AS (
            SELECT id, repo_name, branch, completed_at
            FROM workflow_runs
            WHERE conclusion = 'failure' AND started_at >= :cutoff
            AND (:repo IS NULL OR repo_name = :repo)
        ),
        next_success AS (
            SELECT f.id AS failed_id, min(s.started_at) AS recovery_time
            FROM failed_runs f
            JOIN workflow_runs s ON f.repo_name = s.repo_name 
                                 AND f.branch = s.branch 
                                 AND s.conclusion = 'success'
                                 AND s.started_at > f.completed_at
            GROUP BY f.id
        )
        SELECT AVG(EXTRACT(EPOCH FROM (n.recovery_time - f.completed_at))) AS mttr_seconds
        FROM failed_runs f
        JOIN next_success n ON f.id = n.failed_id
    """)
    mttr_result = db.execute(mttr_query, {"cutoff": cutoff, "repo": repo}).scalar()
    
    return SummaryResponse(
        total_runs=total_runs,
        success_rate=success_rate,
        avg_duration_seconds=float(avg_duration) if avg_duration else 0.0,
        mttr_seconds=float(mttr_result) if mttr_result else None
    )

@router.get("/runs", response_model=List[WorkflowRunResponse])
def get_runs(
    repo: Optional[str] = None,
    branch: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(WorkflowRun)
    if repo:
        query = query.filter(WorkflowRun.repo_name == repo)
    if branch:
        query = query.filter(WorkflowRun.branch == branch)
        
    return query.order_by(WorkflowRun.started_at.desc()).offset(offset).limit(limit).all()

@router.get("/duration-trend", response_model=List[TrendDataPoint])
def get_duration_trend(
    repo: Optional[str] = None,
    branch: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    cutoff = datetime.utcnow() - timedelta(days=days)
    date_trunc = func.date_trunc('day', WorkflowRun.started_at)
    
    query = db.query(
        date_trunc.label('day'),
        func.avg(WorkflowRun.duration_seconds).label('avg_duration')
    ).filter(WorkflowRun.started_at >= cutoff, WorkflowRun.duration_seconds.isnot(None))
    
    if repo:
        query = query.filter(WorkflowRun.repo_name == repo)
    if branch:
        query = query.filter(WorkflowRun.branch == branch)
        
    results = query.group_by('day').order_by('day').all()
    
    return [TrendDataPoint(date=r.day.strftime('%Y-%m-%d'), avg_duration_seconds=float(r.avg_duration)) for r in results]

@router.get("/failure-rate", response_model=List[FailureRateDataPoint])
def get_failure_rate(
    repo: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    cutoff = datetime.utcnow() - timedelta(days=days)
    date_trunc = func.date_trunc('day', WorkflowRun.started_at)
    
    query = db.query(
        date_trunc.label('day'),
        func.count(WorkflowRun.id).label('total'),
        func.sum(case((WorkflowRun.conclusion == 'failure', 1), else_=0)).label('failures')
    ).filter(WorkflowRun.started_at >= cutoff, WorkflowRun.conclusion.in_(['success', 'failure']))
    
    if repo:
        query = query.filter(WorkflowRun.repo_name == repo)
        
    results = query.group_by('day').order_by('day').all()
    
    trend = []
    for r in results:
        rate = (r.failures / r.total) * 100.0 if r.total > 0 else 0.0
        trend.append(FailureRateDataPoint(date=r.day.strftime('%Y-%m-%d'), failure_rate=rate))
        
    return trend

@router.get("/repos", response_model=List[str])
def get_repos(db: Session = Depends(get_db)):
    results = db.query(WorkflowRun.repo_name).distinct().all()
    return [r[0] for r in results if r[0]]

@router.get("/flaky-workflows", response_model=List[FlakyWorkflow])
def get_flaky_workflows(
    repo: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    query = text("""
        WITH recent_runs AS (
            SELECT 
                repo_name, 
                workflow_name, 
                conclusion,
                LAG(conclusion) OVER (PARTITION BY repo_name, workflow_name ORDER BY started_at) as prev_conclusion
            FROM workflow_runs
            WHERE started_at >= :cutoff AND conclusion IN ('success', 'failure')
            AND (:repo IS NULL OR repo_name = :repo)
        ),
        flaky_stats AS (
            SELECT 
                workflow_name,
                COUNT(*) as total_runs,
                SUM(CASE WHEN conclusion != prev_conclusion THEN 1 ELSE 0 END) as alternations
            FROM recent_runs
            GROUP BY repo_name, workflow_name
        )
        SELECT 
            workflow_name,
            total_runs,
            CAST(alternations AS FLOAT) / NULLIF(total_runs - 1, 0) as flakiness_score
        FROM flaky_stats
        WHERE total_runs > 1
        ORDER BY flakiness_score DESC NULLS LAST
        LIMIT 5
    """)
    
    results = db.execute(query, {"cutoff": cutoff, "repo": repo}).mappings().all()
    return [
        FlakyWorkflow(
            workflow_name=r["workflow_name"], 
            flakiness_score=float(r["flakiness_score"] or 0.0), 
            total_runs=r["total_runs"]
        ) for r in results
    ]
