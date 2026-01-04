"""
AURORA™ In-Memory Data Store
Thread-safe storage with full audit trail support

Note: This is a proof-of-concept implementation.
Data will be lost on application restart.
Production deployment would use persistent storage.
"""

from datetime import datetime
from threading import Lock
from typing import Optional
import uuid

from app.models.schemas import (
    Signal,
    ThreatObject,
    NarrativeIntelligenceObject,
    AuditEntry,
    FeedbackEntry,
    ThreatProbabilityCurve,
    IntentGradient,
    IntentStage,
    ConfidenceBound,
    MonitoringPosture,
    HistoricalAnalog,
    JurisdictionContext,
    GovernancePosture,
    AuthorityEmphasis,
    ThreatClassCategory,
    ThreatClassAlignment,
    ThreatClassAlignmentResult,
    SignalDomain,
    DecisionPathwayCategory,
    DecisionPathwayRelevance,
    ImpactDomain,
    AuthorityDomain,
    ConfidenceBandType,
    RegionConfidenceBand,
    LayeredRegionConfidenceBands,
    ContextPriority,
    DecisionContext,
    ContextStackSummary,
    RegionContextStack,
    MultiRegionIntelligence,
    RegionSummary,
)


class InMemoryStore:
    """
    Thread-safe in-memory data store for AURORA™
    Maintains full audit trail for all operations.
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._data_lock = Lock()
        
        self.threats: dict[str, ThreatObject] = {}
        self.signals: dict[str, Signal] = {}
        self.nios: dict[str, NarrativeIntelligenceObject] = {}
        self.audit_entries: list[AuditEntry] = []
        self.feedback_entries: list[FeedbackEntry] = []
        self.jurisdictions: dict[str, JurisdictionContext] = {}
        
        self._probability_history: dict[str, list[dict]] = {}
        self._current_jurisdiction: str = "US"
        
        self.multi_region_intelligence: Optional[MultiRegionIntelligence] = None
        
        self._initialized = True
        
        self._seed_jurisdictions()
        self._seed_demo_data()
        self._seed_multi_region_intelligence()
    
    def _seed_jurisdictions(self):
        """
        Seed jurisdiction contexts for signal interpretation.
        
        CRITICAL DISTINCTION:
        - United States: Real operational context with full decision intelligence
        - Non-US Jurisdictions: Synthetic demonstration data ONLY for architectural validation
        
        IMPORTANT: Jurisdiction context adjusts signal interpretation, weighting,
        historical analogs, and narrative framing. It does NOT activate new data
        collection or imply active monitoring of individuals or regions.
        
        SEED LIMITS (FOUNDER-LEVEL GUIDANCE):
        - Best practice: 10 non-US jurisdictions + 1 United States
        - Maximum: 12 non-US jurisdictions
        """
        
        us_jurisdiction = JurisdictionContext(
            code="US",
            name="United States",
            region="North America",
            is_synthetic=False,
            is_operational=True,
            governance_posture=GovernancePosture.FEDERAL,
            authority_emphasis=AuthorityEmphasis.MIXED,
            public_communication_norm="transparent",
            escalation_sensitivity="moderate",
            decision_pathway_adjustments={
                "economic_engagement": "Federal and state-level coordination",
                "community_outreach": "Multi-jurisdictional community engagement",
                "communications": "Public affairs with transparency emphasis",
            },
            signal_weight_modifiers={
                "economic_stress": 1.0,
                "social_discourse": 1.0,
                "behavioral_trend": 1.0,
                "environmental_stressor": 1.0,
            },
            historical_analog_tags=["north_america", "developed_economy", "federal_republic"],
            narrative_context={
                "governance_type": "Federal Republic",
                "economic_classification": "Developed",
            },
            economic_baseline={
                "baseline_unemployment": 4.0,
                "baseline_inflation": 2.5,
            },
            cultural_context_notes=[],
            legal_framework_notes=[],
            synthetic_disclaimer="",
            is_active=True,
        )
        self.jurisdictions["US"] = us_jurisdiction
        
        synthetic_jurisdictions = [
            {
                "code": "GB",
                "name": "United Kingdom",
                "region": "Europe",
                "governance_posture": GovernancePosture.UNITARY,
                "authority_emphasis": AuthorityEmphasis.CIVIL,
                "public_communication_norm": "reserved",
                "escalation_sensitivity": "moderate",
                "governance_descriptor": "Highly centralized governance context with parliamentary tradition",
            },
            {
                "code": "DE",
                "name": "Germany",
                "region": "Europe",
                "governance_posture": GovernancePosture.FEDERAL,
                "authority_emphasis": AuthorityEmphasis.ADMINISTRATIVE,
                "public_communication_norm": "balanced",
                "escalation_sensitivity": "moderate",
                "governance_descriptor": "Federal structure with strong administrative emphasis",
            },
            {
                "code": "FR",
                "name": "France",
                "region": "Europe",
                "governance_posture": GovernancePosture.CENTRALIZED,
                "authority_emphasis": AuthorityEmphasis.ADMINISTRATIVE,
                "public_communication_norm": "balanced",
                "escalation_sensitivity": "high",
                "governance_descriptor": "Centralized governance with strong civil-administrative response preference",
            },
            {
                "code": "JP",
                "name": "Japan",
                "region": "Asia Pacific",
                "governance_posture": GovernancePosture.UNITARY,
                "authority_emphasis": AuthorityEmphasis.ADMINISTRATIVE,
                "public_communication_norm": "reserved",
                "escalation_sensitivity": "high",
                "governance_descriptor": "Unitary parliamentary system with consensus-based decision making",
            },
            {
                "code": "AU",
                "name": "Australia",
                "region": "Asia Pacific",
                "governance_posture": GovernancePosture.FEDERAL,
                "authority_emphasis": AuthorityEmphasis.MIXED,
                "public_communication_norm": "transparent",
                "escalation_sensitivity": "moderate",
                "governance_descriptor": "Federal parliamentary system with state-level coordination",
            },
            {
                "code": "CA",
                "name": "Canada",
                "region": "North America",
                "governance_posture": GovernancePosture.FEDERAL,
                "authority_emphasis": AuthorityEmphasis.CIVIL,
                "public_communication_norm": "transparent",
                "escalation_sensitivity": "low",
                "governance_descriptor": "Federal parliamentary democracy with provincial autonomy",
            },
            {
                "code": "BR",
                "name": "Brazil",
                "region": "South America",
                "governance_posture": GovernancePosture.FEDERAL,
                "authority_emphasis": AuthorityEmphasis.MIXED,
                "public_communication_norm": "balanced",
                "escalation_sensitivity": "moderate",
                "governance_descriptor": "Federal republic with multi-level governance coordination",
            },
            {
                "code": "IN",
                "name": "India",
                "region": "Asia Pacific",
                "governance_posture": GovernancePosture.FEDERAL,
                "authority_emphasis": AuthorityEmphasis.ADMINISTRATIVE,
                "public_communication_norm": "balanced",
                "escalation_sensitivity": "moderate",
                "governance_descriptor": "Federal parliamentary system with state-level diversity",
            },
            {
                "code": "SG",
                "name": "Singapore",
                "region": "Asia Pacific",
                "governance_posture": GovernancePosture.UNITARY,
                "authority_emphasis": AuthorityEmphasis.ADMINISTRATIVE,
                "public_communication_norm": "reserved",
                "escalation_sensitivity": "high",
                "governance_descriptor": "Highly centralized city-state with strong administrative capacity",
            },
            {
                "code": "AE",
                "name": "United Arab Emirates",
                "region": "Middle East",
                "governance_posture": GovernancePosture.FEDERAL,
                "authority_emphasis": AuthorityEmphasis.ADMINISTRATIVE,
                "public_communication_norm": "reserved",
                "escalation_sensitivity": "high",
                "governance_descriptor": "Federal structure with emirate-level coordination",
            },
        ]
        
        synthetic_disclaimer = (
            "SYNTHETIC DEMONSTRATION DATA: This jurisdiction context uses synthetic, "
            "non-representative seed profiles for demonstration and architectural validation only. "
            "This does NOT represent real-world intelligence, monitoring, or coverage. "
            "No foreign actor modeling, population-level inference, or event prediction is performed."
        )
        
        for j in synthetic_jurisdictions:
            jurisdiction = JurisdictionContext(
                code=j["code"],
                name=j["name"],
                region=j["region"],
                is_synthetic=True,
                is_operational=False,
                governance_posture=j["governance_posture"],
                authority_emphasis=j["authority_emphasis"],
                public_communication_norm=j["public_communication_norm"],
                escalation_sensitivity=j["escalation_sensitivity"],
                decision_pathway_adjustments={
                    "governance_context": j["governance_descriptor"],
                },
                signal_weight_modifiers={},
                historical_analog_tags=[],
                narrative_context={
                    "governance_descriptor": j["governance_descriptor"],
                    "data_status": "SYNTHETIC DEMONSTRATION ONLY",
                },
                economic_baseline={},
                cultural_context_notes=[],
                legal_framework_notes=[],
                synthetic_disclaimer=synthetic_disclaimer,
                is_active=True,
            )
            self.jurisdictions[j["code"]] = jurisdiction
        
        self._log_audit(
            action_type="jurisdictions_seeded",
            actor="system",
            target_type="jurisdiction",
            target_id="all",
            reasoning=f"Seeded 1 operational (US) + {len(synthetic_jurisdictions)} synthetic jurisdiction contexts"
        )
    
    def _seed_demo_data(self):
        """Seed initial demo data for demonstration purposes"""
        
        signal1 = Signal(
            id=str(uuid.uuid4()),
            domain="social_discourse",
            signal_type="sentiment_shift",
            source_description="Public forum sentiment analysis - Regional economic discussion boards",
            raw_confidence=0.72,
            weight=1.3,
            reasoning="Detected 45% increase in negative sentiment toward local economic conditions over 14-day period",
            metadata={"region": "midwest", "topic": "economic_anxiety"}
        )
        
        signal2 = Signal(
            id=str(uuid.uuid4()),
            domain="behavioral_trend",
            signal_type="frequency_increase",
            source_description="Public event attendance tracking - Community meetings",
            raw_confidence=0.65,
            weight=1.1,
            reasoning="Community meeting attendance increased 3x compared to historical baseline",
            metadata={"event_type": "town_hall", "attendance_delta": 3.2}
        )
        
        signal3 = Signal(
            id=str(uuid.uuid4()),
            domain="environmental_stressor",
            signal_type="economic_stress",
            source_description="Public economic indicators - Regional unemployment data",
            raw_confidence=0.88,
            weight=1.5,
            reasoning="Regional unemployment rate increased 2.3 percentage points in 60 days",
            metadata={"unemployment_delta": 2.3, "timeframe_days": 60}
        )
        
        signal4 = Signal(
            id=str(uuid.uuid4()),
            domain="social_discourse",
            signal_type="narrative_amplification",
            source_description="Public media analysis - Local news coverage patterns",
            raw_confidence=0.58,
            weight=1.0,
            reasoning="Grievance-related narratives showing 2.5x amplification in local media coverage",
            metadata={"amplification_factor": 2.5}
        )
        
        signal5 = Signal(
            id=str(uuid.uuid4()),
            domain="behavioral_trend",
            signal_type="escalation_pattern",
            source_description="Public records - Permit applications and public gatherings",
            raw_confidence=0.61,
            weight=1.2,
            reasoning="Escalating pattern in public demonstration permit applications",
            metadata={"permit_increase_pct": 180}
        )
        
        for sig in [signal1, signal2, signal3, signal4, signal5]:
            self.signals[sig.id] = sig
        
        threat1 = ThreatObject(
            id=str(uuid.uuid4()),
            name="Regional Economic Stress Convergence",
            description="Multiple weak signals converging around economic stress indicators in midwest region, suggesting potential for social unrest escalation",
            category="socioeconomic",
            signals=[signal1, signal2, signal3, signal4, signal5],
            probability_curve=ThreatProbabilityCurve(
                current_probability=67.3,
                confidence_bounds=ConfidenceBound(lower=52.1, upper=78.9),
                trend="increasing",
                trend_velocity=2.1,
                convergence_score=0.73,
                contributing_signals=5,
                domain_coverage={
                    "social_discourse": 2,
                    "behavioral_trend": 2,
                    "environmental_stressor": 1
                },
                history=[
                    {"timestamp": "2026-01-01T10:00:00Z", "probability": 45.2},
                    {"timestamp": "2026-01-02T10:00:00Z", "probability": 58.7},
                    {"timestamp": "2026-01-03T10:00:00Z", "probability": 67.3},
                ]
            ),
            intent_gradient=IntentGradient(
                current_stage=IntentStage.COGNITIVE_FIXATION,
                stage_confidence=0.78,
                velocity=0.35,
                acceleration=0.08,
                time_in_stage=72.5,
                stage_history=[
                    {"stage": "grievance_formation", "entered": "2025-12-28T00:00:00Z", "exited": "2025-12-31T00:00:00Z"},
                    {"stage": "cognitive_fixation", "entered": "2025-12-31T00:00:00Z", "exited": None}
                ],
                stage_1_score=0.92,
                stage_2_score=0.78,
                stage_3_score=0.31,
                stage_4_score=0.12
            ),
            historical_analogs=[
                HistoricalAnalog(
                    name="2008 Midwest Economic Protests",
                    description="Series of economic grievance demonstrations following financial crisis",
                    similarity_score=0.72,
                    outcome="Peaceful protests with policy engagement, no significant escalation",
                    lessons_learned="Early community engagement and transparent communication reduced escalation risk",
                    date_range="2008-2009"
                ),
                HistoricalAnalog(
                    name="2011 Regional Labor Disputes",
                    description="Labor-related demonstrations in response to policy changes",
                    similarity_score=0.65,
                    outcome="Extended protests with eventual negotiated resolution",
                    lessons_learned="Prolonged uncertainty increased mobilization; clear timelines helped de-escalation",
                    date_range="2011"
                )
            ],
            region_context={
                "primary_region": "Midwest Industrial Corridor",
                "secondary_regions": ["Great Lakes Metro-Adjacent", "Ohio Valley Transition Zone"],
                "region_type": "multi-state industrial corridor",
                "attribution_confidence": 0.76,
                "attribution_rationale": "Signal clustering indicates concentration in manufacturing-dependent areas with recent economic disruption. Attribution based on aggregate economic indicators and public discourse patterns, not individual tracking.",
                "population_scale": "large metro-adjacent",
                "economic_profile": "manufacturing-dependent with service transition",
                "granularity_level": "macro",
                "policy_notes": [
                    "Region context is abstracted and non-targeting",
                    "No precise coordinates or map pins are provided",
                    "Regional attribution is pattern-based, not surveillance-derived"
                ]
            },
            escalation_pathway={
                "pathway_id": str(uuid.uuid4()),
                "pathway_name": "Economic Stress → Social Mobilization Pattern",
                "pathway_description": "Classic pattern where structural economic stress leads to discourse amplification, behavioral organization, and potential mobilization",
                "stages": [
                    {
                        "stage_name": "Structural Stress Emergence",
                        "stage_description": "Economic or environmental stressors create conditions for grievance formation",
                        "typical_indicators": ["Unemployment increase", "Cost of living pressure", "Industry disruption"],
                        "typical_duration_hours": [168, 720],
                        "transition_triggers": ["Media coverage", "Community discussion", "Political attention"]
                    },
                    {
                        "stage_name": "Discourse Amplification",
                        "stage_description": "Grievances become topics of public discussion with increasing intensity",
                        "typical_indicators": ["Sentiment shift", "Narrative emergence", "Opinion leader engagement"],
                        "typical_duration_hours": [72, 336],
                        "transition_triggers": ["Organizing activity", "Event planning", "Coalition formation"]
                    },
                    {
                        "stage_name": "Behavioral Organization",
                        "stage_description": "Discourse translates into organized activity and preparation",
                        "typical_indicators": ["Meeting frequency", "Permit applications", "Resource gathering"],
                        "typical_duration_hours": [48, 168],
                        "transition_triggers": ["Catalyst event", "Leadership emergence", "External support"]
                    },
                    {
                        "stage_name": "Mobilization Potential",
                        "stage_description": "Conditions exist for coordinated action if trajectory continues",
                        "typical_indicators": ["Coordination signals", "Timeline indicators", "Resource readiness"],
                        "typical_duration_hours": [24, 72],
                        "transition_triggers": ["Specific catalyst", "Window of opportunity", "Critical mass"]
                    }
                ],
                "current_stage_index": 1,
                "stage_entry_time": "2025-12-31T00:00:00Z",
                "progression_probability": 0.42,
                "regression_probability": 0.28,
                "projected_progression_window": [72, 240],
                "projection_confidence": 0.58,
                "historical_pattern_matches": ["2008 Midwest Economic Protests", "2011 Regional Labor Disputes"],
                "policy_notes": [
                    "Pathway modeling is pattern-based, not predictive of specific incidents",
                    "Projections are for decision support only, not forecasting",
                    "No individual actors or specific events are predicted"
                ]
            },
            threat_class_alignment={
                "threat_id": "",
                "alignments": [
                    {
                        "class_category": ThreatClassCategory.SOCIOECONOMIC_INSTABILITY.value,
                        "alignment_score": 0.72,
                        "confidence": 0.78,
                        "primary_contributing_domains": ["environmental_stressor", "social_discourse"],
                        "intent_stage_influence": 0.35,
                        "escalation_pathway_influence": 0.20,
                        "velocity_influence": 0.15,
                        "rationale": "Signal composition shows strong environmental stress signals combined with social discourse patterns with patterns typical of socioeconomic stress scenarios. Cognitive fixation stage suggests elevated pattern consistency."
                    },
                    {
                        "class_category": ThreatClassCategory.CIVIL_UNREST_PROTEST.value,
                        "alignment_score": 0.58,
                        "confidence": 0.72,
                        "primary_contributing_domains": ["social_discourse", "behavioral_trend"],
                        "intent_stage_influence": 0.40,
                        "escalation_pathway_influence": 0.35,
                        "velocity_influence": 0.25,
                        "rationale": "Pattern alignment indicates social discourse patterns combined with behavioral trend indicators consistent with civil unrest or protest escalation dynamics. Cognitive fixation stage suggests elevated pattern consistency."
                    },
                    {
                        "class_category": ThreatClassCategory.IDEOLOGICAL_MOBILIZATION.value,
                        "alignment_score": 0.41,
                        "confidence": 0.65,
                        "primary_contributing_domains": ["social_discourse", "behavioral_trend"],
                        "intent_stage_influence": 0.45,
                        "escalation_pathway_influence": 0.30,
                        "velocity_influence": 0.20,
                        "rationale": "Discourse patterns and behavioral indicators suggest social discourse patterns combined with behavioral trend indicators aligned with ideological mobilization trajectories. Cognitive fixation stage suggests elevated pattern consistency."
                    },
                    {
                        "class_category": ThreatClassCategory.COORDINATED_DISINFORMATION.value,
                        "alignment_score": 0.35,
                        "confidence": 0.58,
                        "primary_contributing_domains": ["social_discourse"],
                        "intent_stage_influence": 0.30,
                        "escalation_pathway_influence": 0.40,
                        "velocity_influence": 0.10,
                        "rationale": "Discourse analysis reveals social discourse patterns with characteristics of coordinated information amplification patterns. Current stage shows moderate alignment with disinformation dynamics."
                    },
                    {
                        "class_category": ThreatClassCategory.INFRASTRUCTURE_DISRUPTION.value,
                        "alignment_score": 0.28,
                        "confidence": 0.52,
                        "primary_contributing_domains": ["environmental_stressor", "behavioral_trend"],
                        "intent_stage_influence": 0.20,
                        "escalation_pathway_influence": 0.25,
                        "velocity_influence": 0.15,
                        "rationale": "Environmental and behavioral indicators show environmental stress signals combined with behavioral trend indicators aligned with infrastructure disruption risk scenarios. Early stage reduces mobilization-related alignment."
                    }
                ],
                "top_alignment": ThreatClassCategory.SOCIOECONOMIC_INSTABILITY.value,
                "alignment_diversity": 0.62,
                "intent_stage_at_computation": "cognitive_fixation",
                "escalation_stage_at_computation": 1,
                "last_updated": datetime.utcnow().isoformat(),
                "disclaimer": "Class alignment reflects analytic pattern similarity and may evolve as new signals emerge. These are probabilistic assessments, not predictions or accusations.",
                "policy_notes": [
                    "Class alignments are analytic pattern similarities only",
                    "No identity attribution or individual labeling",
                    "No prediction of specific events or actions",
                    "No law-enforcement or investigative framing",
                    "Maintains pre-incident decision-intelligence posture"
                ]
            },
            decision_advantage_layer={
                "threat_id": "",
                "decision_pathways": {
                    "threat_id": "",
                    "pathways": [
                        {
                            "pathway_category": DecisionPathwayCategory.ECONOMIC_ENGAGEMENT.value,
                            "relevance": DecisionPathwayRelevance.HIGH.value,
                            "relevance_score": 0.82,
                            "advisory_summary": "Consider economic engagement strategies to address underlying structural stressors",
                            "suggested_considerations": [
                                "Review economic support mechanisms in affected areas",
                                "Assess workforce development program alignment",
                                "Evaluate community economic resilience indicators"
                            ],
                            "proportionality_note": "Economic engagement is most effective in early-stage patterns where structural stressors are primary drivers",
                            "contributing_factors": [
                                "Threat class alignment: Socioeconomic Instability",
                                "Intent stage: Cognitive Fixation",
                                "Threat probability: 67.3%"
                            ],
                            "confidence": 0.78
                        },
                        {
                            "pathway_category": DecisionPathwayCategory.COMMUNITY_OUTREACH.value,
                            "relevance": DecisionPathwayRelevance.HIGH.value,
                            "relevance_score": 0.78,
                            "advisory_summary": "Community outreach may help address grievance formation and build trust",
                            "suggested_considerations": [
                                "Identify trusted community intermediaries",
                                "Assess communication channel effectiveness",
                                "Review community feedback mechanisms"
                            ],
                            "proportionality_note": "Community outreach is proportional across all stages but most impactful before behavioral acceleration",
                            "contributing_factors": [
                                "Threat class alignment: Socioeconomic Instability",
                                "Intent stage: Cognitive Fixation",
                                "Threat probability: 67.3%"
                            ],
                            "confidence": 0.75
                        },
                        {
                            "pathway_category": DecisionPathwayCategory.COMMUNICATIONS_STRATEGY.value,
                            "relevance": DecisionPathwayRelevance.MODERATE.value,
                            "relevance_score": 0.65,
                            "advisory_summary": "Strategic communications may help counter narrative amplification and provide accurate information",
                            "suggested_considerations": [
                                "Review public messaging alignment with community concerns",
                                "Assess information environment for misinformation patterns",
                                "Evaluate proactive communication opportunities"
                            ],
                            "proportionality_note": "Communications strategy is particularly relevant when discourse amplification is detected",
                            "contributing_factors": [
                                "Threat class alignment: Socioeconomic Instability",
                                "Intent stage: Cognitive Fixation",
                                "Threat probability: 67.3%"
                            ],
                            "confidence": 0.68
                        },
                        {
                            "pathway_category": DecisionPathwayCategory.STAKEHOLDER_COORDINATION.value,
                            "relevance": DecisionPathwayRelevance.MODERATE.value,
                            "relevance_score": 0.58,
                            "advisory_summary": "Cross-stakeholder coordination may improve response coherence and resource alignment",
                            "suggested_considerations": [
                                "Identify key stakeholder groups and their concerns",
                                "Assess coordination mechanisms and gaps",
                                "Review information sharing protocols"
                            ],
                            "proportionality_note": "Stakeholder coordination becomes more critical as pattern complexity increases",
                            "contributing_factors": [
                                "Threat class alignment: Socioeconomic Instability",
                                "Intent stage: Cognitive Fixation",
                                "Threat probability: 67.3%"
                            ],
                            "confidence": 0.62
                        },
                        {
                            "pathway_category": DecisionPathwayCategory.MONITORING_ADJUSTMENT.value,
                            "relevance": DecisionPathwayRelevance.MODERATE.value,
                            "relevance_score": 0.52,
                            "advisory_summary": "Monitoring posture adjustments may improve situational awareness",
                            "suggested_considerations": [
                                "Review current monitoring coverage and gaps",
                                "Assess information collection priorities",
                                "Evaluate reporting frequency and channels"
                            ],
                            "proportionality_note": "Monitoring adjustments should be proportional to uncertainty levels and information gaps",
                            "contributing_factors": [
                                "Threat class alignment: Socioeconomic Instability",
                                "Intent stage: Cognitive Fixation",
                                "Threat probability: 67.3%"
                            ],
                            "confidence": 0.58
                        }
                    ],
                    "primary_pathway": DecisionPathwayCategory.ECONOMIC_ENGAGEMENT.value,
                    "overall_advisory_posture": "Elevated awareness posture. Consider proactive engagement through high-relevance pathways.",
                    "proportionality_assessment": "Response proportionality should align with current threat probability (67.3%) and intent stage (Cognitive Fixation). All guidance remains advisory and optional.",
                    "last_updated": datetime.utcnow().isoformat(),
                    "disclaimer": "Decision pathways are advisory and optional. All guidance is proportional to assessed patterns and does not constitute enforcement direction or tactical instruction.",
                    "policy_notes": [
                        "All pathways are optional and advisory",
                        "No enforcement or tactical instruction provided",
                        "Guidance is proportional to assessed risk patterns",
                        "Leadership retains full decision authority",
                        "Pre-incident decision support only"
                    ]
                },
                "impact_forecast": {
                    "threat_id": "",
                    "projections": [
                        {
                            "domain": ImpactDomain.ECONOMIC_RESILIENCE.value,
                            "current_assessment": "Economic resilience under stress from structural factors",
                            "projected_trajectory": "Persistent economic stress patterns may compound community vulnerability and grievance formation",
                            "impact_severity": "significant",
                            "impact_severity_score": 0.72,
                            "time_horizon_hours": [72, 336],
                            "confidence": 0.68,
                            "confidence_band": [0.57, 0.87],
                            "key_assumptions": [
                                "Structural economic factors persist",
                                "No targeted economic interventions"
                            ],
                            "mitigating_factors": [
                                "Economic support mechanisms",
                                "Workforce development programs",
                                "Business assistance initiatives"
                            ]
                        },
                        {
                            "domain": ImpactDomain.COMMUNITY_STABILITY.value,
                            "current_assessment": "Community stability indicators showing stress signals",
                            "projected_trajectory": "Continued pattern escalation may increase community tension and reduce social cohesion",
                            "impact_severity": "moderate",
                            "impact_severity_score": 0.58,
                            "time_horizon_hours": [72, 336],
                            "confidence": 0.65,
                            "confidence_band": [0.43, 0.73],
                            "key_assumptions": [
                                "Economic stressors remain unaddressed",
                                "Discourse amplification continues"
                            ],
                            "mitigating_factors": [
                                "Economic support programs",
                                "Community dialogue initiatives",
                                "Local leadership engagement"
                            ]
                        },
                        {
                            "domain": ImpactDomain.SOCIAL_COHESION.value,
                            "current_assessment": "Social cohesion showing early stress indicators",
                            "projected_trajectory": "Continued polarization patterns may reduce social cohesion and increase community fragmentation",
                            "impact_severity": "moderate",
                            "impact_severity_score": 0.52,
                            "time_horizon_hours": [72, 336],
                            "confidence": 0.62,
                            "confidence_band": [0.37, 0.67],
                            "key_assumptions": [
                                "Polarizing discourse continues",
                                "No cohesion-building interventions"
                            ],
                            "mitigating_factors": [
                                "Cross-community dialogue programs",
                                "Shared interest initiatives",
                                "Inclusive communication strategies"
                            ]
                        },
                        {
                            "domain": ImpactDomain.INSTITUTIONAL_TRUST.value,
                            "current_assessment": "Institutional trust levels within normal parameters",
                            "projected_trajectory": "If current discourse patterns persist, institutional trust may experience erosion in affected communities",
                            "impact_severity": "moderate",
                            "impact_severity_score": 0.45,
                            "time_horizon_hours": [72, 336],
                            "confidence": 0.58,
                            "confidence_band": [0.30, 0.60],
                            "key_assumptions": [
                                "Current discourse patterns continue",
                                "No significant trust-building interventions occur"
                            ],
                            "mitigating_factors": [
                                "Proactive transparent communication",
                                "Community engagement initiatives",
                                "Responsive grievance mechanisms"
                            ]
                        }
                    ],
                    "overall_impact_assessment": "System-level impact assessment indicates moderate potential consequences in key domains if current trajectory persists.",
                    "primary_concern_domain": ImpactDomain.ECONOMIC_RESILIENCE.value,
                    "aggregate_severity_score": 0.57,
                    "projection_time_horizon": "72-336 hours (3.0-14.0 days)",
                    "last_updated": datetime.utcnow().isoformat(),
                    "disclaimer": "Impact projections are system-level estimates based on current trajectory patterns. They do not predict specific events, actors, or outcomes. All projections include uncertainty bounds.",
                    "policy_notes": [
                        "Projections focus on institutional and community outcomes",
                        "No prediction of specific events or actors",
                        "All projections include confidence bands and time horizons",
                        "System-level analysis only, not individual attribution",
                        "For decision support, not operational forecasting"
                    ]
                },
                "authority_recommendations": {
                    "threat_id": "",
                    "recommendations": [
                        {
                            "authority_domain": AuthorityDomain.EXECUTIVE_LEADERSHIP.value,
                            "relevance_score": 0.78,
                            "positioning_rationale": "Executive leadership is positioned to provide strategic direction and authorize cross-functional responses",
                            "suggested_awareness_areas": [
                                "Overall threat pattern trajectory",
                                "Resource allocation decisions",
                                "External stakeholder communications"
                            ],
                            "coordination_considerations": [
                                "Strategic Planning",
                                "External Affairs",
                                "Risk Management"
                            ],
                            "context_applicability": ["government", "enterprise", "multi-agency"],
                            "confidence": 0.82
                        },
                        {
                            "authority_domain": AuthorityDomain.COMMUNITY_RELATIONS.value,
                            "relevance_score": 0.75,
                            "positioning_rationale": "Community relations can engage trusted intermediaries and address grievance formation",
                            "suggested_awareness_areas": [
                                "Community sentiment indicators",
                                "Trusted intermediary networks",
                                "Grievance patterns"
                            ],
                            "coordination_considerations": [
                                "Communications/Public Affairs",
                                "External Affairs",
                                "Executive Leadership"
                            ],
                            "context_applicability": ["government", "enterprise"],
                            "confidence": 0.78
                        },
                        {
                            "authority_domain": AuthorityDomain.COMMUNICATIONS_PUBLIC_AFFAIRS.value,
                            "relevance_score": 0.68,
                            "positioning_rationale": "Communications is positioned to manage public messaging and counter narrative amplification",
                            "suggested_awareness_areas": [
                                "Information environment dynamics",
                                "Public sentiment indicators",
                                "Messaging alignment needs"
                            ],
                            "coordination_considerations": [
                                "Executive Leadership",
                                "Community Relations",
                                "Legal Compliance"
                            ],
                            "context_applicability": ["government", "enterprise", "multi-agency"],
                            "confidence": 0.72
                        },
                        {
                            "authority_domain": AuthorityDomain.RISK_MANAGEMENT.value,
                            "relevance_score": 0.62,
                            "positioning_rationale": "Risk management can assess threat patterns and recommend proportional mitigation measures",
                            "suggested_awareness_areas": [
                                "Threat probability trends",
                                "Vulnerability assessments",
                                "Mitigation option effectiveness"
                            ],
                            "coordination_considerations": [
                                "Operations Management",
                                "Executive Leadership",
                                "Strategic Planning"
                            ],
                            "context_applicability": ["government", "enterprise", "multi-agency"],
                            "confidence": 0.68
                        },
                        {
                            "authority_domain": AuthorityDomain.STRATEGIC_PLANNING.value,
                            "relevance_score": 0.55,
                            "positioning_rationale": "Strategic planning can assess long-term implications and recommend adaptive strategies",
                            "suggested_awareness_areas": [
                                "Long-term trend implications",
                                "Strategic option development",
                                "Resource planning needs"
                            ],
                            "coordination_considerations": [
                                "Executive Leadership",
                                "Risk Management",
                                "Operations Management"
                            ],
                            "context_applicability": ["government", "enterprise"],
                            "confidence": 0.62
                        }
                    ],
                    "primary_authority_domain": AuthorityDomain.EXECUTIVE_LEADERSHIP.value,
                    "coordination_summary": "Cross-domain coordination recommended among: Strategic Planning, External Affairs, Risk Management, Communications/Public Affairs. Information sharing and aligned messaging are key coordination priorities.",
                    "context_applicability": "all",
                    "last_updated": datetime.utcnow().isoformat(),
                    "disclaimer": "Authority recommendations identify leadership domains, not individuals or units. All recommendations are advisory and support decision-making without directing specific actions.",
                    "policy_notes": [
                        "No individuals, units, or enforcement targets named",
                        "Domain-level recommendations only",
                        "Supports government, enterprise, and multi-agency contexts",
                        "Advisory only, not directive",
                        "Leadership retains full decision authority"
                    ]
                },
                "overall_decision_posture": "Elevated awareness with proactive engagement consideration",
                "confidence_weighted_priority": 0.65,
                "last_updated": datetime.utcnow().isoformat(),
                "master_disclaimer": "The Decision Advantage Layer provides advisory guidance for leadership decision-making. All outputs are pre-incident, non-enforcement, and non-investigative. No surveillance, mandates, or identity attribution is included.",
                "policy_compliance": [
                    "Pre-incident decision intelligence posture maintained",
                    "No enforcement, investigative, or surveillance outputs",
                    "No identity attribution",
                    "All recommendations auditable and confidence-weighted",
                    "Leadership retains full decision authority"
                ]
            },
            status="active"
        )
        
        nio1 = NarrativeIntelligenceObject(
            id=str(uuid.uuid4()),
            threat_id=threat1.id,
            executive_summary="A convergence of economic stress indicators in the midwest region suggests elevated potential for organized social response. Five distinct signals across three domains show consistent patterns of grievance formation transitioning to cognitive fixation. Current probability assessment is 67.3% with moderate confidence.",
            why_it_matters="This threat pattern represents a classic pre-mobilization signature where economic stressors combine with amplified grievance narratives. Historical analogs suggest a 6-8 week window before potential behavioral acceleration if current trajectory continues. Early intervention through community engagement has proven effective in similar cases.",
            converged_signals=[
                "Sentiment shift in regional economic discussions (+45%)",
                "Community meeting attendance surge (3x baseline)",
                "Regional unemployment spike (+2.3 points)",
                "Grievance narrative amplification (2.5x coverage)",
                "Escalating public demonstration permits (+180%)"
            ],
            signal_narrative="The convergence began with environmental stressors (unemployment increase) which created conditions for grievance formation. This was followed by measurable shifts in public discourse sentiment and increased community organizing activity. The pattern shows classic weak-signal convergence where no single indicator would trigger concern, but their simultaneous emergence creates a coherent threat picture.",
            confidence_level=73.0,
            confidence_explanation="Confidence is moderate-high due to strong signal convergence across multiple domains (3 of 3 domains represented), consistent historical analog patterns, and clear temporal correlation. Confidence is limited by incomplete coverage of all potential contributing factors and inherent uncertainty in predictive modeling.",
            known_unknowns=[
                "Leadership emergence within organizing groups not yet observable",
                "External catalyst events that could accelerate timeline",
                "Effectiveness of any ongoing mitigation efforts",
                "Cross-regional coordination potential"
            ],
            assumptions=[
                "Current economic conditions will persist for at least 30 days",
                "No major external events will significantly alter trajectory",
                "Historical analog patterns remain relevant to current context",
                "Signal sources remain representative of broader population"
            ],
            monitoring_posture=MonitoringPosture.ELEVATED,
            posture_rationale="Elevated monitoring is recommended due to the clear convergence pattern and transition to cognitive fixation stage. This posture allows for early detection of behavioral acceleration while avoiding resource over-commitment. Recommend daily signal refresh and weekly NIO updates.",
            recommended_actions=[
                "Increase signal collection frequency in affected region",
                "Identify community engagement opportunities",
                "Prepare contingency communication strategies",
                "Monitor for leadership emergence indicators"
            ],
            reasoning_chain=[
                "Step 1: Identified 5 signals across 3 domains showing temporal correlation",
                "Step 2: Calculated convergence score of 0.73 based on signal weights and confidence",
                "Step 3: Assessed intent gradient showing transition from Stage 1 to Stage 2",
                "Step 4: Compared pattern to historical analogs with 0.72 and 0.65 similarity scores",
                "Step 5: Generated probability curve with 67.3% current value and increasing trend",
                "Step 6: Determined elevated monitoring posture based on stage velocity and convergence strength"
            ]
        )
        
        threat1.current_nio = nio1
        self.threats[threat1.id] = threat1
        self.nios[nio1.id] = nio1
        
        self._probability_history[threat1.id] = [
            {"timestamp": "2026-01-01T10:00:00Z", "probability": 45.2, "confidence_lower": 32.1, "confidence_upper": 58.3},
            {"timestamp": "2026-01-02T10:00:00Z", "probability": 58.7, "confidence_lower": 44.2, "confidence_upper": 71.5},
            {"timestamp": "2026-01-03T10:00:00Z", "probability": 67.3, "confidence_lower": 52.1, "confidence_upper": 78.9},
        ]
        
        self._log_audit(
            action_type="system_initialization",
            actor="system",
            target_type="store",
            target_id="aurora_store",
            reasoning="Initial system startup with demo data seeding"
        )
    
    def _log_audit(
        self,
        action_type: str,
        actor: str,
        target_type: str,
        target_id: str,
        reasoning: str,
        before_state: Optional[dict] = None,
        after_state: Optional[dict] = None,
        metadata: Optional[dict] = None
    ) -> AuditEntry:
        """Create and store an audit entry"""
        entry = AuditEntry(
            action_type=action_type,
            actor=actor,
            target_type=target_type,
            target_id=target_id,
            reasoning=reasoning,
            before_state=before_state,
            after_state=after_state,
            metadata=metadata or {}
        )
        self.audit_entries.append(entry)
        return entry
    
    def get_all_threats(self) -> list[ThreatObject]:
        """Get all threat objects"""
        with self._data_lock:
            return list(self.threats.values())
    
    def get_threat(self, threat_id: str) -> Optional[ThreatObject]:
        """Get a specific threat by ID"""
        with self._data_lock:
            return self.threats.get(threat_id)
    
    def create_threat(self, name: str, description: str, category: str) -> ThreatObject:
        """Create a new threat object with default values"""
        with self._data_lock:
            threat = ThreatObject(
                name=name,
                description=description,
                category=category,
                signals=[],
                probability_curve=ThreatProbabilityCurve(
                    current_probability=0.0,
                    confidence_bounds=ConfidenceBound(lower=0.0, upper=10.0),
                    trend="stable",
                    trend_velocity=0.0,
                    convergence_score=0.0,
                    contributing_signals=0,
                    domain_coverage={},
                    history=[]
                ),
                intent_gradient=IntentGradient(
                    current_stage=IntentStage.GRIEVANCE_FORMATION,
                    stage_confidence=0.5,
                    velocity=0.0,
                    time_in_stage=0.0,
                    stage_history=[]
                )
            )
            self.threats[threat.id] = threat
            self._probability_history[threat.id] = []
            
            self._log_audit(
                action_type="threat_created",
                actor="api",
                target_type="threat",
                target_id=threat.id,
                reasoning=f"New threat object created: {name}",
                after_state={"name": name, "category": category}
            )
            
            return threat
    
    def add_signal_to_threat(self, threat_id: str, signal: Signal) -> Optional[ThreatObject]:
        """Add a signal to a threat and trigger recalculation"""
        with self._data_lock:
            threat = self.threats.get(threat_id)
            if not threat:
                return None
            
            self.signals[signal.id] = signal
            threat.signals.append(signal)
            threat.updated_at = datetime.utcnow()
            
            self._log_audit(
                action_type="signal_added",
                actor="api",
                target_type="threat",
                target_id=threat_id,
                reasoning=f"Signal added: {signal.signal_type} from {signal.domain}",
                after_state={"signal_id": signal.id, "signal_type": signal.signal_type}
            )
            
            return threat
    
    def get_threat_history(self, threat_id: str) -> list[dict]:
        """Get probability history for a threat"""
        with self._data_lock:
            return self._probability_history.get(threat_id, [])
    
    def add_probability_history(self, threat_id: str, probability: float, lower: float, upper: float):
        """Add a probability history entry"""
        with self._data_lock:
            if threat_id not in self._probability_history:
                self._probability_history[threat_id] = []
            
            self._probability_history[threat_id].append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "probability": probability,
                "confidence_lower": lower,
                "confidence_upper": upper
            })
    
    def store_nio(self, nio: NarrativeIntelligenceObject) -> NarrativeIntelligenceObject:
        """Store a NIO and link to threat"""
        with self._data_lock:
            self.nios[nio.id] = nio
            
            threat = self.threats.get(nio.threat_id)
            if threat:
                if threat.current_nio:
                    threat.nio_history.append(threat.current_nio.id)
                threat.current_nio = nio
                threat.updated_at = datetime.utcnow()
            
            self._log_audit(
                action_type="nio_generated",
                actor="narrative_engine",
                target_type="nio",
                target_id=nio.id,
                reasoning="New Narrative Intelligence Object generated",
                after_state={"threat_id": nio.threat_id, "confidence": nio.confidence_level}
            )
            
            return nio
    
    def get_nio(self, nio_id: str) -> Optional[NarrativeIntelligenceObject]:
        """Get a NIO by ID"""
        with self._data_lock:
            return self.nios.get(nio_id)
    
    def add_feedback(self, feedback: FeedbackEntry) -> FeedbackEntry:
        """Add analyst feedback"""
        with self._data_lock:
            self.feedback_entries.append(feedback)
            
            self._log_audit(
                action_type="feedback_submitted",
                actor=feedback.analyst_id,
                target_type="threat",
                target_id=feedback.threat_id,
                reasoning=feedback.rationale,
                before_state={"value": feedback.original_value} if feedback.original_value else None,
                after_state={"value": feedback.adjusted_value} if feedback.adjusted_value else None
            )
            
            return feedback
    
    def get_feedback_for_threat(self, threat_id: str) -> list[FeedbackEntry]:
        """Get all feedback for a threat"""
        with self._data_lock:
            return [f for f in self.feedback_entries if f.threat_id == threat_id]
    
    def get_audit_trail(self, limit: int = 100, target_id: Optional[str] = None) -> list[AuditEntry]:
        """Get audit trail entries"""
        with self._data_lock:
            entries = self.audit_entries
            if target_id:
                entries = [e for e in entries if e.target_id == target_id]
            return sorted(entries, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def update_threat(self, threat: ThreatObject) -> ThreatObject:
        """Update a threat object"""
        with self._data_lock:
            threat.updated_at = datetime.utcnow()
            self.threats[threat.id] = threat
            return threat
    
    def get_all_jurisdictions(self) -> list[JurisdictionContext]:
        """Get all jurisdiction contexts"""
        with self._data_lock:
            return list(self.jurisdictions.values())
    
    def get_jurisdiction(self, code: str) -> Optional[JurisdictionContext]:
        """Get a specific jurisdiction by code"""
        with self._data_lock:
            return self.jurisdictions.get(code)
    
    def get_current_jurisdiction(self) -> JurisdictionContext:
        """Get the currently active jurisdiction context"""
        with self._data_lock:
            return self.jurisdictions.get(self._current_jurisdiction, self.jurisdictions.get("US"))
    
    def set_current_jurisdiction(self, code: str) -> Optional[JurisdictionContext]:
        """
        Set the current jurisdiction context.
        
        IMPORTANT: This adjusts signal interpretation, weighting, historical analogs,
        and narrative framing. It does NOT activate new data collection or imply
        active monitoring of individuals or regions.
        """
        with self._data_lock:
            if code not in self.jurisdictions:
                return None
            
            old_jurisdiction = self._current_jurisdiction
            self._current_jurisdiction = code
            
            self._log_audit(
                action_type="jurisdiction_changed",
                actor="api",
                target_type="jurisdiction",
                target_id=code,
                reasoning="Jurisdiction context changed for signal interpretation adjustment",
                before_state={"jurisdiction": old_jurisdiction},
                after_state={"jurisdiction": code}
            )
            
            return self.jurisdictions[code]
    
    def _seed_multi_region_intelligence(self):
        """
        Seed multi-region intelligence with demo contexts.
        
        CONTEXT STACK RULES:
        - Optimal displayed contexts: 3-5 per region
        - Hard maximum: 8 contexts per region
        - Contexts are NEVER automatically merged
        - No compounded probabilities or combined threat labels
        
        MULTI-REGION HANDLING:
        - Display only one region at a time
        - Each region maintains independent context stack
        - No simultaneous multi-region overlays
        """
        
        threat_ids = list(self.threats.keys())
        primary_threat_id = threat_ids[0] if threat_ids else str(uuid.uuid4())
        
        midwest_core_band = RegionConfidenceBand(
            band_type=ConfidenceBandType.CORE,
            region_name="Midwest Industrial Corridor",
            relevance_score=0.82,
            description="Core region with strongest signal convergence and analytical relevance",
            visual_style="solid"
        )
        
        midwest_adjacent_band = RegionConfidenceBand(
            band_type=ConfidenceBandType.ADJACENT,
            region_name="Great Lakes Metro-Adjacent",
            relevance_score=0.58,
            description="Adjacent zone with moderate signal spillover and contextual relevance",
            visual_style="dashed"
        )
        
        midwest_peripheral_band = RegionConfidenceBand(
            band_type=ConfidenceBandType.PERIPHERAL,
            region_name="Ohio Valley Transition Zone",
            relevance_score=0.34,
            description="Peripheral influence zone with soft boundary and limited signal presence",
            visual_style="faded"
        )
        
        midwest_confidence_bands = LayeredRegionConfidenceBands(
            region_id="midwest_industrial",
            region_name="Midwest Industrial Corridor",
            core_band=midwest_core_band,
            adjacent_band=midwest_adjacent_band,
            peripheral_band=midwest_peripheral_band,
            overall_confidence=0.76
        )
        
        midwest_context_1 = DecisionContext(
            context_id=str(uuid.uuid4()),
            context_name="Economic Stress Convergence",
            context_description="Multiple weak signals converging around economic stress indicators",
            threat_id=primary_threat_id,
            intent_stage=IntentStage.COGNITIVE_FIXATION,
            intent_stage_confidence=0.78,
            confidence_score=0.73,
            persistence_score=0.82,
            decision_impact_score=0.71,
            priority=ContextPriority.PRIMARY,
            priority_score=0.85,
            is_expanded=True,
            signal_count=5
        )
        
        midwest_context_2 = DecisionContext(
            context_id=str(uuid.uuid4()),
            context_name="Labor Market Transition Stress",
            context_description="Signals related to workforce displacement and retraining gaps",
            threat_id=primary_threat_id,
            intent_stage=IntentStage.GRIEVANCE_FORMATION,
            intent_stage_confidence=0.65,
            confidence_score=0.58,
            persistence_score=0.72,
            decision_impact_score=0.54,
            priority=ContextPriority.SECONDARY,
            priority_score=0.62,
            is_expanded=False,
            signal_count=3
        )
        
        midwest_context_3 = DecisionContext(
            context_id=str(uuid.uuid4()),
            context_name="Community Discourse Amplification",
            context_description="Increasing public discourse around economic grievances",
            threat_id=primary_threat_id,
            intent_stage=IntentStage.GRIEVANCE_FORMATION,
            intent_stage_confidence=0.58,
            confidence_score=0.52,
            persistence_score=0.65,
            decision_impact_score=0.48,
            priority=ContextPriority.TERTIARY,
            priority_score=0.55,
            is_expanded=False,
            signal_count=2
        )
        
        midwest_stack = RegionContextStack(
            region_id="midwest_industrial",
            region_name="Midwest Industrial Corridor",
            contexts=[midwest_context_1, midwest_context_2, midwest_context_3],
            displayed_count=3,
            total_count=3,
            summarized_contexts=None,
            expanded_context_id=midwest_context_1.context_id,
            confidence_bands=midwest_confidence_bands
        )
        
        northeast_core_band = RegionConfidenceBand(
            band_type=ConfidenceBandType.CORE,
            region_name="Northeast Urban Corridor",
            relevance_score=0.68,
            description="Core region with urban density signal patterns",
            visual_style="solid"
        )
        
        northeast_adjacent_band = RegionConfidenceBand(
            band_type=ConfidenceBandType.ADJACENT,
            region_name="Mid-Atlantic Transition Zone",
            relevance_score=0.42,
            description="Adjacent zone with moderate urban-suburban signal mixing",
            visual_style="dashed"
        )
        
        northeast_confidence_bands = LayeredRegionConfidenceBands(
            region_id="northeast_urban",
            region_name="Northeast Urban Corridor",
            core_band=northeast_core_band,
            adjacent_band=northeast_adjacent_band,
            peripheral_band=None,
            overall_confidence=0.62
        )
        
        northeast_context_1 = DecisionContext(
            context_id=str(uuid.uuid4()),
            context_name="Infrastructure Stress Indicators",
            context_description="Signals related to aging infrastructure and service disruption concerns",
            threat_id=primary_threat_id,
            intent_stage=IntentStage.GRIEVANCE_FORMATION,
            intent_stage_confidence=0.62,
            confidence_score=0.58,
            persistence_score=0.68,
            decision_impact_score=0.55,
            priority=ContextPriority.PRIMARY,
            priority_score=0.68,
            is_expanded=True,
            signal_count=4
        )
        
        northeast_context_2 = DecisionContext(
            context_id=str(uuid.uuid4()),
            context_name="Housing Affordability Discourse",
            context_description="Public discourse patterns around housing costs and displacement",
            threat_id=primary_threat_id,
            intent_stage=IntentStage.GRIEVANCE_FORMATION,
            intent_stage_confidence=0.55,
            confidence_score=0.48,
            persistence_score=0.58,
            decision_impact_score=0.45,
            priority=ContextPriority.SECONDARY,
            priority_score=0.52,
            is_expanded=False,
            signal_count=2
        )
        
        northeast_stack = RegionContextStack(
            region_id="northeast_urban",
            region_name="Northeast Urban Corridor",
            contexts=[northeast_context_1, northeast_context_2],
            displayed_count=2,
            total_count=2,
            summarized_contexts=None,
            expanded_context_id=northeast_context_1.context_id,
            confidence_bands=northeast_confidence_bands
        )
        
        self.multi_region_intelligence = MultiRegionIntelligence(
            regions={
                "midwest_industrial": midwest_stack,
                "northeast_urban": northeast_stack
            },
            active_region_id="midwest_industrial",
            total_regions=2,
            total_contexts=5
        )
        
        self._log_audit(
            action_type="multi_region_intelligence_seeded",
            actor="system",
            target_type="multi_region_intelligence",
            target_id="all",
            reasoning="Seeded multi-region intelligence with 2 regions and 5 contexts"
        )
    
    def get_multi_region_intelligence(self) -> Optional[MultiRegionIntelligence]:
        """Get the multi-region intelligence container"""
        with self._data_lock:
            return self.multi_region_intelligence
    
    def get_active_region_stack(self) -> Optional[RegionContextStack]:
        """Get the currently active region's context stack"""
        with self._data_lock:
            if not self.multi_region_intelligence:
                return None
            active_id = self.multi_region_intelligence.active_region_id
            if not active_id:
                return None
            return self.multi_region_intelligence.regions.get(active_id)
    
    def set_active_region(self, region_id: str) -> Optional[RegionContextStack]:
        """
        Set the active region for display.
        
        RULE: Display only one region at a time.
        No simultaneous multi-region overlays permitted.
        """
        with self._data_lock:
            if not self.multi_region_intelligence:
                return None
            if region_id not in self.multi_region_intelligence.regions:
                return None
            
            old_region = self.multi_region_intelligence.active_region_id
            self.multi_region_intelligence.active_region_id = region_id
            self.multi_region_intelligence.last_updated = datetime.utcnow()
            
            self._log_audit(
                action_type="active_region_changed",
                actor="api",
                target_type="region",
                target_id=region_id,
                reasoning="Active region changed for focused context view",
                before_state={"region_id": old_region},
                after_state={"region_id": region_id}
            )
            
            return self.multi_region_intelligence.regions[region_id]
    
    def expand_context(self, region_id: str, context_id: str) -> Optional[DecisionContext]:
        """
        Expand a specific context within a region.
        
        RULE: Only one context expanded at a time per region.
        """
        with self._data_lock:
            if not self.multi_region_intelligence:
                return None
            region_stack = self.multi_region_intelligence.regions.get(region_id)
            if not region_stack:
                return None
            
            expanded_context = None
            for ctx in region_stack.contexts:
                if ctx.context_id == context_id:
                    ctx.is_expanded = True
                    expanded_context = ctx
                else:
                    ctx.is_expanded = False
            
            region_stack.expanded_context_id = context_id
            region_stack.last_updated = datetime.utcnow()
            
            self._log_audit(
                action_type="context_expanded",
                actor="api",
                target_type="context",
                target_id=context_id,
                reasoning="Context expanded for detailed view (only one at a time)",
                metadata={"region_id": region_id}
            )
            
            return expanded_context
    
    def get_region_summaries(self) -> list[RegionSummary]:
        """Get lightweight summaries of all regions for selector dropdown"""
        with self._data_lock:
            if not self.multi_region_intelligence:
                return []
            
            summaries = []
            for region_id, stack in self.multi_region_intelligence.regions.items():
                highest_stage = None
                max_stage_score = 0
                stage_order = {
                    IntentStage.GRIEVANCE_FORMATION: 1,
                    IntentStage.COGNITIVE_FIXATION: 2,
                    IntentStage.BEHAVIORAL_ACCELERATION: 3,
                    IntentStage.MOBILIZATION_RISK: 4
                }
                
                for ctx in stack.contexts:
                    stage_score = stage_order.get(ctx.intent_stage, 0)
                    if stage_score > max_stage_score:
                        max_stage_score = stage_score
                        highest_stage = ctx.intent_stage.value
                
                avg_confidence = sum(ctx.confidence_score for ctx in stack.contexts) / len(stack.contexts) if stack.contexts else 0.0
                
                summaries.append(RegionSummary(
                    region_id=region_id,
                    region_name=stack.region_name,
                    context_count=stack.displayed_count,
                    highest_intent_stage=highest_stage,
                    overall_confidence=avg_confidence,
                    is_active=(region_id == self.multi_region_intelligence.active_region_id)
                ))
            
            return summaries
    
    def prioritize_contexts(self, region_id: str) -> list[DecisionContext]:
        """
        Prioritize contexts within a region based on:
        - Intent stage (higher stages = higher priority)
        - Persistence
        - Decision impact
        - Confidence
        
        RULES:
        - Optimal displayed: 3-5 contexts
        - Hard maximum: 8 contexts
        - If > 8, summarize excess
        """
        with self._data_lock:
            if not self.multi_region_intelligence:
                return []
            region_stack = self.multi_region_intelligence.regions.get(region_id)
            if not region_stack:
                return []
            
            stage_weights = {
                IntentStage.GRIEVANCE_FORMATION: 0.25,
                IntentStage.COGNITIVE_FIXATION: 0.50,
                IntentStage.BEHAVIORAL_ACCELERATION: 0.75,
                IntentStage.MOBILIZATION_RISK: 1.0
            }
            
            for ctx in region_stack.contexts:
                stage_weight = stage_weights.get(ctx.intent_stage, 0.25)
                ctx.priority_score = (
                    stage_weight * 0.35 +
                    ctx.persistence_score * 0.25 +
                    ctx.decision_impact_score * 0.25 +
                    ctx.confidence_score * 0.15
                )
                
                if ctx.priority_score >= 0.7:
                    ctx.priority = ContextPriority.PRIMARY
                elif ctx.priority_score >= 0.5:
                    ctx.priority = ContextPriority.SECONDARY
                else:
                    ctx.priority = ContextPriority.TERTIARY
            
            sorted_contexts = sorted(region_stack.contexts, key=lambda x: x.priority_score, reverse=True)
            
            if len(sorted_contexts) > 8:
                displayed = sorted_contexts[:8]
                excess = sorted_contexts[8:]
                avg_confidence = sum(ctx.confidence_score for ctx in excess) / len(excess)
                region_stack.summarized_contexts = ContextStackSummary(
                    summarized_count=len(excess),
                    average_confidence=avg_confidence
                )
                region_stack.contexts = displayed
                region_stack.displayed_count = 8
            else:
                region_stack.contexts = sorted_contexts
                region_stack.displayed_count = len(sorted_contexts)
                region_stack.summarized_contexts = None
            
            region_stack.last_updated = datetime.utcnow()
            
            return region_stack.contexts


_store_instance: Optional[InMemoryStore] = None


def get_store() -> InMemoryStore:
    """Get the singleton store instance"""
    global _store_instance
    if _store_instance is None:
        _store_instance = InMemoryStore()
    return _store_instance
