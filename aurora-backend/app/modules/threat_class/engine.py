"""
AURORA™ Probabilistic Threat Class Alignment Engine

Computes probabilistic alignment scores for threat classes based on:
- Signal domain composition
- Intent Gradient stage
- Escalation pathway position
- Temporal acceleration / velocity
- Confidence weighting

CRITICAL CONSTRAINTS:
- NOT definitive labels, accusations, or enforcement framing
- Pre-incident, non-investigative, non-attributive
- Multiple classes may be active simultaneously
- Percentages are relative likelihoods, not predictions
- No single class is required to reach 100%
"""

from datetime import datetime
from typing import Optional
from app.models.schemas import (
    ThreatClassCategory,
    ThreatClassAlignment,
    ThreatClassAlignmentResult,
    Signal,
    IntentGradient,
    SignalDomain,
)


# Class alignment weights based on signal domain composition
# Each class has affinities for different signal domains
CLASS_DOMAIN_AFFINITIES = {
    ThreatClassCategory.SOCIOECONOMIC_INSTABILITY: {
        SignalDomain.ENVIRONMENTAL_STRESSOR: 0.45,
        SignalDomain.SOCIAL_DISCOURSE: 0.35,
        SignalDomain.BEHAVIORAL_TREND: 0.20,
    },
    ThreatClassCategory.CIVIL_UNREST_PROTEST: {
        SignalDomain.SOCIAL_DISCOURSE: 0.40,
        SignalDomain.BEHAVIORAL_TREND: 0.40,
        SignalDomain.ENVIRONMENTAL_STRESSOR: 0.20,
    },
    ThreatClassCategory.IDEOLOGICAL_MOBILIZATION: {
        SignalDomain.SOCIAL_DISCOURSE: 0.50,
        SignalDomain.BEHAVIORAL_TREND: 0.35,
        SignalDomain.ENVIRONMENTAL_STRESSOR: 0.15,
    },
    ThreatClassCategory.LONE_ACTOR_GRIEVANCE: {
        SignalDomain.BEHAVIORAL_TREND: 0.45,
        SignalDomain.SOCIAL_DISCOURSE: 0.40,
        SignalDomain.ENVIRONMENTAL_STRESSOR: 0.15,
    },
    ThreatClassCategory.INSIDER_GRIEVANCE_DISRUPTION: {
        SignalDomain.BEHAVIORAL_TREND: 0.50,
        SignalDomain.SOCIAL_DISCOURSE: 0.30,
        SignalDomain.ENVIRONMENTAL_STRESSOR: 0.20,
    },
    ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE: {
        SignalDomain.BEHAVIORAL_TREND: 0.45,
        SignalDomain.ENVIRONMENTAL_STRESSOR: 0.35,
        SignalDomain.SOCIAL_DISCOURSE: 0.20,
    },
    ThreatClassCategory.INFRASTRUCTURE_DISRUPTION: {
        SignalDomain.ENVIRONMENTAL_STRESSOR: 0.50,
        SignalDomain.BEHAVIORAL_TREND: 0.30,
        SignalDomain.SOCIAL_DISCOURSE: 0.20,
    },
    ThreatClassCategory.COORDINATED_DISINFORMATION: {
        SignalDomain.SOCIAL_DISCOURSE: 0.60,
        SignalDomain.BEHAVIORAL_TREND: 0.30,
        SignalDomain.ENVIRONMENTAL_STRESSOR: 0.10,
    },
}

