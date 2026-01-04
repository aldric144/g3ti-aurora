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
    decision_advantage_layer: Optional[dict] = Field(default=None, description="Phase 3: Decision Advantage Layer")
    
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


class GovernancePosture(str, Enum):
    """
    Governance posture classification for jurisdiction context.
    Used for decision pathway adjustment, not intelligence assessment.
    """
    CENTRALIZED = "centralized"
    DECENTRALIZED = "decentralized"
    FEDERAL = "federal"
    UNITARY = "unitary"


class AuthorityEmphasis(str, Enum):
    """
    Authority emphasis classification for jurisdiction context.
    Affects decision pathway phrasing and tone.
    """
    CIVIL = "civil"
    ADMINISTRATIVE = "administrative"
    MIXED = "mixed"


class JurisdictionContext(BaseModel):
    """
    Jurisdiction Context for signal interpretation and narrative framing.
    
    IMPORTANT: This adjusts signal interpretation, weighting, historical analogs,
    and narrative framing. It does NOT activate new data collection or imply
    active monitoring of individuals or regions.
    
    All signal ingestion remains abstracted and globally lawful.
    
    Architecture supports phased expansion of jurisdiction-specific context models.
    
    CRITICAL DISTINCTION:
    - United States: Real operational context with full decision intelligence
    - Non-US Jurisdictions: Synthetic demonstration data ONLY for architectural validation
    """
    code: str = Field(..., description="ISO 3166-1 alpha-2 country code")
    name: str = Field(..., description="Country/jurisdiction name")
    region: str = Field(..., description="Geographic region")
    
    is_synthetic: bool = Field(
        default=False,
        description="True for non-US jurisdictions using synthetic demonstration data"
    )
    
    is_operational: bool = Field(
        default=False,
        description="True only for United States - real operational context"
    )
    
    governance_posture: GovernancePosture = Field(
        default=GovernancePosture.FEDERAL,
        description="Governance structure classification"
    )
    
    authority_emphasis: AuthorityEmphasis = Field(
        default=AuthorityEmphasis.MIXED,
        description="Civil vs administrative authority emphasis"
    )
    
    public_communication_norm: str = Field(
        default="balanced",
        description="Public communication norms (transparent, reserved, balanced)"
    )
    
    escalation_sensitivity: str = Field(
        default="moderate",
        description="Policy-level escalation sensitivity (low, moderate, high)"
    )
    
    decision_pathway_adjustments: dict[str, str] = Field(
        default_factory=dict,
        description="Jurisdiction-specific pathway phrasing and tone adjustments"
    )
    
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
    
    synthetic_disclaimer: str = Field(
        default="",
        description="Disclaimer text for synthetic non-US jurisdictions"
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
    is_synthetic: bool = False
    is_operational: bool = False


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


class DecisionPathwayCategory(str, Enum):
    """
    Decision Pathway Categories - Advisory Only
    
    These are non-enforcement decision pathway categories for leadership guidance.
    All pathways are optional, advisory, and proportional.
    
    POLICY-SAFE: No enforcement, tactical, or investigative framing.
    """
    ECONOMIC_ENGAGEMENT = "economic_engagement"
    COMMUNITY_OUTREACH = "community_outreach"
    COMMUNICATIONS_STRATEGY = "communications_strategy"
    STAKEHOLDER_COORDINATION = "stakeholder_coordination"
    RESOURCE_POSITIONING = "resource_positioning"
    MONITORING_ADJUSTMENT = "monitoring_adjustment"
    INSTITUTIONAL_RESILIENCE = "institutional_resilience"
    INTERAGENCY_LIAISON = "interagency_liaison"


class DecisionPathwayRelevance(str, Enum):
    """Relevance ranking for decision pathways"""
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


class DecisionPathway(BaseModel):
    """
    Individual Decision Pathway with advisory guidance.
    
    Maps current threat patterns to decision pathway categories.
    All guidance is optional, advisory, and proportional.
    
    EXPLICITLY AVOIDS: Enforcement, tactical instruction, investigative framing.
    """
    pathway_category: DecisionPathwayCategory = Field(..., description="Decision pathway category")
    relevance: DecisionPathwayRelevance = Field(..., description="Relevance ranking")
    relevance_score: float = Field(..., ge=0, le=1, description="Numeric relevance score (0-1)")
    
    advisory_summary: str = Field(..., description="Brief advisory summary for this pathway")
    
    suggested_considerations: list[str] = Field(
        default_factory=list,
        description="Optional considerations for leadership (not directives)"
    )
    
    proportionality_note: str = Field(
        ..., description="Note on proportional response considerations"
    )
    
    contributing_factors: list[str] = Field(
        default_factory=list,
        description="Threat factors that make this pathway relevant"
    )
    
    confidence: float = Field(..., ge=0, le=1, description="Confidence in pathway relevance")


class DecisionPathwayIntelligence(BaseModel):
    """
    Decision Pathway Intelligence - Phase 3 Component 1
    
    Advisory layer that maps current threat patterns to decision pathway categories.
    Provides leadership with early, proportional, non-enforcement decision guidance.
    
    CRITICAL CONSTRAINTS:
    - All guidance is optional and advisory
    - No enforcement or tactical instruction
    - Proportional to assessed risk level
    - Pre-incident decision support only
    """
    threat_id: str = Field(..., description="Associated threat object ID")
    
    pathways: list[DecisionPathway] = Field(
        default_factory=list,
        description="Ranked decision pathways by relevance"
    )
    
    primary_pathway: Optional[DecisionPathwayCategory] = Field(
        None, description="Highest-relevance pathway category"
    )
    
    overall_advisory_posture: str = Field(
        ..., description="Overall advisory posture summary"
    )
    
    proportionality_assessment: str = Field(
        ..., description="Assessment of proportional response considerations"
    )
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    disclaimer: str = Field(
        default="Decision pathways are advisory and optional. All guidance is proportional to assessed patterns and does not constitute enforcement direction or tactical instruction.",
        description="Required disclaimer"
    )
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "All pathways are optional and advisory",
            "No enforcement or tactical instruction provided",
            "Guidance is proportional to assessed risk patterns",
            "Leadership retains full decision authority",
            "Pre-incident decision support only"
        ],
        description="Policy compliance notes"
    )


