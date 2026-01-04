"""
AURORA™ Live Data Governance Module - Phase 1.4

Implements four governance layers for live U.S. data ingestion:
1. Live Data Governance Mode (Policy Enforcement Layer)
2. Data Freshness & Time Semantics
3. Live-Data Fail-Safe & Dampening Controls
4. Provenance & Context Attribution

GLOBAL SAFETY RULES (NON-NEGOTIABLE):
- No alerts
- No event detection
- No actor modeling
- No individual or population surveillance
- No public-facing live feeds
- U.S. context only (global synthetic remains unchanged)
"""

from .engine import LiveDataGovernanceEngine, live_data_governance_engine
from .sources import (
    LiveDataSourceHandler,
    LiveDataSourceType,
    LiveDataSourceConfig,
    LiveDataInput,
    live_data_source_handler
)

__all__ = [
    "LiveDataGovernanceEngine",
    "live_data_governance_engine",
    "LiveDataSourceHandler",
    "LiveDataSourceType",
    "LiveDataSourceConfig",
    "LiveDataInput",
    "live_data_source_handler"
]
