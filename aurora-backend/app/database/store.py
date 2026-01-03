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
        
        self._initialized = True
        
        self._seed_jurisdictions()
        self._seed_demo_data()
    
    def _seed_jurisdictions(self):
        """
        Seed global jurisdiction contexts for signal interpretation.
        
        IMPORTANT: Jurisdiction context adjusts signal interpretation, weighting,
        historical analogs, and narrative framing. It does NOT activate new data
        collection or imply active monitoring of individuals or regions.
        """
        jurisdictions_data = [
            {"code": "US", "name": "United States", "region": "North America", "tags": ["north_america", "developed_economy", "federal_republic"]},
            {"code": "CA", "name": "Canada", "region": "North America", "tags": ["north_america", "developed_economy", "parliamentary"]},
            {"code": "MX", "name": "Mexico", "region": "North America", "tags": ["north_america", "emerging_economy", "federal_republic"]},
            {"code": "GB", "name": "United Kingdom", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary"]},
            {"code": "DE", "name": "Germany", "region": "Europe", "tags": ["europe", "developed_economy", "federal_republic", "eu_member"]},
            {"code": "FR", "name": "France", "region": "Europe", "tags": ["europe", "developed_economy", "semi_presidential", "eu_member"]},
            {"code": "IT", "name": "Italy", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "ES", "name": "Spain", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "PT", "name": "Portugal", "region": "Europe", "tags": ["europe", "developed_economy", "semi_presidential", "eu_member"]},
            {"code": "NL", "name": "Netherlands", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "BE", "name": "Belgium", "region": "Europe", "tags": ["europe", "developed_economy", "federal_parliamentary", "eu_member"]},
            {"code": "AT", "name": "Austria", "region": "Europe", "tags": ["europe", "developed_economy", "federal_republic", "eu_member"]},
            {"code": "CH", "name": "Switzerland", "region": "Europe", "tags": ["europe", "developed_economy", "federal_republic"]},
            {"code": "SE", "name": "Sweden", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "NO", "name": "Norway", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary"]},
            {"code": "DK", "name": "Denmark", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "FI", "name": "Finland", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "IE", "name": "Ireland", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "PL", "name": "Poland", "region": "Europe", "tags": ["europe", "emerging_economy", "parliamentary", "eu_member"]},
            {"code": "CZ", "name": "Czech Republic", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "HU", "name": "Hungary", "region": "Europe", "tags": ["europe", "emerging_economy", "parliamentary", "eu_member"]},
            {"code": "RO", "name": "Romania", "region": "Europe", "tags": ["europe", "emerging_economy", "semi_presidential", "eu_member"]},
            {"code": "BG", "name": "Bulgaria", "region": "Europe", "tags": ["europe", "emerging_economy", "parliamentary", "eu_member"]},
            {"code": "GR", "name": "Greece", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "HR", "name": "Croatia", "region": "Europe", "tags": ["europe", "emerging_economy", "parliamentary", "eu_member"]},
            {"code": "SK", "name": "Slovakia", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "SI", "name": "Slovenia", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "LT", "name": "Lithuania", "region": "Europe", "tags": ["europe", "developed_economy", "semi_presidential", "eu_member"]},
            {"code": "LV", "name": "Latvia", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "EE", "name": "Estonia", "region": "Europe", "tags": ["europe", "developed_economy", "parliamentary", "eu_member"]},
            {"code": "RU", "name": "Russia", "region": "Europe", "tags": ["europe", "emerging_economy", "federal_republic"]},
            {"code": "UA", "name": "Ukraine", "region": "Europe", "tags": ["europe", "emerging_economy", "semi_presidential"]},
            {"code": "TR", "name": "Turkey", "region": "Middle East", "tags": ["middle_east", "emerging_economy", "presidential"]},
            {"code": "IL", "name": "Israel", "region": "Middle East", "tags": ["middle_east", "developed_economy", "parliamentary"]},
            {"code": "SA", "name": "Saudi Arabia", "region": "Middle East", "tags": ["middle_east", "emerging_economy", "monarchy"]},
            {"code": "AE", "name": "United Arab Emirates", "region": "Middle East", "tags": ["middle_east", "developed_economy", "federation"]},
            {"code": "QA", "name": "Qatar", "region": "Middle East", "tags": ["middle_east", "developed_economy", "monarchy"]},
            {"code": "KW", "name": "Kuwait", "region": "Middle East", "tags": ["middle_east", "developed_economy", "constitutional_monarchy"]},
            {"code": "BH", "name": "Bahrain", "region": "Middle East", "tags": ["middle_east", "developed_economy", "constitutional_monarchy"]},
            {"code": "OM", "name": "Oman", "region": "Middle East", "tags": ["middle_east", "emerging_economy", "monarchy"]},
            {"code": "JO", "name": "Jordan", "region": "Middle East", "tags": ["middle_east", "emerging_economy", "constitutional_monarchy"]},
            {"code": "LB", "name": "Lebanon", "region": "Middle East", "tags": ["middle_east", "emerging_economy", "parliamentary"]},
            {"code": "EG", "name": "Egypt", "region": "Africa", "tags": ["africa", "emerging_economy", "presidential"]},
            {"code": "ZA", "name": "South Africa", "region": "Africa", "tags": ["africa", "emerging_economy", "parliamentary"]},
            {"code": "NG", "name": "Nigeria", "region": "Africa", "tags": ["africa", "emerging_economy", "federal_republic"]},
            {"code": "KE", "name": "Kenya", "region": "Africa", "tags": ["africa", "emerging_economy", "presidential"]},
            {"code": "GH", "name": "Ghana", "region": "Africa", "tags": ["africa", "emerging_economy", "presidential"]},
            {"code": "ET", "name": "Ethiopia", "region": "Africa", "tags": ["africa", "emerging_economy", "federal_republic"]},
            {"code": "TZ", "name": "Tanzania", "region": "Africa", "tags": ["africa", "emerging_economy", "presidential"]},
            {"code": "MA", "name": "Morocco", "region": "Africa", "tags": ["africa", "emerging_economy", "constitutional_monarchy"]},
            {"code": "DZ", "name": "Algeria", "region": "Africa", "tags": ["africa", "emerging_economy", "presidential"]},
            {"code": "TN", "name": "Tunisia", "region": "Africa", "tags": ["africa", "emerging_economy", "semi_presidential"]},
            {"code": "CN", "name": "China", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "single_party"]},
            {"code": "JP", "name": "Japan", "region": "Asia Pacific", "tags": ["asia_pacific", "developed_economy", "parliamentary"]},
            {"code": "KR", "name": "South Korea", "region": "Asia Pacific", "tags": ["asia_pacific", "developed_economy", "presidential"]},
            {"code": "IN", "name": "India", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "federal_parliamentary"]},
            {"code": "AU", "name": "Australia", "region": "Asia Pacific", "tags": ["asia_pacific", "developed_economy", "federal_parliamentary"]},
            {"code": "NZ", "name": "New Zealand", "region": "Asia Pacific", "tags": ["asia_pacific", "developed_economy", "parliamentary"]},
            {"code": "SG", "name": "Singapore", "region": "Asia Pacific", "tags": ["asia_pacific", "developed_economy", "parliamentary"]},
            {"code": "MY", "name": "Malaysia", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "federal_parliamentary"]},
            {"code": "TH", "name": "Thailand", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "constitutional_monarchy"]},
            {"code": "VN", "name": "Vietnam", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "single_party"]},
            {"code": "ID", "name": "Indonesia", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "presidential"]},
            {"code": "PH", "name": "Philippines", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "presidential"]},
            {"code": "PK", "name": "Pakistan", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "federal_parliamentary"]},
            {"code": "BD", "name": "Bangladesh", "region": "Asia Pacific", "tags": ["asia_pacific", "emerging_economy", "parliamentary"]},
            {"code": "TW", "name": "Taiwan", "region": "Asia Pacific", "tags": ["asia_pacific", "developed_economy", "semi_presidential"]},
            {"code": "HK", "name": "Hong Kong", "region": "Asia Pacific", "tags": ["asia_pacific", "developed_economy", "special_administrative"]},
            {"code": "BR", "name": "Brazil", "region": "South America", "tags": ["south_america", "emerging_economy", "federal_republic"]},
            {"code": "AR", "name": "Argentina", "region": "South America", "tags": ["south_america", "emerging_economy", "federal_republic"]},
            {"code": "CL", "name": "Chile", "region": "South America", "tags": ["south_america", "emerging_economy", "presidential"]},
            {"code": "CO", "name": "Colombia", "region": "South America", "tags": ["south_america", "emerging_economy", "presidential"]},
            {"code": "PE", "name": "Peru", "region": "South America", "tags": ["south_america", "emerging_economy", "presidential"]},
            {"code": "VE", "name": "Venezuela", "region": "South America", "tags": ["south_america", "emerging_economy", "federal_republic"]},
            {"code": "EC", "name": "Ecuador", "region": "South America", "tags": ["south_america", "emerging_economy", "presidential"]},
            {"code": "UY", "name": "Uruguay", "region": "South America", "tags": ["south_america", "emerging_economy", "presidential"]},
            {"code": "PY", "name": "Paraguay", "region": "South America", "tags": ["south_america", "emerging_economy", "presidential"]},
            {"code": "BO", "name": "Bolivia", "region": "South America", "tags": ["south_america", "emerging_economy", "presidential"]},
            {"code": "PA", "name": "Panama", "region": "Central America", "tags": ["central_america", "emerging_economy", "presidential"]},
            {"code": "CR", "name": "Costa Rica", "region": "Central America", "tags": ["central_america", "emerging_economy", "presidential"]},
            {"code": "GT", "name": "Guatemala", "region": "Central America", "tags": ["central_america", "emerging_economy", "presidential"]},
            {"code": "HN", "name": "Honduras", "region": "Central America", "tags": ["central_america", "emerging_economy", "presidential"]},
            {"code": "SV", "name": "El Salvador", "region": "Central America", "tags": ["central_america", "emerging_economy", "presidential"]},
            {"code": "NI", "name": "Nicaragua", "region": "Central America", "tags": ["central_america", "emerging_economy", "presidential"]},
            {"code": "JM", "name": "Jamaica", "region": "Caribbean", "tags": ["caribbean", "emerging_economy", "parliamentary"]},
            {"code": "TT", "name": "Trinidad and Tobago", "region": "Caribbean", "tags": ["caribbean", "emerging_economy", "parliamentary"]},
            {"code": "DO", "name": "Dominican Republic", "region": "Caribbean", "tags": ["caribbean", "emerging_economy", "presidential"]},
            {"code": "CU", "name": "Cuba", "region": "Caribbean", "tags": ["caribbean", "emerging_economy", "single_party"]},
            {"code": "PR", "name": "Puerto Rico", "region": "Caribbean", "tags": ["caribbean", "developed_economy", "us_territory"]},
        ]
        
        for j in jurisdictions_data:
            jurisdiction = JurisdictionContext(
                code=j["code"],
                name=j["name"],
                region=j["region"],
                signal_weight_modifiers={
                    "economic_stress": 1.0,
                    "social_discourse": 1.0,
                    "behavioral_trend": 1.0,
                    "environmental_stressor": 1.0,
                },
                historical_analog_tags=j["tags"],
                narrative_context={
                    "governance_type": j["tags"][-1].replace("_", " ").title() if j["tags"] else "Unknown",
                    "economic_classification": "Developed" if "developed_economy" in j["tags"] else "Emerging",
                },
                economic_baseline={
                    "baseline_unemployment": 5.0,
                    "baseline_inflation": 2.0,
                },
                cultural_context_notes=[],
                legal_framework_notes=[],
                is_active=True,
            )
            self.jurisdictions[j["code"]] = jurisdiction
        
        self._log_audit(
            action_type="jurisdictions_seeded",
            actor="system",
            target_type="jurisdiction",
            target_id="all",
            reasoning=f"Seeded {len(jurisdictions_data)} global jurisdiction contexts"
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


_store_instance: Optional[InMemoryStore] = None


def get_store() -> InMemoryStore:
    """Get the singleton store instance"""
    global _store_instance
    if _store_instance is None:
        _store_instance = InMemoryStore()
    return _store_instance
