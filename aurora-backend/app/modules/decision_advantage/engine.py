"""
Decision Advantage Layer Engine - Phase 3

Computes decision pathway intelligence, impact forecasting, and authority-aware
recommendations based on threat patterns.

CRITICAL CONSTRAINTS:
- No surveillance, mandates, or investigative framing
- Pre-incident decision intelligence posture
- All outputs auditable and confidence-weighted
- No identity attribution
"""

from datetime import datetime
from typing import Optional

from app.models.schemas import (
    ThreatObject,
    IntentStage,
    DecisionPathwayCategory,
    DecisionPathwayRelevance,
    DecisionPathway,
    DecisionPathwayIntelligence,
    ImpactDomain,
    ImpactProjection,
    ImpactForecast,
    AuthorityDomain,
    AuthorityRecommendation,
    AuthorityAwareRecommendations,
    DecisionAdvantageLayer,
    ThreatClassCategory,
)


PATHWAY_THREAT_CLASS_AFFINITIES: dict[str, dict[DecisionPathwayCategory, float]] = {
    ThreatClassCategory.SOCIOECONOMIC_INSTABILITY.value: {
        DecisionPathwayCategory.ECONOMIC_ENGAGEMENT: 0.9,
        DecisionPathwayCategory.COMMUNITY_OUTREACH: 0.8,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 0.7,
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 0.6,
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 0.5,
    },
    ThreatClassCategory.CIVIL_UNREST_PROTEST.value: {
        DecisionPathwayCategory.COMMUNITY_OUTREACH: 0.9,
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 0.85,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 0.7,
        DecisionPathwayCategory.RESOURCE_POSITIONING: 0.6,
        DecisionPathwayCategory.INTERAGENCY_LIAISON: 0.5,
    },
    ThreatClassCategory.IDEOLOGICAL_MOBILIZATION.value: {
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 0.85,
        DecisionPathwayCategory.COMMUNITY_OUTREACH: 0.75,
        DecisionPathwayCategory.MONITORING_ADJUSTMENT: 0.7,
        DecisionPathwayCategory.INTERAGENCY_LIAISON: 0.6,
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 0.5,
    },
    ThreatClassCategory.LONE_ACTOR_GRIEVANCE.value: {
        DecisionPathwayCategory.COMMUNITY_OUTREACH: 0.8,
        DecisionPathwayCategory.MONITORING_ADJUSTMENT: 0.75,
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 0.7,
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 0.5,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 0.4,
    },
    ThreatClassCategory.INSIDER_GRIEVANCE_DISRUPTION.value: {
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 0.9,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 0.7,
        DecisionPathwayCategory.MONITORING_ADJUSTMENT: 0.65,
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 0.5,
        DecisionPathwayCategory.RESOURCE_POSITIONING: 0.4,
    },
    ThreatClassCategory.CYBER_PHYSICAL_CONVERGENCE.value: {
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 0.85,
        DecisionPathwayCategory.RESOURCE_POSITIONING: 0.8,
        DecisionPathwayCategory.INTERAGENCY_LIAISON: 0.75,
        DecisionPathwayCategory.MONITORING_ADJUSTMENT: 0.7,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 0.6,
    },
    ThreatClassCategory.INFRASTRUCTURE_DISRUPTION.value: {
        DecisionPathwayCategory.RESOURCE_POSITIONING: 0.9,
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 0.85,
        DecisionPathwayCategory.INTERAGENCY_LIAISON: 0.8,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 0.7,
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 0.6,
    },
    ThreatClassCategory.COORDINATED_DISINFORMATION.value: {
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 0.95,
        DecisionPathwayCategory.COMMUNITY_OUTREACH: 0.7,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 0.65,
        DecisionPathwayCategory.MONITORING_ADJUSTMENT: 0.6,
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 0.5,
    },
}