class ImpactDomain(str, Enum):
    """
    Impact domains for system-level forecasting.
    Focuses on institutional and community outcomes.
    """
    INSTITUTIONAL_TRUST = "institutional_trust"
    COMMUNITY_STABILITY = "community_stability"
    OPERATIONAL_CONTINUITY = "operational_continuity"
    ECONOMIC_RESILIENCE = "economic_resilience"
    SOCIAL_COHESION = "social_cohesion"
    INFRASTRUCTURE_INTEGRITY = "infrastructure_integrity"


class ImpactProjection(BaseModel):
    """
    Individual impact projection for a specific domain.
    
    Estimates consequences if current trajectories persist.
    Focuses on institutional and community outcomes.
    """
    domain: ImpactDomain = Field(..., description="Impact domain")
    
    current_assessment: str = Field(..., description="Current state assessment")
    
    projected_trajectory: str = Field(
        ..., description="Projected trajectory if current patterns persist"
    )
    
    impact_severity: str = Field(
        ..., description="Projected impact severity: minimal, moderate, significant, substantial"
    )
    impact_severity_score: float = Field(..., ge=0, le=1, description="Numeric severity score")
    
    time_horizon_hours: tuple[float, float] = Field(
        ..., description="Time horizon for projection (min, max hours)"
    )
    
    confidence: float = Field(..., ge=0, le=1, description="Confidence in projection")
    confidence_band: tuple[float, float] = Field(
        ..., description="Confidence band (lower, upper) for severity score"
    )
    
    key_assumptions: list[str] = Field(
        default_factory=list,
        description="Key assumptions underlying this projection"
    )
    
    mitigating_factors: list[str] = Field(
        default_factory=list,
        description="Factors that could reduce projected impact"
    )


class ImpactForecast(BaseModel):
    """
    Impact Forecasting - Phase 3 Component 2
    
    System-level impact projection that estimates consequences
    if current trajectories persist.
    
    CRITICAL CONSTRAINTS:
    - Focuses on institutional and community outcomes
    - Includes time horizons and confidence bands
    - Avoids predicting specific events or actors
    - System-level only, not individual-level
    """
    threat_id: str = Field(..., description="Associated threat object ID")
    
    projections: list[ImpactProjection] = Field(
        default_factory=list,
        description="Impact projections by domain"
    )
    
    overall_impact_assessment: str = Field(
        ..., description="Overall system-level impact assessment"
    )
    
    primary_concern_domain: Optional[ImpactDomain] = Field(
        None, description="Domain with highest projected impact"
    )
    
    aggregate_severity_score: float = Field(
        ..., ge=0, le=1, description="Aggregate severity across all domains"
    )
    
    projection_time_horizon: str = Field(
        ..., description="Overall time horizon for projections"
    )
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    disclaimer: str = Field(
        default="Impact projections are system-level estimates based on current trajectory patterns. They do not predict specific events, actors, or outcomes. All projections include uncertainty bounds.",
        description="Required disclaimer"
    )
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "Projections focus on institutional and community outcomes",
            "No prediction of specific events or actors",
            "All projections include confidence bands and time horizons",
            "System-level analysis only, not individual attribution",
            "For decision support, not operational forecasting"
        ],
        description="Policy compliance notes"
    )


