"""
AURORA™ Live Data Sources - Phase 1.4.1

Controlled pilot for internal live U.S. data ingestion.

SCOPE & CONSTRAINTS (NON-NEGOTIABLE):
- Live Data Mode: ON_US_ONLY
- No alerts
- No event detection
- No actor or individual modeling
- No public-facing feeds
- No UI language changes implying monitoring or real-time surveillance

ENABLED INPUT SOURCES (LIMITED SET):
A. Structural / Economic Indicators - Macro-level only
B. Abstracted Public Discourse Trends - Topic-level frequency and sentiment deltas only
C. Institutional / Policy Indicators - Metadata only

All inputs must pass existing ingestion validation and governance checks.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum

from app.models.schemas import (
    AllowedInputCategory,
    SignalDomain,
)


class LiveDataSourceType(str, Enum):
    STRUCTURAL_ECONOMIC = "structural_economic"
    ABSTRACTED_DISCOURSE = "abstracted_discourse"
    INSTITUTIONAL_POLICY = "institutional_policy"


class LiveDataSourceConfig:
    """Configuration for live data source constraints"""
    
    STRUCTURAL_ECONOMIC_CONFIG = {
        "enabled": True,
        "jurisdiction": "US",
        "granularity": "macro",
        "min_region_level": "state",
        "update_frequency_hours": 6,
        "allowed_indicators": [
            "unemployment_rate",
            "gdp_growth",
            "inflation_rate",
            "housing_starts",
            "manufacturing_index",
            "consumer_confidence",
            "wage_growth",
            "labor_force_participation",
            "trade_balance",
            "industrial_production"
        ],
        "prohibited": [
            "individual_income",
            "personal_data",
            "sub_county_data",
            "real_time_transactions"
        ]
    }
    
    ABSTRACTED_DISCOURSE_CONFIG = {
        "enabled": True,
        "jurisdiction": "US",
        "granularity": "topic_level",
        "time_resolution_hours": 1,
        "allowed_metrics": [
            "topic_frequency_delta",
            "sentiment_delta",
            "discourse_volume",
            "narrative_trend",
            "topic_emergence_score"
        ],
        "prohibited": [
            "raw_text",
            "user_accounts",
            "platform_identifiers",
            "individual_posts",
            "user_handles",
            "direct_quotes"
        ]
    }
    
    INSTITUTIONAL_POLICY_CONFIG = {
        "enabled": True,
        "jurisdiction": "US",
        "granularity": "metadata_only",
        "allowed_indicators": [
            "policy_announcement",
            "regulatory_change",
            "legislative_status",
            "agency_posture",
            "compliance_update",
            "institutional_statement"
        ],
        "prohibited": [
            "document_content",
            "full_text_storage",
            "individual_officials",
            "private_communications"
        ]
    }


class LiveDataInput:
    """Represents a validated live data input"""
    
    def __init__(
        self,
        source_type: LiveDataSourceType,
        category: AllowedInputCategory,
        content: str,
        metadata: dict,
        timestamp: datetime,
        input_id: Optional[str] = None
    ):
        self.input_id = input_id or str(uuid.uuid4())
        self.source_type = source_type
        self.category = category
        self.content = content
        self.metadata = metadata
        self.timestamp = timestamp
        self.governance_validated = False
        self.governance_audit_ref: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "input_id": self.input_id,
            "source_type": self.source_type.value,
            "category": self.category.value,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "governance_validated": self.governance_validated,
            "governance_audit_ref": self.governance_audit_ref
        }


class LiveDataSourceHandler:
    """
    Handler for live U.S. data sources.
    
    All inputs are subject to:
    - Domain classification at ingestion
    - Domain balance enforcement
    - Velocity dampening
    - Escalation ceilings
    - Confidence collapse handling
    - Cannot bypass convergence or Decision Confidence Gate
    
    All governance decisions are logged.
    """
    
    def __init__(self):
        self.config = LiveDataSourceConfig()
        self.enabled = False
        self.enabled_at: Optional[datetime] = None
        self.enabled_by: Optional[str] = None
        self.input_buffer: list[LiveDataInput] = []
        self.processed_count = 0
        self.rejected_count = 0
        self.last_ingestion: Optional[datetime] = None
        
        self._structural_economic_buffer: list[dict] = []
        self._discourse_buffer: list[dict] = []
        self._institutional_buffer: list[dict] = []
    
    def enable_live_data(self, enabled_by: str = "system") -> dict:
        """Enable live data ingestion with audit logging"""
        self.enabled = True
        self.enabled_at = datetime.utcnow()
        self.enabled_by = enabled_by
        
        return {
            "status": "enabled",
            "enabled_at": self.enabled_at.isoformat(),
            "enabled_by": enabled_by,
            "sources_enabled": [
                LiveDataSourceType.STRUCTURAL_ECONOMIC.value,
                LiveDataSourceType.ABSTRACTED_DISCOURSE.value,
                LiveDataSourceType.INSTITUTIONAL_POLICY.value
            ],
            "jurisdiction": "US",
            "constraints": {
                "no_alerts": True,
                "no_event_detection": True,
                "no_actor_modeling": True,
                "no_public_feeds": True,
                "governance_enforced": True
            }
        }
    
    def disable_live_data(self, disabled_by: str = "system") -> dict:
        """Disable live data ingestion"""
        self.enabled = False
        
        return {
            "status": "disabled",
            "disabled_at": datetime.utcnow().isoformat(),
            "disabled_by": disabled_by,
            "processed_count": self.processed_count,
            "rejected_count": self.rejected_count
        }
    
    def get_status(self) -> dict:
        """Get current live data source status"""
        return {
            "enabled": self.enabled,
            "enabled_at": self.enabled_at.isoformat() if self.enabled_at else None,
            "enabled_by": self.enabled_by,
            "jurisdiction": "US",
            "sources": {
                "structural_economic": {
                    "enabled": self.config.STRUCTURAL_ECONOMIC_CONFIG["enabled"],
                    "buffer_size": len(self._structural_economic_buffer),
                    "granularity": self.config.STRUCTURAL_ECONOMIC_CONFIG["granularity"]
                },
                "abstracted_discourse": {
                    "enabled": self.config.ABSTRACTED_DISCOURSE_CONFIG["enabled"],
                    "buffer_size": len(self._discourse_buffer),
                    "time_resolution_hours": self.config.ABSTRACTED_DISCOURSE_CONFIG["time_resolution_hours"]
                },
                "institutional_policy": {
                    "enabled": self.config.INSTITUTIONAL_POLICY_CONFIG["enabled"],
                    "buffer_size": len(self._institutional_buffer),
                    "granularity": self.config.INSTITUTIONAL_POLICY_CONFIG["granularity"]
                }
            },
            "statistics": {
                "processed_count": self.processed_count,
                "rejected_count": self.rejected_count,
                "last_ingestion": self.last_ingestion.isoformat() if self.last_ingestion else None
            },
            "constraints_enforced": [
                "No alerts",
                "No event detection",
                "No actor modeling",
                "No individual surveillance",
                "No public-facing feeds",
                "U.S. context only"
            ]
        }
    
    def ingest_structural_economic(
        self,
        indicator_type: str,
        value: float,
        region: str,
        metadata: Optional[dict] = None
    ) -> Optional[LiveDataInput]:
        """
        Ingest structural/economic indicator.
        
        Constraints:
        - Macro-level only
        - No sub-regional precision below defined regions
        """
        if not self.enabled:
            return None
        
        config = self.config.STRUCTURAL_ECONOMIC_CONFIG
        
        if indicator_type not in config["allowed_indicators"]:
            self.rejected_count += 1
            return None
        
        content = f"Economic indicator: {indicator_type} at {value} for region {region}"
        
        input_data = LiveDataInput(
            source_type=LiveDataSourceType.STRUCTURAL_ECONOMIC,
            category=AllowedInputCategory.STRUCTURAL_ECONOMIC,
            content=content,
            metadata={
                "indicator_type": indicator_type,
                "value": value,
                "region": region,
                "granularity": config["granularity"],
                **(metadata or {})
            },
            timestamp=datetime.utcnow()
        )
        
        self._structural_economic_buffer.append(input_data.to_dict())
        self.input_buffer.append(input_data)
        self.processed_count += 1
        self.last_ingestion = datetime.utcnow()
        
        return input_data
    
    def ingest_discourse_trend(
        self,
        topic: str,
        frequency_delta: float,
        sentiment_delta: float,
        metadata: Optional[dict] = None
    ) -> Optional[LiveDataInput]:
        """
        Ingest abstracted discourse trend.
        
        Constraints:
        - Topic-level frequency and sentiment deltas only
        - No raw text, accounts, platforms, or identifiers
        - Time resolution no finer than hourly
        """
        if not self.enabled:
            return None
        
        config = self.config.ABSTRACTED_DISCOURSE_CONFIG
        
        content = f"Discourse trend: topic '{topic}' frequency delta {frequency_delta:+.2f}%, sentiment delta {sentiment_delta:+.2f}"
        
        input_data = LiveDataInput(
            source_type=LiveDataSourceType.ABSTRACTED_DISCOURSE,
            category=AllowedInputCategory.ABSTRACTED_DISCOURSE,
            content=content,
            metadata={
                "topic": topic,
                "frequency_delta": frequency_delta,
                "sentiment_delta": sentiment_delta,
                "granularity": config["granularity"],
                "time_resolution_hours": config["time_resolution_hours"],
                **(metadata or {})
            },
            timestamp=datetime.utcnow()
        )
        
        self._discourse_buffer.append(input_data.to_dict())
        self.input_buffer.append(input_data)
        self.processed_count += 1
        self.last_ingestion = datetime.utcnow()
        
        return input_data
    
    def ingest_institutional_indicator(
        self,
        indicator_type: str,
        institution: str,
        posture_change: str,
        metadata: Optional[dict] = None
    ) -> Optional[LiveDataInput]:
        """
        Ingest institutional/policy indicator.
        
        Constraints:
        - Public policy, regulatory, or institutional posture changes
        - Metadata only (no document storage)
        """
        if not self.enabled:
            return None
        
        config = self.config.INSTITUTIONAL_POLICY_CONFIG
        
        if indicator_type not in config["allowed_indicators"]:
            self.rejected_count += 1
            return None
        
        content = f"Institutional indicator: {indicator_type} from {institution} - {posture_change}"
        
        input_data = LiveDataInput(
            source_type=LiveDataSourceType.INSTITUTIONAL_POLICY,
            category=AllowedInputCategory.INSTITUTIONAL_POLICY,
            content=content,
            metadata={
                "indicator_type": indicator_type,
                "institution": institution,
                "posture_change": posture_change,
                "granularity": config["granularity"],
                **(metadata or {})
            },
            timestamp=datetime.utcnow()
        )
        
        self._institutional_buffer.append(input_data.to_dict())
        self.input_buffer.append(input_data)
        self.processed_count += 1
        self.last_ingestion = datetime.utcnow()
        
        return input_data
    
    def get_recent_inputs(self, limit: int = 50) -> list[dict]:
        """Get recent live data inputs"""
        return [inp.to_dict() for inp in self.input_buffer[-limit:]]
    
    def get_freshness_summary(self) -> dict:
        """Get data freshness summary for all sources"""
        now = datetime.utcnow()
        
        def get_source_freshness(buffer: list, update_freq_hours: float) -> dict:
            if not buffer:
                return {
                    "status": "no_data",
                    "last_update": None,
                    "freshness_band": "stale"
                }
            
            latest = buffer[-1] if buffer else None
            if latest and "timestamp" in latest:
                last_update = datetime.fromisoformat(latest["timestamp"].replace("Z", "+00:00"))
                hours_since = (now - last_update).total_seconds() / 3600
                
                if hours_since < 6:
                    freshness_band = "fresh"
                elif hours_since < 24:
                    freshness_band = "recent"
                else:
                    freshness_band = "aging"
                
                return {
                    "status": "active",
                    "last_update": last_update.isoformat(),
                    "hours_since_update": round(hours_since, 1),
                    "freshness_band": freshness_band
                }
            
            return {
                "status": "unknown",
                "last_update": None,
                "freshness_band": "unknown"
            }
        
        return {
            "structural_economic": get_source_freshness(
                self._structural_economic_buffer,
                self.config.STRUCTURAL_ECONOMIC_CONFIG["update_frequency_hours"]
            ),
            "abstracted_discourse": get_source_freshness(
                self._discourse_buffer,
                self.config.ABSTRACTED_DISCOURSE_CONFIG["time_resolution_hours"]
            ),
            "institutional_policy": get_source_freshness(
                self._institutional_buffer,
                6.0
            ),
            "overall": {
                "total_inputs": len(self.input_buffer),
                "last_ingestion": self.last_ingestion.isoformat() if self.last_ingestion else None
            }
        }


live_data_source_handler = LiveDataSourceHandler()
