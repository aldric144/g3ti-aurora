"""
AURORA™ Probabilistic Threat Class Alignment Module

Computes probabilistic alignment scores for analytic threat classes.
NOT definitive labels, accusations, or enforcement framing.
"""

from app.modules.threat_class.engine import (
    compute_threat_class_alignment,
    compute_domain_composition,
    ThreatClassCategory,
)

__all__ = [
    "compute_threat_class_alignment",
    "compute_domain_composition",
    "ThreatClassCategory",
]
