"""
AURORA™ Core Data Schemas
Patent-grade, government-ready intelligence platform schemas

These schemas define the core data structures for:
- Weak-Signal Convergence Engine
- Intent Gradient Modeling
- Narrative Intelligence Objects (NIOs)
- Audit Trail and Feedback Systems
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import uuid


class SignalDomain(str, Enum):
    """
    Signal domains for weak-signal convergence.
    Each domain represents a distinct category of observable indicators.
    """
    SOCIAL_DISCOURSE = "social_discourse"
    BEHAVIORAL_TREND = "behavioral_trend"
    ENVIRONMENTAL_STRESSOR = "environmental_stressor"


class SignalType(str, Enum):
    """
    Specific signal types within each domain.
    Provides granular categorization for correlation logic.
    """
    SENTIMENT_SHIFT = "sentiment_shift"
    TOPIC_EMERGENCE = "topic_emergence"
    NARRATIVE_AMPLIFICATION = "narrative_amplification"
    FREQUENCY_INCREASE = "frequency_increase"
    ESCALATION_PATTERN = "escalation_pattern"
    FIXATION_INDICATOR = "fixation_indicator"
    ECONOMIC_STRESS = "economic_stress"
    GEOGRAPHIC_CLUSTERING = "geographic_clustering"
    TEMPORAL_PATTERN = "temporal_pattern"
    NETWORK_EXPANSION = "network_expansion"


class IntentStage(str, Enum):
    """
    Intent Gradient stages for threat evolution modeling.
    Represents the progression from grievance to potential mobilization.
    """
    GRIEVANCE_FORMATION = "grievance_formation"
    COGNITIVE_FIXATION = "cognitive_fixation"
    BEHAVIORAL_ACCELERATION = "behavioral_acceleration"
    MOBILIZATION_RISK = "mobilization_risk"


class MonitoringPosture(str, Enum):
    """
    Suggested monitoring postures for threat objects.
    These are recommendations, not enforcement directives.
    """
    ROUTINE = "routine"
    ELEVATED = "elevated"
    HEIGHTENED = "heightened"
    CRITICAL = "critical"


class ConfidenceBound(BaseModel):
    """
    Confidence bounds for probability estimates.
    Provides uncertainty quantification for all assessments.
    """
    lower: float = Field(..., ge=0, le=100, description="Lower confidence bound (0-100)")
    upper: float = Field(..., ge=0, le=100, description="Upper confidence bound (0-100)")
    confidence_level: float = Field(default=0.95, description="Statistical confidence level")


class Signal(BaseModel):
    """
    Individual signal object for weak-signal convergence.
    Represents a single observable indicator from any domain.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    domain: SignalDomain
    signal_type: SignalType
    source_description: str = Field(..., description="Abstracted source description (no PII)")
    raw_confidence: float = Field(..., ge=0, le=1, description="Initial signal confidence (0-1)")
    weight: float = Field(default=1.0, ge=0, description="Signal weight for convergence calculation")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict = Field(default_factory=dict, description="Additional signal metadata")
    reasoning: str = Field(..., description="Explanation of why this signal is relevant")
    
    class Config:
        json_schema_extra = {
            "example": {
                "domain": "social_discourse",
                "signal_type": "sentiment_shift",
                "source_description": "Public forum sentiment analysis",
                "raw_confidence": 0.65,
                "weight": 1.2,
                "reasoning": "Detected 40% increase in negative sentiment toward target topic"
            }
        }


class SignalCreate(BaseModel):
    """Schema for creating new signals via API"""
    domain: SignalDomain
    signal_type: SignalType
    source_description: str
    raw_confidence: float = Field(..., ge=0, le=1)
    weight: float = Field(default=1.0, ge=0)
    metadata: dict = Field(default_factory=dict)
    reasoning: str