INTENT_STAGE_PATHWAY_MODIFIERS: dict[IntentStage, dict[DecisionPathwayCategory, float]] = {
    IntentStage.GRIEVANCE_FORMATION: {
        DecisionPathwayCategory.ECONOMIC_ENGAGEMENT: 1.2,
        DecisionPathwayCategory.COMMUNITY_OUTREACH: 1.15,
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 1.0,
        DecisionPathwayCategory.MONITORING_ADJUSTMENT: 0.8,
    },
    IntentStage.COGNITIVE_FIXATION: {
        DecisionPathwayCategory.COMMUNITY_OUTREACH: 1.2,
        DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: 1.15,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 1.1,
        DecisionPathwayCategory.MONITORING_ADJUSTMENT: 1.0,
    },
    IntentStage.BEHAVIORAL_ACCELERATION: {
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 1.2,
        DecisionPathwayCategory.RESOURCE_POSITIONING: 1.15,
        DecisionPathwayCategory.INTERAGENCY_LIAISON: 1.1,
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 1.1,
    },
    IntentStage.MOBILIZATION_RISK: {
        DecisionPathwayCategory.RESOURCE_POSITIONING: 1.25,
        DecisionPathwayCategory.INTERAGENCY_LIAISON: 1.2,
        DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: 1.15,
        DecisionPathwayCategory.STAKEHOLDER_COORDINATION: 1.1,
    },
}

PATHWAY_ADVISORY_TEMPLATES: dict[DecisionPathwayCategory, dict] = {
    DecisionPathwayCategory.ECONOMIC_ENGAGEMENT: {
        "summary": "Consider economic engagement strategies to address underlying structural stressors",
        "considerations": [
            "Review economic support mechanisms in affected areas",
            "Assess workforce development program alignment",
            "Evaluate community economic resilience indicators",
        ],
        "proportionality": "Economic engagement is most effective in early-stage patterns where structural stressors are primary drivers",
    },
    DecisionPathwayCategory.COMMUNITY_OUTREACH: {
        "summary": "Community outreach may help address grievance formation and build trust",
        "considerations": [
            "Identify trusted community intermediaries",
            "Assess communication channel effectiveness",
            "Review community feedback mechanisms",
        ],
        "proportionality": "Community outreach is proportional across all stages but most impactful before behavioral acceleration",
    },
    DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: {
        "summary": "Strategic communications may help counter narrative amplification and provide accurate information",
        "considerations": [
            "Review public messaging alignment with community concerns",
            "Assess information environment for misinformation patterns",
            "Evaluate proactive communication opportunities",
        ],
        "proportionality": "Communications strategy is particularly relevant when discourse amplification is detected",
    },
    DecisionPathwayCategory.STAKEHOLDER_COORDINATION: {
        "summary": "Cross-stakeholder coordination may improve response coherence and resource alignment",
        "considerations": [
            "Identify key stakeholder groups and their concerns",
            "Assess coordination mechanisms and gaps",
            "Review information sharing protocols",
        ],
        "proportionality": "Stakeholder coordination becomes more critical as pattern complexity increases",
    },
    DecisionPathwayCategory.RESOURCE_POSITIONING: {
        "summary": "Resource positioning may support institutional readiness without escalatory signaling",
        "considerations": [
            "Review resource availability and positioning options",
            "Assess operational continuity requirements",
            "Evaluate non-escalatory readiness measures",
        ],
        "proportionality": "Resource positioning should be proportional to assessed probability and avoid escalatory perception",
    },
    DecisionPathwayCategory.MONITORING_ADJUSTMENT: {
        "summary": "Monitoring posture adjustments may improve situational awareness",
        "considerations": [
            "Review current monitoring coverage and gaps",
            "Assess information collection priorities",
            "Evaluate reporting frequency and channels",
        ],
        "proportionality": "Monitoring adjustments should be proportional to uncertainty levels and information gaps",
    },
    DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: {
        "summary": "Institutional resilience measures may reduce vulnerability to disruption",
        "considerations": [
            "Review business continuity and resilience plans",
            "Assess critical function redundancy",
            "Evaluate staff awareness and preparedness",
        ],
        "proportionality": "Resilience measures are proportional when disruption risk indicators are elevated",
    },
    DecisionPathwayCategory.INTERAGENCY_LIAISON: {
        "summary": "Interagency coordination may improve collective awareness and response coherence",
        "considerations": [
            "Identify relevant partner agencies and their equities",
            "Review information sharing agreements and protocols",
            "Assess coordination meeting frequency and format",
        ],
        "proportionality": "Interagency liaison is most relevant for patterns with cross-jurisdictional or multi-domain characteristics",
    },
}