class AuthorityDomain(str, Enum):
    """
    Leadership/authority domains for recommendation alignment.
    Identifies which domains are best positioned to respond.
    
    POLICY-SAFE: No naming of individuals, units, or enforcement targets.
    """
    EXECUTIVE_LEADERSHIP = "executive_leadership"
    OPERATIONS_MANAGEMENT = "operations_management"
    COMMUNICATIONS_PUBLIC_AFFAIRS = "communications_public_affairs"
    COMMUNITY_RELATIONS = "community_relations"
    RISK_MANAGEMENT = "risk_management"
    LEGAL_COMPLIANCE = "legal_compliance"
    HUMAN_RESOURCES = "human_resources"
    EXTERNAL_AFFAIRS = "external_affairs"
    STRATEGIC_PLANNING = "strategic_planning"
    INTERAGENCY_COORDINATION = "interagency_coordination"


class AuthorityRecommendation(BaseModel):
    """
    Individual authority-aware recommendation.
    
    Identifies which leadership domains are best positioned to respond
    without naming individuals, units, or enforcement targets.
    """
    authority_domain: AuthorityDomain = Field(..., description="Leadership domain")
    
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance to current threat pattern")
    
    positioning_rationale: str = Field(
        ..., description="Why this domain is well-positioned to respond"
    )
    
    suggested_awareness_areas: list[str] = Field(
        default_factory=list,
        description="Areas this domain should be aware of (not directives)"
    )
    
    coordination_considerations: list[str] = Field(
        default_factory=list,
        description="Considerations for coordination with other domains"
    )
    
    context_applicability: list[str] = Field(
        default_factory=list,
        description="Contexts where this applies: government, enterprise, multi-agency"
    )
    
    confidence: float = Field(..., ge=0, le=1, description="Confidence in recommendation")


class AuthorityAwareRecommendations(BaseModel):
    """
    Authority-Aware Recommendation Layer - Phase 3 Component 3
    
    Role/domain alignment model that identifies which leadership domains
    are best positioned to respond.
    
    CRITICAL CONSTRAINTS:
    - No naming of individuals, units, or enforcement targets
    - Supports government, enterprise, and multi-agency contexts
    - Advisory only, not directive
    - Domain-level, not person-level
    """
    threat_id: str = Field(..., description="Associated threat object ID")
    
    recommendations: list[AuthorityRecommendation] = Field(
        default_factory=list,
        description="Authority-aware recommendations by domain"
    )
    
    primary_authority_domain: Optional[AuthorityDomain] = Field(
        None, description="Domain with highest relevance"
    )
    
    coordination_summary: str = Field(
        ..., description="Summary of cross-domain coordination considerations"
    )
    
    context_applicability: str = Field(
        ..., description="Applicable contexts: government, enterprise, multi-agency, or all"
    )
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    disclaimer: str = Field(
        default="Authority recommendations identify leadership domains, not individuals or units. All recommendations are advisory and support decision-making without directing specific actions.",
        description="Required disclaimer"
    )
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "No individuals, units, or enforcement targets named",
            "Domain-level recommendations only",
            "Supports government, enterprise, and multi-agency contexts",
            "Advisory only, not directive",
            "Leadership retains full decision authority"
        ],
        description="Policy compliance notes"
    )


