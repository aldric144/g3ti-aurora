"""
AURORA™ API Routes
Complete API-first design for threat intelligence platform

Endpoints:
- GET /threats - List all threat objects
- GET /threats/{id} - Get specific threat with full details
- POST /threats - Create new threat object
- GET /threats/{id}/narrative - Export NIO for a threat
- POST /threats/{id}/narrative/regenerate - Regenerate NIO
- GET /threats/{id}/history - Confidence trend history
- POST /signals - Ingest new signals
- POST /signals/{threat_id} - Add signal to specific threat
- POST /feedback - Human-in-the-loop feedback
- GET /audit - Audit trail access
- POST /threats/{id}/recalculate - Recalculate threat assessment
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.models.schemas import (
    Signal,
    SignalCreate,
    ThreatObject,
    ThreatCreate,
    ThreatSummary,
    NarrativeIntelligenceObject,
    AuditEntry,
    FeedbackEntry,
    FeedbackCreate,
    IntentStage,
    MonitoringPosture,
    JurisdictionContext,
    JurisdictionSummary,
)
from app.database.store import get_store
from app.modules.signal_ingestion import SignalIngestionEngine
from app.modules.correlation import ConvergenceEngine
from app.modules.intent_modeling import IntentGradientEngine
from app.modules.narrative_generation import NarrativeEngine


router = APIRouter()


class ThreatListResponse(BaseModel):
    """Response model for threat list"""
    threats: list[ThreatSummary]
    total: int


class HistoryResponse(BaseModel):
    """Response model for probability history"""
    threat_id: str
    history: list[dict]
    current_probability: float
    trend: str


class AuditResponse(BaseModel):
    """Response model for audit trail"""
    entries: list[AuditEntry]
    total: int


class RecalculateResponse(BaseModel):
    """Response model for recalculation"""
    threat_id: str
    previous_probability: float
    new_probability: float
    previous_stage: str
    new_stage: str
    message: str


@router.get("/threats", response_model=ThreatListResponse)
async def list_threats(
    status: Optional[str] = Query(None, description="Filter by status: active, resolved, archived"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_probability: Optional[float] = Query(None, ge=0, le=100, description="Minimum probability threshold"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    List all threat objects with optional filtering.
    
    Returns lightweight summaries for efficient list views.
    Use GET /threats/{id} for full threat details.
    """
    store = get_store()
    threats = store.get_all_threats()
    
    if status:
        threats = [t for t in threats if t.status == status]
    
    if category:
        threats = [t for t in threats if t.category == category]
    
    if min_probability is not None:
        threats = [t for t in threats if t.probability_curve.current_probability >= min_probability]
    
    threats = sorted(threats, key=lambda t: t.probability_curve.current_probability, reverse=True)
    
    total = len(threats)
    threats = threats[offset:offset + limit]
    
    summaries = []
    for threat in threats:
        posture = MonitoringPosture.ROUTINE
        if threat.current_nio:
            posture = threat.current_nio.monitoring_posture
        
        summary = ThreatSummary(
            id=threat.id,
            name=threat.name,
            category=threat.category,
            current_probability=threat.probability_curve.current_probability,
            intent_stage=threat.intent_gradient.current_stage,
            monitoring_posture=posture,
            signal_count=len(threat.signals),
            updated_at=threat.updated_at
        )
        summaries.append(summary)
    
    return ThreatListResponse(threats=summaries, total=total)


@router.get("/threats/{threat_id}", response_model=ThreatObject)
async def get_threat(threat_id: str):
    """
    Get full details for a specific threat.
    
    Returns complete threat object including:
    - All contributing signals
    - Probability curve with history
    - Intent gradient with stage scores
    - Historical analogs
    - Current NIO (if generated)
    """
    store = get_store()
    threat = store.get_threat(threat_id)
    
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {threat_id} not found")
    
    return threat