IMPACT_DOMAIN_THREAT_CLASS_AFFINITIES: dict[str, dict[ImpactDomain, float]] = {
    ThreatClassCategory.SOCIOECONOMIC_INSTABILITY.value: {
        ImpactDomain.ECONOMIC_RESILIENCE: 0.9,
        ImpactDomain.COMMUNITY_STABILITY: 0.8,
        ImpactDomain.SOCIAL_COHESION: 0.75,
        ImpactDomain.INSTITUTIONAL_TRUST: 0.6,
    },
    ThreatClassCategory.CIVIL_UNREST_PROTEST.value: {
        ImpactDomain.COMMUNITY_STABILITY: 0.9,
        ImpactDomain.SOCIAL_COHESION: 0.85,
        ImpactDomain.INSTITUTIONAL_TRUST: 0.8,
        ImpactDomain.OPERATIONAL_CONTINUITY: 0.6,
    },
    ThreatClassCategory.IDEOLOGICAL_MOBILIZATION.value: {
        ImpactDomain.SOCIAL_COHESION: 0.85,
        ImpactDomain.INSTITUTIONAL_TRUST: 0.8,
        ImpactDomain.COMMUNITY_STABILITY: 0.7,
    },
    ThreatClassCategory.INFRASTRUCTURE_DISRUPTION.value: {
        ImpactDomain.INFRASTRUCTURE_INTEGRITY: 0.95,
        ImpactDomain.OPERATIONAL_CONTINUITY: 0.9,
        ImpactDomain.ECONOMIC_RESILIENCE: 0.7,
        ImpactDomain.COMMUNITY_STABILITY: 0.6,
    },
    ThreatClassCategory.COORDINATED_DISINFORMATION.value: {
        ImpactDomain.INSTITUTIONAL_TRUST: 0.9,
        ImpactDomain.SOCIAL_COHESION: 0.85,
        ImpactDomain.COMMUNITY_STABILITY: 0.6,
    },
}

IMPACT_DOMAIN_TEMPLATES: dict[ImpactDomain, dict] = {
    ImpactDomain.INSTITUTIONAL_TRUST: {
        "current": "Institutional trust levels within normal parameters",
        "trajectory": "If current discourse patterns persist, institutional trust may experience erosion in affected communities",
        "assumptions": ["Current discourse patterns continue", "No significant trust-building interventions occur"],
        "mitigating": ["Proactive transparent communication", "Community engagement initiatives", "Responsive grievance mechanisms"],
    },
    ImpactDomain.COMMUNITY_STABILITY: {
        "current": "Community stability indicators showing stress signals",
        "trajectory": "Continued pattern escalation may increase community tension and reduce social cohesion",
        "assumptions": ["Economic stressors remain unaddressed", "Discourse amplification continues"],
        "mitigating": ["Economic support programs", "Community dialogue initiatives", "Local leadership engagement"],
    },
    ImpactDomain.OPERATIONAL_CONTINUITY: {
        "current": "Operational continuity within acceptable parameters",
        "trajectory": "Pattern progression may create operational disruption risks requiring contingency activation",
        "assumptions": ["Current trajectory continues", "No preemptive resilience measures implemented"],
        "mitigating": ["Business continuity plan activation", "Resource pre-positioning", "Staff preparedness measures"],
    },
    ImpactDomain.ECONOMIC_RESILIENCE: {
        "current": "Economic resilience under stress from structural factors",
        "trajectory": "Persistent economic stress patterns may compound community vulnerability and grievance formation",
        "assumptions": ["Structural economic factors persist", "No targeted economic interventions"],
        "mitigating": ["Economic support mechanisms", "Workforce development programs", "Business assistance initiatives"],
    },
    ImpactDomain.SOCIAL_COHESION: {
        "current": "Social cohesion showing early stress indicators",
        "trajectory": "Continued polarization patterns may reduce social cohesion and increase community fragmentation",
        "assumptions": ["Polarizing discourse continues", "No cohesion-building interventions"],
        "mitigating": ["Cross-community dialogue programs", "Shared interest initiatives", "Inclusive communication strategies"],
    },
    ImpactDomain.INFRASTRUCTURE_INTEGRITY: {
        "current": "Infrastructure integrity within normal parameters",
        "trajectory": "If disruption risk patterns materialize, infrastructure integrity may be compromised",
        "assumptions": ["Current risk patterns continue", "No protective measures implemented"],
        "mitigating": ["Infrastructure hardening measures", "Redundancy improvements", "Monitoring enhancements"],
    },
}

