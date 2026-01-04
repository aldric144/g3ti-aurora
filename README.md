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

## Version History

- **v1.1-decision-advantage** (Current): Complete Phase 1 + Phase 2 + Phase 3 implementation
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
