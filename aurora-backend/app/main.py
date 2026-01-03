"""
AURORA™ - Pre-Incident Decision Intelligence Engine
Global 3 Technology & Intelligence (G3TI)

A patent-grade, government-ready intelligence platform that detects
emerging threats before they manifest using weak-signal convergence.

DEMONSTRATION ENVIRONMENT - Pre-patent technology preview.
Synthetic data only. Not for operational use, real-world monitoring, or enforcement.

Core Components:
- Weak-Signal Convergence Engine (PATENT CRITICAL)
- Intent Gradient Modeling
- Narrative Intelligence Objects (NIOs)
- Human-in-the-Loop Feedback System
- Full Audit Trail for Government-Grade Accountability
"""

import time
import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api import router

access_logs: List[dict] = []

app = FastAPI(
    title="AURORA™ Decision Intelligence Simulation",
    description="Pre-Incident Decision Intelligence Engine by G3TI - DEMONSTRATION ENVIRONMENT",
    version="1.0.0-mvp",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router, prefix="/api/v1", tags=["AURORA API"])


@app.middleware("http")
async def log_access(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    log_entry = {
        "id": request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "method": request.method,
        "path": str(request.url.path),
        "query_params": str(request.query_params) if request.query_params else None,
        "client_ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "status_code": response.status_code,
        "process_time_ms": round(process_time * 1000, 2),
    }
    
    access_logs.append(log_entry)
    
    if len(access_logs) > 10000:
        access_logs.pop(0)
    
    return response


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {
        "name": "AURORA™ Intelligence Platform",
        "version": "1.0.0-mvp",
        "description": "Pre-Incident Decision Intelligence Engine by G3TI",
        "documentation": "/docs",
        "api_base": "/api/v1",
        "endpoints": {
            "threats": "/api/v1/threats",
            "signals": "/api/v1/signals",
            "feedback": "/api/v1/feedback",
            "audit": "/api/v1/audit",
            "status": "/api/v1/system/status"
        }
    }