AUTHORITY_DOMAIN_PATHWAY_AFFINITIES: dict[DecisionPathwayCategory, list[tuple[AuthorityDomain, float]]] = {
    DecisionPathwayCategory.ECONOMIC_ENGAGEMENT: [
        (AuthorityDomain.EXECUTIVE_LEADERSHIP, 0.8),
        (AuthorityDomain.STRATEGIC_PLANNING, 0.75),
        (AuthorityDomain.EXTERNAL_AFFAIRS, 0.7),
        (AuthorityDomain.COMMUNITY_RELATIONS, 0.65),
    ],
    DecisionPathwayCategory.COMMUNITY_OUTREACH: [
        (AuthorityDomain.COMMUNITY_RELATIONS, 0.9),
        (AuthorityDomain.COMMUNICATIONS_PUBLIC_AFFAIRS, 0.8),
        (AuthorityDomain.EXTERNAL_AFFAIRS, 0.7),
        (AuthorityDomain.EXECUTIVE_LEADERSHIP, 0.6),
    ],
    DecisionPathwayCategory.COMMUNICATIONS_STRATEGY: [
        (AuthorityDomain.COMMUNICATIONS_PUBLIC_AFFAIRS, 0.95),
        (AuthorityDomain.EXECUTIVE_LEADERSHIP, 0.7),
        (AuthorityDomain.COMMUNITY_RELATIONS, 0.65),
        (AuthorityDomain.LEGAL_COMPLIANCE, 0.5),
    ],
    DecisionPathwayCategory.STAKEHOLDER_COORDINATION: [
        (AuthorityDomain.EXTERNAL_AFFAIRS, 0.85),
        (AuthorityDomain.EXECUTIVE_LEADERSHIP, 0.8),
        (AuthorityDomain.STRATEGIC_PLANNING, 0.7),
        (AuthorityDomain.INTERAGENCY_COORDINATION, 0.65),
    ],
    DecisionPathwayCategory.RESOURCE_POSITIONING: [
        (AuthorityDomain.OPERATIONS_MANAGEMENT, 0.9),
        (AuthorityDomain.RISK_MANAGEMENT, 0.85),
        (AuthorityDomain.EXECUTIVE_LEADERSHIP, 0.7),
        (AuthorityDomain.STRATEGIC_PLANNING, 0.6),
    ],
    DecisionPathwayCategory.MONITORING_ADJUSTMENT: [
        (AuthorityDomain.RISK_MANAGEMENT, 0.9),
        (AuthorityDomain.OPERATIONS_MANAGEMENT, 0.8),
        (AuthorityDomain.STRATEGIC_PLANNING, 0.65),
        (AuthorityDomain.EXECUTIVE_LEADERSHIP, 0.6),
    ],
    DecisionPathwayCategory.INSTITUTIONAL_RESILIENCE: [
        (AuthorityDomain.RISK_MANAGEMENT, 0.9),
        (AuthorityDomain.OPERATIONS_MANAGEMENT, 0.85),
        (AuthorityDomain.HUMAN_RESOURCES, 0.7),
        (AuthorityDomain.EXECUTIVE_LEADERSHIP, 0.65),
    ],
    DecisionPathwayCategory.INTERAGENCY_LIAISON: [
        (AuthorityDomain.INTERAGENCY_COORDINATION, 0.95),
        (AuthorityDomain.EXTERNAL_AFFAIRS, 0.85),
        (AuthorityDomain.EXECUTIVE_LEADERSHIP, 0.75),
        (AuthorityDomain.LEGAL_COMPLIANCE, 0.6),
    ],
}

