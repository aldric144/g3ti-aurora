# AURORA - Pre-Incident Decision Intelligence Engine

**Global 3 Technology & Intelligence (G3TI)**

AURORA is a patent-grade, government-ready intelligence platform that detects emerging threats before they manifest using weak-signal convergence across multiple domains. It produces human-readable intelligence narratives with confidence scoring for executive decision support.

---

## DEMONSTRATION ENVIRONMENT NOTICE

This is a **pre-patent technology preview** using **synthetic/demo data only**.

- Not for operational use
- Not for real-world monitoring or enforcement
- No live data feeds or surveillance capabilities
- All data is simulated for demonstration purposes

---

## System Architecture

AURORA follows a modular microservices architecture with clear separation between:

```
aurora/
├── aurora-backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/            # REST API endpoints
│   │   ├── database/       # In-memory data store
│   │   ├── models/         # Pydantic schemas
│   │   └── modules/        # Core intelligence modules
│   │       ├── signal_ingestion/      # Signal intake & validation
│   │       ├── correlation/           # Weak-signal convergence
│   │       ├── intent_modeling/       # Intent gradient analysis
│   │       └── narrative_generation/  # NIO generation
│   └── pyproject.toml
│
└── aurora-frontend/         # React + TypeScript frontend
    ├── src/
    │   ├── components/     # UI components (shadcn/ui)
    │   └── App.tsx         # Main application
    └── package.json
```

## Core Capabilities

### Phase 1: Context-Aware Color Intelligence

- **Intent Stage Mapping**: Blue (Grievance Formation) → Amber (Cognitive Fixation) → Orange (Behavioral Acceleration) → Red (Mobilization Risk)
- **Probability Intensity Scaling**: Color saturation scales with threat probability
- **Confidence-Based Saturation**: Visual confidence indicators
- **WCAG AA Compliance**: Accessible color contrast throughout

### Phase 2: Decision Intelligence Enhancements

#### 1. Region-Aware Intelligence (Safe "Where")
- Abstracted geographic context (multi-state, metro-adjacent, regional corridors)
- No exact locations, maps, or pinpoint coordinates
- Confidence scoring for regional attribution
- Policy-safe and non-targeting

#### 2. Escalation Pathway Modeling (Safe "How")
- Pattern-based progression: Structural Stress → Discourse → Behavior → Mobilization
- Current position indicator within pathway
- Projected progression windows with uncertainty bounds
- Decision support only, not forecasting specific incidents

#### 3. Authorized Drill-Down Logic (Safe "When")
- Role-based access controls (BASIC, ANALYST, SENIOR_ANALYST, SUPERVISOR)
- Region granularity refinement (macro → sub-region)
- Signal class inspection without exposing raw data
- Timing sensitivity and acceleration indicators
- Full audit logging

#### 4. Probabilistic Threat Class Alignment
- 8 analytic threat class categories (non-exclusive, non-criminal)
- Probabilistic weighting based on signals, intent stage, escalation pathway
- Intent-aware evolution with gradual transitions
- Full explainability with rationale for each alignment

### Phase 3: Decision Advantage & Authority-Aware Guidance

#### 1. Decision Pathway Intelligence
- 8 advisory pathway categories (economic engagement, community outreach, communications, etc.)
- Relevance ranking (High / Moderate / Low) with confidence scores
- Proportionality notes and suggested considerations
- Explicitly avoids enforcement or tactical instruction
- All guidance is optional, advisory, and proportional

#### 2. Impact Forecasting (System-Level)
- 6 impact domains (institutional trust, community stability, operational continuity, etc.)
- System-level impact projections with time horizons
- Confidence bands and severity scoring
- Focuses on institutional and community outcomes
- Does not predict specific events or actors

#### 3. Authority-Aware Recommendations
- 10 leadership domains (executive leadership, operations management, communications, etc.)
- Identifies which domains are best positioned to respond
- Context applicability (government, enterprise, multi-agency)
- No naming of individuals, units, or enforcement targets
- Supports cross-domain coordination

#### 4. Decision Advantage Summary
- Overall decision posture assessment
- Confidence-weighted priority scoring
- Master disclaimer and policy compliance badges
- Full audit trail for all recommendations

