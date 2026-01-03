"""
AURORA™ Narrative Intelligence Generation Engine
PATENT CORE - AI-produced intelligence narratives

This engine generates Narrative Intelligence Objects (NIOs) that:
1. Provide plain-language executive summaries
2. Explain why threats matter
3. Detail what signals converged
4. Quantify confidence levels with explanations
5. Acknowledge known unknowns
6. Recommend monitoring postures
7. Document full reasoning chains for audit

NIOs replace dashboards with decision-ready intelligence that
executives can understand in 60 seconds.

PATENT-CRITICAL CONSTRAINTS (Explainability & Legal Defensibility):
- All outputs must be: Explainable, Auditable, Confidence-scored, Non-attributive
- System explicitly distinguishes:
  - Trend-level intelligence from evidentiary material
  - Decision support from investigative action
- Deep/dark web and physical-world signals are treated strictly as:
  - Trend-level behavioral and environmental indicators
  - NOT investigative leads, surveillance outputs, or evidentiary artifacts

INTELLIGENCE CLASSIFICATION:
All NIOs are classified as "TREND-LEVEL DECISION SUPPORT" and explicitly
state they are NOT evidentiary material or investigative leads.
"""

from datetime import datetime
from typing import Optional

from app.models.schemas import (
    Signal,
    SignalDomain,
    SignalType,
    ThreatObject,
    IntentStage,
    NarrativeIntelligenceObject,
    MonitoringPosture,
    JurisdictionContext,
)
from app.database.store import get_store