AUTHORITY_DOMAIN_TEMPLATES: dict[AuthorityDomain, dict] = {
    AuthorityDomain.EXECUTIVE_LEADERSHIP: {
        "rationale": "Executive leadership is positioned to provide strategic direction and authorize cross-functional responses",
        "awareness_areas": ["Overall threat pattern trajectory", "Resource allocation decisions", "External stakeholder communications"],
        "coordination": ["Strategic Planning", "External Affairs", "Risk Management"],
        "contexts": ["government", "enterprise", "multi-agency"],
    },
    AuthorityDomain.OPERATIONS_MANAGEMENT: {
        "rationale": "Operations management can implement operational adjustments and continuity measures",
        "awareness_areas": ["Operational continuity requirements", "Resource positioning needs", "Staff readiness levels"],
        "coordination": ["Risk Management", "Human Resources", "Executive Leadership"],
        "contexts": ["government", "enterprise"],
    },
    AuthorityDomain.COMMUNICATIONS_PUBLIC_AFFAIRS: {
        "rationale": "Communications is positioned to manage public messaging and counter narrative amplification",
        "awareness_areas": ["Information environment dynamics", "Public sentiment indicators", "Messaging alignment needs"],
        "coordination": ["Executive Leadership", "Community Relations", "Legal Compliance"],
        "contexts": ["government", "enterprise", "multi-agency"],
    },
    AuthorityDomain.COMMUNITY_RELATIONS: {
        "rationale": "Community relations can engage trusted intermediaries and address grievance formation",
        "awareness_areas": ["Community sentiment indicators", "Trusted intermediary networks", "Grievance patterns"],
        "coordination": ["Communications/Public Affairs", "External Affairs", "Executive Leadership"],
        "contexts": ["government", "enterprise"],
    },
    AuthorityDomain.RISK_MANAGEMENT: {
        "rationale": "Risk management can assess threat patterns and recommend proportional mitigation measures",
        "awareness_areas": ["Threat probability trends", "Vulnerability assessments", "Mitigation option effectiveness"],
        "coordination": ["Operations Management", "Executive Leadership", "Strategic Planning"],
        "contexts": ["government", "enterprise", "multi-agency"],
    },
    AuthorityDomain.LEGAL_COMPLIANCE: {
        "rationale": "Legal/compliance can ensure response measures remain within appropriate boundaries",
        "awareness_areas": ["Legal constraints on response options", "Compliance requirements", "Liability considerations"],
        "coordination": ["Executive Leadership", "Communications/Public Affairs", "Risk Management"],
        "contexts": ["government", "enterprise"],
    },
    AuthorityDomain.HUMAN_RESOURCES: {
        "rationale": "Human resources can address internal workforce concerns and insider risk indicators",
        "awareness_areas": ["Workforce sentiment indicators", "Internal communication needs", "Employee support requirements"],
        "coordination": ["Operations Management", "Executive Leadership", "Risk Management"],
        "contexts": ["enterprise"],
    },
    AuthorityDomain.EXTERNAL_AFFAIRS: {
        "rationale": "External affairs can coordinate with external stakeholders and partner organizations",
        "awareness_areas": ["External stakeholder concerns", "Partnership coordination needs", "Public-private interface"],
        "coordination": ["Executive Leadership", "Communications/Public Affairs", "Interagency Coordination"],
        "contexts": ["government", "enterprise", "multi-agency"],
    },
    AuthorityDomain.STRATEGIC_PLANNING: {
        "rationale": "Strategic planning can assess long-term implications and recommend adaptive strategies",
        "awareness_areas": ["Long-term trend implications", "Strategic option development", "Resource planning needs"],
        "coordination": ["Executive Leadership", "Risk Management", "Operations Management"],
        "contexts": ["government", "enterprise"],
    },
    AuthorityDomain.INTERAGENCY_COORDINATION: {
        "rationale": "Interagency coordination can facilitate information sharing and collective response alignment",
        "awareness_areas": ["Partner agency equities", "Information sharing opportunities", "Coordination mechanism effectiveness"],
        "coordination": ["External Affairs", "Executive Leadership", "Risk Management"],
        "contexts": ["government", "multi-agency"],
    },
}