### Phase 3.x: Decision Discipline & Trust Hardening

#### 1. Decision Confidence Gate
- Gating mechanism (NOT a numeric score) that controls what the system is allowed to recommend
- Inputs: Signal diversity, persistence over time, cross-domain convergence, data confidence
- Gate states: OPEN (full recommendations), LIMITED (restricted outputs), CLOSED (monitoring only)
- When confidence is below threshold: Limits outputs to monitoring or informational posture
- All gating decisions logged in the audit trail

#### 2. Decision Readiness Levels (DRL)
- Advisory framing layer (NOT threat levels)
- DRL-0: Informational Awareness - Pattern detected but not yet decision-relevant
- DRL-1: Monitor & Observe - Pattern warrants continued attention
- DRL-2: Consider Engagement - Pattern suggests potential for escalation
- DRL-3: Prepare Cross-Functional Response - Pattern indicates elevated decision relevance
- One DRL active per context at a time
- No enforcement language

#### 3. Context Aging & Decay Language
- Explicit aging and decay indicators for contexts
- States: STABLE, COOLING, DECAYING, STALE
- Contexts must not feel permanent
- No sudden removals without explanation
- All aging events logged for auditability

#### 4. "Why This Is Shown" Explainability Panel
- Expandable element on Decision Pathways, Impact Forecasting, Authority-Aware Recommendations
- Explains what factors caused the panel to appear
- Shows what factors did NOT trigger it
- States what the system is explicitly NOT claiming
- Supports audits and demos

#### 5. Visual & UX Restraint Rules
- Urgency conveyed through consistency and persistence, not animation
- No blinking, pulsing, or alarm-style UI
- No red/yellow/green threat status framing
- No global "top threats" or "alert counts"
- The loudest visual element must never be the most urgent element

#### 6. Silent Audit Mode (Foundational Hook)
- Backend support for future review of historical system state
- Enables post-hoc decision review
- Supports training and governance use
- No live UI exposure yet

### Phase 4: Multi-Context Regional Intelligence

#### 1. Context Stack Model
- Multiple independent decision contexts per region (3-5 optimal, max 8 displayed)
- Each context has its own signals, intent stage, decision pathways, impact forecasting, and confidence score
- Contexts are never automatically merged
- No compounded probabilities or combined threat labels
- Excess contexts (>8) summarized as "Additional low-confidence contexts detected and summarized"

#### 2. Context Prioritization & Display Rules
- Prioritization based on intent stage, persistence, decision impact, and confidence
- Priority scoring formula: (stage_weight * 0.35) + (persistence * 0.25) + (decision_impact * 0.25) + (confidence * 0.15)
- Only one context expanded at a time in UI
- Context overlap indicated textually (e.g., "3 active contexts in this region")
- No automatic escalation across contexts

#### 3. Region-as-Context Map (Layered Confidence Bands)
- Display only one region at a time (no global map overlays)
- Layered Region Confidence Bands visualization:
  - **Core Region**: Solid outline, strongest analytical relevance
  - **Adjacent Zone**: Dashed outline, moderate relevance
  - **Peripheral Influence**: Soft/faded boundary, limited relevance
- Bands represent analytical relevance only, not events, actors, or threats
- Map remains visually stable across context switches

#### 4. Multi-Region Handling (Safe & Controlled)
- Internal support for multiple regions concurrently
- Regional Context Selector for switching between regions
- Each region maintains its own independent context stack
- No simultaneous multi-region overlays permitted

#### 5. Safety & Governance Constraints
- No context merging across or within regions
- No combined escalation language
- No "compound threat" labels
- No global surveillance views
- No actor attribution or event prediction
- All outputs remain pre-incident, advisory, explainable, auditable, non-investigative

### Phase 1.4: Live Data Governance

Prepares AURORA for internal live U.S. data ingestion while maintaining strict pre-incident, non-surveillance, non-alerting posture.

#### 1. Live Data Governance Mode (Policy Enforcement Layer)
- System-wide Live Data Mode flag with explicit behavior controls
- Modes: OFF (demo/synthetic only) or ON_US_ONLY (live contextual indicators under constraints)
- When ON: Only allows permitted input categories:
  - Structural / Economic indicators
  - Abstracted Discourse (topic-level only)
  - Institutional / Policy indicators
