import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

# Set test environment variables BEFORE importing app
import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from backend.main import app
from backend.db import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

from sqlalchemy.pool import StaticPool

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

def test_webhook_ingestion_and_summary():
    with TestClient(app) as client:
        payload = {
            "action": "completed",
            "workflow_run": {
                "id": 12345,
                "name": "CI",
                "head_branch": "main",
                "status": "completed",
                "conclusion": "success",
                "run_started_at": "2026-01-01T10:00:00Z",
                "updated_at": "2026-01-01T10:05:00Z",
                "actor": {"login": "testuser"}
            },
            "repository": {
                "full_name": "test/repo"
            }
        }
        
        response = client.post(
            "/webhook/github",
            json=payload,
            headers={"x-github-event": "workflow_run"}
        )
        assert response.status_code == 200
        
        summary_response = client.get("/api/summary?repo=test/repo&days=300")
        assert summary_response.status_code == 200
        data = summary_response.json()
        assert data["total_runs"] == 1
        assert data["success_rate"] == 100.0
        assert data["avg_duration_seconds"] == 300.0