@router.post("/threats", response_model=ThreatObject)
async def create_threat(threat_data: ThreatCreate):
    """
    Create a new threat object.
    
    Creates threat with baseline values. Add signals using
    POST /signals/{threat_id} to build the threat assessment.
    """
    store = get_store()
    threat = store.create_threat(
        name=threat_data.name,
        description=threat_data.description,
        category=threat_data.category
    )
    
    return threat


@router.get("/threats/{threat_id}/narrative", response_model=NarrativeIntelligenceObject)
async def get_threat_narrative(threat_id: str):
    """
    Get the current Narrative Intelligence Object for a threat.
    
    Returns the most recent NIO with:
    - Executive summary
    - Signal convergence narrative
    - Confidence explanation
    - Known unknowns
    - Monitoring posture recommendation
    - Full reasoning chain
    """
    store = get_store()
    threat = store.get_threat(threat_id)
    
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {threat_id} not found")
    
    if not threat.current_nio:
        narrative_engine = NarrativeEngine()
        nio = narrative_engine.generate_nio(threat)
        return nio
    
    return threat.current_nio


@router.post("/threats/{threat_id}/narrative/regenerate", response_model=NarrativeIntelligenceObject)
async def regenerate_narrative(threat_id: str):
    """
    Regenerate the Narrative Intelligence Object for a threat.
    
    Use this after significant changes to threat assessment
    or to get updated narrative based on latest signals.
    """
    store = get_store()
    threat = store.get_threat(threat_id)
    
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {threat_id} not found")
    
    narrative_engine = NarrativeEngine()
    nio = narrative_engine.generate_nio(threat)
    
    return nio


@router.get("/threats/{threat_id}/history", response_model=HistoryResponse)
async def get_threat_history(
    threat_id: str,
    limit: int = Query(100, ge=1, le=500, description="Maximum history entries")
):
    """
    Get probability trend history for a threat.
    
    Returns historical probability values with timestamps
    for trend analysis and visualization.
    """
    store = get_store()
    threat = store.get_threat(threat_id)
    
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {threat_id} not found")
    
    history = store.get_threat_history(threat_id)
    history = history[-limit:] if len(history) > limit else history
    
    return HistoryResponse(
        threat_id=threat_id,
        history=history,
        current_probability=threat.probability_curve.current_probability,
        trend=threat.probability_curve.trend
    )


@router.post("/signals", response_model=Signal)
async def ingest_signal(signal_data: SignalCreate):
    """
    Ingest a new signal into the system.
    
    Signal will be stored but not associated with any threat.
    Use POST /signals/{threat_id} to add signal to a specific threat.
    """
    ingestion_engine = SignalIngestionEngine()
    
    is_valid, errors = ingestion_engine.validate_signal(signal_data)
    if not is_valid:
        raise HTTPException(status_code=400, detail={"errors": errors})
    
    signal = ingestion_engine.ingest_signal(signal_data)
    
    return signal


@router.post("/signals/{threat_id}", response_model=ThreatObject)
async def add_signal_to_threat(threat_id: str, signal_data: SignalCreate):
    """
    Add a signal to a specific threat and recalculate assessment.
    
    This will:
    1. Validate and ingest the signal
    2. Associate it with the threat
    3. Recalculate convergence and probability
    4. Update intent gradient
    
    Returns updated threat object.
    """
    store = get_store()
    threat = store.get_threat(threat_id)
    
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {threat_id} not found")
    
    ingestion_engine = SignalIngestionEngine()
    
    is_valid, errors = ingestion_engine.validate_signal(signal_data)
    if not is_valid:
        raise HTTPException(status_code=400, detail={"errors": errors})
    
    signal = ingestion_engine.ingest_signal(signal_data, threat_id)
    
    convergence_engine = ConvergenceEngine()
    threat = convergence_engine.recalculate_threat(threat_id)
    
    intent_engine = IntentGradientEngine()
    threat = intent_engine.recalculate_threat_gradient(threat_id)
    
    return threat