def compute_decision_pathways(
    threat: ThreatObject,
    top_threat_class: Optional[str],
    threat_probability: float,
    intent_stage: IntentStage,
) -> DecisionPathwayIntelligence:
    """Compute decision pathway intelligence based on threat patterns."""
    
    pathway_scores: dict[DecisionPathwayCategory, float] = {}
    
    base_affinities = PATHWAY_THREAT_CLASS_AFFINITIES.get(
        top_threat_class, 
        {cat: 0.5 for cat in DecisionPathwayCategory}
    )
    
    for pathway_cat in DecisionPathwayCategory:
        base_score = base_affinities.get(pathway_cat, 0.3)
        
        stage_modifier = INTENT_STAGE_PATHWAY_MODIFIERS.get(intent_stage, {}).get(pathway_cat, 1.0)
        
        probability_factor = 0.5 + (threat_probability / 200)
        
        final_score = min(1.0, base_score * stage_modifier * probability_factor)
        pathway_scores[pathway_cat] = final_score
    
    sorted_pathways = sorted(pathway_scores.items(), key=lambda x: x[1], reverse=True)
    
    pathways: list[DecisionPathway] = []
    for pathway_cat, score in sorted_pathways[:5]:
        template = PATHWAY_ADVISORY_TEMPLATES.get(pathway_cat, {})
        
        if score >= 0.7:
            relevance = DecisionPathwayRelevance.HIGH
        elif score >= 0.5:
            relevance = DecisionPathwayRelevance.MODERATE
        else:
            relevance = DecisionPathwayRelevance.LOW
        
        contributing_factors = []
        if top_threat_class:
            contributing_factors.append(f"Threat class alignment: {top_threat_class.replace('_', ' ').title()}")
        contributing_factors.append(f"Intent stage: {intent_stage.value.replace('_', ' ').title()}")
        contributing_factors.append(f"Threat probability: {threat_probability:.1f}%")
        
        pathway = DecisionPathway(
            pathway_category=pathway_cat,
            relevance=relevance,
            relevance_score=score,
            advisory_summary=template.get("summary", "Consider this pathway based on current threat patterns"),
            suggested_considerations=template.get("considerations", []),
            proportionality_note=template.get("proportionality", "Proportional to assessed risk level"),
            contributing_factors=contributing_factors,
            confidence=0.6 + (score * 0.3),
        )
        pathways.append(pathway)
    
    primary_pathway = pathways[0].pathway_category if pathways else None
    
    if threat_probability < 40:
        posture = "Awareness posture recommended. Current patterns suggest monitoring with selective engagement opportunities."
    elif threat_probability < 60:
        posture = "Elevated awareness posture. Consider proactive engagement through high-relevance pathways."
    elif threat_probability < 80:
        posture = "Active engagement posture. Multiple pathways warrant consideration for proportional response."
    else:
        posture = "Heightened engagement posture. Coordinated multi-pathway approach may be warranted."
    
    proportionality = f"Response proportionality should align with current threat probability ({threat_probability:.1f}%) and intent stage ({intent_stage.value.replace('_', ' ').title()}). All guidance remains advisory and optional."
    
    return DecisionPathwayIntelligence(
        threat_id=threat.id,
        pathways=pathways,
        primary_pathway=primary_pathway,
        overall_advisory_posture=posture,
        proportionality_assessment=proportionality,
        last_updated=datetime.utcnow(),
    )