class HistoricalAnalog(BaseModel):
    """
    Historical analog for threat comparison.
    Provides context through similar past events.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Name/identifier of historical event")
    description: str = Field(..., description="Brief description of the analog")
    similarity_score: float = Field(..., ge=0, le=1, description="Similarity to current threat (0-1)")
    outcome: str = Field(..., description="What happened in the historical case")
    lessons_learned: str = Field(..., description="Key takeaways from the analog")
    date_range: str = Field(..., description="When the historical event occurred")


class IntentGradient(BaseModel):
    """
    Intent Gradient model for threat evolution tracking.
    Models threat progression as a continuous gradient, not binary states.
    """
    current_stage: IntentStage
    stage_confidence: float = Field(..., ge=0, le=1, description="Confidence in current stage assessment")
    velocity: float = Field(..., description="Rate of escalation (-1 to 1, negative = de-escalation)")
    acceleration: float = Field(default=0.0, description="Change in velocity over time")
    time_in_stage: float = Field(..., description="Hours spent in current stage")
    stage_history: list[dict] = Field(default_factory=list, description="History of stage transitions")
    
    stage_1_score: float = Field(default=0.0, ge=0, le=1, description="Grievance Formation score")
    stage_2_score: float = Field(default=0.0, ge=0, le=1, description="Cognitive Fixation score")
    stage_3_score: float = Field(default=0.0, ge=0, le=1, description="Behavioral Acceleration score")
    stage_4_score: float = Field(default=0.0, ge=0, le=1, description="Mobilization Risk score")


class ThreatProbabilityCurve(BaseModel):
    """
    Threat Probability Curve with confidence bounds.
    Core output of the Weak-Signal Convergence Engine.
    """
    current_probability: float = Field(..., ge=0, le=100, description="Current threat probability (0-100)")
    confidence_bounds: ConfidenceBound
    trend: str = Field(..., description="Trend direction: increasing, stable, decreasing")
    trend_velocity: float = Field(..., description="Rate of probability change per hour")
    convergence_score: float = Field(..., ge=0, le=1, description="Strength of signal convergence")
    contributing_signals: int = Field(..., description="Number of signals contributing to assessment")
    domain_coverage: dict[str, int] = Field(default_factory=dict, description="Signal count by domain")
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    history: list[dict] = Field(default_factory=list, description="Historical probability values")


class NarrativeIntelligenceObject(BaseModel):
    """
    Narrative Intelligence Object (NIO) - PATENT CORE
    AI-generated intelligence narrative for decision support.
    Replaces dashboards with decision-ready intelligence.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    threat_id: str = Field(..., description="Associated threat object ID")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    
    executive_summary: str = Field(..., description="Plain-language summary (executive-readable)")
    why_it_matters: str = Field(..., description="Significance and potential impact")
    converged_signals: list[str] = Field(..., description="List of signals that converged")
    signal_narrative: str = Field(..., description="Narrative explanation of signal convergence")
    
    confidence_level: float = Field(..., ge=0, le=100, description="Overall confidence (0-100)")
    confidence_explanation: str = Field(..., description="Why we have this confidence level")
    
    known_unknowns: list[str] = Field(..., description="Acknowledged gaps in intelligence")
    assumptions: list[str] = Field(..., description="Key assumptions underlying the assessment")
    
    monitoring_posture: MonitoringPosture
    posture_rationale: str = Field(..., description="Why this monitoring posture is recommended")
    
    recommended_actions: list[str] = Field(default_factory=list, description="Suggested next steps")
    
    reasoning_chain: list[str] = Field(..., description="Step-by-step reasoning for audit trail")
    
    version: int = Field(default=1, description="NIO version number")


