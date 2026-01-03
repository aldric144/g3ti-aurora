"""
AURORA™ Signal Ingestion Engine
Handles intake, validation, and preprocessing of weak signals

PATENT-CRITICAL CONSTRAINTS:
- No user identities, handles, device identifiers, or personal identifiers stored
- No raw content (posts, messages, pages, images) persisted
- Only abstracted, non-attributive behavioral indicators retained
- All indicators must be mathematically derived and non-reversible

This module is responsible for:
- Validating incoming signals against schema requirements
- Enforcing privacy safeguards and content abstraction rules
- Normalizing signal confidence values
- Applying domain-specific preprocessing
- Logging all ingestion events for audit trail
"""

import re
from datetime import datetime
from typing import Optional
import uuid

from app.models.schemas import (
    Signal,
    SignalCreate,
    SignalDomain,
    SignalType,
    AuditEntry,
)
from app.database.store import get_store

PII_PATTERNS = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
    r'\b(?:@|#)[A-Za-z0-9_]{1,50}\b',
    r'\b(?:user|handle|username|account)[:\s]*[A-Za-z0-9_]{3,30}\b',
    r'\b(?:IP|ip)[:\s]*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    r'\b[A-Fa-f0-9]{2}(?::[A-Fa-f0-9]{2}){5}\b',
]

PROHIBITED_CONTENT_INDICATORS = [
    'raw_post', 'raw_message', 'raw_content', 'full_text',
    'screenshot', 'image_data', 'file_content', 'attachment',
    'private_message', 'dm_content', 'credential', 'password',
]