- Automatically rejects or quarantines inputs containing:
  - Individual identifiers (PII)
  - Precise geolocation (below regional level)
  - Actor-level or event-level observation
  - Alerting semantics
  - Non-U.S. context
- Enforcement at ingestion, not post-analysis
- All mode changes explicitly logged

#### 2. Data Freshness & Time Semantics
- Time-aware context labeling across system
- Data freshness bands: Fresh (<6 hours), Recent (6-24 hours), Aging (>24 hours)
- Context persistence states: Fresh, Persistent, Cooling, Decaying, Stale
- Rules:
  - No expectation of instant change
  - Intent stages may only advance based on persistence over time
  - Freshness labels displayed where context is summarized (non-intrusive)

#### 3. Live-Data Fail-Safe & Dampening Controls
- **Velocity Dampening**: Caps rate of probability change per time window
- **Domain Balance Enforcement**: No single signal domain may dominate without cross-domain confirmation
- **Escalation Ceilings**: Intent stages cannot advance more than one level within defined time window
- **Confidence Collapse Handling**: If confidence drops suddenly, system softens outputs rather than escalating
- All fail-safe activations logged for audit purposes

#### 4. Provenance & Context Attribution (Non-Source Disclosing)
- Internal context provenance tagging without revealing sources
- Provenance labels:
  - "Context primarily driven by structural indicators"
  - "Discourse-weighted context"
  - "Institutional policy-influenced context"
  - "Economic indicator-driven context"
  - "Behavioral pattern-influenced context"
- Provenance visible in "Why This Is Shown" panels and audit logs
- Does NOT expose raw sources, feeds, or platforms
- Purpose is explanation, not traceability

#### Global Safety Rules (Non-Negotiable)
- No alerts
- No event detection
- No actor modeling
- No individual or population surveillance
- No public-facing live feeds
- U.S. context only (global synthetic remains unchanged)

### Phase 1.4.1: Live U.S. Data Enabled (Controlled Pilot)

Enables internal live U.S. data ingestion under the existing Live Data Governance framework.

#### Scope & Constraints (Non-Negotiable)
- Live Data Mode: ON_US_ONLY
- No alerts
- No event detection
- No actor or individual modeling
- No public-facing feeds
- No UI language changes implying monitoring or real-time surveillance

#### Enabled Input Sources (Limited Set)

**A. Structural / Economic Indicators**
- Macro-level only
- No sub-regional precision below defined regions
- Allowed indicators: unemployment_rate, gdp_growth, inflation_rate, housing_starts, manufacturing_index, consumer_confidence, wage_growth, labor_force_participation, trade_balance, industrial_production

**B. Abstracted Public Discourse Trends**
- Topic-level frequency and sentiment deltas only
- No raw text, accounts, platforms, or identifiers
- Time resolution no finer than hourly

**C. Institutional / Policy Indicators**
- Public policy, regulatory, or institutional posture changes
- Metadata only (no document storage)
- Allowed indicators: policy_announcement, regulatory_change, legislative_status, agency_posture, compliance_update, institutional_statement

#### Governance Enforcement
All live inputs:
- Are classified by domain at ingestion
- Are subject to domain balance enforcement, velocity dampening, escalation ceilings, confidence collapse handling
- Cannot bypass convergence or Decision Confidence Gate
- Log all governance decisions

#### API Endpoints for Live Data
- `GET /api/v1/live-data/status` - Get current live data source status
- `POST /api/v1/live-data/enable` - Enable live U.S. data ingestion
- `POST /api/v1/live-data/disable` - Disable live data ingestion
- `POST /api/v1/live-data/ingest/structural-economic` - Ingest structural/economic indicator
- `POST /api/v1/live-data/ingest/discourse` - Ingest abstracted discourse trend
- `POST /api/v1/live-data/ingest/institutional` - Ingest institutional/policy indicator
- `GET /api/v1/live-data/inputs` - Get recent live data inputs
- `GET /api/v1/live-data/freshness` - Get data freshness summary

#### Labeling & Transparency
- Data freshness labels visible where context is summarized
- Provenance labels appear in "Why This Is Shown" panels
- No UI elements imply urgency or alerting