class ThreatObject(BaseModel):
    """
    Core Threat Object schema.
    Represents an emerging threat with full intelligence context.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    name: str = Field(..., description="Threat identifier/name")
    description: str = Field(..., description="Brief threat description")
    category: str = Field(..., description="Threat category")
    
    signals: list[Signal] = Field(default_factory=list, description="Contributing signals")
    probability_curve: ThreatProbabilityCurve
    intent_gradient: IntentGradient
    
    historical_analogs: list[HistoricalAnalog] = Field(default_factory=list)
    
    current_nio: Optional[NarrativeIntelligenceObject] = None
    nio_history: list[str] = Field(default_factory=list, description="Previous NIO IDs")
    
    region_context: Optional[dict] = Field(default=None, description="Phase 2: Region-Aware Intelligence context")
    escalation_pathway: Optional[dict] = Field(default=None, description="Phase 2: Escalation Pathway model")
    threat_class_alignment: Optional[dict] = Field(default=None, description="Probabilistic Threat Class Alignment result")
    
    status: str = Field(default="active", description="Threat status: active, resolved, archived")
    
    audit_trail: list[str] = Field(default_factory=list, description="Audit entry IDs")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Economic Stress Indicator Cluster",
                "description": "Convergence of economic stress signals in target region",
                "category": "socioeconomic"
            }
        }


class ThreatCreate(BaseModel):
    """Schema for creating new threat objects via API"""
    name: str
    description: str
    category: str


class AuditEntry(BaseModel):
    """
    Audit trail entry for government-grade accountability.
    Every system action is logged with full context.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    action_type: str = Field(..., description="Type of action performed")
    actor: str = Field(..., description="System component or user that performed action")
    target_type: str = Field(..., description="Type of object affected")
    target_id: str = Field(..., description="ID of affected object")
    
    before_state: Optional[dict] = Field(None, description="State before action")
    after_state: Optional[dict] = Field(None, description="State after action")
    
    reasoning: str = Field(..., description="Why this action was taken")
    metadata: dict = Field(default_factory=dict)