# Intent stage influence on class alignment
# Early stages favor structural/grievance classes, later stages favor mobilization
INTENT_STAGE_CLASS_MODIFIERS = {
    "grievance_formation": {
        ThreatClassCategory.SOCIOECONOMIC_INSTABILITY: 1.3,
        ThreatClassCategory.LONE_ACTOR_GRIEVANCE: 1.2,
        ThreatClassCategory.INSIDER_GRIEVANCE_DISRUPTION: 1.2,
        ThreatClassCategory.CIVIL_UNREST_PROTEST: 0.9,
        ThreatClassCategory.IDEOLOGICAL_MOBILIZATION: 0.8,
        ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE: 0.7,
        ThreatClassCategory.INFRASTRUCTURE_DISRUPTION: 0.7,
        ThreatClassCategory.COORDINATED_DISINFORMATION: 0.9,
    },
    "cognitive_fixation": {
        ThreatClassCategory.SOCIOECONOMIC_INSTABILITY: 1.1,
        ThreatClassCategory.LONE_ACTOR_GRIEVANCE: 1.3,
        ThreatClassCategory.INSIDER_GRIEVANCE_DISRUPTION: 1.2,
        ThreatClassCategory.CIVIL_UNREST_PROTEST: 1.1,
        ThreatClassCategory.IDEOLOGICAL_MOBILIZATION: 1.2,
        ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE: 0.9,
        ThreatClassCategory.INFRASTRUCTURE_DISRUPTION: 0.8,
        ThreatClassCategory.COORDINATED_DISINFORMATION: 1.1,
    },
    "behavioral_acceleration": {
        ThreatClassCategory.SOCIOECONOMIC_INSTABILITY: 0.9,
        ThreatClassCategory.LONE_ACTOR_GRIEVANCE: 1.1,
        ThreatClassCategory.INSIDER_GRIEVANCE_DISRUPTION: 1.1,
        ThreatClassCategory.CIVIL_UNREST_PROTEST: 1.3,
        ThreatClassCategory.IDEOLOGICAL_MOBILIZATION: 1.2,
        ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE: 1.2,
        ThreatClassCategory.INFRASTRUCTURE_DISRUPTION: 1.1,
        ThreatClassCategory.COORDINATED_DISINFORMATION: 1.0,
    },
    "mobilization_risk": {
        ThreatClassCategory.SOCIOECONOMIC_INSTABILITY: 0.8,
        ThreatClassCategory.LONE_ACTOR_GRIEVANCE: 0.9,
        ThreatClassCategory.INSIDER_GRIEVANCE_DISRUPTION: 1.0,
        ThreatClassCategory.CIVIL_UNREST_PROTEST: 1.4,
        ThreatClassCategory.IDEOLOGICAL_MOBILIZATION: 1.3,
        ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE: 1.3,
        ThreatClassCategory.INFRASTRUCTURE_DISRUPTION: 1.3,
        ThreatClassCategory.COORDINATED_DISINFORMATION: 1.1,
    },
}

# Escalation pathway stage influence
# Higher stages increase mobilization-related class alignment
ESCALATION_STAGE_MODIFIERS = {
    0: {  # Structural Stress Emergence
        ThreatClassCategory.SOCIOECONOMIC_INSTABILITY: 1.3,
        ThreatClassCategory.INFRASTRUCTURE_DISRUPTION: 1.1,
    },
    1: {  # Discourse Amplification
        ThreatClassCategory.COORDINATED_DISINFORMATION: 1.2,
        ThreatClassCategory.IDEOLOGICAL_MOBILIZATION: 1.1,
        ThreatClassCategory.CIVIL_UNREST_PROTEST: 1.1,
    },
    2: {  # Behavioral Organization
        ThreatClassCategory.CIVIL_UNREST_PROTEST: 1.3,
        ThreatClassCategory.IDEOLOGICAL_MOBILIZATION: 1.2,
        ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE: 1.1,
    },
    3: {  # Mobilization Potential
        ThreatClassCategory.CIVIL_UNREST_PROTEST: 1.4,
        ThreatClassCategory.INFRASTRUCTURE_DISRUPTION: 1.2,
        ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE: 1.2,
    },
}

# Class-specific rationale templates
CLASS_RATIONALE_TEMPLATES = {
    ThreatClassCategory.SOCIOECONOMIC_INSTABILITY: "Signal composition shows {domain_desc} with patterns typical of socioeconomic stress scenarios. {stage_desc}",
    ThreatClassCategory.CIVIL_UNREST_PROTEST: "Pattern alignment indicates {domain_desc} consistent with civil unrest or protest escalation dynamics. {stage_desc}",
    ThreatClassCategory.IDEOLOGICAL_MOBILIZATION: "Discourse patterns and behavioral indicators suggest {domain_desc} aligned with ideological mobilization trajectories. {stage_desc}",
    ThreatClassCategory.LONE_ACTOR_GRIEVANCE: "Behavioral trend analysis shows {domain_desc} with characteristics associated with grievance-based individual risk patterns. {stage_desc}",
    ThreatClassCategory.INSIDER_GRIEVANCE_DISRUPTION: "Signal clustering indicates {domain_desc} with patterns consistent with insider grievance or organizational disruption risk. {stage_desc}",
    ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE: "Cross-domain signals show {domain_desc} suggesting potential cyber-physical convergence risk patterns. {stage_desc}",
    ThreatClassCategory.INFRASTRUCTURE_DISRUPTION: "Environmental and behavioral indicators show {domain_desc} aligned with infrastructure disruption risk scenarios. {stage_desc}",
    ThreatClassCategory.COORDINATED_DISINFORMATION: "Discourse analysis reveals {domain_desc} with characteristics of coordinated information amplification patterns. {stage_desc}",
}