class SignalIngestionEngine:
    """
    Signal Ingestion Engine for AURORA™
    
    Processes incoming signals from multiple domains and prepares them
    for correlation analysis. All operations are logged for audit purposes.
    """
    
    DOMAIN_WEIGHTS = {
        SignalDomain.SOCIAL_DISCOURSE: 1.0,
        SignalDomain.BEHAVIORAL_TREND: 1.2,
        SignalDomain.ENVIRONMENTAL_STRESSOR: 1.3,
    }
    
    SIGNAL_TYPE_WEIGHTS = {
        SignalType.SENTIMENT_SHIFT: 1.0,
        SignalType.TOPIC_EMERGENCE: 0.9,
        SignalType.NARRATIVE_AMPLIFICATION: 1.1,
        SignalType.FREQUENCY_INCREASE: 1.0,
        SignalType.ESCALATION_PATTERN: 1.3,
        SignalType.FIXATION_INDICATOR: 1.4,
        SignalType.ECONOMIC_STRESS: 1.2,
        SignalType.GEOGRAPHIC_CLUSTERING: 1.1,
        SignalType.TEMPORAL_PATTERN: 0.9,
        SignalType.NETWORK_EXPANSION: 1.2,
    }
    
    def __init__(self):
        self.store = get_store()
    
    def ingest_signal(self, signal_data: SignalCreate, threat_id: Optional[str] = None) -> Signal:
        """
        Ingest a new signal into the system.
        
        Args:
            signal_data: The signal creation data
            threat_id: Optional threat ID to associate the signal with
            
        Returns:
            The created Signal object with computed weights
        """
        base_weight = self._calculate_base_weight(signal_data.domain, signal_data.signal_type)
        adjusted_weight = base_weight * signal_data.weight
        
        normalized_confidence = self._normalize_confidence(
            signal_data.raw_confidence,
            signal_data.domain
        )
        
        signal = Signal(
            id=str(uuid.uuid4()),
            domain=signal_data.domain,
            signal_type=signal_data.signal_type,
            source_description=signal_data.source_description,
            raw_confidence=normalized_confidence,
            weight=adjusted_weight,
            timestamp=datetime.utcnow(),
            metadata=signal_data.metadata,
            reasoning=signal_data.reasoning
        )
        
        self.store.signals[signal.id] = signal
        
        if threat_id:
            threat = self.store.get_threat(threat_id)
            if threat:
                self.store.add_signal_to_threat(threat_id, signal)
        
        self._log_ingestion(signal, threat_id)
        
        return signal
    
    def _calculate_base_weight(self, domain: SignalDomain, signal_type: SignalType) -> float:
        """
        Calculate base weight for a signal based on domain and type.
        
        Weight calculation considers:
        - Domain importance (environmental stressors weighted higher)
        - Signal type specificity (escalation patterns weighted higher)
        """
        domain_weight = self.DOMAIN_WEIGHTS.get(domain, 1.0)
        type_weight = self.SIGNAL_TYPE_WEIGHTS.get(signal_type, 1.0)
        
        return domain_weight * type_weight
    
    def _normalize_confidence(self, raw_confidence: float, domain: SignalDomain) -> float:
        """
        Normalize confidence values based on domain characteristics.
        
        Different domains have different baseline reliability levels.
        This normalization ensures fair comparison across domains.
        """
        domain_reliability = {
            SignalDomain.SOCIAL_DISCOURSE: 0.85,
            SignalDomain.BEHAVIORAL_TREND: 0.90,
            SignalDomain.ENVIRONMENTAL_STRESSOR: 0.95,
        }
        
        reliability_factor = domain_reliability.get(domain, 0.9)
        normalized = raw_confidence * reliability_factor
        
        return min(max(normalized, 0.0), 1.0)
    
    def _log_ingestion(self, signal: Signal, threat_id: Optional[str]):
        """Log signal ingestion for audit trail"""
        self.store._log_audit(
            action_type="signal_ingested",
            actor="signal_ingestion_engine",
            target_type="signal",
            target_id=signal.id,
            reasoning=f"Signal ingested: {signal.signal_type} from {signal.domain}",
            after_state={
                "domain": signal.domain,
                "signal_type": signal.signal_type,
                "confidence": signal.raw_confidence,
                "weight": signal.weight,
                "threat_id": threat_id
            }
        )
    
    def validate_signal(self, signal_data: SignalCreate) -> tuple[bool, list[str]]:
        """
        Validate signal data before ingestion.
        
        PATENT-CRITICAL: Enforces privacy safeguards and content abstraction rules.
        
        Returns:
            Tuple of (is_valid, list of validation errors)
        """
        errors = []
        
        if signal_data.raw_confidence < 0 or signal_data.raw_confidence > 1:
            errors.append("raw_confidence must be between 0 and 1")
        
        if signal_data.weight < 0:
            errors.append("weight must be non-negative")
        
        if not signal_data.source_description or len(signal_data.source_description) < 10:
            errors.append("source_description must be at least 10 characters")
        
        if not signal_data.reasoning or len(signal_data.reasoning) < 20:
            errors.append("reasoning must be at least 20 characters for audit purposes")
        
        pii_errors = self._check_for_pii(signal_data)
        errors.extend(pii_errors)
        
        content_errors = self._check_for_prohibited_content(signal_data)
        errors.extend(content_errors)
        
        return len(errors) == 0, errors
    
    def _check_for_pii(self, signal_data: SignalCreate) -> list[str]:
        """
        PATENT-CRITICAL: Check for personally identifiable information.
        
        Enforces Identity & Privacy Safeguards:
        - No user identities, handles, device identifiers stored
        - No personal identifiers or persistent personas tracked
        """
        errors = []
        text_to_check = f"{signal_data.source_description} {signal_data.reasoning}"
        
        if signal_data.metadata:
            text_to_check += f" {str(signal_data.metadata)}"
        
        for pattern in PII_PATTERNS:
            if re.search(pattern, text_to_check, re.IGNORECASE):
                errors.append(
                    "PRIVACY VIOLATION: Signal contains potential PII (personal identifiable information). "
                    "Only abstracted, non-attributive behavioral indicators are permitted."
                )
                break
        
        return errors
    
    def _check_for_prohibited_content(self, signal_data: SignalCreate) -> list[str]:
        """
        PATENT-CRITICAL: Check for prohibited raw content indicators.
        
        Enforces Content Abstraction Rules:
        - Raw content (posts, messages, pages, images) is NEVER persisted
        - Only mathematically derived, non-reversible indicators retained
        """
        errors = []
        
        if signal_data.metadata:
            metadata_str = str(signal_data.metadata).lower()
            for indicator in PROHIBITED_CONTENT_INDICATORS:
                if indicator in metadata_str:
                    errors.append(
                        f"CONTENT VIOLATION: Signal metadata contains prohibited content indicator '{indicator}'. "
                        "Raw content must not be persisted. Only abstracted behavioral indicators are permitted."
                    )
                    break
        
        return errors
    
    def get_signals_by_domain(self, domain: SignalDomain) -> list[Signal]:
        """Get all signals for a specific domain"""
        return [s for s in self.store.signals.values() if s.domain == domain]
    
    def get_signals_by_type(self, signal_type: SignalType) -> list[Signal]:
        """Get all signals of a specific type"""
        return [s for s in self.store.signals.values() if s.signal_type == signal_type]
    
    def get_recent_signals(self, hours: int = 24) -> list[Signal]:
        """Get signals from the last N hours"""
        cutoff = datetime.utcnow().timestamp() - (hours * 3600)
        return [
            s for s in self.store.signals.values()
            if s.timestamp.timestamp() > cutoff
        ]