class FeedbackEntry(BaseModel):
    """
    Human-in-the-loop feedback entry.
    Allows analysts to adjust system behavior without overriding history.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    analyst_id: str = Field(..., description="Analyst identifier")
    threat_id: str = Field(..., description="Associated threat object")
    
    feedback_type: str = Field(..., description="Type: weight_adjustment, stage_correction, signal_validation")
    
    original_value: Optional[float] = None
    adjusted_value: Optional[float] = None
    
    rationale: str = Field(..., description="Analyst's reasoning for feedback")
    
    applied: bool = Field(default=False, description="Whether feedback has been applied")
    applied_at: Optional[datetime] = None


class FeedbackCreate(BaseModel):
    """Schema for submitting feedback via API"""
    analyst_id: str
    threat_id: str
    feedback_type: str
    original_value: Optional[float] = None
    adjusted_value: Optional[float] = None
    rationale: str


class ThreatSummary(BaseModel):
    """Lightweight threat summary for list views"""
    id: str
    name: str
    category: str
    current_probability: float
    intent_stage: IntentStage
    monitoring_posture: MonitoringPosture
    signal_count: int
    updated_at: datetime


class JurisdictionContext(BaseModel):
    """
    Jurisdiction Context for signal interpretation and narrative framing.
    
    IMPORTANT: This adjusts signal interpretation, weighting, historical analogs,
    and narrative framing. It does NOT activate new data collection or imply
    active monitoring of individuals or regions.
    
    All signal ingestion remains abstracted and globally lawful.
    
    Architecture supports phased expansion of jurisdiction-specific context models.
    """
    code: str = Field(..., description="ISO 3166-1 alpha-2 country code")
    name: str = Field(..., description="Country/jurisdiction name")
    region: str = Field(..., description="Geographic region")
    
    signal_weight_modifiers: dict[str, float] = Field(
        default_factory=dict,
        description="Domain-specific weight adjustments for this jurisdiction"
    )
    
    historical_analog_tags: list[str] = Field(
        default_factory=list,
        description="Tags for filtering relevant historical analogs"
    )
    
    narrative_context: dict[str, str] = Field(
        default_factory=dict,
        description="Jurisdiction-specific narrative framing elements"
    )
    
    economic_baseline: dict[str, float] = Field(
        default_factory=dict,
        description="Economic stress baseline indicators for normalization"
    )
    
    cultural_context_notes: list[str] = Field(
        default_factory=list,
        description="Non-attributive cultural context for signal interpretation"
    )
    
    legal_framework_notes: list[str] = Field(
        default_factory=list,
        description="Relevant legal/regulatory context for narrative framing"
    )
    
    is_active: bool = Field(default=True, description="Whether this jurisdiction context is active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "US",
                "name": "United States",
                "region": "North America",
                "signal_weight_modifiers": {
                    "economic_stress": 1.0,
                    "social_discourse": 1.0
                },
                "historical_analog_tags": ["north_america", "developed_economy"],
                "narrative_context": {
                    "governance_type": "Federal Republic",
                    "economic_classification": "Developed"
                }
            }
        }


class JurisdictionSummary(BaseModel):
    """Lightweight jurisdiction summary for dropdown selection"""
    code: str
    name: str
    region: str


class RegionGranularity(str, Enum):
    """
    Region granularity levels for authorized drill-down.
    Macro → Sub-region progression without precise geolocation.
    """
    MACRO = "macro"
    REGIONAL = "regional"
    SUB_REGIONAL = "sub_regional"


class RegionContext(BaseModel):
    """
    Region-Aware Intelligence - Safe "Where"
    
    Abstracted geographic context layer that:
    - Identifies primary and secondary regions (e.g., multi-state, metro-adjacent, regional corridors)
    - Avoids exact locations, maps, or pinpoint coordinates
    - Includes confidence scoring for regional attribution
    
    POLICY-SAFE: No precise geolocation, no map pins, no targeting.
    """
    primary_region: str = Field(..., description="Primary abstracted region (e.g., 'Midwest Corridor', 'Northeast Metro-Adjacent')")
    secondary_regions: list[str] = Field(default_factory=list, description="Secondary/adjacent regions of relevance")
    region_type: str = Field(..., description="Region classification (e.g., 'multi-state', 'metro-adjacent', 'regional corridor')")
    
    attribution_confidence: float = Field(..., ge=0, le=1, description="Confidence in regional attribution (0-1)")
    attribution_rationale: str = Field(..., description="Explanation of regional attribution logic")
    
    population_scale: str = Field(default="unspecified", description="Abstracted population scale (e.g., 'large metro', 'mid-size regional', 'rural corridor')")
    economic_profile: str = Field(default="unspecified", description="Abstracted economic profile (e.g., 'manufacturing-dependent', 'service-economy', 'mixed')")
    
    granularity_level: RegionGranularity = Field(default=RegionGranularity.MACRO, description="Current drill-down granularity level")
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "Region context is abstracted and non-targeting",
            "No precise coordinates or map pins are provided",
            "Regional attribution is pattern-based, not surveillance-derived"
        ],
        description="Policy compliance notes"
    )


class EscalationPathwayStage(BaseModel):
    """Individual stage within an escalation pathway"""
    stage_name: str = Field(..., description="Stage name in the pathway")
    stage_description: str = Field(..., description="Description of this stage")
    typical_indicators: list[str] = Field(default_factory=list, description="Typical indicators at this stage")
    typical_duration_hours: tuple[float, float] = Field(default=(24, 168), description="Typical duration range (min, max hours)")
    transition_triggers: list[str] = Field(default_factory=list, description="What typically triggers transition to next stage")


class EscalationPathway(BaseModel):
    """
    Escalation Pathway Modeling - Safe "How"
    
    Pattern-based escalation pathway that:
    - Shows how signals typically progress from structural stress → discourse → behavior → mobilization
    - Indicates current position within the pathway
    - Estimates projected progression windows using uncertainty bounds
    
    DECISION SUPPORT ONLY: Not predictive of specific actors or events.
    """
    pathway_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    pathway_name: str = Field(..., description="Name of the escalation pathway pattern")
    pathway_description: str = Field(..., description="Description of this pathway type")
    
    stages: list[EscalationPathwayStage] = Field(default_factory=list, description="Ordered stages in the pathway")
    
    current_stage_index: int = Field(default=0, ge=0, description="Current position in pathway (0-indexed)")
    stage_entry_time: datetime = Field(default_factory=datetime.utcnow, description="When current stage was entered")
    
    progression_probability: float = Field(..., ge=0, le=1, description="Probability of progressing to next stage")
    regression_probability: float = Field(..., ge=0, le=1, description="Probability of regressing to previous stage")
    
    projected_progression_window: tuple[float, float] = Field(
        default=(24, 168),
        description="Projected time window for next stage transition (min, max hours) with uncertainty"
    )
    projection_confidence: float = Field(default=0.5, ge=0, le=1, description="Confidence in progression projection")
    
    historical_pattern_matches: list[str] = Field(default_factory=list, description="Historical patterns this matches")
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "Pathway modeling is pattern-based, not predictive of specific incidents",
            "Projections are for decision support only, not forecasting",
            "No individual actors or specific events are predicted"
        ],
        description="Policy compliance notes"
    )


class DrillDownPermission(str, Enum):
    """Authorization levels for drill-down access"""
    BASIC = "basic"
    ANALYST = "analyst"
    SENIOR_ANALYST = "senior_analyst"
    SUPERVISOR = "supervisor"


class DrillDownRequest(BaseModel):
    """
    Authorized Drill-Down Logic - Safe "When"
    
    Role-based drill-down controls that:
    - Allow authorized users to refine region granularity (macro → sub-region)
    - Allow deeper signal class inspection without exposing raw data or identities
    - Surface timing sensitivity and acceleration indicators
    
    NEVER exposes: personal identifiers, raw content, or enforcement triggers.
    """
    threat_id: str = Field(..., description="Threat object to drill down on")
    user_role: DrillDownPermission = Field(..., description="User's authorization level")
    
    requested_region_granularity: Optional[RegionGranularity] = Field(None, description="Requested region detail level")
    requested_signal_depth: Optional[str] = Field(None, description="Requested signal inspection depth: 'summary', 'detailed', 'full_abstracted'")
    requested_timing_detail: bool = Field(default=False, description="Request timing sensitivity indicators")
    
    rationale: str = Field(..., description="Reason for drill-down request (logged for audit)")


class DrillDownResponse(BaseModel):
    """Response to an authorized drill-down request"""
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    threat_id: str
    authorized: bool = Field(..., description="Whether the request was authorized")
    authorization_level: DrillDownPermission
    
    region_detail: Optional[RegionContext] = Field(None, description="Refined region context if authorized")
    
    signal_detail: Optional[dict] = Field(None, description="Abstracted signal detail if authorized")
    
    timing_indicators: Optional[dict] = Field(None, description="Timing sensitivity indicators if authorized")
    
    redacted_fields: list[str] = Field(default_factory=list, description="Fields that were redacted due to authorization level")
    
    audit_note: str = Field(..., description="Audit trail note for this drill-down")
    
    policy_compliance: list[str] = Field(
        default_factory=lambda: [
            "No personal identifiers exposed",
            "No raw content provided",
            "No enforcement triggers included",
            "All data remains abstracted and non-attributive"
        ],
        description="Policy compliance confirmation"
    )


class ThreatClassCategory(str, Enum):
    """
    Probabilistic Threat Class Taxonomy - Analytic Categories Only
    
    These are analytic pattern categories, NOT criminal labels or accusations.
    Classes are non-exclusive and probabilistic.
    
    POLICY-SAFE: No enforcement framing, no identity attribution.
    """
    SOCIOECONOMIC_INSTABILITY = "socioeconomic_instability"
    CIVIL_UNREST_PROTEST = "civil_unrest_protest"
    IDEOLOGICAL_MOBILIZATION = "ideological_mobilization"
    LONE_ACTOR_GRIEVANCE = "lone_actor_grievance"
    INSIDER_GRIEVANCE_DISRUPTION = "insider_grievance_disruption"
    CYBER_PHYSICAL_CONVERGENCE = "cyber_physical_convergence"
    INFRASTRUCTURE_DISRUPTION = "infrastructure_disruption"
    COORDINATED_DISINFORMATION = "coordinated_disinformation"


class ThreatClassAlignment(BaseModel):
    """
    Individual threat class alignment with probabilistic weighting.
    
    Represents analytic pattern similarity, not prediction or accusation.
    """
    class_category: ThreatClassCategory = Field(..., description="Analytic threat class category")
    alignment_score: float = Field(..., ge=0, le=1, description="Probabilistic alignment score (0-1)")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in this alignment")
    
    primary_contributing_domains: list[str] = Field(
        default_factory=list, 
        description="Signal domains contributing to this alignment"
    )
    intent_stage_influence: float = Field(
        default=0.0, ge=0, le=1,
        description="How much intent stage influenced this alignment"
    )
    escalation_pathway_influence: float = Field(
        default=0.0, ge=0, le=1,
        description="How much escalation pathway influenced this alignment"
    )
    velocity_influence: float = Field(
        default=0.0, ge=0, le=1,
        description="How much temporal velocity influenced this alignment"
    )
    
    rationale: str = Field(..., description="Explainable rationale for this alignment")
    
    class Config:
        json_schema_extra = {
            "example": {
                "class_category": "socioeconomic_instability",
                "alignment_score": 0.72,
                "confidence": 0.68,
                "primary_contributing_domains": ["environmental_stressor", "social_discourse"],
                "intent_stage_influence": 0.35,
                "escalation_pathway_influence": 0.25,
                "velocity_influence": 0.15,
                "rationale": "Signal composition shows strong economic stress indicators combined with grievance discourse patterns typical of socioeconomic instability scenarios."
            }
        }


class ThreatClassAlignmentResult(BaseModel):
    """
    Probabilistic Threat Class Alignment - Complete Result
    
    Expresses what category of threat a pattern most closely resembles
    using probabilistic analytic alignment.
    
    CRITICAL CONSTRAINTS:
    - NOT definitive labels, accusations, or enforcement framing
    - Pre-incident, non-investigative, non-attributive
    - Multiple classes may be active simultaneously
    - Percentages are relative likelihoods, not predictions
    - No single class is required to reach 100%
    """
    threat_id: str = Field(..., description="Associated threat object ID")
    
    alignments: list[ThreatClassAlignment] = Field(
        default_factory=list,
        description="Ordered list of class alignments (highest score first)"
    )
    
    top_alignment: Optional[ThreatClassCategory] = Field(
        None, description="Highest-scoring class category"
    )
    
    alignment_diversity: float = Field(
        default=0.0, ge=0, le=1,
        description="How distributed alignments are across classes (0=concentrated, 1=diverse)"
    )
    
    intent_stage_at_computation: str = Field(
        ..., description="Intent stage when alignment was computed"
    )
    escalation_stage_at_computation: int = Field(
        default=0, description="Escalation pathway stage when alignment was computed"
    )
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    disclaimer: str = Field(
        default="Class alignment reflects analytic pattern similarity and may evolve as new signals emerge. These are probabilistic assessments, not predictions or accusations.",
        description="Required disclaimer for all class alignment outputs"
    )
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "Class alignments are analytic pattern similarities only",
            "No identity attribution or individual labeling",
            "No prediction of specific events or actions",
            "No law-enforcement or investigative framing",
            "Maintains pre-incident decision-intelligence posture"
        ],
        description="Policy compliance notes"
    )