def compute_impact_forecast(
    threat: ThreatObject,
    top_threat_class: Optional[str],
    threat_probability: float,
    intent_stage: IntentStage,
    escalation_stage: int,
) -> ImpactForecast:
    """Compute system-level impact forecast based on threat patterns."""
    
    domain_scores: dict[ImpactDomain, float] = {}
    
    base_affinities = IMPACT_DOMAIN_THREAT_CLASS_AFFINITIES.get(
        top_threat_class,
        {domain: 0.4 for domain in ImpactDomain}
    )
    
    stage_multipliers = {
        IntentStage.GRIEVANCE_FORMATION: 0.6,
        IntentStage.COGNITIVE_FIXATION: 0.8,
        IntentStage.BEHAVIORAL_ACCELERATION: 1.0,
        IntentStage.MOBILIZATION_RISK: 1.2,
    }
    stage_mult = stage_multipliers.get(intent_stage, 0.8)
    
    probability_factor = threat_probability / 100
    
    for domain in ImpactDomain:
        base_score = base_affinities.get(domain, 0.3)
        final_score = min(1.0, base_score * stage_mult * (0.5 + probability_factor * 0.5))
        domain_scores[domain] = final_score
    
    sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
    
    base_hours = {
        IntentStage.GRIEVANCE_FORMATION: (168, 720),
        IntentStage.COGNITIVE_FIXATION: (72, 336),
        IntentStage.BEHAVIORAL_ACCELERATION: (24, 168),
        IntentStage.MOBILIZATION_RISK: (12, 72),
    }
    time_range = base_hours.get(intent_stage, (72, 336))
    
    projections: list[ImpactProjection] = []
    for domain, score in sorted_domains[:4]:
        template = IMPACT_DOMAIN_TEMPLATES.get(domain, {})
        
        if score >= 0.7:
            severity = "significant"
        elif score >= 0.5:
            severity = "moderate"
        elif score >= 0.3:
            severity = "minimal"
        else:
            severity = "minimal"
        
        confidence = 0.5 + (0.3 * (1 - score))
        confidence_band = (max(0, score - 0.15), min(1.0, score + 0.15))
        
        projection = ImpactProjection(
            domain=domain,
            current_assessment=template.get("current", "Current state within normal parameters"),
            projected_trajectory=template.get("trajectory", "Trajectory dependent on pattern evolution"),
            impact_severity=severity,
            impact_severity_score=score,
            time_horizon_hours=time_range,
            confidence=confidence,
            confidence_band=confidence_band,
            key_assumptions=template.get("assumptions", []),
            mitigating_factors=template.get("mitigating", []),
        )
        projections.append(projection)
    
    primary_domain = projections[0].domain if projections else None
    aggregate_severity = sum(p.impact_severity_score for p in projections) / len(projections) if projections else 0.0
    
    time_horizon_str = f"{time_range[0]}-{time_range[1]} hours ({time_range[0]/24:.1f}-{time_range[1]/24:.1f} days)"
    
    if aggregate_severity >= 0.7:
        overall = "System-level impact assessment indicates significant potential consequences across multiple domains if current trajectory persists."
    elif aggregate_severity >= 0.5:
        overall = "System-level impact assessment indicates moderate potential consequences in key domains if current trajectory persists."
    else:
        overall = "System-level impact assessment indicates limited potential consequences under current trajectory."
    
    return ImpactForecast(
        threat_id=threat.id,
        projections=projections,
        overall_impact_assessment=overall,
        primary_concern_domain=primary_domain,
        aggregate_severity_score=aggregate_severity,
        projection_time_horizon=time_horizon_str,
        last_updated=datetime.utcnow(),
    )