@router.post("/threats/{threat_id}/recalculate", response_model=RecalculateResponse)
async def recalculate_threat(threat_id: str):
    """
    Manually trigger recalculation of threat assessment.
    
    Recalculates:
    - Convergence score and probability
    - Intent gradient and stage
    - Historical analogs
    
    Use after feedback application or signal weight adjustments.
    """
    store = get_store()
    threat = store.get_threat(threat_id)
    
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {threat_id} not found")
    
    prev_prob = threat.probability_curve.current_probability
    prev_stage = threat.intent_gradient.current_stage.value
    
    convergence_engine = ConvergenceEngine()
    threat = convergence_engine.recalculate_threat(threat_id)
    
    intent_engine = IntentGradientEngine()
    threat = intent_engine.recalculate_threat_gradient(threat_id)
    
    return RecalculateResponse(
        threat_id=threat_id,
        previous_probability=prev_prob,
        new_probability=threat.probability_curve.current_probability,
        previous_stage=prev_stage,
        new_stage=threat.intent_gradient.current_stage.value,
        message="Threat assessment recalculated successfully"
    )


@router.post("/feedback", response_model=FeedbackEntry)
async def submit_feedback(feedback_data: FeedbackCreate):
    """
    Submit human-in-the-loop feedback.
    
    Feedback types:
    - weight_adjustment: Adjust signal weights
    - stage_correction: Correct stage assessment
    - signal_validation: Validate/invalidate signals
    
    Feedback is logged but does not override historical data.
    """
    store = get_store()
    
    threat = store.get_threat(feedback_data.threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {feedback_data.threat_id} not found")
    
    valid_types = ["weight_adjustment", "stage_correction", "signal_validation", "confidence_adjustment"]
    if feedback_data.feedback_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid feedback_type. Must be one of: {valid_types}"
        )
    
    feedback = FeedbackEntry(
        analyst_id=feedback_data.analyst_id,
        threat_id=feedback_data.threat_id,
        feedback_type=feedback_data.feedback_type,
        original_value=feedback_data.original_value,
        adjusted_value=feedback_data.adjusted_value,
        rationale=feedback_data.rationale
    )
    
    store.add_feedback(feedback)
    
    return feedback