class DecisionAdvantageLayer(BaseModel):
    """
    Decision Advantage Layer - Phase 3 Complete Result
    
    Provides leadership with early, proportional, non-enforcement decision guidance
    based on modeled risk patterns.
    
    Combines:
    - Decision Pathway Intelligence
    - Impact Forecasting
    - Authority-Aware Recommendations
    
    CRITICAL CONSTRAINTS:
    - No surveillance, mandates, or investigative framing
    - Pre-incident decision intelligence posture
    - All outputs auditable and confidence-weighted
    """
    threat_id: str = Field(..., description="Associated threat object ID")
    
    decision_pathways: Optional[DecisionPathwayIntelligence] = Field(
        None, description="Decision Pathway Intelligence"
    )
    
    impact_forecast: Optional[ImpactForecast] = Field(
        None, description="System-level Impact Forecast"
    )
    
    authority_recommendations: Optional[AuthorityAwareRecommendations] = Field(
        None, description="Authority-Aware Recommendations"
    )
    
    overall_decision_posture: str = Field(
        ..., description="Overall decision posture summary"
    )
    
    confidence_weighted_priority: float = Field(
        ..., ge=0, le=1, description="Confidence-weighted priority score"
    )
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    master_disclaimer: str = Field(
        default="The Decision Advantage Layer provides advisory guidance for leadership decision-making. All outputs are pre-incident, non-enforcement, and non-investigative. No surveillance, mandates, or identity attribution is included.",
        description="Master disclaimer for entire layer"
    )
    
    policy_compliance: list[str] = Field(
        default_factory=lambda: [
            "Pre-incident decision intelligence posture maintained",
            "No enforcement, investigative, or surveillance outputs",
            "No identity attribution",
            "All recommendations auditable and confidence-weighted",
            "Leadership retains full decision authority"
        ],
        description="Policy compliance confirmation"
    )


class ConfidenceBandType(str, Enum):
    """
    Layered Region Confidence Band Types for Region-as-Context Map.
    Represents analytical relevance, not events, actors, or threats.
    """
    CORE = "core"
    ADJACENT = "adjacent"
    PERIPHERAL = "peripheral"


class RegionConfidenceBand(BaseModel):
    """
    Individual confidence band for region visualization.
    
    POLICY-SAFE: Represents analytical relevance only.
    No pins, heatmaps, or city-level targeting.
    """
    band_type: ConfidenceBandType = Field(..., description="Band classification")
    region_name: str = Field(..., description="Abstracted region name")
    relevance_score: float = Field(..., ge=0, le=1, description="Analytical relevance (0-1)")
    description: str = Field(..., description="Band description")
    
    visual_style: str = Field(
        default="solid",
        description="Visual style: solid (core), dashed (adjacent), faded (peripheral)"
    )


class LayeredRegionConfidenceBands(BaseModel):
    """
    Layered Region Confidence Bands for focused context view.
    
    CRITICAL CONSTRAINTS:
    - Display only one region at a time
    - No global map with multiple regions visible simultaneously
    - No pins, no heatmaps, no city-level targeting
    - Bands represent analytical relevance, not events or actors
    """
    region_id: str = Field(..., description="Region identifier")
    region_name: str = Field(..., description="Primary region name")
    
    core_band: RegionConfidenceBand = Field(..., description="Core region - strongest relevance")
    adjacent_band: Optional[RegionConfidenceBand] = Field(None, description="Adjacent zone - moderate relevance")
    peripheral_band: Optional[RegionConfidenceBand] = Field(None, description="Peripheral influence - soft boundary")
    
    overall_confidence: float = Field(..., ge=0, le=1, description="Overall regional confidence")
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "Bands represent analytical relevance, not events or actors",
            "No precise coordinates or map pins",
            "Single region view only - no global overlays"
        ],
        description="Policy compliance notes"
    )