def compute_authority_recommendations(
    threat: ThreatObject,
    decision_pathways: DecisionPathwayIntelligence,
) -> AuthorityAwareRecommendations:
    """Compute authority-aware recommendations based on decision pathways."""
    
    authority_scores: dict[AuthorityDomain, float] = {domain: 0.0 for domain in AuthorityDomain}
    
    for pathway in decision_pathways.pathways:
        affinities = AUTHORITY_DOMAIN_PATHWAY_AFFINITIES.get(pathway.pathway_category, [])
        for authority_domain, affinity in affinities:
            contribution = pathway.relevance_score * affinity
            authority_scores[authority_domain] = max(authority_scores[authority_domain], contribution)
    
    sorted_authorities = sorted(authority_scores.items(), key=lambda x: x[1], reverse=True)
    
    recommendations: list[AuthorityRecommendation] = []
    for authority_domain, score in sorted_authorities[:5]:
        if score < 0.3:
            continue
            
        template = AUTHORITY_DOMAIN_TEMPLATES.get(authority_domain, {})
        
        recommendation = AuthorityRecommendation(
            authority_domain=authority_domain,
            relevance_score=score,
            positioning_rationale=template.get("rationale", "This domain may be relevant to current threat patterns"),
            suggested_awareness_areas=template.get("awareness_areas", []),
            coordination_considerations=template.get("coordination", []),
            context_applicability=template.get("contexts", ["government", "enterprise"]),
            confidence=0.6 + (score * 0.3),
        )
        recommendations.append(recommendation)
    
    primary_domain = recommendations[0].authority_domain if recommendations else None
    
    coordination_domains = set()
    for rec in recommendations[:3]:
        coordination_domains.update(rec.coordination_considerations)
    
    coordination_summary = f"Cross-domain coordination recommended among: {', '.join(list(coordination_domains)[:4])}. Information sharing and aligned messaging are key coordination priorities."
    
    all_contexts = set()
    for rec in recommendations:
        all_contexts.update(rec.context_applicability)
    
    if len(all_contexts) >= 3:
        context_applicability = "all"
    else:
        context_applicability = ", ".join(sorted(all_contexts))
    
    return AuthorityAwareRecommendations(
        threat_id=threat.id,
        recommendations=recommendations,
        primary_authority_domain=primary_domain,
        coordination_summary=coordination_summary,
        context_applicability=context_applicability,
        last_updated=datetime.utcnow(),
    )


def compute_decision_advantage_layer(threat: ThreatObject) -> DecisionAdvantageLayer:
    """
    Compute the complete Decision Advantage Layer for a threat object.
    
    Combines:
    - Decision Pathway Intelligence
    - Impact Forecasting
    - Authority-Aware Recommendations
    """
    
    threat_probability = threat.probability_curve.current_probability
    intent_stage = threat.intent_gradient.current_stage
    
    top_threat_class = None
    if threat.threat_class_alignment:
        top_threat_class = threat.threat_class_alignment.get("top_alignment")
    
    escalation_stage = 0
    if threat.escalation_pathway:
        escalation_stage = threat.escalation_pathway.get("current_stage_index", 0)
    
    decision_pathways = compute_decision_pathways(
        threat=threat,
        top_threat_class=top_threat_class,
        threat_probability=threat_probability,
        intent_stage=intent_stage,
    )
    
    impact_forecast = compute_impact_forecast(
        threat=threat,
        top_threat_class=top_threat_class,
        threat_probability=threat_probability,
        intent_stage=intent_stage,
        escalation_stage=escalation_stage,
    )
    
    authority_recommendations = compute_authority_recommendations(
        threat=threat,
        decision_pathways=decision_pathways,
    )
    
    if threat_probability < 40:
        posture = "Awareness posture with selective engagement"
    elif threat_probability < 60:
        posture = "Elevated awareness with proactive engagement consideration"
    elif threat_probability < 80:
        posture = "Active engagement posture with multi-pathway coordination"
    else:
        posture = "Heightened engagement with comprehensive coordination"
    
    confidence_weighted_priority = (
        threat_probability / 100 * 0.4 +
        impact_forecast.aggregate_severity_score * 0.3 +
        (decision_pathways.pathways[0].relevance_score if decision_pathways.pathways else 0.5) * 0.3
    )
    
    return DecisionAdvantageLayer(
        threat_id=threat.id,
        decision_pathways=decision_pathways,
        impact_forecast=impact_forecast,
        authority_recommendations=authority_recommendations,
        overall_decision_posture=posture,
        confidence_weighted_priority=min(1.0, confidence_weighted_priority),
        last_updated=datetime.utcnow(),
    )
