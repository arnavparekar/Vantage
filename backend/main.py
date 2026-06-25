from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time

from backend.db import engine, Base
from backend.routers import webhooks, analytics
from backend.metrics import api_requests_total, api_request_duration_seconds

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Vantage API", lifespan=lifespan)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    endpoint = request.url.path
    api_request_duration_seconds.labels(endpoint=endpoint).observe(duration)
    api_requests_total.labels(endpoint=endpoint, status_code=response.status_code).inc()
    
    return response

app.include_router(webhooks.router, prefix="/webhook", tags=["webhooks"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/metrics", response_class=PlainTextResponse)
def get_metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