class ContextPriority(str, Enum):
    """Context priority levels for display ordering"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    SUMMARIZED = "summarized"


class DecisionContext(BaseModel):
    """
    Individual Decision Context within a region.
    
    Each context is independent with its own:
    - Signals, Intent stage, Decision pathways
    - Impact forecasting, Authority-aware recommendations
    - Confidence score
    
    CRITICAL: Contexts are NEVER automatically merged.
    No compounded probabilities or combined threat labels.
    """
    context_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    context_name: str = Field(..., description="Context identifier/name")
    context_description: str = Field(..., description="Brief context description")
    
    threat_id: str = Field(..., description="Associated threat object ID")
    
    intent_stage: IntentStage = Field(..., description="Current intent stage")
    intent_stage_confidence: float = Field(..., ge=0, le=1, description="Confidence in intent stage")
    
    confidence_score: float = Field(..., ge=0, le=1, description="Overall context confidence")
    persistence_score: float = Field(default=0.5, ge=0, le=1, description="How persistent this context has been")
    decision_impact_score: float = Field(default=0.5, ge=0, le=1, description="Potential decision impact")
    
    priority: ContextPriority = Field(default=ContextPriority.SECONDARY, description="Display priority")
    priority_score: float = Field(default=0.5, ge=0, le=1, description="Numeric priority for sorting")
    
    is_expanded: bool = Field(default=False, description="Whether context is expanded in UI")
    
    signal_count: int = Field(default=0, ge=0, description="Number of contributing signals")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "Context is independent - not merged with other contexts",
            "No compounded probabilities across contexts",
            "Pre-incident, non-investigative posture maintained"
        ],
        description="Policy compliance notes"
    )


class ContextStackSummary(BaseModel):
    """
    Summary of excess contexts when more than 8 are detected.
    
    RULE: If more than 8 contexts detected, summarize excess as:
    "Additional low-confidence contexts detected and summarized (not decision-relevant at this time)."
    """
    summarized_count: int = Field(..., ge=0, description="Number of summarized contexts")
    average_confidence: float = Field(..., ge=0, le=1, description="Average confidence of summarized contexts")
    summary_note: str = Field(
        default="Additional low-confidence contexts detected and summarized (not decision-relevant at this time).",
        description="Standard summary note"
    )


class RegionContextStack(BaseModel):
    """
    Context Stack for a single region.
    
    CONTEXT STACK RULES:
    - Optimal displayed contexts: 3-5 per region
    - Hard maximum: 8 contexts per region
    - If more than 8 detected, summarize excess
    - Contexts are NEVER automatically merged
    - No compounded probabilities or combined threat labels
    
    PRIORITIZATION:
    - Intent stage
    - Persistence
    - Decision impact
    - Confidence
    """
    region_id: str = Field(..., description="Region identifier")
    region_name: str = Field(..., description="Region display name")
    
    contexts: list[DecisionContext] = Field(
        default_factory=list,
        description="Active decision contexts (max 8 displayed)"
    )
    
    displayed_count: int = Field(default=0, ge=0, le=8, description="Number of displayed contexts")
    total_count: int = Field(default=0, ge=0, description="Total contexts including summarized")
    
    summarized_contexts: Optional[ContextStackSummary] = Field(
        None, description="Summary of excess contexts if > 8 detected"
    )
    
    expanded_context_id: Optional[str] = Field(
        None, description="ID of currently expanded context (only one at a time)"
    )
    
    confidence_bands: Optional[LayeredRegionConfidenceBands] = Field(
        None, description="Layered confidence bands for this region"
    )
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    policy_notes: list[str] = Field(
        default_factory=lambda: [
            "Contexts are independent - never automatically merged",
            "No compounded probabilities or combined threat labels",
            "No automatic escalation across contexts",
            "Only one context expanded at a time"
        ],
        description="Policy compliance notes"
    )


class MultiRegionIntelligence(BaseModel):
    """
    Multi-Region Intelligence Container.
    
    MULTI-REGION HANDLING RULES:
    - Internally support multiple regions concurrently
    - Display only one region's map at a time
    - Use Regional Context Selector to switch regions
    - Each region maintains independent context stack
    - No simultaneous multi-region overlays permitted
    
    SAFETY CONSTRAINTS:
    - No context merging across regions
    - No combined escalation language
    - No "compound threat" labels
    - No global surveillance views
    - No actor attribution or event prediction
    """
    regions: dict[str, RegionContextStack] = Field(
        default_factory=dict,
        description="Region context stacks keyed by region_id"
    )
    
    active_region_id: Optional[str] = Field(
        None, description="Currently displayed region (only one at a time)"
    )
    
    total_regions: int = Field(default=0, ge=0, description="Total number of regions")
    total_contexts: int = Field(default=0, ge=0, description="Total contexts across all regions")
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    
    master_disclaimer: str = Field(
        default="Multi-region intelligence displays one region at a time. Contexts within regions are independent and never merged. No global surveillance views, compound threats, or actor attribution.",
        description="Master disclaimer for multi-region display"
    )
    
    safety_constraints: list[str] = Field(
        default_factory=lambda: [
            "No context merging across regions or within regions",
            "No combined escalation language",
            "No 'compound threat' labels",
            "No global surveillance views",
            "No actor attribution or event prediction",
            "Pre-incident, advisory, explainable, auditable, non-investigative"
        ],
        description="Safety constraints confirmation"
    )


class RegionSummary(BaseModel):
    """Lightweight region summary for selector dropdown"""
    region_id: str
    region_name: str
    context_count: int = Field(default=0, ge=0)
    highest_intent_stage: Optional[str] = None
    overall_confidence: float = Field(default=0.0, ge=0, le=1)
    is_active: bool = Field(default=False)