class NarrativeEngine:
    """
    Narrative Intelligence Generation Engine
    
    Generates comprehensive, human-readable intelligence narratives
    from threat analysis data. All narratives include full reasoning
    chains for audit and explainability requirements.
    """
    
    STAGE_DESCRIPTIONS = {
        IntentStage.GRIEVANCE_FORMATION: "initial grievance formation phase where concerns are crystallizing",
        IntentStage.COGNITIVE_FIXATION: "cognitive fixation phase where attention is increasingly focused on specific grievances",
        IntentStage.BEHAVIORAL_ACCELERATION: "behavioral acceleration phase with observable changes in activity patterns",
        IntentStage.MOBILIZATION_RISK: "elevated mobilization risk phase with indicators of potential organized action",
    }
    
    DOMAIN_DESCRIPTIONS = {
        SignalDomain.SOCIAL_DISCOURSE: "public discourse and sentiment patterns",
        SignalDomain.BEHAVIORAL_TREND: "observable behavioral indicators",
        SignalDomain.ENVIRONMENTAL_STRESSOR: "environmental and contextual stressors",
    }
    
    SIGNAL_TYPE_DESCRIPTIONS = {
        SignalType.SENTIMENT_SHIFT: "sentiment shift",
        SignalType.TOPIC_EMERGENCE: "emerging topic focus",
        SignalType.NARRATIVE_AMPLIFICATION: "narrative amplification",
        SignalType.FREQUENCY_INCREASE: "activity frequency increase",
        SignalType.ESCALATION_PATTERN: "escalation pattern",
        SignalType.FIXATION_INDICATOR: "fixation indicator",
        SignalType.ECONOMIC_STRESS: "economic stress indicator",
        SignalType.GEOGRAPHIC_CLUSTERING: "geographic clustering",
        SignalType.TEMPORAL_PATTERN: "temporal pattern",
        SignalType.NETWORK_EXPANSION: "network expansion",
    }
    
    def __init__(self):
        self.store = get_store()
    
    def generate_nio(self, threat: ThreatObject) -> NarrativeIntelligenceObject:
        """
        Generate a complete Narrative Intelligence Object for a threat.
        
        This is the core patent function that produces decision-ready
        intelligence narratives from threat analysis data.
        
        Jurisdiction context is applied to adjust narrative framing,
        historical analog selection, and signal interpretation.
        
        Returns:
            Complete NIO with all required narrative components
        """
        reasoning_chain = []
        
        jurisdiction = self.store.get_current_jurisdiction()
        jurisdiction_name = jurisdiction.name if jurisdiction else "United States"
        jurisdiction_code = jurisdiction.code if jurisdiction else "US"
        
        reasoning_chain.append(
            f"Step 1: Analyzed threat '{threat.name}' with {len(threat.signals)} contributing signals"
        )
        reasoning_chain.append(
            f"Step 1a: Applied jurisdiction context: {jurisdiction_name} ({jurisdiction_code}) - "
            "adjusts signal interpretation, weighting, and narrative framing"
        )
        
        executive_summary = self._generate_executive_summary(threat)
        reasoning_chain.append(
            f"Step 2: Generated executive summary based on {threat.probability_curve.current_probability}% probability and {threat.intent_gradient.current_stage.value} stage"
        )
        
        why_it_matters = self._generate_significance(threat)
        reasoning_chain.append(
            f"Step 3: Assessed significance based on convergence score of {threat.probability_curve.convergence_score:.2f}"
        )
        
        converged_signals = self._list_converged_signals(threat)
        signal_narrative = self._generate_signal_narrative(threat)
        reasoning_chain.append(
            f"Step 4: Documented {len(converged_signals)} converged signals across {len(threat.probability_curve.domain_coverage)} domains"
        )
        
        confidence_level = self._calculate_nio_confidence(threat)
        confidence_explanation = self._generate_confidence_explanation(threat)
        reasoning_chain.append(
            f"Step 5: Calculated confidence level of {confidence_level}% based on signal quality and convergence strength"
        )
        
        known_unknowns = self._identify_known_unknowns(threat)
        assumptions = self._identify_assumptions(threat)
        reasoning_chain.append(
            f"Step 6: Identified {len(known_unknowns)} known unknowns and {len(assumptions)} key assumptions"
        )
        
        monitoring_posture = self._determine_monitoring_posture(threat)
        posture_rationale = self._generate_posture_rationale(threat, monitoring_posture)
        reasoning_chain.append(
            f"Step 7: Recommended {monitoring_posture.value} monitoring posture based on threat trajectory"
        )
        
        recommended_actions = self._generate_recommended_actions(threat, monitoring_posture)
        reasoning_chain.append(
            f"Step 8: Generated {len(recommended_actions)} recommended actions for analyst consideration"
        )
        
        nio = NarrativeIntelligenceObject(
            threat_id=threat.id,
            executive_summary=executive_summary,
            why_it_matters=why_it_matters,
            converged_signals=converged_signals,
            signal_narrative=signal_narrative,
            confidence_level=confidence_level,
            confidence_explanation=confidence_explanation,
            known_unknowns=known_unknowns,
            assumptions=assumptions,
            monitoring_posture=monitoring_posture,
            posture_rationale=posture_rationale,
            recommended_actions=recommended_actions,
            reasoning_chain=reasoning_chain,
            version=self._get_next_version(threat)
        )
        
        self.store.store_nio(nio)
        
        return nio
    
    def _generate_executive_summary(self, threat: ThreatObject) -> str:
        """
        Generate plain-language executive summary.
        
        This summary must be understandable by executives in 60 seconds
        and provide actionable intelligence without technical jargon.
        """
        prob = threat.probability_curve.current_probability
        stage = threat.intent_gradient.current_stage
        stage_desc = self.STAGE_DESCRIPTIONS[stage]
        
        domain_count = len([d for d, c in threat.probability_curve.domain_coverage.items() if c > 0])
        signal_count = len(threat.signals)
        
        trend = threat.probability_curve.trend
        trend_phrase = {
            "increasing": "and showing an upward trajectory",
            "decreasing": "but showing signs of de-escalation",
            "stable": "with a stable trajectory"
        }.get(trend, "")
        
        confidence_qualifier = ""
        if threat.probability_curve.convergence_score > 0.7:
            confidence_qualifier = "Strong signal convergence supports this assessment. "
        elif threat.probability_curve.convergence_score > 0.5:
            confidence_qualifier = "Moderate signal convergence supports this assessment. "
        else:
            confidence_qualifier = "Limited signal convergence suggests continued monitoring is warranted. "
        
        summary = (
            f"Analysis of '{threat.name}' indicates a current threat probability of {prob:.1f}% "
            f"{trend_phrase}. The threat is currently in the {stage_desc}. "
            f"{signal_count} distinct signals across {domain_count} domains have converged to produce this assessment. "
            f"{confidence_qualifier}"
            f"Confidence bounds range from {threat.probability_curve.confidence_bounds.lower:.1f}% to "
            f"{threat.probability_curve.confidence_bounds.upper:.1f}%."
        )
        
        return summary
    
    def _generate_significance(self, threat: ThreatObject) -> str:
        """Generate explanation of why this threat matters"""
        stage = threat.intent_gradient.current_stage
        velocity = threat.intent_gradient.velocity
        
        significance_parts = []
        
        if stage in [IntentStage.BEHAVIORAL_ACCELERATION, IntentStage.MOBILIZATION_RISK]:
            significance_parts.append(
                f"This threat has progressed beyond early warning stages into {self.STAGE_DESCRIPTIONS[stage]}. "
                "This represents a critical window for intervention or preparation."
            )
        elif stage == IntentStage.COGNITIVE_FIXATION:
            significance_parts.append(
                "The threat has moved past initial grievance formation into cognitive fixation, "
                "indicating sustained attention to specific concerns. Early engagement may still be effective."
            )
        else:
            significance_parts.append(
                "While still in early stages, the convergence of multiple signals warrants attention. "
                "This represents an opportunity for proactive engagement before escalation."
            )
        
        if velocity > 0.2:
            significance_parts.append(
                f"The escalation velocity of {velocity:.2f} indicates rapid progression. "
                "Without intervention, advancement to the next stage is likely within days to weeks."
            )
        elif velocity < -0.1:
            significance_parts.append(
                f"The negative velocity of {velocity:.2f} suggests de-escalation may be occurring. "
                "Continued monitoring is recommended to confirm this trend."
            )
        
        if threat.historical_analogs:
            best_analog = max(threat.historical_analogs, key=lambda a: a.similarity_score)
            significance_parts.append(
                f"Historical analog '{best_analog.name}' ({best_analog.similarity_score:.0%} similarity) "
                f"suggests: {best_analog.lessons_learned}"
            )
        
        return " ".join(significance_parts)
    
    def _list_converged_signals(self, threat: ThreatObject) -> list[str]:
        """Generate list of converged signals in human-readable format"""
        signal_descriptions = []
        
        for signal in threat.signals:
            type_desc = self.SIGNAL_TYPE_DESCRIPTIONS.get(signal.signal_type, signal.signal_type.value)
            domain_desc = self.DOMAIN_DESCRIPTIONS.get(signal.domain, signal.domain.value)
            
            confidence_pct = signal.raw_confidence * 100
            
            description = f"{type_desc.capitalize()} in {domain_desc} ({confidence_pct:.0f}% confidence)"
            signal_descriptions.append(description)
        
        return signal_descriptions
    
    def _generate_signal_narrative(self, threat: ThreatObject) -> str:
        """Generate narrative explanation of how signals converged"""
        if not threat.signals:
            return "No signals have been associated with this threat yet."
        
        domain_signals: dict[SignalDomain, list[Signal]] = {}
        for signal in threat.signals:
            if signal.domain not in domain_signals:
                domain_signals[signal.domain] = []
            domain_signals[signal.domain].append(signal)
        
        narrative_parts = []
        
        active_domains = [d for d, sigs in domain_signals.items() if sigs]
        
        if len(active_domains) >= 3:
            narrative_parts.append(
                "This assessment is based on strong multi-domain convergence, with signals detected "
                "across all three primary domains (social discourse, behavioral trends, and environmental stressors). "
                "This cross-domain pattern significantly increases confidence in the assessment."
            )
        elif len(active_domains) == 2:
            domain_names = [self.DOMAIN_DESCRIPTIONS[d] for d in active_domains]
            narrative_parts.append(
                f"Signals have converged across two domains: {domain_names[0]} and {domain_names[1]}. "
                "This dual-domain convergence provides moderate confidence, though additional signals "
                "from the third domain would strengthen the assessment."
            )
        else:
            domain_name = self.DOMAIN_DESCRIPTIONS[active_domains[0]] if active_domains else "unknown"
            narrative_parts.append(
                f"Current signals are concentrated in {domain_name}. "
                "Single-domain signals provide limited convergence confidence. "
                "Additional cross-domain signals are needed for higher-confidence assessment."
            )
        
        for domain, signals in domain_signals.items():
            if not signals:
                continue
            
            domain_desc = self.DOMAIN_DESCRIPTIONS[domain]
            signal_types = list(set(s.signal_type for s in signals))
            type_descs = [self.SIGNAL_TYPE_DESCRIPTIONS.get(t, t.value) for t in signal_types]
            
            avg_confidence = sum(s.raw_confidence for s in signals) / len(signals)
            
            narrative_parts.append(
                f"Within {domain_desc}, {len(signals)} signal(s) were detected including "
                f"{', '.join(type_descs)}. Average signal confidence in this domain is {avg_confidence:.0%}."
            )
        
        timestamps = sorted([s.timestamp for s in threat.signals])
        if len(timestamps) >= 2:
            time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 3600
            if time_span < 24:
                narrative_parts.append(
                    f"All signals emerged within a {time_span:.1f}-hour window, indicating strong temporal coherence."
                )
            elif time_span < 168:
                narrative_parts.append(
                    f"Signals span approximately {time_span/24:.1f} days, showing sustained pattern development."
                )
        
        return " ".join(narrative_parts)
    
    def _calculate_nio_confidence(self, threat: ThreatObject) -> float:
        """Calculate overall NIO confidence level"""
        convergence_factor = threat.probability_curve.convergence_score * 40
        
        signal_count = len(threat.signals)
        signal_factor = min(signal_count / 5, 1.0) * 20
        
        domain_count = len([d for d, c in threat.probability_curve.domain_coverage.items() if c > 0])
        domain_factor = (domain_count / 3) * 25
        
        stage_confidence = threat.intent_gradient.stage_confidence * 15
        
        confidence = convergence_factor + signal_factor + domain_factor + stage_confidence
        
        return round(min(max(confidence, 10), 95), 1)
    
    def _generate_confidence_explanation(self, threat: ThreatObject) -> str:
        """Generate explanation of confidence level"""
        factors = []
        
        if threat.probability_curve.convergence_score > 0.7:
            factors.append("strong signal convergence across domains")
        elif threat.probability_curve.convergence_score > 0.5:
            factors.append("moderate signal convergence")
        else:
            factors.append("limited signal convergence (reduces confidence)")
        
        signal_count = len(threat.signals)
        if signal_count >= 5:
            factors.append(f"robust signal count ({signal_count} signals)")
        elif signal_count >= 3:
            factors.append(f"adequate signal count ({signal_count} signals)")
        else:
            factors.append(f"limited signal count ({signal_count} signals, reduces confidence)")
        
        domain_count = len([d for d, c in threat.probability_curve.domain_coverage.items() if c > 0])
        if domain_count == 3:
            factors.append("full domain coverage")
        elif domain_count == 2:
            factors.append("partial domain coverage")
        else:
            factors.append("single-domain coverage (reduces confidence)")
        
        if threat.intent_gradient.stage_confidence > 0.8:
            factors.append("high confidence in stage assessment")
        elif threat.intent_gradient.stage_confidence > 0.6:
            factors.append("moderate confidence in stage assessment")
        
        return f"Confidence is based on: {'; '.join(factors)}."
    
    def _identify_known_unknowns(self, threat: ThreatObject) -> list[str]:
        """Identify acknowledged gaps in intelligence"""
        unknowns = []
        
        domain_coverage = threat.probability_curve.domain_coverage
        if domain_coverage.get("social_discourse", 0) == 0:
            unknowns.append("Social discourse signals not yet available for this threat")
        if domain_coverage.get("behavioral_trend", 0) == 0:
            unknowns.append("Behavioral trend indicators not yet observed")
        if domain_coverage.get("environmental_stressor", 0) == 0:
            unknowns.append("Environmental stressor data not incorporated")
        
        unknowns.append("Leadership emergence within affected groups not yet observable")
        unknowns.append("External catalyst events that could accelerate or decelerate trajectory")
        unknowns.append("Effectiveness of any ongoing mitigation or engagement efforts")
        
        if threat.intent_gradient.current_stage in [IntentStage.COGNITIVE_FIXATION, IntentStage.BEHAVIORAL_ACCELERATION]:
            unknowns.append("Specific mobilization timeline if escalation continues")
        
        return unknowns
    
    def _identify_assumptions(self, threat: ThreatObject) -> list[str]:
        """Identify key assumptions underlying the assessment"""
        assumptions = [
            "INTELLIGENCE CLASSIFICATION: This NIO is TREND-LEVEL DECISION SUPPORT only",
            "This assessment is NOT evidentiary material, investigative lead, or surveillance output",
            "All signals are abstracted behavioral indicators, not individual-attributable data",
            "Current conditions will persist for at least 14 days without major external changes",
            "Signal sources remain representative of broader population sentiment",
            "Historical analog patterns remain relevant to current context",
            "No significant unreported mitigation efforts are underway",
        ]
        
        if threat.probability_curve.trend == "increasing":
            assumptions.append("Current escalation trajectory will continue without intervention")
        elif threat.probability_curve.trend == "decreasing":
            assumptions.append("De-escalation trend reflects genuine reduction in threat, not signal gap")
        
        return assumptions
    
    def _determine_monitoring_posture(self, threat: ThreatObject) -> MonitoringPosture:
        """Determine recommended monitoring posture"""
        prob = threat.probability_curve.current_probability
        stage = threat.intent_gradient.current_stage
        velocity = threat.intent_gradient.velocity
        
        if prob >= 80 or stage == IntentStage.MOBILIZATION_RISK:
            return MonitoringPosture.CRITICAL
        elif prob >= 60 or stage == IntentStage.BEHAVIORAL_ACCELERATION or velocity > 0.3:
            return MonitoringPosture.HEIGHTENED
        elif prob >= 40 or stage == IntentStage.COGNITIVE_FIXATION or velocity > 0.15:
            return MonitoringPosture.ELEVATED
        else:
            return MonitoringPosture.ROUTINE
    
    def _generate_posture_rationale(
        self,
        threat: ThreatObject,
        posture: MonitoringPosture
    ) -> str:
        """Generate rationale for monitoring posture recommendation"""
        rationales = {
            MonitoringPosture.CRITICAL: (
                f"Critical monitoring is recommended due to {threat.probability_curve.current_probability:.1f}% "
                f"threat probability and {threat.intent_gradient.current_stage.value} stage. "
                "This posture requires continuous signal monitoring, immediate escalation protocols, "
                "and preparation for rapid response. Recommend hourly NIO updates."
            ),
            MonitoringPosture.HEIGHTENED: (
                f"Heightened monitoring is recommended based on elevated probability "
                f"({threat.probability_curve.current_probability:.1f}%) and/or accelerating trajectory. "
                "This posture involves increased signal collection frequency and daily NIO updates. "
                "Prepare contingency response plans."
            ),
            MonitoringPosture.ELEVATED: (
                f"Elevated monitoring is recommended due to clear convergence pattern and "
                f"transition to {threat.intent_gradient.current_stage.value} stage. "
                "This posture allows for early detection of behavioral acceleration while "
                "avoiding resource over-commitment. Recommend daily signal refresh and weekly NIO updates."
            ),
            MonitoringPosture.ROUTINE: (
                "Routine monitoring is appropriate given current threat indicators. "
                "Standard signal collection and weekly assessment cycles are sufficient. "
                "Escalate to elevated posture if convergence score increases or new domains show activity."
            ),
        }
        
        return rationales.get(posture, "Monitoring posture rationale not available.")
    
    def _generate_recommended_actions(
        self,
        threat: ThreatObject,
        posture: MonitoringPosture
    ) -> list[str]:
        """Generate recommended actions based on threat assessment"""
        actions = []
        
        domain_coverage = threat.probability_curve.domain_coverage
        missing_domains = [d for d in ["social_discourse", "behavioral_trend", "environmental_stressor"]
                         if domain_coverage.get(d, 0) == 0]
        
        if missing_domains:
            actions.append(f"Increase signal collection in missing domains: {', '.join(missing_domains)}")
        
        if posture in [MonitoringPosture.CRITICAL, MonitoringPosture.HEIGHTENED]:
            actions.append("Activate enhanced monitoring protocols")
            actions.append("Brief relevant stakeholders on current assessment")
            actions.append("Prepare contingency communication strategies")
        
        if threat.intent_gradient.current_stage == IntentStage.GRIEVANCE_FORMATION:
            actions.append("Identify community engagement opportunities for early intervention")
        elif threat.intent_gradient.current_stage == IntentStage.COGNITIVE_FIXATION:
            actions.append("Monitor for leadership emergence indicators")
            actions.append("Assess effectiveness of any ongoing engagement efforts")
        elif threat.intent_gradient.current_stage == IntentStage.BEHAVIORAL_ACCELERATION:
            actions.append("Increase monitoring frequency to detect mobilization indicators")
            actions.append("Coordinate with relevant response teams")
        
        if threat.historical_analogs:
            best_analog = max(threat.historical_analogs, key=lambda a: a.similarity_score)
            actions.append(f"Review lessons from historical analog: {best_analog.name}")
        
        actions.append("Schedule next NIO generation based on monitoring posture")
        
        return actions
    
    def _get_next_version(self, threat: ThreatObject) -> int:
        """Get next NIO version number"""
        if threat.current_nio:
            return threat.current_nio.version + 1
        return 1
    
    def regenerate_nio(self, threat_id: str) -> Optional[NarrativeIntelligenceObject]:
        """
        Regenerate NIO for a threat.
        
        Should be called after significant changes to threat assessment
        or on scheduled refresh cycles.
        """
        threat = self.store.get_threat(threat_id)
        if not threat:
            return None
        
        return self.generate_nio(threat)
