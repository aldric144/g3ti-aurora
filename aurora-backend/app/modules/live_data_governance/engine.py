"""
AURORA™ Live Data Governance Engine - Phase 1.4

Implements four governance layers for live U.S. data ingestion:
1. Live Data Governance Mode (Policy Enforcement Layer)
2. Data Freshness & Time Semantics
3. Live-Data Fail-Safe & Dampening Controls
4. Provenance & Context Attribution

All governance decisions are logged for audit purposes.
"""

import re
import uuid
from datetime import datetime, timedelta
from typing import Optional

from app.models.schemas import (
    LiveDataMode,
    AllowedInputCategory,
    RejectedInputReason,
    LiveDataGovernanceMode,
    InputValidationResult,
    DataFreshnessBand,
    ContextPersistenceState,
    DataFreshnessIndicator,
    FailSafeType,
    VelocityDampeningConfig,
    DomainBalanceConfig,
    EscalationCeilingConfig,
    ConfidenceCollapseConfig,
    FailSafeActivation,
    LiveDataFailSafeControls,
    ProvenanceCategory,
    ContextProvenance,
    LiveDataGovernanceLayer,
    SignalDomain,
    SilentAuditEntry,
)


class LiveDataGovernanceEngine:
    """
    Live Data Governance Engine
    
    Enforces all four governance layers at the system level:
    1. Policy enforcement at ingestion
    2. Time semantics and freshness tracking
    3. Fail-safe and dampening controls
    4. Provenance attribution
    
    GLOBAL SAFETY RULES (NON-NEGOTIABLE):
    - No alerts
    - No event detection
    - No actor modeling
    - No individual or population surveillance
    - No public-facing live feeds
    - U.S. context only (global synthetic remains unchanged)
    """
    
    def __init__(self):
        self.governance_mode = LiveDataGovernanceMode()
        self.fail_safe_controls = LiveDataFailSafeControls()
        self.audit_log: list[SilentAuditEntry] = []
        self.probability_history: dict[str, list[tuple[datetime, float]]] = {}
        self.stage_history: dict[str, list[tuple[datetime, int]]] = {}
        
        self.PII_PATTERNS = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
            r'@[A-Za-z0-9_]+',
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
        ]
        
        self.ALERTING_KEYWORDS = [
            'alert', 'warning', 'urgent', 'immediate', 'emergency',
            'breaking', 'critical alert', 'action required', 'respond now',
            'threat detected', 'incident', 'attack', 'breach'
        ]
        
        self.ACTOR_KEYWORDS = [
            'suspect', 'perpetrator', 'individual identified', 'person of interest',
            'target', 'subject', 'actor', 'operative', 'cell member'
        ]
        
        self.EVENT_KEYWORDS = [
            'occurred at', 'happened at', 'took place', 'incident at',
            'event at', 'attack on', 'explosion', 'shooting', 'bombing'
        ]
        
        self.PRECISE_GEO_PATTERNS = [
            r'\b\d+\s+[A-Za-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b',
            r'\b\d{5}(-\d{4})?\b',
            r'\b-?\d{1,3}\.\d{4,},\s*-?\d{1,3}\.\d{4,}\b',
        ]
    
    def set_live_data_mode(self, mode: LiveDataMode, set_by: str = "system") -> LiveDataGovernanceMode:
        """Set the live data governance mode with audit logging"""
        old_mode = self.governance_mode.mode
        self.governance_mode.mode = mode
        self.governance_mode.mode_set_at = datetime.utcnow()
        self.governance_mode.mode_set_by = set_by
        self.governance_mode.rejection_count = 0
        self.governance_mode.quarantine_count = 0
        
        self._log_audit_entry(
            entry_type="mode_change",
            metadata={
                "old_mode": old_mode.value,
                "new_mode": mode.value,
                "set_by": set_by
            }
        )
        
        return self.governance_mode
    
    def validate_input(
        self,
        content: str,
        jurisdiction: str,
        metadata: Optional[dict] = None
    ) -> InputValidationResult:
        """
        Validate input against live data governance rules.
        
        ENFORCEMENT AT INGESTION - not post-analysis.
        
        When Live Data Mode is ON:
        - Only allow permitted input categories
        - Automatically reject/quarantine prohibited inputs
        """
        audit_ref = str(uuid.uuid4())
        
        if self.governance_mode.mode == LiveDataMode.OFF:
            return InputValidationResult(
                is_valid=True,
                input_category=AllowedInputCategory.STRUCTURAL_ECONOMIC,
                audit_reference=audit_ref
            )
        
        if jurisdiction.upper() != "US" and jurisdiction.upper() != "UNITED STATES":
            self.governance_mode.rejection_count += 1
            self.governance_mode.last_rejection_reason = RejectedInputReason.NON_US_CONTEXT
            self._log_audit_entry(
                entry_type="input_rejection",
                metadata={
                    "reason": "non_us_context",
                    "jurisdiction": jurisdiction,
                    "audit_ref": audit_ref
                }
            )
            return InputValidationResult(
                is_valid=False,
                rejection_reason=RejectedInputReason.NON_US_CONTEXT,
                rejection_details=f"Live data mode only permits U.S. context. Received: {jurisdiction}",
                audit_reference=audit_ref
            )
        
        for pattern in self.PII_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                self.governance_mode.rejection_count += 1
                self.governance_mode.last_rejection_reason = RejectedInputReason.INDIVIDUAL_IDENTIFIER
                self._log_audit_entry(
                    entry_type="input_rejection",
                    metadata={
                        "reason": "individual_identifier",
                        "pattern_matched": pattern,
                        "audit_ref": audit_ref
                    }
                )
                return InputValidationResult(
                    is_valid=False,
                    rejection_reason=RejectedInputReason.INDIVIDUAL_IDENTIFIER,
                    rejection_details="Input contains individual identifiers (PII)",
                    audit_reference=audit_ref
                )
        
        for pattern in self.PRECISE_GEO_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                self.governance_mode.rejection_count += 1
                self.governance_mode.last_rejection_reason = RejectedInputReason.PRECISE_GEOLOCATION
                self._log_audit_entry(
                    entry_type="input_rejection",
                    metadata={
                        "reason": "precise_geolocation",
                        "audit_ref": audit_ref
                    }
                )
                return InputValidationResult(
                    is_valid=False,
                    rejection_reason=RejectedInputReason.PRECISE_GEOLOCATION,
                    rejection_details="Input contains precise geolocation (below regional level)",
                    audit_reference=audit_ref
                )
        
        content_lower = content.lower()
        for keyword in self.ACTOR_KEYWORDS:
            if keyword in content_lower:
                self.governance_mode.rejection_count += 1
                self.governance_mode.last_rejection_reason = RejectedInputReason.ACTOR_LEVEL_OBSERVATION
                self._log_audit_entry(
                    entry_type="input_rejection",
                    metadata={
                        "reason": "actor_level_observation",
                        "keyword_matched": keyword,
                        "audit_ref": audit_ref
                    }
                )
                return InputValidationResult(
                    is_valid=False,
                    rejection_reason=RejectedInputReason.ACTOR_LEVEL_OBSERVATION,
                    rejection_details="Input implies actor-level observation",
                    audit_reference=audit_ref
                )
        
        for keyword in self.EVENT_KEYWORDS:
            if keyword in content_lower:
                self.governance_mode.rejection_count += 1
                self.governance_mode.last_rejection_reason = RejectedInputReason.EVENT_LEVEL_OBSERVATION
                self._log_audit_entry(
                    entry_type="input_rejection",
                    metadata={
                        "reason": "event_level_observation",
                        "keyword_matched": keyword,
                        "audit_ref": audit_ref
                    }
                )
                return InputValidationResult(
                    is_valid=False,
                    rejection_reason=RejectedInputReason.EVENT_LEVEL_OBSERVATION,
                    rejection_details="Input implies event-level observation",
                    audit_reference=audit_ref
                )
        
        for keyword in self.ALERTING_KEYWORDS:
            if keyword in content_lower:
                self.governance_mode.rejection_count += 1
                self.governance_mode.last_rejection_reason = RejectedInputReason.ALERTING_SEMANTICS
                self._log_audit_entry(
                    entry_type="input_rejection",
                    metadata={
                        "reason": "alerting_semantics",
                        "keyword_matched": keyword,
                        "audit_ref": audit_ref
                    }
                )
                return InputValidationResult(
                    is_valid=False,
                    rejection_reason=RejectedInputReason.ALERTING_SEMANTICS,
                    rejection_details="Input contains alerting semantics",
                    audit_reference=audit_ref
                )
        
        category = self._categorize_input(content, metadata)
        if category is None:
            self.governance_mode.quarantine_count += 1
            self._log_audit_entry(
                entry_type="input_quarantine",
                metadata={
                    "reason": "uncategorized",
                    "audit_ref": audit_ref
                }
            )
            return InputValidationResult(
                is_valid=False,
                rejection_reason=RejectedInputReason.UNCATEGORIZED_INPUT,
                rejection_details="Input could not be categorized into allowed categories",
                quarantined=True,
                audit_reference=audit_ref
            )
        
        self._log_audit_entry(
            entry_type="input_accepted",
            metadata={
                "category": category.value,
                "audit_ref": audit_ref
            }
        )
        
        return InputValidationResult(
            is_valid=True,
            input_category=category,
            audit_reference=audit_ref
        )
    
    def _categorize_input(self, content: str, metadata: Optional[dict] = None) -> Optional[AllowedInputCategory]:
        """Categorize input into allowed categories"""
        content_lower = content.lower()
        
        economic_keywords = [
            'economic', 'unemployment', 'gdp', 'inflation', 'market',
            'employment', 'wage', 'income', 'poverty', 'housing',
            'manufacturing', 'industrial', 'trade', 'fiscal', 'monetary'
        ]
        
        discourse_keywords = [
            'sentiment', 'discourse', 'topic', 'narrative', 'discussion',
            'public opinion', 'social media trend', 'conversation', 'debate'
        ]
        
        institutional_keywords = [
            'policy', 'regulation', 'legislation', 'government', 'agency',
            'institutional', 'regulatory', 'compliance', 'law', 'statute'
        ]
        
        economic_score = sum(1 for kw in economic_keywords if kw in content_lower)
        discourse_score = sum(1 for kw in discourse_keywords if kw in content_lower)
        institutional_score = sum(1 for kw in institutional_keywords if kw in content_lower)
        
        if metadata:
            if metadata.get("category") == "economic":
                economic_score += 5
            elif metadata.get("category") == "discourse":
                discourse_score += 5
            elif metadata.get("category") == "institutional":
                institutional_score += 5
        
        max_score = max(economic_score, discourse_score, institutional_score)
        
        if max_score == 0:
            return None
        
        if economic_score == max_score:
            return AllowedInputCategory.STRUCTURAL_ECONOMIC
        elif discourse_score == max_score:
            return AllowedInputCategory.ABSTRACTED_DISCOURSE
        else:
            return AllowedInputCategory.INSTITUTIONAL_POLICY
    
    def calculate_data_freshness(
        self,
        context_id: str,
        last_data_update: datetime,
        signal_persistence_hours: float = 0
    ) -> DataFreshnessIndicator:
        """
        Calculate data freshness and persistence state.
        
        RULES:
        - No expectation of instant change
        - Intent stages may only advance based on persistence over time
        """
        now = datetime.utcnow()
        hours_since_update = (now - last_data_update).total_seconds() / 3600
        
        if hours_since_update < 6:
            freshness_band = DataFreshnessBand.FRESH
            freshness_label = "Updated < 6 hours ago"
        elif hours_since_update < 24:
            freshness_band = DataFreshnessBand.RECENT
            freshness_label = f"Updated {int(hours_since_update)} hours ago"
        else:
            freshness_band = DataFreshnessBand.AGING
            freshness_label = f"Updated > {int(hours_since_update / 24)} days ago"
        
        if signal_persistence_hours < 6:
            persistence_state = ContextPersistenceState.FRESH
            persistence_label = "Fresh context - recently emerged"
        elif signal_persistence_hours < 24:
            persistence_state = ContextPersistenceState.PERSISTENT
            persistence_label = "Persistent context - sustained signals"
        elif signal_persistence_hours < 72:
            persistence_state = ContextPersistenceState.COOLING
            persistence_label = "Cooling context - signal intensity decreasing"
        elif signal_persistence_hours < 168:
            persistence_state = ContextPersistenceState.DECAYING
            persistence_label = "Decaying context - approaching staleness"
        else:
            persistence_state = ContextPersistenceState.STALE
            persistence_label = "Stale context - requires refresh"
        
        minimum_persistence_hours = 24.0
        can_advance = signal_persistence_hours >= minimum_persistence_hours
        
        return DataFreshnessIndicator(
            context_id=context_id,
            freshness_band=freshness_band,
            persistence_state=persistence_state,
            last_data_update=last_data_update,
            hours_since_update=hours_since_update,
            freshness_label=freshness_label,
            persistence_label=persistence_label,
            can_advance_intent_stage=can_advance,
            minimum_persistence_hours=minimum_persistence_hours,
            freshness_note="Intent stages advance based on persistence, not instant changes"
        )
    
    def apply_velocity_dampening(
        self,
        context_id: str,
        current_probability: float,
        new_probability: float
    ) -> tuple[float, Optional[FailSafeActivation]]:
        """
        Apply velocity dampening to cap rate of probability change.
        
        Returns adjusted probability and activation record if triggered.
        """
        config = self.fail_safe_controls.velocity_dampening
        
        if not config.dampening_active:
            return new_probability, None
        
        if context_id not in self.probability_history:
            self.probability_history[context_id] = []
        
        now = datetime.utcnow()
        self.probability_history[context_id].append((now, current_probability))
        
        self.probability_history[context_id] = [
            (ts, prob) for ts, prob in self.probability_history[context_id]
            if (now - ts).total_seconds() < 86400
        ]
        
        change = abs(new_probability - current_probability)
        max_change = config.max_probability_change_per_hour / 100
        
        if change > max_change:
            if new_probability > current_probability:
                adjusted = current_probability + max_change
            else:
                adjusted = current_probability - max_change
            
            activation = FailSafeActivation(
                fail_safe_type=FailSafeType.VELOCITY_DAMPENING,
                context_id=context_id,
                trigger_value=change * 100,
                threshold_value=config.max_probability_change_per_hour,
                action_taken=f"Capped probability change from {change*100:.1f}% to {max_change*100:.1f}%",
                original_value=new_probability,
                adjusted_value=adjusted
            )
            
            self.fail_safe_controls.recent_activations.append(activation)
            self.fail_safe_controls.total_activations_count += 1
            
            self._log_audit_entry(
                entry_type="fail_safe_activation",
                context_id=context_id,
                metadata={
                    "type": "velocity_dampening",
                    "original": new_probability,
                    "adjusted": adjusted,
                    "change_capped": change * 100
                }
            )
            
            return adjusted, activation
        
        return new_probability, None
    
    def check_domain_balance(
        self,
        domain_weights: dict[str, float]
    ) -> tuple[bool, Optional[FailSafeActivation]]:
        """
        Check domain balance enforcement.
        
        No single domain may dominate conclusions without cross-domain confirmation.
        """
        config = self.fail_safe_controls.domain_balance
        
        if not config.cross_domain_required:
            return True, None
        
        domains_present = len([w for w in domain_weights.values() if w > 0])
        
        if domains_present < config.min_domains_for_conclusion:
            activation = FailSafeActivation(
                fail_safe_type=FailSafeType.DOMAIN_BALANCE_ENFORCEMENT,
                trigger_value=float(domains_present),
                threshold_value=float(config.min_domains_for_conclusion),
                action_taken=f"Insufficient domain diversity: {domains_present} domains present, {config.min_domains_for_conclusion} required"
            )
            
            self.fail_safe_controls.recent_activations.append(activation)
            self.fail_safe_controls.total_activations_count += 1
            
            self._log_audit_entry(
                entry_type="fail_safe_activation",
                metadata={
                    "type": "domain_balance_enforcement",
                    "domains_present": domains_present,
                    "required": config.min_domains_for_conclusion
                }
            )
            
            return False, activation
        
        max_weight = max(domain_weights.values()) if domain_weights else 0
        
        if max_weight > config.max_single_domain_weight:
            dominant_domain = max(domain_weights, key=domain_weights.get)
            activation = FailSafeActivation(
                fail_safe_type=FailSafeType.DOMAIN_BALANCE_ENFORCEMENT,
                trigger_value=max_weight,
                threshold_value=config.max_single_domain_weight,
                action_taken=f"Single domain ({dominant_domain}) exceeds maximum weight: {max_weight:.2f} > {config.max_single_domain_weight}"
            )
            
            self.fail_safe_controls.recent_activations.append(activation)
            self.fail_safe_controls.total_activations_count += 1
            
            self._log_audit_entry(
                entry_type="fail_safe_activation",
                metadata={
                    "type": "domain_balance_enforcement",
                    "dominant_domain": dominant_domain,
                    "weight": max_weight,
                    "max_allowed": config.max_single_domain_weight
                }
            )
            
            return False, activation
        
        return True, None
    
    def check_escalation_ceiling(
        self,
        context_id: str,
        current_stage: int,
        proposed_stage: int
    ) -> tuple[int, Optional[FailSafeActivation]]:
        """
        Check escalation ceiling.
        
        Intent stages cannot advance more than one level within a defined time window.
        """
        config = self.fail_safe_controls.escalation_ceiling
        
        if not config.ceiling_active:
            return proposed_stage, None
        
        if context_id not in self.stage_history:
            self.stage_history[context_id] = []
        
        now = datetime.utcnow()
        window_start = now - timedelta(hours=config.time_window_hours)
        
        recent_changes = [
            (ts, stage) for ts, stage in self.stage_history[context_id]
            if ts >= window_start
        ]
        
        advances_in_window = 0
        if recent_changes:
            sorted_changes = sorted(recent_changes, key=lambda x: x[0])
            for i in range(1, len(sorted_changes)):
                if sorted_changes[i][1] > sorted_changes[i-1][1]:
                    advances_in_window += 1
        
        stage_advance = proposed_stage - current_stage
        
        if stage_advance > 0 and advances_in_window >= config.max_stage_advance_per_window:
            activation = FailSafeActivation(
                fail_safe_type=FailSafeType.ESCALATION_CEILING,
                context_id=context_id,
                trigger_value=float(advances_in_window + 1),
                threshold_value=float(config.max_stage_advance_per_window),
                action_taken=f"Escalation ceiling reached: {advances_in_window} advances in {config.time_window_hours}h window",
                original_value=float(proposed_stage),
                adjusted_value=float(current_stage)
            )
            
            self.fail_safe_controls.recent_activations.append(activation)
            self.fail_safe_controls.total_activations_count += 1
            
            self._log_audit_entry(
                entry_type="fail_safe_activation",
                context_id=context_id,
                metadata={
                    "type": "escalation_ceiling",
                    "proposed_stage": proposed_stage,
                    "current_stage": current_stage,
                    "advances_in_window": advances_in_window
                }
            )
            
            return current_stage, activation
        
        if stage_advance > config.max_stage_advance_per_window:
            capped_stage = current_stage + config.max_stage_advance_per_window
            
            activation = FailSafeActivation(
                fail_safe_type=FailSafeType.ESCALATION_CEILING,
                context_id=context_id,
                trigger_value=float(stage_advance),
                threshold_value=float(config.max_stage_advance_per_window),
                action_taken=f"Stage advance capped from {stage_advance} to {config.max_stage_advance_per_window}",
                original_value=float(proposed_stage),
                adjusted_value=float(capped_stage)
            )
            
            self.fail_safe_controls.recent_activations.append(activation)
            self.fail_safe_controls.total_activations_count += 1
            
            self._log_audit_entry(
                entry_type="fail_safe_activation",
                context_id=context_id,
                metadata={
                    "type": "escalation_ceiling",
                    "proposed_stage": proposed_stage,
                    "capped_stage": capped_stage
                }
            )
            
            self.stage_history[context_id].append((now, capped_stage))
            return capped_stage, activation
        
        self.stage_history[context_id].append((now, proposed_stage))
        return proposed_stage, None
    
    def handle_confidence_collapse(
        self,
        context_id: str,
        previous_confidence: float,
        current_confidence: float,
        current_outputs: dict
    ) -> tuple[dict, Optional[FailSafeActivation]]:
        """
        Handle confidence collapse.
        
        If confidence drops suddenly, system must soften outputs, not escalate.
        """
        config = self.fail_safe_controls.confidence_collapse
        
        confidence_drop = previous_confidence - current_confidence
        
        if confidence_drop >= config.collapse_threshold:
            softened_outputs = current_outputs.copy()
            
            if "probability" in softened_outputs:
                softened_outputs["probability"] *= config.softening_factor
            
            if "recommendations" in softened_outputs:
                softened_outputs["recommendations"] = [
                    {**rec, "confidence": rec.get("confidence", 0.5) * config.softening_factor}
                    for rec in softened_outputs.get("recommendations", [])
                ]
            
            if config.prevent_escalation_on_collapse:
                softened_outputs["escalation_blocked"] = True
                softened_outputs["escalation_block_reason"] = "Confidence collapse detected"
            
            activation = FailSafeActivation(
                fail_safe_type=FailSafeType.CONFIDENCE_COLLAPSE_HANDLING,
                context_id=context_id,
                trigger_value=confidence_drop,
                threshold_value=config.collapse_threshold,
                action_taken=f"Confidence collapse detected ({confidence_drop:.2f}). Outputs softened by {config.softening_factor}",
                original_value=previous_confidence,
                adjusted_value=current_confidence
            )
            
            self.fail_safe_controls.recent_activations.append(activation)
            self.fail_safe_controls.total_activations_count += 1
            
            self._log_audit_entry(
                entry_type="fail_safe_activation",
                context_id=context_id,
                metadata={
                    "type": "confidence_collapse_handling",
                    "previous_confidence": previous_confidence,
                    "current_confidence": current_confidence,
                    "drop": confidence_drop,
                    "softening_applied": config.softening_factor
                }
            )
            
            return softened_outputs, activation
        
        return current_outputs, None
    
    def calculate_provenance(
        self,
        context_id: str,
        signals: list[dict],
        domain_weights: dict[str, float]
    ) -> ContextProvenance:
        """
        Calculate context provenance (non-source disclosing).
        
        PURPOSE: Explanation, not traceability.
        Does NOT expose raw sources, feeds, or platforms.
        """
        provenance_weights = {
            ProvenanceCategory.STRUCTURAL_INDICATORS.value: 0.0,
            ProvenanceCategory.DISCOURSE_WEIGHTED.value: 0.0,
            ProvenanceCategory.INSTITUTIONAL_POLICY.value: 0.0,
            ProvenanceCategory.ECONOMIC_INDICATORS.value: 0.0,
            ProvenanceCategory.BEHAVIORAL_PATTERNS.value: 0.0,
        }
        
        for signal in signals:
            domain = signal.get("domain", "")
            weight = signal.get("weight", 1.0)
            
            if domain == SignalDomain.ENVIRONMENTAL_STRESSOR.value:
                provenance_weights[ProvenanceCategory.STRUCTURAL_INDICATORS.value] += weight
                provenance_weights[ProvenanceCategory.ECONOMIC_INDICATORS.value] += weight * 0.5
            elif domain == SignalDomain.SOCIAL_DISCOURSE.value:
                provenance_weights[ProvenanceCategory.DISCOURSE_WEIGHTED.value] += weight
            elif domain == SignalDomain.BEHAVIORAL_TREND.value:
                provenance_weights[ProvenanceCategory.BEHAVIORAL_PATTERNS.value] += weight
        
        total_weight = sum(provenance_weights.values())
        if total_weight > 0:
            provenance_weights = {k: v / total_weight for k, v in provenance_weights.items()}
        
        primary_category = max(provenance_weights, key=provenance_weights.get)
        primary_provenance = ProvenanceCategory(primary_category)
        
        sorted_weights = sorted(provenance_weights.items(), key=lambda x: x[1], reverse=True)
        secondary_provenance = None
        if len(sorted_weights) > 1 and sorted_weights[1][1] > 0.1:
            secondary_provenance = ProvenanceCategory(sorted_weights[1][0])
        
        provenance_labels = {
            ProvenanceCategory.STRUCTURAL_INDICATORS: "Context primarily driven by structural indicators",
            ProvenanceCategory.DISCOURSE_WEIGHTED: "Discourse-weighted context",
            ProvenanceCategory.INSTITUTIONAL_POLICY: "Institutional policy-influenced context",
            ProvenanceCategory.ECONOMIC_INDICATORS: "Economic indicator-driven context",
            ProvenanceCategory.BEHAVIORAL_PATTERNS: "Behavioral pattern-influenced context",
            ProvenanceCategory.MIXED_PROVENANCE: "Mixed provenance context",
        }
        
        if secondary_provenance and provenance_weights[primary_category] < 0.5:
            provenance_label = "Mixed provenance context"
            primary_provenance = ProvenanceCategory.MIXED_PROVENANCE
        else:
            provenance_label = provenance_labels.get(primary_provenance, "Context provenance determined")
        
        indicator_types = []
        if provenance_weights.get(ProvenanceCategory.ECONOMIC_INDICATORS.value, 0) > 0.1:
            indicator_types.append("Economic/structural indicators")
        if provenance_weights.get(ProvenanceCategory.DISCOURSE_WEIGHTED.value, 0) > 0.1:
            indicator_types.append("Abstracted discourse patterns")
        if provenance_weights.get(ProvenanceCategory.BEHAVIORAL_PATTERNS.value, 0) > 0.1:
            indicator_types.append("Behavioral trend indicators")
        if provenance_weights.get(ProvenanceCategory.INSTITUTIONAL_POLICY.value, 0) > 0.1:
            indicator_types.append("Institutional/policy indicators")
        
        source_diversity = min(len([v for v in provenance_weights.values() if v > 0.05]) / 5.0, 1.0)
        
        return ContextProvenance(
            context_id=context_id,
            primary_provenance=primary_provenance,
            secondary_provenance=secondary_provenance,
            provenance_weights=provenance_weights,
            provenance_label=provenance_label,
            provenance_description=f"{provenance_label}. Analysis based on {len(indicator_types)} indicator types.",
            indicator_types_present=indicator_types,
            source_diversity_score=source_diversity,
            temporal_coverage="Past 7 days",
            geographic_scope="Regional (U.S.)"
        )
    
    def get_governance_layer(
        self,
        context_id: str,
        last_data_update: Optional[datetime] = None,
        signal_persistence_hours: float = 0,
        signals: Optional[list[dict]] = None,
        domain_weights: Optional[dict[str, float]] = None
    ) -> LiveDataGovernanceLayer:
        """
        Get the complete Live Data Governance Layer for a context.
        
        Combines all four governance layers.
        """
        data_freshness = None
        if last_data_update:
            data_freshness = self.calculate_data_freshness(
                context_id=context_id,
                last_data_update=last_data_update,
                signal_persistence_hours=signal_persistence_hours
            )
        
        context_provenance = None
        if signals and domain_weights:
            context_provenance = self.calculate_provenance(
                context_id=context_id,
                signals=signals,
                domain_weights=domain_weights
            )
        
        self.fail_safe_controls.recent_activations = self.fail_safe_controls.recent_activations[-10:]
        self.fail_safe_controls.last_evaluation = datetime.utcnow()
        
        return LiveDataGovernanceLayer(
            governance_mode=self.governance_mode,
            data_freshness=data_freshness,
            fail_safe_controls=self.fail_safe_controls,
            context_provenance=context_provenance,
            governance_status="active" if self.governance_mode.governance_active else "inactive",
            last_governance_check=datetime.utcnow()
        )
    
    def _log_audit_entry(
        self,
        entry_type: str,
        context_id: Optional[str] = None,
        threat_id: Optional[str] = None,
        metadata: Optional[dict] = None
    ):
        """Log an audit entry for governance decisions"""
        entry = SilentAuditEntry(
            entry_type=entry_type,
            context_id=context_id,
            threat_id=threat_id,
            metadata=metadata or {},
            governance_tags=["live_data_governance", entry_type]
        )
        self.audit_log.append(entry)
        
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-500:]
    
    def get_audit_log(self, limit: int = 100) -> list[SilentAuditEntry]:
        """Get recent audit log entries"""
        return self.audit_log[-limit:]


live_data_governance_engine = LiveDataGovernanceEngine()