def compute_domain_composition(signals: list[Signal]) -> dict[SignalDomain, float]:
    """Compute the weighted domain composition from signals."""
    domain_weights = {domain: 0.0 for domain in SignalDomain}
    total_weight = 0.0
    
    for signal in signals:
        weight = signal.weight * signal.raw_confidence
        domain_weights[signal.domain] += weight
        total_weight += weight
    
    if total_weight > 0:
        for domain in domain_weights:
            domain_weights[domain] /= total_weight
    
    return domain_weights


def compute_class_alignment_score(
    threat_class: ThreatClassCategory,
    domain_composition: dict[SignalDomain, float],
    intent_stage: str,
    escalation_stage: int,
    velocity: float,
) -> tuple[float, dict]:
    """
    Compute the alignment score for a single threat class.
    
    Returns:
        tuple: (alignment_score, influence_breakdown)
    """
    # Base score from domain affinity
    domain_affinities = CLASS_DOMAIN_AFFINITIES.get(threat_class, {})
    base_score = 0.0
    for domain, composition in domain_composition.items():
        affinity = domain_affinities.get(domain, 0.1)
        base_score += composition * affinity
    
    # Intent stage modifier
    stage_modifiers = INTENT_STAGE_CLASS_MODIFIERS.get(intent_stage, {})
    intent_modifier = stage_modifiers.get(threat_class, 1.0)
    
    # Escalation pathway modifier
    escalation_modifiers = ESCALATION_STAGE_MODIFIERS.get(escalation_stage, {})
    escalation_modifier = escalation_modifiers.get(threat_class, 1.0)
    
    # Velocity influence (positive velocity increases mobilization-related classes)
    velocity_modifier = 1.0
    if velocity > 0:
        if threat_class in [
            ThreatClassCategory.CIVIL_UNREST_PROTEST,
            ThreatClassCategory.IDEOLOGICAL_MOBILIZATION,
            ThreatClassCategory.INFRASTRUCTURE_DISRUPTION,
        ]:
            velocity_modifier = 1.0 + (velocity * 0.3)
    elif velocity < 0:
        if threat_class in [
            ThreatClassCategory.SOCIOECONOMIC_INSTABILITY,
            ThreatClassCategory.LONE_ACTOR_GRIEVANCE,
        ]:
            velocity_modifier = 1.0 + (abs(velocity) * 0.2)
    
    # Compute final score
    final_score = base_score * intent_modifier * escalation_modifier * velocity_modifier
    
    # Normalize to 0-1 range
    final_score = min(max(final_score, 0.0), 1.0)
    
    # Compute influence breakdown
    influence_breakdown = {
        "base_domain_score": base_score,
        "intent_stage_influence": (intent_modifier - 1.0) / 0.5 if intent_modifier != 1.0 else 0.0,
        "escalation_pathway_influence": (escalation_modifier - 1.0) / 0.5 if escalation_modifier != 1.0 else 0.0,
        "velocity_influence": (velocity_modifier - 1.0) / 0.5 if velocity_modifier != 1.0 else 0.0,
    }
    
    # Normalize influences to 0-1
    for key in influence_breakdown:
        influence_breakdown[key] = min(max(influence_breakdown[key], 0.0), 1.0)
    
    return final_score, influence_breakdown