@router.get("/feedback/{threat_id}", response_model=list[FeedbackEntry])
async def get_threat_feedback(threat_id: str):
    """
    Get all feedback entries for a specific threat.
    """
    store = get_store()
    
    threat = store.get_threat(threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {threat_id} not found")
    
    feedback = store.get_feedback_for_threat(threat_id)
    
    return feedback


@router.get("/audit", response_model=AuditResponse)
async def get_audit_trail(
    limit: int = Query(100, ge=1, le=500, description="Maximum entries to return"),
    target_id: Optional[str] = Query(None, description="Filter by target object ID"),
    action_type: Optional[str] = Query(None, description="Filter by action type")
):
    """
    Get audit trail entries.
    
    Returns chronological log of all system actions for
    government-grade accountability and explainability.
    """
    store = get_store()
    
    entries = store.get_audit_trail(limit=limit, target_id=target_id)
    
    if action_type:
        entries = [e for e in entries if e.action_type == action_type]
    
    return AuditResponse(entries=entries, total=len(entries))


@router.get("/system/access-logs")
async def get_access_logs(
    limit: int = Query(100, ge=1, le=1000, description="Maximum entries to return")
):
    """
    Get access logs for all API requests.
    
    Returns timestamped log of all requests with:
    - Request ID
    - Timestamp
    - Method and path
    - Client IP
    - User agent
    - Response status
    - Processing time
    
    Required for government-grade accountability.
    """
    from app.main import access_logs
    
    logs = access_logs[-limit:] if len(access_logs) > limit else access_logs
    logs = list(reversed(logs))
    
    return {
        "logs": logs,
        "total": len(access_logs),
        "returned": len(logs)
    }


@router.get("/system/status")
async def get_system_status():
    """
    Get system status and statistics.
    """
    store = get_store()
    
    threats = store.get_all_threats()
    active_threats = [t for t in threats if t.status == "active"]
    
    critical_count = sum(
        1 for t in active_threats
        if t.current_nio and t.current_nio.monitoring_posture == MonitoringPosture.CRITICAL
    )
    heightened_count = sum(
        1 for t in active_threats
        if t.current_nio and t.current_nio.monitoring_posture == MonitoringPosture.HEIGHTENED
    )
    
    return {
        "status": "operational",
        "version": "1.0.0-mvp",
        "statistics": {
            "total_threats": len(threats),
            "active_threats": len(active_threats),
            "total_signals": len(store.signals),
            "total_nios": len(store.nios),
            "audit_entries": len(store.audit_entries),
            "feedback_entries": len(store.feedback_entries),
        },
        "alerts": {
            "critical_posture_count": critical_count,
            "heightened_posture_count": heightened_count,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


class JurisdictionListResponse(BaseModel):
    """Response model for jurisdiction list"""
    jurisdictions: list[JurisdictionSummary]
    total: int
    current_jurisdiction: str


class JurisdictionSetRequest(BaseModel):
    """Request model for setting jurisdiction"""
    code: str


@router.get("/jurisdictions", response_model=JurisdictionListResponse)
async def list_jurisdictions():
    """
    List all available jurisdiction contexts.
    
    IMPORTANT: Jurisdiction context adjusts signal interpretation, weighting,
    historical analogs, and narrative framing. It does NOT activate new data
    collection or imply active monitoring of individuals or regions.
    
    All signal ingestion remains abstracted and globally lawful.
    """
    store = get_store()
    jurisdictions = store.get_all_jurisdictions()
    current = store.get_current_jurisdiction()
    
    summaries = [
        JurisdictionSummary(
            code=j.code,
            name=j.name,
            region=j.region
        )
        for j in sorted(jurisdictions, key=lambda x: (x.region, x.name))
    ]
    
    return JurisdictionListResponse(
        jurisdictions=summaries,
        total=len(summaries),
        current_jurisdiction=current.code if current else "US"
    )


@router.get("/jurisdictions/current", response_model=JurisdictionContext)
async def get_current_jurisdiction():
    """
    Get the currently active jurisdiction context.
    
    Returns full jurisdiction context including:
    - Signal weight modifiers
    - Historical analog tags
    - Narrative context
    - Economic baseline
    """
    store = get_store()
    jurisdiction = store.get_current_jurisdiction()
    
    if not jurisdiction:
        raise HTTPException(status_code=404, detail="No jurisdiction context set")
    
    return jurisdiction


@router.get("/jurisdictions/{code}", response_model=JurisdictionContext)
async def get_jurisdiction(code: str):
    """
    Get a specific jurisdiction context by ISO 3166-1 alpha-2 code.
    """
    store = get_store()
    jurisdiction = store.get_jurisdiction(code.upper())
    
    if not jurisdiction:
        raise HTTPException(status_code=404, detail=f"Jurisdiction {code} not found")
    
    return jurisdiction


@router.post("/jurisdictions/current", response_model=JurisdictionContext)
async def set_current_jurisdiction(request: JurisdictionSetRequest):
    """
    Set the current jurisdiction context.
    
    IMPORTANT: This adjusts signal interpretation, weighting, historical analogs,
    and narrative framing. It does NOT activate new data collection or imply
    active monitoring of individuals or regions.
    
    All signal ingestion remains abstracted and globally lawful.
    
    The system is architected to allow phased expansion of jurisdiction-specific
    context models for government and Fortune-500 scalability.
    """
    store = get_store()
    jurisdiction = store.set_current_jurisdiction(request.code.upper())
    
    if not jurisdiction:
        raise HTTPException(
            status_code=404,
            detail=f"Jurisdiction {request.code} not found. Use GET /jurisdictions for available options."
        )
    
    return jurisdiction