This phase is observational only. No tuning or feature expansion.

## Patent-Critical Features

### Weak-Signal Convergence Engine
- Ingests low-confidence signals from multiple domains
- Threat probability emerges from convergence, not thresholds
- No single domain can independently trigger alerts
- Multi-domain convergence required for intelligence elevation

### Intent Gradient Modeling
- Models threat evolution as a gradient, not binary state
- Four stages: Grievance Formation → Cognitive Fixation → Behavioral Acceleration → Mobilization Risk
- Tracks velocity, acceleration, and historical analogs
- Fully auditable and explainable

### Narrative Intelligence Objects (NIOs)
- AI-generated intelligence narratives for every emerging threat
- Executive-readable plain-language summaries
- Confidence levels and known unknowns
- Suggested monitoring posture (not enforcement)
- Complete reasoning chain audit trail

## Data & Privacy Constraints

AURORA is designed with strict privacy and civil liberties protections:

- **No surveillance tooling**: System does not monitor individuals
- **No identity attribution**: No personal identifiers stored or tracked
- **No raw content retention**: Only abstracted behavioral indicators
- **Jurisdictional neutrality**: Operates on lawfully obtainable, abstracted indicators
- **Trend-level intelligence only**: Not evidentiary material or investigative leads

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Package Manager**: Poetry
- **Database**: In-memory store (demo environment)
- **API**: RESTful with OpenAPI documentation

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Charts**: Recharts
- **Icons**: Lucide React

## Local Development

### Backend
```bash
cd aurora-backend
poetry install
poetry run fastapi dev app/main.py --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd aurora-frontend
npm install
npm run dev
```

Access the application at `http://localhost:5173`

## Building for Production

### Backend
```bash
cd aurora-backend
poetry build
```

### Frontend
```bash
cd aurora-frontend
npm run build
```

The production build will be in `aurora-frontend/dist/`

## API Documentation

When running locally, API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Deployed Demo

- **Frontend**: https://threat-intelligence-engine-i8cqhqgl.devinapps.com
- **Backend API**: https://app-umjbrpgo.fly.dev
- **API Docs**: https://app-umjbrpgo.fly.dev/docs

## Operational Continuity & Runtime Behavior

### State Persistence (IMPORTANT)

**Current Implementation: In-Memory Data Store**

The current AURORA implementation uses an in-memory data store for demonstration and proof-of-concept purposes. This means:

- **Context state** (relevance, confidence, intent stage): **EPHEMERAL** - resets on restart
- **Context aging / decay timestamps**: **EPHEMERAL** - resets on restart
- **Provenance labels**: **EPHEMERAL** - resets on restart
- **Audit logs**: **EPHEMERAL** - resets on restart
- **Live Data Mode (ON_US_ONLY)**: **EPHEMERAL** - resets to OFF on restart
- **Ingested live data**: **EPHEMERAL** - lost on restart

**A restart will RESET state, not resume.**

This is acceptable for demonstration, validation, and stakeholder review purposes. Production deployment would require persistent storage (database).

### Background Operation Status

The following describes the current runtime behavior:

- [ ] Live data ingestion runs continuously via background workers - **NOT IMPLEMENTED**
- [x] Live data ingestion runs only when the backend is active - **CURRENT BEHAVIOR**
- [x] Live data ingestion pauses if the service sleeps or restarts - **CURRENT BEHAVIOR**

**Current Behavior:**
- Live data ingestion is API-driven (on-demand via POST endpoints)
- No background workers or continuous polling
- Backend must be active to receive ingestion requests
- Service restart resets all state to demo defaults
- System does not require UI to be open to function (API-first design)

### Deployment Stability

- Backend service can restart without data loss: **NO** (in-memory store resets)
- Frontend redeploy does not affect backend state: **YES** (independent deployments)
- API ingestion endpoints remain governed after redeploy: **YES** (governance logic in code)
- No dependency on UI traffic for ingestion logic: **YES** (API-first design)

## Feature Freeze (v1.4.2+)

**FEATURE FREEZE IN EFFECT**

As of v1.4.2-stability-preserved, the following constraints apply:

**ALLOWED:**
- Bug fixes
- Stability improvements
- Documentation updates

