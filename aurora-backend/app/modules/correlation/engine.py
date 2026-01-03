"""
AURORA™ Weak-Signal Convergence Engine
PATENT CRITICAL - Core Innovation

This engine implements the novel convergence algorithm that:
1. Detects emerging threats from multiple low-confidence signals
2. Requires signals from multiple domains (no single-signal triggers)
3. Produces threat probability through convergence, NOT thresholds
4. Provides full explainability and audit trail

Key Innovation: Threat probability emerges from the CONVERGENCE of weak signals
across domains, not from any single strong signal or threshold crossing.

PATENT-CRITICAL CONSTRAINTS (Deep/Dark Web & Physical-Digital):
- NO single domain may independently trigger alerts or threat elevation
- Intelligence elevation ONLY through multi-domain convergence
- Physical-world signals function as contextual amplifiers only
- All outputs are trend-level indicators, NOT evidentiary material
- System explicitly distinguishes decision support from investigative action
"""

from datetime import datetime
from typing import Optional
import math

from app.models.schemas import (
    Signal,
    SignalDomain,
    ThreatObject,
    ThreatProbabilityCurve,
    ConfidenceBound,
)
from app.database.store import get_store


class ConvergenceEngine:
    """
    Weak-Signal Convergence Engine
    
    Core algorithm for detecting emerging threats through signal convergence.
    This is the patent-critical innovation of AURORA™.
    """
    
    MIN_DOMAINS_FOR_CONVERGENCE = 2
    
    DOMAIN_CORRELATION_WEIGHTS = {
        (SignalDomain.SOCIAL_DISCOURSE, SignalDomain.BEHAVIORAL_TREND): 1.3,
        (SignalDomain.SOCIAL_DISCOURSE, SignalDomain.ENVIRONMENTAL_STRESSOR): 1.2,
        (SignalDomain.BEHAVIORAL_TREND, SignalDomain.ENVIRONMENTAL_STRESSOR): 1.4,
    }
    
    def __init__(self):
        self.store = get_store()
    
    def calculate_convergence(self, threat: ThreatObject) -> ThreatProbabilityCurve:
        """
        Calculate threat probability through weak-signal convergence.
        
        This is the core patent-critical algorithm. Probability emerges from:
        1. Multi-domain signal presence (required)
        2. Weighted signal confidence aggregation
        3. Cross-domain correlation amplification
        4. Temporal coherence assessment
        
        Returns:
            Updated ThreatProbabilityCurve with convergence-based probability
        """
        signals = threat.signals
        
        if not signals:
            return self._create_zero_probability_curve()
        
        domain_signals = self._group_signals_by_domain(signals)
        active_domains = [d for d, sigs in domain_signals.items() if len(sigs) > 0]
        
        if len(active_domains) < self.MIN_DOMAINS_FOR_CONVERGENCE:
            base_probability = self._calculate_single_domain_probability(signals)
            return self._create_low_convergence_curve(base_probability, signals, domain_signals)
        
        domain_scores = self._calculate_domain_scores(domain_signals)
        
        cross_domain_amplification = self._calculate_cross_domain_amplification(
            domain_signals, domain_scores
        )
        
        temporal_coherence = self._calculate_temporal_coherence(signals)
        
        convergence_score = self._calculate_convergence_score(
            domain_scores, cross_domain_amplification, temporal_coherence
        )
        
        raw_probability = self._convergence_to_probability(convergence_score)
        
        confidence_bounds = self._calculate_confidence_bounds(
            raw_probability, signals, convergence_score
        )
        
        trend, velocity = self._calculate_trend(threat)
        
        probability_curve = ThreatProbabilityCurve(
            current_probability=raw_probability,
            confidence_bounds=confidence_bounds,
            trend=trend,
            trend_velocity=velocity,
            convergence_score=convergence_score,
            contributing_signals=len(signals),
            domain_coverage={d.value: len(sigs) for d, sigs in domain_signals.items()},
            last_updated=datetime.utcnow(),
            history=threat.probability_curve.history if threat.probability_curve else []
        )
        
        self._log_convergence_calculation(threat.id, probability_curve, domain_scores)
        
        return probability_curve
    
    def _group_signals_by_domain(self, signals: list[Signal]) -> dict[SignalDomain, list[Signal]]:
        """Group signals by their domain"""
        domain_signals: dict[SignalDomain, list[Signal]] = {
            SignalDomain.SOCIAL_DISCOURSE: [],
            SignalDomain.BEHAVIORAL_TREND: [],
            SignalDomain.ENVIRONMENTAL_STRESSOR: [],
        }
        
        for signal in signals:
            if signal.domain in domain_signals:
                domain_signals[signal.domain].append(signal)
        
        return domain_signals
    
    def _calculate_domain_scores(
        self, domain_signals: dict[SignalDomain, list[Signal]]
    ) -> dict[SignalDomain, float]:
        """
        Calculate weighted score for each domain.
        
        Uses weighted average of signal confidences within each domain,
        with diminishing returns for additional signals (log scaling).
        """
        domain_scores = {}
        
        for domain, signals in domain_signals.items():
            if not signals:
                domain_scores[domain] = 0.0
                continue
            
            weighted_sum = sum(s.raw_confidence * s.weight for s in signals)
            weight_sum = sum(s.weight for s in signals)
            
            if weight_sum > 0:
                base_score = weighted_sum / weight_sum
            else:
                base_score = 0.0
            
            signal_count_factor = 1 + (math.log(len(signals) + 1) / 3)
            
            domain_scores[domain] = min(base_score * signal_count_factor, 1.0)
        
        return domain_scores
    
    def _calculate_cross_domain_amplification(
        self,
        domain_signals: dict[SignalDomain, list[Signal]],
        domain_scores: dict[SignalDomain, float]
    ) -> float:
        """
        Calculate cross-domain correlation amplification.
        
        When signals from different domains show correlation (temporal proximity,
        related metadata), the convergence is amplified. This is the key innovation
        that makes weak signals meaningful through convergence.
        """
        amplification = 1.0
        
        active_domains = [d for d, score in domain_scores.items() if score > 0]
        
        for i, domain1 in enumerate(active_domains):
            for domain2 in active_domains[i+1:]:
                pair = tuple(sorted([domain1, domain2], key=lambda x: x.value))
                pair_weight = self.DOMAIN_CORRELATION_WEIGHTS.get(pair, 1.1)
                
                score1 = domain_scores[domain1]
                score2 = domain_scores[domain2]
                correlation_strength = (score1 * score2) ** 0.5
                
                pair_amplification = 1 + (pair_weight - 1) * correlation_strength
                amplification *= pair_amplification
        
        return min(amplification, 2.0)
    
    def _calculate_temporal_coherence(self, signals: list[Signal]) -> float:
        """
        Calculate temporal coherence of signals.
        
        Signals that cluster in time indicate stronger convergence.
        Scattered signals over long periods indicate weaker convergence.
        """
        if len(signals) < 2:
            return 0.5
        
        timestamps = sorted([s.timestamp.timestamp() for s in signals])
        
        time_span = timestamps[-1] - timestamps[0]
        
        if time_span == 0:
            return 1.0
        
        intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
        avg_interval = sum(intervals) / len(intervals)
        
        if avg_interval == 0:
            return 1.0
        
        variance = sum((i - avg_interval) ** 2 for i in intervals) / len(intervals)
        std_dev = variance ** 0.5
        cv = std_dev / avg_interval if avg_interval > 0 else 0
        
        coherence = 1 / (1 + cv)
        
        hours_span = time_span / 3600
        if hours_span > 168:
            coherence *= 0.8
        elif hours_span < 24:
            coherence *= 1.1
        
        return min(max(coherence, 0.0), 1.0)
    
    def _calculate_convergence_score(
        self,
        domain_scores: dict[SignalDomain, float],
        cross_domain_amplification: float,
        temporal_coherence: float
    ) -> float:
        """
        Calculate final convergence score.
        
        This is the core metric that determines threat probability.
        Convergence requires multiple domains - single domain signals
        cannot produce high convergence scores.
        """
        active_domains = [d for d, score in domain_scores.items() if score > 0]
        
        if len(active_domains) < self.MIN_DOMAINS_FOR_CONVERGENCE:
            return max(domain_scores.values()) * 0.3 if domain_scores else 0.0
        
        domain_coverage_bonus = len(active_domains) / 3.0
        
        avg_domain_score = sum(domain_scores.values()) / len(domain_scores)
        
        convergence = (
            avg_domain_score * 
            cross_domain_amplification * 
            temporal_coherence * 
            (0.7 + 0.3 * domain_coverage_bonus)
        )
        
        return min(max(convergence, 0.0), 1.0)
    
    def _convergence_to_probability(self, convergence_score: float) -> float:
        """
        Convert convergence score to threat probability (0-100).
        
        Uses a sigmoid-like transformation to map convergence to probability,
        ensuring that low convergence produces low probability and high
        convergence produces high probability, with smooth transitions.
        """
        if convergence_score < 0.1:
            return convergence_score * 100
        
        x = (convergence_score - 0.5) * 6
        sigmoid = 1 / (1 + math.exp(-x))
        
        probability = sigmoid * 100
        
        return round(probability, 1)
    
    def _calculate_confidence_bounds(
        self,
        probability: float,
        signals: list[Signal],
        convergence_score: float
    ) -> ConfidenceBound:
        """
        Calculate confidence bounds for the probability estimate.
        
        Bounds are wider when:
        - Fewer signals are available
        - Signal confidences are lower
        - Convergence score is lower
        """
        base_uncertainty = 15.0
        
        signal_factor = 1 / (1 + math.log(len(signals) + 1) / 2)
        
        avg_confidence = sum(s.raw_confidence for s in signals) / len(signals) if signals else 0.5
        confidence_factor = 1.5 - avg_confidence
        
        convergence_factor = 1.5 - convergence_score
        
        uncertainty = base_uncertainty * signal_factor * confidence_factor * convergence_factor
        uncertainty = min(max(uncertainty, 5.0), 30.0)
        
        lower = max(0.0, probability - uncertainty)
        upper = min(100.0, probability + uncertainty)
        
        return ConfidenceBound(lower=round(lower, 1), upper=round(upper, 1))
    
    def _calculate_trend(self, threat: ThreatObject) -> tuple[str, float]:
        """Calculate probability trend and velocity"""
        history = threat.probability_curve.history if threat.probability_curve else []
        
        if len(history) < 2:
            return "stable", 0.0
        
        recent = history[-3:] if len(history) >= 3 else history
        
        if len(recent) < 2:
            return "stable", 0.0
        
        first_prob = recent[0].get("probability", 0)
        last_prob = recent[-1].get("probability", 0)
        
        change = last_prob - first_prob
        
        if abs(change) < 2:
            return "stable", 0.0
        elif change > 0:
            return "increasing", round(change / len(recent), 2)
        else:
            return "decreasing", round(change / len(recent), 2)
    
    def _create_zero_probability_curve(self) -> ThreatProbabilityCurve:
        """Create a zero-probability curve for threats with no signals"""
        return ThreatProbabilityCurve(
            current_probability=0.0,
            confidence_bounds=ConfidenceBound(lower=0.0, upper=10.0),
            trend="stable",
            trend_velocity=0.0,
            convergence_score=0.0,
            contributing_signals=0,
            domain_coverage={},
            history=[]
        )
    
    def _create_low_convergence_curve(
        self,
        base_probability: float,
        signals: list[Signal],
        domain_signals: dict[SignalDomain, list[Signal]]
    ) -> ThreatProbabilityCurve:
        """Create a low-convergence curve when domain requirements not met"""
        return ThreatProbabilityCurve(
            current_probability=base_probability,
            confidence_bounds=ConfidenceBound(
                lower=max(0, base_probability - 20),
                upper=min(100, base_probability + 20)
            ),
            trend="stable",
            trend_velocity=0.0,
            convergence_score=0.2,
            contributing_signals=len(signals),
            domain_coverage={d.value: len(sigs) for d, sigs in domain_signals.items()},
            history=[]
        )
    
    def _calculate_single_domain_probability(self, signals: list[Signal]) -> float:
        """Calculate limited probability when only one domain has signals"""
        if not signals:
            return 0.0
        
        weighted_sum = sum(s.raw_confidence * s.weight for s in signals)
        weight_sum = sum(s.weight for s in signals)
        
        if weight_sum > 0:
            avg_confidence = weighted_sum / weight_sum
        else:
            avg_confidence = 0.0
        
        return round(avg_confidence * 30, 1)
    
    def _log_convergence_calculation(
        self,
        threat_id: str,
        curve: ThreatProbabilityCurve,
        domain_scores: dict[SignalDomain, float]
    ):
        """Log convergence calculation for audit trail"""
        self.store._log_audit(
            action_type="convergence_calculated",
            actor="convergence_engine",
            target_type="threat",
            target_id=threat_id,
            reasoning=f"Convergence calculation completed: probability={curve.current_probability}, convergence_score={curve.convergence_score}",
            after_state={
                "probability": curve.current_probability,
                "convergence_score": curve.convergence_score,
                "domain_scores": {d.value: s for d, s in domain_scores.items()},
                "contributing_signals": curve.contributing_signals
            }
        )
    
    def recalculate_threat(self, threat_id: str) -> Optional[ThreatObject]:
        """
        Recalculate convergence for a threat and update its probability curve.
        
        This should be called whenever:
        - New signals are added
        - Signal weights are adjusted
        - Feedback is applied
        """
        threat = self.store.get_threat(threat_id)
        if not threat:
            return None
        
        new_curve = self.calculate_convergence(threat)
        
        if threat.probability_curve:
            new_curve.history = threat.probability_curve.history.copy()
        
        new_curve.history.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "probability": new_curve.current_probability
        })
        
        if len(new_curve.history) > 100:
            new_curve.history = new_curve.history[-100:]
        
        threat.probability_curve = new_curve
        threat.updated_at = datetime.utcnow()
        
        self.store.update_threat(threat)
        
        self.store.add_probability_history(
            threat_id,
            new_curve.current_probability,
            new_curve.confidence_bounds.lower,
            new_curve.confidence_bounds.upper
        )
        
        return threat