def generate_rationale(
    threat_class: ThreatClassCategory,
    domain_composition: dict[SignalDomain, float],
    intent_stage: str,
    alignment_score: float,
) -> str:
    """Generate an explainable rationale for the class alignment."""
    # Describe dominant domains
    sorted_domains = sorted(domain_composition.items(), key=lambda x: x[1], reverse=True)
    top_domains = [d for d, v in sorted_domains[:2] if v > 0.2]
    
    domain_names = {
        SignalDomain.SOCIAL_DISCOURSE: "social discourse patterns",
        SignalDomain.BEHAVIORAL_TREND: "behavioral trend indicators",
        SignalDomain.ENVIRONMENTAL_STRESSOR: "environmental stress signals",
    }
    
    if len(top_domains) >= 2:
        domain_desc = f"{domain_names.get(top_domains[0], 'mixed signals')} combined with {domain_names.get(top_domains[1], 'other indicators')}"
    elif len(top_domains) == 1:
        domain_desc = f"strong {domain_names.get(top_domains[0], 'signal patterns')}"
    else:
        domain_desc = "distributed signal patterns across multiple domains"
    
    # Describe stage influence
    stage_descriptions = {
        "grievance_formation": "Current grievance formation stage increases alignment with structural stress patterns.",
        "cognitive_fixation": "Cognitive fixation stage suggests elevated pattern consistency.",
        "behavioral_acceleration": "Behavioral acceleration stage indicates increased mobilization trajectory alignment.",
        "mobilization_risk": "Mobilization risk stage significantly elevates action-oriented class alignment.",
    }
    stage_desc = stage_descriptions.get(intent_stage, "")
    
    template = CLASS_RATIONALE_TEMPLATES.get(
        threat_class,
        "Signal analysis indicates {domain_desc}. {stage_desc}"
    )
    
    return template.format(domain_desc=domain_desc, stage_desc=stage_desc)


def compute_threat_class_alignment(
    threat_id: str,
    signals: list[Signal],
    intent_gradient: IntentGradient,
    escalation_stage: int = 0,
    top_n: int = 5,
) -> ThreatClassAlignmentResult:
    """
    Compute probabilistic threat class alignment for a threat object.
    
    Args:
        threat_id: The threat object ID
        signals: List of contributing signals
        intent_gradient: Current intent gradient state
        escalation_stage: Current escalation pathway stage (0-3)
        top_n: Number of top alignments to return
    
    Returns:
        ThreatClassAlignmentResult with probabilistic alignments
    """
    # Compute domain composition
    domain_composition = compute_domain_composition(signals)
    
    # Get intent stage and velocity
    intent_stage = intent_gradient.current_stage
    velocity = intent_gradient.velocity
    
    # Compute alignment for each class
    alignments = []
    for threat_class in ThreatClassCategory:
        score, influences = compute_class_alignment_score(
            threat_class,
            domain_composition,
            intent_stage,
            escalation_stage,
            velocity,
        )
        
        # Only include classes with meaningful alignment
        if score > 0.1:
            # Compute confidence based on signal coverage and consistency
            signal_count = len(signals)
            domain_coverage = sum(1 for v in domain_composition.values() if v > 0.1)
            confidence = min(0.9, 0.4 + (signal_count * 0.05) + (domain_coverage * 0.1))
            
            # Get contributing domains
            contributing_domains = [
                d.value for d, v in domain_composition.items() if v > 0.15
            ]
            
            # Generate rationale
            rationale = generate_rationale(
                threat_class,
                domain_composition,
                intent_stage,
                score,
            )
            
            alignment = ThreatClassAlignment(
                class_category=threat_class,
                alignment_score=round(score, 3),
                confidence=round(confidence, 2),
                primary_contributing_domains=contributing_domains,
                intent_stage_influence=round(influences["intent_stage_influence"], 2),
                escalation_pathway_influence=round(influences["escalation_pathway_influence"], 2),
                velocity_influence=round(influences["velocity_influence"], 2),
                rationale=rationale,
            )
            alignments.append(alignment)
    
    # Sort by alignment score (descending)
    alignments.sort(key=lambda x: x.alignment_score, reverse=True)
    
    # Take top N
    top_alignments = alignments[:top_n]
    
    # Compute alignment diversity (entropy-like measure)
    if len(top_alignments) > 1:
        scores = [a.alignment_score for a in top_alignments]
        max_score = max(scores)
        if max_score > 0:
            normalized = [s / max_score for s in scores]
            diversity = 1.0 - (normalized[0] - sum(normalized[1:]) / len(normalized[1:]))
            diversity = min(max(diversity, 0.0), 1.0)
        else:
            diversity = 0.5
    else:
        diversity = 0.0
    
    # Create result
    result = ThreatClassAlignmentResult(
        threat_id=threat_id,
        alignments=top_alignments,
        top_alignment=top_alignments[0].class_category if top_alignments else None,
        alignment_diversity=round(diversity, 2),
        intent_stage_at_computation=intent_stage,
        escalation_stage_at_computation=escalation_stage,
        last_updated=datetime.utcnow(),
    )
    
    return result