**NOT ALLOWED:**
- No new features
- No tuning
- No new data sources
- No alerting or UI expansion

This freeze remains until explicitly lifted by the project owner.

## Version History

- **v1.4.2-stability-preserved** (Current): Stability and preservation release
  - All v1.4.1 features preserved
  - Documented operational continuity and runtime behavior
  - Documented state persistence (ephemeral in-memory store)
  - Documented background operation status (API-driven, no background workers)
  - Feature freeze in effect (bug fixes, stability, docs only)
  - No new features, tuning, data sources, or alerting

- **v1.4.1-live-us-data-enabled**: Complete Phase 1 + Phase 2 + Phase 3 + Phase 3.x + Phase 4 + Phase 1.4 + Phase 1.4.1 implementation
  - All v1.4 features plus:
  - Live Data Mode enabled (ON_US_ONLY)
  - Live input sources for three allowed classes (Structural/Economic, Abstracted Discourse, Institutional/Policy)
  - API endpoints for live data ingestion with governance validation
  - All inputs pass through governance enforcement at ingestion
  - Data freshness and provenance labels visible in UI
  - Observational only - no tuning or feature expansion

- **v1.4-live-data-governance**: Complete Phase 1 + Phase 2 + Phase 3 + Phase 3.x + Phase 4 + Phase 1.4 implementation
  - All v1.3 features plus:
  - Live Data Governance Mode (policy enforcement at ingestion)
  - Data Freshness & Time Semantics (freshness bands, persistence states)
  - Live-Data Fail-Safe & Dampening Controls (velocity dampening, domain balance, escalation ceilings, confidence collapse handling)
  - Provenance & Context Attribution (non-source disclosing)
  - Global Safety Rules enforcement (no alerts, no event detection, no actor modeling, U.S. only)
  - Full audit logging for all governance decisions

- **v1.3-decision-discipline**: Complete Phase 1 + Phase 2 + Phase 3 + Phase 3.x + Phase 4 implementation
  - All v1.2 features plus:
  - Decision Confidence Gate (gating mechanism for recommendations)
  - Decision Readiness Levels (DRL-0 to DRL-3)
  - Context Aging & Decay Language
  - "Why This Is Shown" Explainability Panels
  - Silent Audit Mode foundational hook (backend only)
  - Visual & UX Restraint Rules enforcement

- **v1.2-multi-context-regional-intelligence**: Complete Phase 1 + Phase 2 + Phase 3 + Phase 4 implementation
  - All v1.1 features plus:
  - Multi-Context Per Region (Context Stack Model with 3-5 optimal, max 8 contexts)
  - Context Prioritization based on intent stage, persistence, decision impact, confidence
  - Region-as-Context Map with Layered Confidence Bands (Core/Adjacent/Peripheral)
  - Multi-Region Handling with Regional Context Selector
  - Safety & Governance Constraints (no merging, no compound threats, no global views)

- **v1.1-decision-advantage**: Complete Phase 1 + Phase 2 + Phase 3 implementation
  - All v1.0 features plus:
  - Decision Pathway Intelligence (8 advisory pathways)
  - Impact Forecasting (6 system-level impact domains)
  - Authority-Aware Recommendations (10 leadership domains)
  - Decision Advantage Summary with confidence-weighted priority
  - Probabilistic Threat Class Alignment (8 analytic categories)

- **v1.0-stable**: Complete Phase 1 + Phase 2 implementation
  - Context-Aware Color Intelligence
  - Region-Aware Intelligence
  - Escalation Pathway Modeling
  - Authorized Drill-Down Logic
  - Probabilistic Threat Class Alignment
  - Jurisdiction Context (90 countries)
  - Full audit trail and access logging

- **v1.0-stable-context-aware**: Phase 1 baseline
  - Context-Aware Color Intelligence
  - Intent Stage color mapping
  - Probability intensity scaling
  - WCAG AA compliance

## License

Proprietary - Global 3 Technology & Intelligence (G3TI)

## Contact

For inquiries regarding AURORA, please contact Global 3 Technology & Intelligence (G3TI).

---

*This system is designed to be something that a federal agency cannot easily replicate internally, legal counsel can defend, procurement officers can justify, analysts can trust, and executives can understand in 60 seconds.*
