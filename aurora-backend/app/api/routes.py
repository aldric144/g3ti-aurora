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
    RegionGranularity,
    DrillDownPermission,
    DrillDownRequest,
    DrillDownResponse,
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
    
    CRITICAL DISTINCTION:
    - United States: Real operational context with full decision intelligence
    - Non-US Jurisdictions: Synthetic demonstration data ONLY for architectural validation
    
    IMPORTANT: Jurisdiction context adjusts signal interpretation, weighting,
    historical analogs, and narrative framing. It does NOT activate new data
    collection or imply active monitoring of individuals or regions.
    
    All signal ingestion remains abstracted and globally lawful.
    
    SEED LIMITS: 10 non-US jurisdictions + 1 United States (maximum 12 non-US)
    """
    store = get_store()
    jurisdictions = store.get_all_jurisdictions()
    current = store.get_current_jurisdiction()
    
    summaries = [
        JurisdictionSummary(
            code=j.code,
            name=j.name,
            region=j.region,
            is_synthetic=j.is_synthetic,
            is_operational=j.is_operational
        )
        for j in sorted(jurisdictions, key=lambda x: (not x.is_operational, x.region, x.name))
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


@router.post("/threats/{threat_id}/drilldown", response_model=DrillDownResponse)
async def drill_down_threat(threat_id: str, request: DrillDownRequest):
    """
    Authorized Drill-Down Logic - Safe "When"
    
    Role-based drill-down controls that:
    - Allow authorized users to refine region granularity (macro → sub-region)
    - Allow deeper signal class inspection without exposing raw data or identities
    - Surface timing sensitivity and acceleration indicators
    
    NEVER exposes: personal identifiers, raw content, or enforcement triggers.
    
    Authorization levels:
    - BASIC: Summary-level access only
    - ANALYST: Regional detail + signal summaries
    - SENIOR_ANALYST: Sub-regional + detailed signals + timing
    - SUPERVISOR: Full abstracted access
    
    All drill-down requests are logged for audit trail.
    """
    store = get_store()
    threat = store.get_threat(threat_id)
    
    if not threat:
        raise HTTPException(status_code=404, detail=f"Threat {threat_id} not found")
    
    authorization_map = {
        DrillDownPermission.BASIC: {
            "max_region_granularity": RegionGranularity.MACRO,
            "max_signal_depth": "summary",
            "timing_access": False
        },
        DrillDownPermission.ANALYST: {
            "max_region_granularity": RegionGranularity.REGIONAL,
            "max_signal_depth": "detailed",
            "timing_access": False
        },
        DrillDownPermission.SENIOR_ANALYST: {
            "max_region_granularity": RegionGranularity.SUB_REGIONAL,
            "max_signal_depth": "detailed",
            "timing_access": True
        },
        DrillDownPermission.SUPERVISOR: {
            "max_region_granularity": RegionGranularity.SUB_REGIONAL,
            "max_signal_depth": "full_abstracted",
            "timing_access": True
        }
    }
    
    auth_level = authorization_map.get(request.user_role, authorization_map[DrillDownPermission.BASIC])
    redacted_fields = []
    
    region_detail = None
    if request.requested_region_granularity and threat.region_context:
        granularity_order = [RegionGranularity.MACRO, RegionGranularity.REGIONAL, RegionGranularity.SUB_REGIONAL]
        requested_idx = granularity_order.index(request.requested_region_granularity)
        max_idx = granularity_order.index(auth_level["max_region_granularity"])
        
        if requested_idx <= max_idx:
            region_detail = threat.region_context.copy()
            region_detail["granularity_level"] = request.requested_region_granularity.value
            
            if request.requested_region_granularity == RegionGranularity.REGIONAL:
                region_detail["detail_note"] = "Regional-level detail: Multi-state corridor with adjacent zone context"
            elif request.requested_region_granularity == RegionGranularity.SUB_REGIONAL:
                region_detail["detail_note"] = "Sub-regional detail: Metro-adjacent zones with economic profile segmentation"
        else:
            redacted_fields.append(f"region_granularity_{request.requested_region_granularity.value}")
    
    signal_detail = None
    if request.requested_signal_depth:
        depth_order = ["summary", "detailed", "full_abstracted"]
        requested_idx = depth_order.index(request.requested_signal_depth) if request.requested_signal_depth in depth_order else 0
        max_idx = depth_order.index(auth_level["max_signal_depth"])
        
        if requested_idx <= max_idx:
            signal_detail = {
                "depth_level": request.requested_signal_depth,
                "signal_count": len(threat.signals),
                "domain_breakdown": threat.probability_curve.domain_coverage,
                "convergence_score": threat.probability_curve.convergence_score,
                "signal_classes": []
            }
            
            for signal in threat.signals:
                signal_info = {
                    "domain": signal.domain.value if hasattr(signal.domain, 'value') else signal.domain,
                    "type": signal.signal_type.value if hasattr(signal.signal_type, 'value') else signal.signal_type,
                    "confidence": signal.raw_confidence,
                    "weight": signal.weight
                }
                
                if request.requested_signal_depth in ["detailed", "full_abstracted"]:
                    signal_info["reasoning"] = signal.reasoning
                    signal_info["source_description"] = signal.source_description
                
                signal_detail["signal_classes"].append(signal_info)
        else:
            redacted_fields.append(f"signal_depth_{request.requested_signal_depth}")
    
    timing_indicators = None
    if request.requested_timing_detail:
        if auth_level["timing_access"]:
            timing_indicators = {
                "velocity": threat.intent_gradient.velocity,
                "acceleration": threat.intent_gradient.acceleration,
                "time_in_current_stage_hours": threat.intent_gradient.time_in_stage,
                "stage_confidence": threat.intent_gradient.stage_confidence,
                "trend": threat.probability_curve.trend,
                "trend_velocity": threat.probability_curve.trend_velocity,
                "sensitivity_assessment": "elevated" if threat.intent_gradient.velocity > 0.2 else "moderate" if threat.intent_gradient.velocity > 0 else "stable",
                "acceleration_indicator": "accelerating" if threat.intent_gradient.acceleration > 0 else "decelerating" if threat.intent_gradient.acceleration < 0 else "steady"
            }
            
            if threat.escalation_pathway:
                timing_indicators["projected_progression_window_hours"] = threat.escalation_pathway.get("projected_progression_window", [72, 240])
                timing_indicators["projection_confidence"] = threat.escalation_pathway.get("projection_confidence", 0.5)
        else:
            redacted_fields.append("timing_indicators")
    
    audit_note = f"Drill-down request by {request.user_role.value} for threat {threat_id}. " \
                 f"Requested: region={request.requested_region_granularity}, " \
                 f"signal_depth={request.requested_signal_depth}, " \
                 f"timing={request.requested_timing_detail}. " \
                 f"Rationale: {request.rationale}"
    
    store._log_audit(
        action_type="drill_down_request",
        actor=f"user:{request.user_role.value}",
        target_type="threat",
        target_id=threat_id,
        reasoning=audit_note,
        metadata={
            "user_role": request.user_role.value,
            "requested_region_granularity": request.requested_region_granularity.value if request.requested_region_granularity else None,
            "requested_signal_depth": request.requested_signal_depth,
            "requested_timing_detail": request.requested_timing_detail,
            "redacted_fields": redacted_fields
        }
    )
    
    return DrillDownResponse(
        threat_id=threat_id,
        authorized=True,
        authorization_level=request.user_role,
        region_detail=region_detail,
        signal_detail=signal_detail,
        timing_indicators=timing_indicators,
        redacted_fields=redacted_fields,
        audit_note=audit_note,
        policy_compliance=[
            "No personal identifiers exposed",
            "No raw content provided",
            "No enforcement triggers included",
            "All data remains abstracted and non-attributive"
        ]
    )
