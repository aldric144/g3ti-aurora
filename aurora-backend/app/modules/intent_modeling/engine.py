"""
AURORA™ Intent Gradient Modeling Engine
Models threat evolution as a continuous gradient

This module implements the Intent Gradient model that:
1. Tracks threat progression through 4 stages
2. Models evolution as a gradient, not binary states
3. Calculates velocity and acceleration of escalation
4. Identifies historical analogs for context
5. Provides full explainability for audit purposes

Stages:
- Stage 1: Grievance Formation
- Stage 2: Cognitive Fixation
- Stage 3: Behavioral Acceleration
- Stage 4: Mobilization Risk
"""

from datetime import datetime
from typing import Optional
import math

from app.models.schemas import (
    Signal,
    SignalType,
    SignalDomain,
    ThreatObject,
    IntentGradient,
    IntentStage,
    HistoricalAnalog,
)
from app.database.store import get_store


class IntentGradientEngine:
    """
    Intent Gradient Modeling Engine
    
    Models threat evolution as a continuous gradient across four stages.
    Each stage has associated signal patterns that indicate progression.
    """
    
    STAGE_SIGNAL_WEIGHTS = {
        IntentStage.GRIEVANCE_FORMATION: {
            SignalType.SENTIMENT_SHIFT: 1.5,
            SignalType.TOPIC_EMERGENCE: 1.3,
            SignalType.ECONOMIC_STRESS: 1.4,
            SignalType.NARRATIVE_AMPLIFICATION: 1.0,
        },
        IntentStage.COGNITIVE_FIXATION: {
            SignalType.FIXATION_INDICATOR: 1.6,
            SignalType.NARRATIVE_AMPLIFICATION: 1.4,
            SignalType.FREQUENCY_INCREASE: 1.3,
            SignalType.TOPIC_EMERGENCE: 1.1,
        },
        IntentStage.BEHAVIORAL_ACCELERATION: {
            SignalType.ESCALATION_PATTERN: 1.6,
            SignalType.FREQUENCY_INCREASE: 1.5,
            SignalType.NETWORK_EXPANSION: 1.4,
            SignalType.GEOGRAPHIC_CLUSTERING: 1.2,
        },
        IntentStage.MOBILIZATION_RISK: {
            SignalType.ESCALATION_PATTERN: 1.7,
            SignalType.NETWORK_EXPANSION: 1.6,
            SignalType.GEOGRAPHIC_CLUSTERING: 1.5,
            SignalType.TEMPORAL_PATTERN: 1.3,
        },
    }
    
    STAGE_THRESHOLDS = {
        IntentStage.GRIEVANCE_FORMATION: 0.0,
        IntentStage.COGNITIVE_FIXATION: 0.35,
        IntentStage.BEHAVIORAL_ACCELERATION: 0.55,
        IntentStage.MOBILIZATION_RISK: 0.75,
    }
    
    HISTORICAL_ANALOGS_DB = [
        {
            "name": "2008 Economic Crisis Social Response",
            "description": "Widespread economic grievance leading to organized protests",
            "outcome": "Peaceful demonstrations with policy engagement",
            "lessons_learned": "Early community engagement reduced escalation",
            "date_range": "2008-2010",
            "signal_pattern": {
                SignalType.ECONOMIC_STRESS: 0.9,
                SignalType.SENTIMENT_SHIFT: 0.8,
                SignalType.NARRATIVE_AMPLIFICATION: 0.7,
            }
        },
        {
            "name": "Regional Labor Movement 2011",
            "description": "Labor-related grievances escalating to sustained action",
            "outcome": "Extended protests with negotiated resolution",
            "lessons_learned": "Clear communication timelines aided de-escalation",
            "date_range": "2011-2012",
            "signal_pattern": {
                SignalType.FREQUENCY_INCREASE: 0.85,
                SignalType.ESCALATION_PATTERN: 0.75,
                SignalType.NETWORK_EXPANSION: 0.7,
            }
        },
        {
            "name": "Community Safety Concerns 2020",
            "description": "Safety-related grievances with rapid mobilization",
            "outcome": "Mixed outcomes with policy changes and continued tension",
            "lessons_learned": "Rapid response and transparency critical",
            "date_range": "2020",
            "signal_pattern": {
                SignalType.SENTIMENT_SHIFT: 0.95,
                SignalType.ESCALATION_PATTERN: 0.9,
                SignalType.GEOGRAPHIC_CLUSTERING: 0.85,
            }
        },
        {
            "name": "Environmental Advocacy Movement",
            "description": "Environmental concerns driving organized action",
            "outcome": "Sustained advocacy with incremental policy wins",
            "lessons_learned": "Long-term engagement more effective than suppression",
            "date_range": "2018-2022",
            "signal_pattern": {
                SignalType.TOPIC_EMERGENCE: 0.8,
                SignalType.NETWORK_EXPANSION: 0.85,
                SignalType.FIXATION_INDICATOR: 0.7,
            }
        },
    ]
    
    def __init__(self):
        self.store = get_store()
    
    def calculate_intent_gradient(self, threat: ThreatObject) -> IntentGradient:
        """
        Calculate the intent gradient for a threat.
        
        This analyzes signal patterns to determine:
        1. Current stage in the threat evolution
        2. Score for each stage (continuous gradient)
        3. Velocity of escalation
        4. Acceleration (change in velocity)
        
        Returns:
            Updated IntentGradient with full gradient analysis
        """
        signals = threat.signals
        
        if not signals:
            return self._create_baseline_gradient()
        
        stage_scores = self._calculate_stage_scores(signals)
        
        current_stage = self._determine_current_stage(stage_scores)
        
        stage_confidence = self._calculate_stage_confidence(stage_scores, current_stage)
        
        velocity, acceleration = self._calculate_velocity_and_acceleration(
            threat, stage_scores
        )
        
        time_in_stage = self._calculate_time_in_stage(threat, current_stage)
        
        stage_history = self._update_stage_history(threat, current_stage)
        
        gradient = IntentGradient(
            current_stage=current_stage,
            stage_confidence=stage_confidence,
            velocity=velocity,
            acceleration=acceleration,
            time_in_stage=time_in_stage,
            stage_history=stage_history,
            stage_1_score=stage_scores[IntentStage.GRIEVANCE_FORMATION],
            stage_2_score=stage_scores[IntentStage.COGNITIVE_FIXATION],
            stage_3_score=stage_scores[IntentStage.BEHAVIORAL_ACCELERATION],
            stage_4_score=stage_scores[IntentStage.MOBILIZATION_RISK],
        )
        
        self._log_gradient_calculation(threat.id, gradient)
        
        return gradient
    
    def _calculate_stage_scores(self, signals: list[Signal]) -> dict[IntentStage, float]:
        """
        Calculate score for each stage based on signal patterns.
        
        Each stage has associated signal types that indicate progression.
        Scores are calculated as weighted sums of matching signals.
        """
        stage_scores = {
            IntentStage.GRIEVANCE_FORMATION: 0.0,
            IntentStage.COGNITIVE_FIXATION: 0.0,
            IntentStage.BEHAVIORAL_ACCELERATION: 0.0,
            IntentStage.MOBILIZATION_RISK: 0.0,
        }
        
        for stage, signal_weights in self.STAGE_SIGNAL_WEIGHTS.items():
            stage_total = 0.0
            weight_total = 0.0
            
            for signal in signals:
                if signal.signal_type in signal_weights:
                    type_weight = signal_weights[signal.signal_type]
                    contribution = signal.raw_confidence * signal.weight * type_weight
                    stage_total += contribution
                    weight_total += type_weight
            
            if weight_total > 0:
                raw_score = stage_total / weight_total
                signal_count_bonus = min(len(signals) / 10, 0.2)
                stage_scores[stage] = min(raw_score + signal_count_bonus, 1.0)
        
        return stage_scores
    
    def _determine_current_stage(self, stage_scores: dict[IntentStage, float]) -> IntentStage:
        """
        Determine the current stage based on gradient scores.
        
        The current stage is the highest stage where the score exceeds
        the threshold AND all previous stages also exceed their thresholds.
        """
        stages_in_order = [
            IntentStage.GRIEVANCE_FORMATION,
            IntentStage.COGNITIVE_FIXATION,
            IntentStage.BEHAVIORAL_ACCELERATION,
            IntentStage.MOBILIZATION_RISK,
        ]
        
        current_stage = IntentStage.GRIEVANCE_FORMATION
        
        for stage in stages_in_order:
            threshold = self.STAGE_THRESHOLDS[stage]
            if stage_scores[stage] >= threshold:
                current_stage = stage
            else:
                break
        
        return current_stage
    
    def _calculate_stage_confidence(
        self,
        stage_scores: dict[IntentStage, float],
        current_stage: IntentStage
    ) -> float:
        """
        Calculate confidence in the current stage assessment.
        
        Confidence is higher when:
        - Current stage score is well above threshold
        - Next stage score is well below its threshold
        - Stage scores show clear progression pattern
        """
        current_score = stage_scores[current_stage]
        current_threshold = self.STAGE_THRESHOLDS[current_stage]
        
        margin_above = current_score - current_threshold
        
        stages_list = list(IntentStage)
        current_idx = stages_list.index(current_stage)
        
        if current_idx < len(stages_list) - 1:
            next_stage = stages_list[current_idx + 1]
            next_score = stage_scores[next_stage]
            next_threshold = self.STAGE_THRESHOLDS[next_stage]
            margin_below = next_threshold - next_score
        else:
            margin_below = 0.5
        
        confidence = 0.5 + (margin_above * 0.3) + (margin_below * 0.3)
        
        return min(max(confidence, 0.3), 0.95)
    
    def _calculate_velocity_and_acceleration(
        self,
        threat: ThreatObject,
        current_scores: dict[IntentStage, float]
    ) -> tuple[float, float]:
        """
        Calculate velocity and acceleration of threat escalation.
        
        Velocity: Rate of change in overall threat progression
        Acceleration: Rate of change in velocity (speeding up or slowing down)
        """
        if not threat.intent_gradient:
            return 0.0, 0.0
        
        prev_gradient = threat.intent_gradient
        
        current_overall = sum(current_scores.values()) / len(current_scores)
        prev_overall = (
            prev_gradient.stage_1_score +
            prev_gradient.stage_2_score +
            prev_gradient.stage_3_score +
            prev_gradient.stage_4_score
        ) / 4
        
        velocity = current_overall - prev_overall
        
        velocity = max(min(velocity, 1.0), -1.0)
        
        prev_velocity = prev_gradient.velocity
        acceleration = velocity - prev_velocity
        
        acceleration = max(min(acceleration, 0.5), -0.5)
        
        return round(velocity, 3), round(acceleration, 3)
    
    def _calculate_time_in_stage(
        self,
        threat: ThreatObject,
        current_stage: IntentStage
    ) -> float:
        """Calculate hours spent in current stage"""
        if not threat.intent_gradient:
            return 0.0
        
        if threat.intent_gradient.current_stage == current_stage:
            return threat.intent_gradient.time_in_stage + 1.0
        else:
            return 0.0
    
    def _update_stage_history(
        self,
        threat: ThreatObject,
        current_stage: IntentStage
    ) -> list[dict]:
        """Update stage transition history"""
        if not threat.intent_gradient:
            return [{
                "stage": current_stage.value,
                "entered": datetime.utcnow().isoformat() + "Z",
                "exited": None
            }]
        
        history = threat.intent_gradient.stage_history.copy()
        
        if threat.intent_gradient.current_stage != current_stage:
            if history and history[-1]["exited"] is None:
                history[-1]["exited"] = datetime.utcnow().isoformat() + "Z"
            
            history.append({
                "stage": current_stage.value,
                "entered": datetime.utcnow().isoformat() + "Z",
                "exited": None
            })
        
        return history
    
    def _create_baseline_gradient(self) -> IntentGradient:
        """Create baseline gradient for threats with no signals"""
        return IntentGradient(
            current_stage=IntentStage.GRIEVANCE_FORMATION,
            stage_confidence=0.5,
            velocity=0.0,
            acceleration=0.0,
            time_in_stage=0.0,
            stage_history=[],
            stage_1_score=0.0,
            stage_2_score=0.0,
            stage_3_score=0.0,
            stage_4_score=0.0,
        )
    
    def find_historical_analogs(
        self,
        threat: ThreatObject,
        max_analogs: int = 3
    ) -> list[HistoricalAnalog]:
        """
        Find historical analogs that match the current threat pattern.
        
        Compares signal patterns to historical cases and returns
        the most similar analogs with similarity scores.
        """
        if not threat.signals:
            return []
        
        current_pattern = self._extract_signal_pattern(threat.signals)
        
        analog_scores = []
        
        for analog_data in self.HISTORICAL_ANALOGS_DB:
            similarity = self._calculate_pattern_similarity(
                current_pattern,
                analog_data["signal_pattern"]
            )
            
            if similarity > 0.3:
                analog = HistoricalAnalog(
                    name=analog_data["name"],
                    description=analog_data["description"],
                    similarity_score=round(similarity, 2),
                    outcome=analog_data["outcome"],
                    lessons_learned=analog_data["lessons_learned"],
                    date_range=analog_data["date_range"]
                )
                analog_scores.append((similarity, analog))
        
        analog_scores.sort(key=lambda x: x[0], reverse=True)
        
        return [analog for _, analog in analog_scores[:max_analogs]]
    
    def _extract_signal_pattern(self, signals: list[Signal]) -> dict[SignalType, float]:
        """Extract signal type pattern from signals"""
        pattern: dict[SignalType, list[float]] = {}
        
        for signal in signals:
            if signal.signal_type not in pattern:
                pattern[signal.signal_type] = []
            pattern[signal.signal_type].append(signal.raw_confidence * signal.weight)
        
        return {
            sig_type: sum(scores) / len(scores)
            for sig_type, scores in pattern.items()
        }
    
    def _calculate_pattern_similarity(
        self,
        current: dict[SignalType, float],
        historical: dict[SignalType, float]
    ) -> float:
        """Calculate similarity between two signal patterns"""
        all_types = set(current.keys()) | set(historical.keys())
        
        if not all_types:
            return 0.0
        
        similarity_sum = 0.0
        
        for sig_type in all_types:
            current_val = current.get(sig_type, 0.0)
            historical_val = historical.get(sig_type, 0.0)
            
            if current_val > 0 and historical_val > 0:
                diff = abs(current_val - historical_val)
                type_similarity = 1 - min(diff, 1.0)
                similarity_sum += type_similarity
        
        overlap_count = len(set(current.keys()) & set(historical.keys()))
        overlap_bonus = overlap_count / len(all_types) if all_types else 0
        
        base_similarity = similarity_sum / len(all_types)
        
        return base_similarity * 0.7 + overlap_bonus * 0.3
    
    def _log_gradient_calculation(self, threat_id: str, gradient: IntentGradient):
        """Log gradient calculation for audit trail"""
        self.store._log_audit(
            action_type="intent_gradient_calculated",
            actor="intent_gradient_engine",
            target_type="threat",
            target_id=threat_id,
            reasoning=f"Intent gradient calculated: stage={gradient.current_stage.value}, velocity={gradient.velocity}",
            after_state={
                "current_stage": gradient.current_stage.value,
                "stage_confidence": gradient.stage_confidence,
                "velocity": gradient.velocity,
                "acceleration": gradient.acceleration,
                "stage_scores": {
                    "stage_1": gradient.stage_1_score,
                    "stage_2": gradient.stage_2_score,
                    "stage_3": gradient.stage_3_score,
                    "stage_4": gradient.stage_4_score,
                }
            }
        )
    
    def recalculate_threat_gradient(self, threat_id: str) -> Optional[ThreatObject]:
        """
        Recalculate intent gradient for a threat.
        
        Should be called after signal changes or feedback application.
        """
        threat = self.store.get_threat(threat_id)
        if not threat:
            return None
        
        new_gradient = self.calculate_intent_gradient(threat)
        threat.intent_gradient = new_gradient
        
        new_analogs = self.find_historical_analogs(threat)
        threat.historical_analogs = new_analogs
        
        threat.updated_at = datetime.utcnow()
        self.store.update_threat(threat)
        
        return threat
