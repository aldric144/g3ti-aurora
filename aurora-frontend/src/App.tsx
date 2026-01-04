import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tooltip as UITooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertTriangle, TrendingUp, TrendingDown, Minus, Shield, Activity, FileText, MessageSquare, Clock, Target, Brain, Eye, MapPin, Route, Lock, Layers, ChevronUp, ChevronDown, Info } from 'lucide-react';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ThreatSummary {
  id: string;
  name: string;
  category: string;
  current_probability: number;
  intent_stage: string;
  monitoring_posture: string;
  signal_count: number;
  updated_at: string;
}

interface Signal {
  id: string;
  domain: string;
  signal_type: string;
  source_description: string;
  raw_confidence: number;
  weight: number;
  reasoning: string;
  timestamp: string;
}

interface IntentGradient {
  current_stage: string;
  stage_confidence: number;
  velocity: number;
  acceleration: number;
  time_in_stage: number;
  stage_1_score: number;
  stage_2_score: number;
  stage_3_score: number;
  stage_4_score: number;
}

interface ProbabilityCurve {
  current_probability: number;
  confidence_bounds: { lower: number; upper: number };
  trend: string;
  trend_velocity: number;
  convergence_score: number;
  contributing_signals: number;
  domain_coverage: Record<string, number>;
}

interface HistoricalAnalog {
  name: string;
  description: string;
  similarity_score: number;
  outcome: string;
  lessons_learned: string;
  date_range: string;
}

interface NIO {
  id: string;
  executive_summary: string;
  why_it_matters: string;
  converged_signals: string[];
  signal_narrative: string;
  confidence_level: number;
  confidence_explanation: string;
  known_unknowns: string[];
  assumptions: string[];
  monitoring_posture: string;
  posture_rationale: string;
  recommended_actions: string[];
  reasoning_chain: string[];
  version: number;
  generated_at: string;
}

interface RegionContext {
  primary_region: string;
  secondary_regions: string[];
  region_type: string;
  attribution_confidence: number;
  attribution_rationale: string;
  population_scale: string;
  economic_profile: string;
  granularity_level: string;
  policy_notes: string[];
}

interface EscalationPathwayStage {
  stage_name: string;
  stage_description: string;
  typical_indicators: string[];
  typical_duration_hours: number[];
  transition_triggers: string[];
}

interface EscalationPathway {
  pathway_id: string;
  pathway_name: string;
  pathway_description: string;
  stages: EscalationPathwayStage[];
  current_stage_index: number;
  stage_entry_time: string;
  progression_probability: number;
  regression_probability: number;
  projected_progression_window: number[];
  projection_confidence: number;
  historical_pattern_matches: string[];
  policy_notes: string[];
}

interface ThreatClassAlignment {
  class_category: string;
  alignment_score: number;
  confidence: number;
  primary_contributing_domains: string[];
  intent_stage_influence: number;
  escalation_pathway_influence: number;
  velocity_influence: number;
  rationale: string;
}

interface ThreatClassAlignmentResult {
  threat_id: string;
  alignments: ThreatClassAlignment[];
  top_alignment: string | null;
  alignment_diversity: number;
  intent_stage_at_computation: string;
  escalation_stage_at_computation: number;
  last_updated: string;
  disclaimer: string;
  policy_notes: string[];
}

interface DecisionPathway {
  pathway_category: string;
  relevance: string;
  relevance_score: number;
  advisory_summary: string;
  suggested_considerations: string[];
  proportionality_note: string;
  contributing_factors: string[];
  confidence: number;
}

interface DecisionPathwayIntelligence {
  threat_id: string;
  pathways: DecisionPathway[];
  primary_pathway: string | null;
  overall_advisory_posture: string;
  proportionality_assessment: string;
  last_updated: string;
  disclaimer: string;
  policy_notes: string[];
}

interface ImpactProjection {
  domain: string;
  current_assessment: string;
  projected_trajectory: string;
  impact_severity: string;
  impact_severity_score: number;
  time_horizon_hours: number[];
  confidence: number;
  confidence_band: number[];
  key_assumptions: string[];
  mitigating_factors: string[];
}

interface ImpactForecast {
  threat_id: string;
  projections: ImpactProjection[];
  overall_impact_assessment: string;
  primary_concern_domain: string | null;
  aggregate_severity_score: number;
  projection_time_horizon: string;
  last_updated: string;
  disclaimer: string;
  policy_notes: string[];
}

interface AuthorityRecommendation {
  authority_domain: string;
  relevance_score: number;
  positioning_rationale: string;
  suggested_awareness_areas: string[];
  coordination_considerations: string[];
  context_applicability: string[];
  confidence: number;
}

interface AuthorityAwareRecommendations {
  threat_id: string;
  recommendations: AuthorityRecommendation[];
  primary_authority_domain: string | null;
  coordination_summary: string;
  context_applicability: string;
  last_updated: string;
  disclaimer: string;
  policy_notes: string[];
}

interface DecisionAdvantageLayer {
  threat_id: string;
  decision_pathways: DecisionPathwayIntelligence | null;
  impact_forecast: ImpactForecast | null;
  authority_recommendations: AuthorityAwareRecommendations | null;
  overall_decision_posture: string;
  confidence_weighted_priority: number;
  last_updated: string;
  master_disclaimer: string;
  policy_compliance: string[];
}

interface ThreatDetail {
  id: string;
  name: string;
  description: string;
  category: string;
  status: string;
  signals: Signal[];
  probability_curve: ProbabilityCurve;
  intent_gradient: IntentGradient;
  historical_analogs: HistoricalAnalog[];
  current_nio: NIO | null;
  region_context: RegionContext | null;
  escalation_pathway: EscalationPathway | null;
  threat_class_alignment: ThreatClassAlignmentResult | null;
  decision_advantage_layer: DecisionAdvantageLayer | null;
  created_at: string;
  updated_at: string;
}

interface SystemStatus {
  status: string;
  version: string;
  statistics: {
    total_threats: number;
    active_threats: number;
    total_signals: number;
    total_nios: number;
    audit_entries: number;
    feedback_entries: number;
  };
  alerts: {
    critical_posture_count: number;
    heightened_posture_count: number;
  };
}

interface JurisdictionSummary {
  code: string;
  name: string;
  region: string;
  is_synthetic: boolean;
  is_operational: boolean;
}

interface JurisdictionListResponse {
  jurisdictions: JurisdictionSummary[];
  total: number;
  current_jurisdiction: string;
}

interface RegionConfidenceBand {
  band_type: string;
  region_name: string;
  relevance_score: number;
  description: string;
  visual_style: string;
}

interface LayeredRegionConfidenceBands {
  region_id: string;
  region_name: string;
  core_band: RegionConfidenceBand;
  adjacent_band: RegionConfidenceBand | null;
  peripheral_band: RegionConfidenceBand | null;
  overall_confidence: number;
  policy_notes: string[];
}

interface DecisionContext {
  context_id: string;
  context_name: string;
  context_description: string;
  threat_id: string;
  intent_stage: string;
  intent_stage_confidence: number;
  confidence_score: number;
  persistence_score: number;
  decision_impact_score: number;
  priority: string;
  priority_score: number;
  is_expanded: boolean;
  signal_count: number;
  created_at: string;
  last_updated: string;
  policy_notes: string[];
}

interface ContextStackSummary {
  summarized_count: number;
  average_confidence: number;
  summary_note: string;
}

interface RegionContextStack {
  region_id: string;
  region_name: string;
  contexts: DecisionContext[];
  displayed_count: number;
  total_count: number;
  summarized_contexts: ContextStackSummary | null;
  expanded_context_id: string | null;
  confidence_bands: LayeredRegionConfidenceBands | null;
  last_updated: string;
  policy_notes: string[];
}

interface RegionSummary {
  region_id: string;
  region_name: string;
  context_count: number;
  highest_intent_stage: string | null;
  overall_confidence: number;
  is_active: boolean;
}

interface MultiRegionIntelligence {
  regions: Record<string, RegionContextStack>;
  active_region_id: string | null;
  total_regions: number;
  total_contexts: number;
  last_updated: string;
  master_disclaimer: string;
  safety_constraints: string[];
}

interface MultiRegionIntelligenceResponse {
  multi_region_intelligence: MultiRegionIntelligence | null;
  active_region: RegionContextStack | null;
  region_summaries: RegionSummary[];
  safety_constraints: string[];
}

interface ExplainabilityFactor {
  factor_name: string;
  factor_description: string;
  contributed: boolean;
  weight: number;
}

interface ExplainabilityPanel {
  panel_type: string;
  panel_title: string;
  triggering_factors: ExplainabilityFactor[];
  non_triggering_factors: ExplainabilityFactor[];
  explicit_non_claims: string[];
  summary: string;
  confidence_note: string;
  audit_reference: string | null;
}

interface DecisionConfidenceGate {
  gate_status: string;
  signal_diversity_score: number;
  persistence_score: number;
  cross_domain_convergence: number;
  data_confidence: number;
  composite_confidence: number;
  threshold_met: boolean;
  limiting_message: string | null;
  allowed_outputs: string[];
  restricted_outputs: string[];
  gate_rationale: string;
  evaluated_at: string;
  audit_logged: boolean;
}

interface ContextAging {
  context_id: string;
  aging_status: string;
  relevance_trend: string;
  signal_persistence_change: number;
  velocity_trend: string;
  aging_message: string;
  days_since_last_signal: number;
  decay_rate: number;
  removal_warning: boolean;
  removal_explanation: string | null;
  last_evaluated: string;
  audit_logged: boolean;
}

interface DRLDetails {
  name: string;
  description: string;
  posture: string;
  action_guidance: string;
}

interface DecisionDisciplineLayer {
  threat_id: string;
  context_id: string | null;
  confidence_gate: DecisionConfidenceGate;
  decision_readiness_level: string;
  drl_details: DRLDetails;
  context_aging: ContextAging | null;
  explainability_panels: ExplainabilityPanel[];
  overall_discipline_posture: string;
  restraint_indicators: string[];
  last_updated: string;
  master_disclaimer: string;
  governance_compliance: string[];
}

interface DecisionDisciplineResponse {
  decision_discipline: DecisionDisciplineLayer | null;
  confidence_gate: DecisionConfidenceGate | null;
  drl: string | null;
  drl_details: DRLDetails | null;
  context_aging: ContextAging | null;
  explainability_panels: ExplainabilityPanel[];
  governance_compliance: string[];
}

const STAGE_LABELS: Record<string, string> = {
  grievance_formation: 'Stage 1: Grievance Formation',
  cognitive_fixation: 'Stage 2: Cognitive Fixation',
  behavioral_acceleration: 'Stage 3: Behavioral Acceleration',
  mobilization_risk: 'Stage 4: Mobilization Risk',
};

const INTENT_STAGE_COLORS: Record<string, { bg: string; text: string; border: string; accent: string }> = {
  grievance_formation: { bg: 'bg-[#4F81BD]/10', text: 'text-[#4F81BD]', border: 'border-[#4F81BD]/30', accent: '#4F81BD' },
  cognitive_fixation: { bg: 'bg-[#F4B400]/10', text: 'text-[#F4B400]', border: 'border-[#F4B400]/30', accent: '#F4B400' },
  behavioral_acceleration: { bg: 'bg-[#F28C28]/10', text: 'text-[#F28C28]', border: 'border-[#F28C28]/30', accent: '#F28C28' },
  mobilization_risk: { bg: 'bg-[#E5533D]/10', text: 'text-[#E5533D]', border: 'border-[#E5533D]/30', accent: '#E5533D' },
};

const POSTURE_COLORS: Record<string, string> = {
  routine: 'bg-[#4F81BD]/15 text-[#4F81BD] border border-[#4F81BD]/50 font-medium',
  elevated: 'bg-[#F4B400]/15 text-[#F4B400] border border-[#F4B400]/50 font-medium',
  heightened: 'bg-[#F28C28]/15 text-[#F28C28] border border-[#F28C28]/50 font-medium',
  critical: 'bg-[#E5533D]/15 text-[#E5533D] border border-[#E5533D]/50 font-medium',
};

const DOMAIN_LABELS: Record<string, string> = {
  social_discourse: 'Social Discourse',
  behavioral_trend: 'Behavioral Trend',
  environmental_stressor: 'Environmental Stressor',
};

const DOMAIN_COLORS: Record<string, { bg: string; text: string; border: string; accent: string }> = {
  social_discourse: { bg: 'bg-[#3EC1C9]/10', text: 'text-[#3EC1C9]', border: 'border-[#3EC1C9]/30', accent: '#3EC1C9' },
  behavioral_trend: { bg: 'bg-[#4F81BD]/10', text: 'text-[#4F81BD]', border: 'border-[#4F81BD]/30', accent: '#4F81BD' },
  environmental_stressor: { bg: 'bg-[#7A8CA3]/10', text: 'text-[#7A8CA3]', border: 'border-[#7A8CA3]/30', accent: '#7A8CA3' },
};

const THREAT_CLASS_LABELS: Record<string, string> = {
  socioeconomic_instability: 'Socioeconomic Instability',
  civil_unrest_protest: 'Civil Unrest / Protest Escalation',
  ideological_mobilization: 'Ideological Mobilization',
  lone_actor_grievance: 'Lone-Actor Grievance Risk',
  insider_grievance_disruption: 'Insider / Grievance-Based Disruption',
  cyber_physical_convergence: 'Cyber-Physical Convergence Risk',
  infrastructure_disruption: 'Infrastructure Disruption Risk',
  coordinated_disinformation: 'Coordinated Disinformation Amplification',
};

const DECISION_PATHWAY_LABELS: Record<string, string> = {
  economic_engagement: 'Economic Engagement',
  community_outreach: 'Community Outreach',
  communications_strategy: 'Communications Strategy',
  stakeholder_coordination: 'Stakeholder Coordination',
  resource_positioning: 'Resource Positioning',
  monitoring_adjustment: 'Monitoring Adjustment',
  institutional_resilience: 'Institutional Resilience',
  interagency_liaison: 'Interagency Liaison',
};

const IMPACT_DOMAIN_LABELS: Record<string, string> = {
  institutional_trust: 'Institutional Trust',
  community_stability: 'Community Stability',
  operational_continuity: 'Operational Continuity',
  economic_resilience: 'Economic Resilience',
  social_cohesion: 'Social Cohesion',
  infrastructure_integrity: 'Infrastructure Integrity',
};

const AUTHORITY_DOMAIN_LABELS: Record<string, string> = {
  executive_leadership: 'Executive Leadership',
  operations_management: 'Operations Management',
  communications_public_affairs: 'Communications / Public Affairs',
  community_relations: 'Community Relations',
  risk_management: 'Risk Management',
  legal_compliance: 'Legal / Compliance',
  human_resources: 'Human Resources',
  external_affairs: 'External Affairs',
  strategic_planning: 'Strategic Planning',
  interagency_coordination: 'Interagency Coordination',
};

const RELEVANCE_COLORS: Record<string, string> = {
  high: 'bg-[#4F81BD]/20 text-[#4F81BD] border-[#4F81BD]/40',
  moderate: 'bg-[#F4B400]/20 text-[#F4B400] border-[#F4B400]/40',
  low: 'bg-[#7A8CA3]/20 text-[#7A8CA3] border-[#7A8CA3]/40',
};

const getConfidenceOpacity= (confidence: number): string => {
  if (confidence >= 0.7) return 'opacity-100';
  if (confidence >= 0.4) return 'opacity-80';
  return 'opacity-60';
};

const getProbabilityIntensity = (probability: number): string => {
  if (probability >= 70) return 'font-bold';
  if (probability >= 40) return 'font-semibold';
  return 'font-medium';
};

const getVelocityStyle = (velocity: number): string => {
  if (velocity > 0) return 'underline decoration-2';
  if (velocity < 0) return 'opacity-70';
  return '';
};

function App() {
  const [threats, setThreats] = useState<ThreatSummary[]>([]);
  const [selectedThreat, setSelectedThreat] = useState<ThreatDetail | null>(null);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [feedbackType, setFeedbackType] = useState('');
  const [feedbackRationale, setFeedbackRationale] = useState('');
  const [historyData, setHistoryData] = useState<Array<{ timestamp: string; probability: number }>>([]);
  const [jurisdictions, setJurisdictions] = useState<JurisdictionSummary[]>([]);
  const [currentJurisdiction, setCurrentJurisdiction] = useState<string>('US');
  const [multiRegionIntelligence, setMultiRegionIntelligence] = useState<MultiRegionIntelligence | null>(null);
  const [activeRegion, setActiveRegion] = useState<RegionContextStack | null>(null);
  const [regionSummaries, setRegionSummaries] = useState<RegionSummary[]>([]);
  const [decisionDiscipline, setDecisionDiscipline] = useState<DecisionDisciplineResponse | null>(null);
  const [expandedExplainability, setExpandedExplainability] = useState<string | null>(null);

  useEffect(() => {
    fetchThreats();
    fetchSystemStatus();
    fetchJurisdictions();
    fetchMultiRegionIntelligence();
  }, []);

  useEffect(() => {
    if (selectedThreat) {
      fetchThreatHistory(selectedThreat.id);
      fetchDecisionDiscipline(selectedThreat.id);
    }
  }, [selectedThreat?.id]);

  const fetchThreats = async () => {
    try {
      const response = await fetch(`${API_URL}/api/v1/threats`);
      const data = await response.json();
      setThreats(data.threats);
      if (data.threats.length > 0 && !selectedThreat) {
        fetchThreatDetail(data.threats[0].id);
      }
    } catch (error) {
      console.error('Failed to fetch threats:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchThreatDetail = async (threatId: string) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/threats/${threatId}`);
      const data = await response.json();
      setSelectedThreat(data);
    } catch (error) {
      console.error('Failed to fetch threat detail:', error);
    }
  };

  const fetchThreatHistory = async (threatId: string) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/threats/${threatId}/history`);
      const data = await response.json();
      setHistoryData(data.history.map((h: { timestamp: string; probability: number }) => ({
        timestamp: new Date(h.timestamp).toLocaleDateString(),
        probability: h.probability,
      })));
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/v1/system/status`);
      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error('Failed to fetch system status:', error);
    }
  };

  const fetchJurisdictions = async () => {
    try {
      const response = await fetch(`${API_URL}/api/v1/jurisdictions`);
      const data: JurisdictionListResponse = await response.json();
      setJurisdictions(data.jurisdictions);
      setCurrentJurisdiction(data.current_jurisdiction);
    } catch (error) {
      console.error('Failed to fetch jurisdictions:', error);
    }
  };

  const fetchMultiRegionIntelligence = async () => {
    try {
      const response = await fetch(`${API_URL}/api/v1/regions`);
      const data: MultiRegionIntelligenceResponse = await response.json();
      setMultiRegionIntelligence(data.multi_region_intelligence);
      setActiveRegion(data.active_region);
      setRegionSummaries(data.region_summaries);
    } catch (error) {
      console.error('Failed to fetch multi-region intelligence:', error);
    }
  };

  const fetchDecisionDiscipline = async (threatId: string) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/decision-discipline/${threatId}`);
      const data: DecisionDisciplineResponse = await response.json();
      setDecisionDiscipline(data);
    } catch (error) {
      console.error('Failed to fetch decision discipline:', error);
    }
  };

  const handleSetActiveRegion = async (regionId: string) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/regions/active`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ region_id: regionId }),
      });
      if (response.ok) {
        const data: RegionContextStack = await response.json();
        setActiveRegion(data);
        setRegionSummaries(prev => prev.map(r => ({
          ...r,
          is_active: r.region_id === regionId
        })));
      }
    } catch (error) {
      console.error('Failed to set active region:', error);
    }
  };

  const handleExpandContext = async (regionId: string, contextId: string) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/regions/${regionId}/expand`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ region_id: regionId, context_id: contextId }),
      });
      if (response.ok) {
        if (activeRegion) {
          setActiveRegion({
            ...activeRegion,
            expanded_context_id: contextId,
            contexts: activeRegion.contexts.map(c => ({
              ...c,
              is_expanded: c.context_id === contextId
            }))
          });
        }
      }
    } catch (error) {
      console.error('Failed to expand context:', error);
    }
  };

  const handleJurisdictionChange = async (code: string) => {
    try {
      const response = await fetch(`${API_URL}/api/v1/jurisdictions/current`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });
      if (response.ok) {
        setCurrentJurisdiction(code);
        if (selectedThreat) {
          regenerateNIO();
        }
      }
    } catch (error) {
      console.error('Failed to set jurisdiction:', error);
    }
  };

  const regenerateNIO = async () => {
    if (!selectedThreat) return;
    try {
      const response = await fetch(`${API_URL}/api/v1/threats/${selectedThreat.id}/narrative/regenerate`, {
        method: 'POST',
      });
      const data = await response.json();
      setSelectedThreat({ ...selectedThreat, current_nio: data });
    } catch (error) {
      console.error('Failed to regenerate NIO:', error);
    }
  };

  const submitFeedback = async () => {
    if (!selectedThreat || !feedbackType || !feedbackRationale) return;
    try {
      await fetch(`${API_URL}/api/v1/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          analyst_id: 'analyst_001',
          threat_id: selectedThreat.id,
          feedback_type: feedbackType,
          rationale: feedbackRationale,
        }),
      });
      setFeedbackType('');
      setFeedbackRationale('');
      alert('Feedback submitted successfully');
    } catch (error) {
      console.error('Failed to submit feedback:', error);
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing':
        return <TrendingUp className="h-4 w-4 text-[#E5533D]" />;
      case 'decreasing':
        return <TrendingDown className="h-4 w-4 text-[#4F81BD]" />;
      default:
        return <Minus className="h-4 w-4 text-[#7A8CA3]" />;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B1220] flex items-center justify-center">
        <div className="text-white text-xl">Loading AURORA Intelligence Platform...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B1220] text-[#C9D4E3]">
      <div className="bg-[#F4B400]/10 border-b border-[#F4B400]/30 py-2 px-4">
        <div className="container mx-auto">
          <div className="flex items-center justify-center gap-2 text-[#F4B400] text-sm">
            <AlertTriangle className="h-4 w-4" />
            <span className="font-medium">DEMONSTRATION ENVIRONMENT</span>
            <span className="text-[#F4B400]/70">|</span>
            <span className="text-[#C9D4E3]">Pre-patent technology preview. Synthetic data only. Not for operational use, real-world monitoring, or enforcement.</span>
          </div>
        </div>
      </div>
      <header className="border-b border-[#16233A] bg-[#121C2D]/90 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Shield className="h-8 w-8 text-[#4F81BD]" />
              <div>
                <h1 className="text-xl font-bold text-white">AURORA</h1>
                <p className="text-xs text-[#9FB0C7]">Pre-Incident Decision Intelligence Simulation</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <span className="text-xs text-[#9FB0C7]">Jurisdiction Context:</span>
                <Select value={currentJurisdiction} onValueChange={handleJurisdictionChange}>
                  <SelectTrigger className="w-56 h-8 bg-[#16233A] border-[#16233A] text-sm text-[#C9D4E3]">
                    <SelectValue placeholder="Select jurisdiction" />
                  </SelectTrigger>
                  <SelectContent className="bg-[#16233A] border-[#16233A] max-h-80">
                    {jurisdictions.filter(j => j.is_operational).map((j) => (
                      <SelectItem key={j.code} value={j.code} className="text-sm text-[#C9D4E3]">
                        <div className="flex items-center gap-2">
                          <span className="w-2 h-2 rounded-full bg-[#4F81BD]"></span>
                          <span>{j.name}</span>
                          <span className="text-[10px] text-[#4F81BD]">(Operational)</span>
                        </div>
                      </SelectItem>
                    ))}
                    <div className="px-2 py-1 text-xs font-semibold text-[#F4B400] bg-[#121C2D] border-t border-[#16233A]">
                      Synthetic Demo Contexts
                    </div>
                    {Object.entries(
                      jurisdictions.filter(j => j.is_synthetic).reduce((acc, j) => {
                        if (!acc[j.region]) acc[j.region] = [];
                        acc[j.region].push(j);
                        return acc;
                      }, {} as Record<string, JurisdictionSummary[]>)
                    ).map(([region, items]) => (
                      <div key={region}>
                        <div className="px-2 py-1 text-xs text-[#9FB0C7] bg-[#121C2D]/50">{region}</div>
                        {items.map((j) => (
                          <SelectItem key={j.code} value={j.code} className="text-sm text-[#9FB0C7]">
                            <div className="flex items-center gap-2">
                              <span className="w-2 h-2 rounded-full bg-[#F4B400]/50"></span>
                              <span>{j.name}</span>
                              <span className="text-[10px] text-[#F4B400]/70">(Synthetic)</span>
                            </div>
                          </SelectItem>
                        ))}
                      </div>
                    ))}
                  </SelectContent>
                </Select>
                {jurisdictions.find(j => j.code === currentJurisdiction)?.is_synthetic && (
                  <Badge className="bg-[#F4B400]/10 text-[#F4B400] border-[#F4B400]/30 text-[10px]">
                    Synthetic Demo
                  </Badge>
                )}
              </div>
              {systemStatus && (
                <div className="flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <Activity className="h-4 w-4 text-[#4F81BD]" />
                    <span className="text-[#C9D4E3]">{systemStatus.statistics.active_threats} Active Threats</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Target className="h-4 w-4 text-[#3EC1C9]" />
                    <span className="text-[#C9D4E3]">{systemStatus.statistics.total_signals} Signals</span>
                  </div>
                  {systemStatus.alerts.critical_posture_count > 0 && (
                    <Badge className="bg-[#E5533D]/10 text-[#E5533D] border-[#E5533D]/30">
                      {systemStatus.alerts.critical_posture_count} Critical
                    </Badge>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {jurisdictions.find(j => j.code === currentJurisdiction)?.is_synthetic && (
        <div className="bg-[#F4B400]/5 border-b border-[#F4B400]/20 py-3 px-4">
          <div className="container mx-auto">
            <Alert className="bg-[#F4B400]/10 border-[#F4B400]/30">
              <AlertTriangle className="h-4 w-4 text-[#F4B400]" />
              <AlertTitle className="text-[#F4B400] text-sm font-medium">Synthetic Demonstration Context Active</AlertTitle>
              <AlertDescription className="text-[#C9D4E3] text-xs mt-1">
                <strong>{jurisdictions.find(j => j.code === currentJurisdiction)?.name}</strong> uses synthetic, non-representative seed profiles for demonstration and architectural validation only. 
                This does NOT represent real-world intelligence, monitoring, or coverage. No foreign actor modeling, population-level inference, threat probabilities, or event prediction is performed outside the United States.
              </AlertDescription>
            </Alert>
          </div>
        </div>
      )}

      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-3">
            <Card className="bg-[#121C2D] border-[#16233A]">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium text-[#C9D4E3]">Active Threats</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <ScrollArea className="h-[calc(100vh-220px)]">
                  {threats.map((threat) => {
                    const stageColors = INTENT_STAGE_COLORS[threat.intent_stage] || INTENT_STAGE_COLORS.grievance_formation;
                    return (
                    <div
                      key={threat.id}
                      onClick={() => fetchThreatDetail(threat.id)}
                      className={`p-4 border-b border-[#16233A] cursor-pointer hover:bg-[#16233A]/50 transition-colors ${
                        selectedThreat?.id === threat.id ? 'bg-[#16233A]' : ''
                      }`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-medium text-sm text-white truncate pr-2">{threat.name}</h3>
                        <Badge className={`text-xs ${POSTURE_COLORS[threat.monitoring_posture]}`}>
                          {threat.monitoring_posture}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-2 mb-2">
                        <div className="flex-1">
                          <Progress value={threat.current_probability} className="h-2" style={{ '--progress-color': stageColors.accent } as React.CSSProperties} />
                        </div>
                        <span className={`text-xs font-mono ${stageColors.text} ${getProbabilityIntensity(threat.current_probability)}`}>
                          {threat.current_probability.toFixed(1)}%
                        </span>
                      </div>
                      <div className="flex items-center justify-between text-xs text-[#9FB0C7]">
                        <span className={stageColors.text}>{STAGE_LABELS[threat.intent_stage]?.split(':')[0]}</span>
                        <span>{threat.signal_count} signals</span>
                      </div>
                    </div>
                    );
                  })}
                </ScrollArea>
              </CardContent>
            </Card>
          </div>

          <div className="col-span-9">
            {selectedThreat ? (
              <div className="space-y-6">
                {(() => {
                  const currentStageColors = INTENT_STAGE_COLORS[selectedThreat.intent_gradient.current_stage] || INTENT_STAGE_COLORS.grievance_formation;
                  const confidenceOpacity = getConfidenceOpacity(selectedThreat.intent_gradient.stage_confidence);
                  const velocityStyle = getVelocityStyle(selectedThreat.intent_gradient.velocity);
                  const probabilityIntensity = getProbabilityIntensity(selectedThreat.probability_curve.current_probability);
                  return (
                <Card className={`bg-[#121C2D] border-[#16233A] border-l-4`} style={{ borderLeftColor: currentStageColors.accent }}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div>
                        <CardTitle className="text-xl text-white">{selectedThreat.name}</CardTitle>
                        <CardDescription className="mt-1 text-[#9FB0C7]">{selectedThreat.description}</CardDescription>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge className={POSTURE_COLORS[selectedThreat.current_nio?.monitoring_posture || 'routine']}>
                          {selectedThreat.current_nio?.monitoring_posture || 'routine'} monitoring
                        </Badge>
                        <Badge variant="outline" className="border-[#16233A] text-[#9FB0C7]">
                          {selectedThreat.category}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-4 gap-4">
                      <div className="bg-[#16233A] rounded-lg p-4">
                        <div className="flex items-center gap-2 mb-2">
                          <AlertTriangle className={`h-4 w-4 ${currentStageColors.text}`} />
                          <span className="text-xs text-[#9FB0C7]">Threat Probability</span>
                        </div>
                        <div className="flex items-baseline gap-2">
                          <span className={`text-3xl text-white ${probabilityIntensity} ${velocityStyle}`}>
                            {selectedThreat.probability_curve.current_probability.toFixed(1)}%
                          </span>
                          {getTrendIcon(selectedThreat.probability_curve.trend)}
                        </div>
                        <div className="text-xs text-[#9FB0C7] mt-1">
                          Bounds: {selectedThreat.probability_curve.confidence_bounds.lower.toFixed(1)}% - {selectedThreat.probability_curve.confidence_bounds.upper.toFixed(1)}%
                        </div>
                      </div>
                      <div className={`bg-[#16233A] rounded-lg p-4 ${confidenceOpacity}`}>
                        <div className="flex items-center gap-2 mb-2">
                          <Brain className={`h-4 w-4 ${currentStageColors.text}`} />
                          <span className="text-xs text-[#9FB0C7]">Intent Stage</span>
                        </div>
                        <div className={`text-lg font-semibold ${currentStageColors.text}`}>
                          {STAGE_LABELS[selectedThreat.intent_gradient.current_stage]?.split(':')[1]?.trim()}
                        </div>
                        <div className="text-xs text-[#9FB0C7] mt-1">
                          Confidence: {(selectedThreat.intent_gradient.stage_confidence * 100).toFixed(0)}%
                        </div>
                      </div>
                      <div className="bg-[#16233A] rounded-lg p-4">
                        <div className="flex items-center gap-2 mb-2">
                          <Activity className="h-4 w-4 text-[#3EC1C9]" />
                          <span className="text-xs text-[#9FB0C7]">Convergence Score</span>
                        </div>
                        <div className="text-3xl font-bold text-white">
                          {(selectedThreat.probability_curve.convergence_score * 100).toFixed(0)}%
                        </div>
                        <div className="text-xs text-[#9FB0C7] mt-1">
                          {selectedThreat.probability_curve.contributing_signals} signals converging
                        </div>
                      </div>
                      <div className="bg-[#16233A] rounded-lg p-4">
                        <div className="flex items-center gap-2 mb-2">
                          <TrendingUp className={`h-4 w-4 ${selectedThreat.intent_gradient.velocity > 0 ? currentStageColors.text : 'text-[#7A8CA3]'}`} />
                          <span className="text-xs text-[#9FB0C7]">Escalation Velocity</span>
                        </div>
                        <div className={`text-3xl font-bold text-white ${velocityStyle}`}>
                          {selectedThreat.intent_gradient.velocity > 0 ? '+' : ''}{(selectedThreat.intent_gradient.velocity * 100).toFixed(1)}%
                        </div>
                        <div className="text-xs text-[#9FB0C7] mt-1">
                          {selectedThreat.intent_gradient.velocity > 0 ? 'Escalating' : selectedThreat.intent_gradient.velocity < 0 ? 'De-escalating' : 'Stable'}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
                  );
                })()}

                <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
                  <TabsList className="bg-[#16233A] border-[#16233A]">
                    <TabsTrigger value="overview" className="data-[state=active]:bg-[#121C2D] text-[#C9D4E3]">
                      <FileText className="h-4 w-4 mr-2" />
                      Intelligence Narrative
                    </TabsTrigger>
                    <TabsTrigger value="situational" className="data-[state=active]:bg-[#121C2D] text-[#C9D4E3]">
                      <MapPin className="h-4 w-4 mr-2" />
                      Situational Awareness
                    </TabsTrigger>
                    <TabsTrigger value="signals" className="data-[state=active]:bg-[#121C2D] text-[#C9D4E3]">
                      <Target className="h-4 w-4 mr-2" />
                      Signal Analysis
                    </TabsTrigger>
                    <TabsTrigger value="gradient" className="data-[state=active]:bg-[#121C2D] text-[#C9D4E3]">
                      <Brain className="h-4 w-4 mr-2" />
                      Intent Gradient
                    </TabsTrigger>
                    <TabsTrigger value="feedback" className="data-[state=active]:bg-[#121C2D] text-[#C9D4E3]">
                      <MessageSquare className="h-4 w-4 mr-2" />
                      Analyst Feedback
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="overview" className="space-y-4">
                    {selectedThreat.current_nio ? (
                      <>
                        <Card className="bg-[#121C2D] border-[#16233A]">
                          <CardHeader>
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-2">
                                <Eye className="h-5 w-5 text-[#3EC1C9]" />
                                <CardTitle className="text-lg text-white">Executive Summary</CardTitle>
                              </div>
                              <div className="flex items-center gap-2">
                                <span className="text-xs text-[#9FB0C7]">
                                  v{selectedThreat.current_nio.version} | Generated {formatDate(selectedThreat.current_nio.generated_at)}
                                </span>
                                <Button size="sm" variant="outline" onClick={regenerateNIO} className="border-[#16233A] text-[#C9D4E3] hover:bg-[#16233A]">
                                  Regenerate
                                </Button>
                              </div>
                            </div>
                          </CardHeader>
                          <CardContent className="space-y-4">
                            <p className="text-[#D8E2EF] leading-7 text-sm">
                              {selectedThreat.current_nio.executive_summary}
                            </p>
                            <Separator className="bg-[#16233A]" />
                            <div>
                              <h4 className="font-semibold text-white mb-2">Why This Matters</h4>
                              <p className="text-[#D8E2EF] leading-7 text-sm">
                                {selectedThreat.current_nio.why_it_matters}
                              </p>
                            </div>
                          </CardContent>
                        </Card>

                        <div className="grid grid-cols-2 gap-4">
                          <Card className="bg-[#121C2D] border-[#16233A]">
                            <CardHeader>
                              <CardTitle className="text-sm text-white">Converged Signals</CardTitle>
                            </CardHeader>
                            <CardContent>
                              <ul className="space-y-2">
                                {selectedThreat.current_nio.converged_signals.map((signal, idx) => (
                                  <li key={idx} className="flex items-start gap-2 text-sm text-[#C9D4E3]">
                                    <span className="text-[#3EC1C9] mt-1">-</span>
                                    {signal}
                                  </li>
                                ))}
                              </ul>
                            </CardContent>
                          </Card>

                          <Card className="bg-[#121C2D] border-[#16233A]">
                            <CardHeader>
                              <CardTitle className="text-sm text-white">Known Unknowns</CardTitle>
                            </CardHeader>
                            <CardContent>
                              <ul className="space-y-2">
                                {selectedThreat.current_nio.known_unknowns.map((unknown, idx) => (
                                  <li key={idx} className="flex items-start gap-2 text-sm text-[#C9D4E3]">
                                    <span className="text-[#F4B400] mt-1">?</span>
                                    {unknown}
                                  </li>
                                ))}
                              </ul>
                            </CardContent>
                          </Card>
                        </div>

                        <Card className="bg-[#121C2D] border-[#16233A]">
                          <CardHeader>
                            <CardTitle className="text-sm text-white">Signal Convergence Narrative</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <p className="text-[#D8E2EF] leading-7 text-sm">
                              {selectedThreat.current_nio.signal_narrative}
                            </p>
                          </CardContent>
                        </Card>

                        <div className="grid grid-cols-2 gap-4">
                          <Card className="bg-[#121C2D] border-[#16233A]">
                            <CardHeader>
                              <CardTitle className="text-sm text-white">Confidence Assessment</CardTitle>
                              <CardDescription className="text-[#9FB0C7]">
                                Overall Confidence: {selectedThreat.current_nio.confidence_level}%
                              </CardDescription>
                            </CardHeader>
                            <CardContent>
                              <p className="text-[#D8E2EF] text-sm leading-7">
                                {selectedThreat.current_nio.confidence_explanation}
                              </p>
                              <Separator className="my-4 bg-[#16233A]" />
                              <h5 className="font-medium text-white mb-2 text-sm">Key Assumptions</h5>
                              <ul className="space-y-1.5">
                                {selectedThreat.current_nio.assumptions.map((assumption, idx) => (
                                  <li key={idx} className="text-xs text-[#B8C5D6] leading-5">- {assumption}</li>
                                ))}
                              </ul>
                            </CardContent>
                          </Card>

                          <Card className="bg-[#121C2D] border-[#16233A]">
                            <CardHeader>
                              <CardTitle className="text-sm text-white">Monitoring Posture</CardTitle>
                              <Badge className={POSTURE_COLORS[selectedThreat.current_nio.monitoring_posture]}>
                                {selectedThreat.current_nio.monitoring_posture}
                              </Badge>
                            </CardHeader>
                            <CardContent>
                              <p className="text-[#C9D4E3] text-sm leading-relaxed mb-4">
                                {selectedThreat.current_nio.posture_rationale}
                              </p>
                              <h5 className="font-medium text-white mb-2 text-sm">Recommended Actions</h5>
                              <ul className="space-y-1">
                                {selectedThreat.current_nio.recommended_actions.map((action, idx) => (
                                  <li key={idx} className="text-xs text-[#9FB0C7]">- {action}</li>
                                ))}
                              </ul>
                            </CardContent>
                          </Card>
                        </div>

                        <Card className="bg-[#121C2D] border-[#16233A]">
                          <CardHeader>
                            <CardTitle className="text-sm text-white">Reasoning Chain (Audit Trail)</CardTitle>
                          </CardHeader>
                          <CardContent>
                            <ol className="space-y-3">
                              {selectedThreat.current_nio.reasoning_chain.map((step, idx) => (
                                <li key={idx} className="flex items-start gap-3 text-sm">
                                  <span className="flex-shrink-0 w-6 h-6 rounded-full bg-[#16233A] flex items-center justify-center text-xs text-[#4F81BD]">
                                    {idx + 1}
                                  </span>
                                  <span className="text-[#D8E2EF] pt-0.5 leading-6">{step.replace(/^Step \d+: /, '')}</span>
                                </li>
                              ))}
                            </ol>
                          </CardContent>
                        </Card>
                      </>
                    ) : (
                      <Alert className="bg-[#16233A] border-[#16233A]">
                        <AlertTriangle className="h-4 w-4 text-[#F4B400]" />
                        <AlertTitle className="text-white">No Intelligence Narrative Available</AlertTitle>
                        <AlertDescription className="text-[#C9D4E3]">
                          Click "Generate NIO" to create an intelligence narrative for this threat.
                          <Button size="sm" className="ml-4 bg-[#4F81BD] hover:bg-[#4F81BD]/80" onClick={regenerateNIO}>
                            Generate NIO
                          </Button>
                        </AlertDescription>
                      </Alert>
                    )}
                  </TabsContent>

                  <TabsContent value="situational" className="space-y-4">
                    {selectedThreat.region_context && (
                      <Card className="bg-[#121C2D] border-[#16233A]">
                        <CardHeader>
                          <div className="flex items-center gap-2">
                            <MapPin className="h-5 w-5 text-[#3EC1C9]" />
                            <CardTitle className="text-lg text-white">Region-Aware Intelligence</CardTitle>
                          </div>
                          <CardDescription className="text-[#9FB0C7]">
                            Abstracted geographic context — policy-safe, non-targeting
                          </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <div className="grid grid-cols-2 gap-4">
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Primary Region</div>
                              <div className="text-lg font-semibold text-white">{selectedThreat.region_context.primary_region}</div>
                              <Badge className="mt-2 bg-[#3EC1C9]/15 text-[#3EC1C9] border border-[#3EC1C9]/30">
                                {selectedThreat.region_context.region_type}
                              </Badge>
                            </div>
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Attribution Confidence</div>
                              <div className="text-3xl font-bold text-white">{(selectedThreat.region_context.attribution_confidence * 100).toFixed(0)}%</div>
                              <Progress value={selectedThreat.region_context.attribution_confidence * 100} className="mt-2 h-2" />
                            </div>
                          </div>
                          
                          {selectedThreat.region_context.secondary_regions.length > 0 && (
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-2">Secondary/Adjacent Regions</div>
                              <div className="flex flex-wrap gap-2">
                                {selectedThreat.region_context.secondary_regions.map((region, idx) => (
                                  <Badge key={idx} variant="outline" className="border-[#3EC1C9]/30 text-[#C9D4E3]">
                                    {region}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          <div className="grid grid-cols-2 gap-4">
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Population Scale</div>
                              <div className="text-sm text-white capitalize">{selectedThreat.region_context.population_scale.replace(/-/g, ' ')}</div>
                            </div>
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Economic Profile</div>
                              <div className="text-sm text-white capitalize">{selectedThreat.region_context.economic_profile.replace(/-/g, ' ')}</div>
                            </div>
                          </div>
                          
                          <div className="bg-[#16233A] rounded-lg p-4">
                            <div className="text-xs text-[#9FB0C7] mb-2">Attribution Rationale</div>
                            <p className="text-sm text-[#D8E2EF] leading-6">{selectedThreat.region_context.attribution_rationale}</p>
                          </div>
                          
                          <Alert className="bg-[#0B1220] border-[#3EC1C9]/30">
                            <Lock className="h-4 w-4 text-[#3EC1C9]" />
                            <AlertTitle className="text-[#3EC1C9] text-sm">Policy Compliance</AlertTitle>
                            <AlertDescription className="text-[#9FB0C7] text-xs">
                              {selectedThreat.region_context.policy_notes.join(' • ')}
                            </AlertDescription>
                          </Alert>
                        </CardContent>
                      </Card>
                    )}

                    {selectedThreat.escalation_pathway && (
                      <Card className="bg-[#121C2D] border-[#16233A]">
                        <CardHeader>
                          <div className="flex items-center gap-2">
                            <Route className="h-5 w-5 text-[#F4B400]" />
                            <CardTitle className="text-lg text-white">Escalation Pathway Modeling</CardTitle>
                          </div>
                          <CardDescription className="text-[#9FB0C7]">
                            Pattern-based progression — decision support only, not forecasting
                          </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <div className="bg-[#16233A] rounded-lg p-4">
                            <div className="text-xs text-[#9FB0C7] mb-1">Current Pathway Pattern</div>
                            <div className="text-lg font-semibold text-white">{selectedThreat.escalation_pathway.pathway_name}</div>
                            <p className="text-sm text-[#C9D4E3] mt-2">{selectedThreat.escalation_pathway.pathway_description}</p>
                          </div>
                          
                          <div className="bg-[#16233A] rounded-lg p-4">
                            <div className="text-xs text-[#9FB0C7] mb-3">Pathway Stages</div>
                            <div className="space-y-3">
                              {selectedThreat.escalation_pathway.stages.map((stage, idx) => {
                                const isCurrentStage = idx === selectedThreat.escalation_pathway!.current_stage_index;
                                const isPastStage = idx < selectedThreat.escalation_pathway!.current_stage_index;
                                const stageColor = idx === 0 ? '#4F81BD' : idx === 1 ? '#F4B400' : idx === 2 ? '#F28C28' : '#E5533D';
                                return (
                                  <div key={idx} className={`flex items-start gap-3 p-3 rounded-lg ${isCurrentStage ? 'bg-[#0B1220] border border-[' + stageColor + ']/50' : ''}`}>
                                    <div className="flex flex-col items-center">
                                        <div 
                                          className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${isCurrentStage ? 'ring-2 ring-offset-2 ring-offset-[#16233A]' : ''}`}
                                          style={{ 
                                            backgroundColor: isPastStage || isCurrentStage ? stageColor : '#16233A',
                                            color: isPastStage || isCurrentStage ? '#0B1220' : '#9FB0C7',
                                            boxShadow: isCurrentStage ? `0 0 0 2px #16233A, 0 0 0 4px ${stageColor}` : undefined
                                          }}
                                        >
                                        {idx + 1}
                                      </div>
                                      {idx < selectedThreat.escalation_pathway!.stages.length - 1 && (
                                        <div className={`w-0.5 h-8 mt-1 ${isPastStage ? 'bg-[#3EC1C9]' : 'bg-[#16233A]'}`} />
                                      )}
                                    </div>
                                    <div className="flex-1">
                                      <div className="flex items-center gap-2">
                                        <span className={`font-medium ${isCurrentStage ? 'text-white' : 'text-[#C9D4E3]'}`}>{stage.stage_name}</span>
                                        {isCurrentStage && (
                                          <Badge className="bg-[#F4B400]/15 text-[#F4B400] border border-[#F4B400]/30 text-xs">
                                            Current Position
                                          </Badge>
                                        )}
                                      </div>
                                      <p className="text-xs text-[#9FB0C7] mt-1">{stage.stage_description}</p>
                                      {isCurrentStage && (
                                        <div className="mt-2 text-xs text-[#9FB0C7]">
                                          Typical duration: {stage.typical_duration_hours[0]}–{stage.typical_duration_hours[1]} hours
                                        </div>
                                      )}
                                    </div>
                                  </div>
                                );
                              })}
                            </div>
                          </div>
                          
                          <div className="grid grid-cols-3 gap-4">
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Progression Probability</div>
                              <div className="text-2xl font-bold text-[#F28C28]">{(selectedThreat.escalation_pathway.progression_probability * 100).toFixed(0)}%</div>
                              <div className="text-xs text-[#9FB0C7] mt-1">to next stage</div>
                            </div>
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Regression Probability</div>
                              <div className="text-2xl font-bold text-[#4F81BD]">{(selectedThreat.escalation_pathway.regression_probability * 100).toFixed(0)}%</div>
                              <div className="text-xs text-[#9FB0C7] mt-1">to previous stage</div>
                            </div>
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Projection Confidence</div>
                              <div className="text-2xl font-bold text-white">{(selectedThreat.escalation_pathway.projection_confidence * 100).toFixed(0)}%</div>
                              <Progress value={selectedThreat.escalation_pathway.projection_confidence * 100} className="mt-2 h-2" />
                            </div>
                          </div>
                          
                          <div className="bg-[#16233A] rounded-lg p-4">
                            <div className="text-xs text-[#9FB0C7] mb-2">Projected Progression Window (with uncertainty)</div>
                            <div className="flex items-center gap-2">
                              <Clock className="h-4 w-4 text-[#F4B400]" />
                              <span className="text-white font-medium">
                                {selectedThreat.escalation_pathway.projected_progression_window[0]}–{selectedThreat.escalation_pathway.projected_progression_window[1]} hours
                              </span>
                              <span className="text-[#9FB0C7] text-sm">
                                ({(selectedThreat.escalation_pathway.projected_progression_window[0] / 24).toFixed(1)}–{(selectedThreat.escalation_pathway.projected_progression_window[1] / 24).toFixed(1)} days)
                              </span>
                            </div>
                          </div>
                          
                          {selectedThreat.escalation_pathway.historical_pattern_matches.length > 0 && (
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-2">Historical Pattern Matches</div>
                              <div className="flex flex-wrap gap-2">
                                {selectedThreat.escalation_pathway.historical_pattern_matches.map((pattern, idx) => (
                                  <Badge key={idx} variant="outline" className="border-[#F4B400]/30 text-[#C9D4E3]">
                                    {pattern}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                          
                          <Alert className="bg-[#0B1220] border-[#F4B400]/30">
                            <Shield className="h-4 w-4 text-[#F4B400]" />
                            <AlertTitle className="text-[#F4B400] text-sm">Decision Support Notice</AlertTitle>
                            <AlertDescription className="text-[#9FB0C7] text-xs">
                              {selectedThreat.escalation_pathway.policy_notes.join(' • ')}
                            </AlertDescription>
                          </Alert>
                        </CardContent>
                      </Card>
                    )}

                    {selectedThreat.threat_class_alignment && (
                      <Card className="bg-[#121C2D] border-[#16233A]">
                        <CardHeader>
                          <div className="flex items-center gap-2">
                            <Target className="h-5 w-5 text-[#7A8CA3]" />
                            <CardTitle className="text-lg text-white">Threat Class Alignment (Analytic)</CardTitle>
                          </div>
                          <CardDescription className="text-[#9FB0C7]">
                            Probabilistic pattern similarity — classes are non-exclusive and may evolve
                          </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <div className="space-y-3">
                            {selectedThreat.threat_class_alignment.alignments.map((alignment, idx) => {
                              const isTopAlignment = alignment.class_category === selectedThreat.threat_class_alignment!.top_alignment;
                              const barWidth = Math.round(alignment.alignment_score * 100);
                              return (
                                <div key={idx} className={`bg-[#16233A] rounded-lg p-4 ${isTopAlignment ? 'border border-[#7A8CA3]/50' : ''}`}>
                                  <div className="flex items-center justify-between mb-2">
                                    <div className="flex items-center gap-2">
                                      <span className={`font-medium ${isTopAlignment ? 'text-white' : 'text-[#C9D4E3]'}`}>
                                        {THREAT_CLASS_LABELS[alignment.class_category] || alignment.class_category}
                                      </span>
                                      {isTopAlignment && (
                                        <Badge className="bg-[#7A8CA3]/15 text-[#7A8CA3] border border-[#7A8CA3]/30 text-xs">
                                          Top Alignment
                                        </Badge>
                                      )}
                                    </div>
                                    <div className="flex items-center gap-3">
                                      <span className="text-lg font-bold text-white">{(alignment.alignment_score * 100).toFixed(0)}%</span>
                                      <span className="text-xs text-[#9FB0C7]">conf: {(alignment.confidence * 100).toFixed(0)}%</span>
                                    </div>
                                  </div>
                                  <div className="w-full bg-[#0B1220] rounded-full h-2 mb-3">
                                    <div 
                                      className="h-2 rounded-full transition-all duration-300"
                                      style={{ 
                                        width: `${barWidth}%`,
                                        backgroundColor: isTopAlignment ? '#7A8CA3' : '#4F81BD',
                                        opacity: 0.6 + (alignment.confidence * 0.4)
                                      }}
                                    />
                                  </div>
                                  <details className="group">
                                    <summary className="text-xs text-[#9FB0C7] cursor-pointer hover:text-[#C9D4E3] transition-colors">
                                      View alignment rationale
                                    </summary>
                                    <div className="mt-3 space-y-2 text-xs">
                                      <p className="text-[#D8E2EF] leading-5">{alignment.rationale}</p>
                                      <div className="grid grid-cols-3 gap-2 mt-2">
                                        <div className="bg-[#0B1220] rounded p-2">
                                          <div className="text-[#9FB0C7]">Intent Stage</div>
                                          <div className="text-[#C9D4E3] font-medium">{(alignment.intent_stage_influence * 100).toFixed(0)}% influence</div>
                                        </div>
                                        <div className="bg-[#0B1220] rounded p-2">
                                          <div className="text-[#9FB0C7]">Escalation Path</div>
                                          <div className="text-[#C9D4E3] font-medium">{(alignment.escalation_pathway_influence * 100).toFixed(0)}% influence</div>
                                        </div>
                                        <div className="bg-[#0B1220] rounded p-2">
                                          <div className="text-[#9FB0C7]">Velocity</div>
                                          <div className="text-[#C9D4E3] font-medium">{(alignment.velocity_influence * 100).toFixed(0)}% influence</div>
                                        </div>
                                      </div>
                                      {alignment.primary_contributing_domains.length > 0 && (
                                        <div className="flex flex-wrap gap-1 mt-2">
                                          <span className="text-[#9FB0C7]">Contributing domains:</span>
                                          {alignment.primary_contributing_domains.map((domain, dIdx) => (
                                            <Badge key={dIdx} variant="outline" className="border-[#4F81BD]/30 text-[#C9D4E3] text-xs">
                                              {DOMAIN_LABELS[domain] || domain}
                                            </Badge>
                                          ))}
                                        </div>
                                      )}
                                    </div>
                                  </details>
                                </div>
                              );
                            })}
                          </div>
                          
                          <div className="grid grid-cols-2 gap-4">
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Alignment Diversity</div>
                              <div className="text-2xl font-bold text-white">{(selectedThreat.threat_class_alignment.alignment_diversity * 100).toFixed(0)}%</div>
                              <div className="text-xs text-[#9FB0C7] mt-1">
                                {selectedThreat.threat_class_alignment.alignment_diversity > 0.5 ? 'Distributed across classes' : 'Concentrated alignment'}
                              </div>
                            </div>
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-1">Computed At</div>
                              <div className="text-sm text-white">
                                Stage: {STAGE_LABELS[selectedThreat.threat_class_alignment.intent_stage_at_computation]?.split(':')[1]?.trim() || selectedThreat.threat_class_alignment.intent_stage_at_computation}
                              </div>
                              <div className="text-xs text-[#9FB0C7] mt-1">
                                Escalation Stage: {selectedThreat.threat_class_alignment.escalation_stage_at_computation + 1}
                              </div>
                            </div>
                          </div>
                          
                          <Alert className="bg-[#0B1220] border-[#7A8CA3]/30">
                            <Shield className="h-4 w-4 text-[#7A8CA3]" />
                            <AlertTitle className="text-[#7A8CA3] text-sm">Analytic Disclaimer</AlertTitle>
                            <AlertDescription className="text-[#9FB0C7] text-xs">
                              {selectedThreat.threat_class_alignment.disclaimer}
                            </AlertDescription>
                          </Alert>
                          
                          <div className="bg-[#16233A] rounded-lg p-3">
                            <div className="text-xs text-[#9FB0C7] mb-2">Policy Compliance</div>
                            <div className="flex flex-wrap gap-2">
                              {selectedThreat.threat_class_alignment.policy_notes.map((note, idx) => (
                                <Badge key={idx} variant="outline" className="border-[#7A8CA3]/30 text-[#9FB0C7] text-xs">
                                  {note}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    )}

                    {selectedThreat.decision_advantage_layer && (
                      <>
                        <Card className="bg-[#121C2D] border-[#16233A]">
                          <CardHeader>
                            <div className="flex items-start justify-between">
                              <div>
                                <CardTitle className="text-lg text-white flex items-center gap-2">
                                  <Target className="h-5 w-5 text-[#4F81BD]" />
                                  Decision Pathway Intelligence
                                </CardTitle>
                                <CardDescription className="text-[#9FB0C7]">
                                  Advisory pathways ranked by relevance - optional, proportional guidance
                                </CardDescription>
                              </div>
                              <Badge className="bg-[#4F81BD]/20 text-[#4F81BD] border-[#4F81BD]/40">
                                Phase 3
                              </Badge>
                            </div>
                          </CardHeader>
                          <CardContent className="space-y-4">
                            {selectedThreat.decision_advantage_layer.decision_pathways && (
                              <>
                                <div className="bg-[#16233A] rounded-lg p-4">
                                  <div className="text-sm text-[#C9D4E3] leading-7 mb-3">
                                    {selectedThreat.decision_advantage_layer.decision_pathways.overall_advisory_posture}
                                  </div>
                                  <div className="text-xs text-[#9FB0C7]">
                                    {selectedThreat.decision_advantage_layer.decision_pathways.proportionality_assessment}
                                  </div>
                                </div>

                                <div className="space-y-3">
                                  {selectedThreat.decision_advantage_layer.decision_pathways.pathways.slice(0, 5).map((pathway, idx) => (
                                    <div key={idx} className="bg-[#16233A] rounded-lg p-4 border-l-4" style={{ borderLeftColor: pathway.relevance === 'high' ? '#4F81BD' : pathway.relevance === 'moderate' ? '#F4B400' : '#7A8CA3' }}>
                                      <div className="flex items-start justify-between mb-2">
                                        <div className="flex items-center gap-2">
                                          <span className="text-white font-medium">
                                            {DECISION_PATHWAY_LABELS[pathway.pathway_category] || pathway.pathway_category}
                                          </span>
                                          <Badge className={`text-xs border ${RELEVANCE_COLORS[pathway.relevance] || RELEVANCE_COLORS.low}`}>
                                            {pathway.relevance.toUpperCase()}
                                          </Badge>
                                        </div>
                                        <div className="text-right">
                                          <div className="text-lg font-bold text-[#4F81BD]">
                                            {(pathway.relevance_score * 100).toFixed(0)}%
                                          </div>
                                          <div className="text-xs text-[#9FB0C7]">relevance</div>
                                        </div>
                                      </div>
                                      <p className="text-sm text-[#C9D4E3] leading-7 mb-2">{pathway.advisory_summary}</p>
                                      <div className="flex items-center gap-2 mb-2">
                                        <Progress value={pathway.relevance_score * 100} className="h-1.5 flex-1" />
                                        <span className="text-xs text-[#9FB0C7]">{(pathway.confidence * 100).toFixed(0)}% conf</span>
                                      </div>
                                      {pathway.suggested_considerations.length > 0 && (
                                        <details className="mt-2">
                                          <summary className="text-xs text-[#9FB0C7] cursor-pointer hover:text-[#C9D4E3]">
                                            View considerations ({pathway.suggested_considerations.length})
                                          </summary>
                                          <div className="mt-2 space-y-1 pl-3 border-l border-[#7A8CA3]/30">
                                            {pathway.suggested_considerations.map((consideration, cIdx) => (
                                              <div key={cIdx} className="text-xs text-[#9FB0C7]">{consideration}</div>
                                            ))}
                                          </div>
                                        </details>
                                      )}
                                      <div className="text-xs text-[#7A8CA3] mt-2 italic">{pathway.proportionality_note}</div>
                                    </div>
                                  ))}
                                </div>

                                <Alert className="bg-[#0B1220] border-[#7A8CA3]/30">
                                  <Shield className="h-4 w-4 text-[#7A8CA3]" />
                                  <AlertTitle className="text-[#7A8CA3] text-sm">Advisory Disclaimer</AlertTitle>
                                  <AlertDescription className="text-[#9FB0C7] text-xs">
                                    {selectedThreat.decision_advantage_layer.decision_pathways.disclaimer}
                                  </AlertDescription>
                                </Alert>
                              </>
                            )}
                          </CardContent>
                        </Card>

                        <Card className="bg-[#121C2D] border-[#16233A]">
                          <CardHeader>
                            <div className="flex items-start justify-between">
                              <div>
                                <CardTitle className="text-lg text-white flex items-center gap-2">
                                  <Activity className="h-5 w-5 text-[#F4B400]" />
                                  Impact Forecasting
                                </CardTitle>
                                <CardDescription className="text-[#9FB0C7]">
                                  System-level impact projections with time horizons and confidence bands
                                </CardDescription>
                              </div>
                              <Badge className="bg-[#F4B400]/20 text-[#F4B400] border-[#F4B400]/40">
                                Phase 3
                              </Badge>
                            </div>
                          </CardHeader>
                          <CardContent className="space-y-4">
                            {selectedThreat.decision_advantage_layer.impact_forecast && (
                              <>
                                <div className="bg-[#16233A] rounded-lg p-4">
                                  <div className="text-sm text-[#C9D4E3] leading-7 mb-2">
                                    {selectedThreat.decision_advantage_layer.impact_forecast.overall_impact_assessment}
                                  </div>
                                  <div className="flex items-center gap-4 text-xs text-[#9FB0C7]">
                                    <span>Time Horizon: {selectedThreat.decision_advantage_layer.impact_forecast.projection_time_horizon}</span>
                                    <span>Aggregate Severity: {(selectedThreat.decision_advantage_layer.impact_forecast.aggregate_severity_score * 100).toFixed(0)}%</span>
                                  </div>
                                </div>

                                <div className="space-y-3">
                                  {selectedThreat.decision_advantage_layer.impact_forecast.projections.slice(0, 5).map((projection, idx) => (
                                    <div key={idx} className="bg-[#16233A] rounded-lg p-4">
                                      <div className="flex items-start justify-between mb-2">
                                        <div>
                                          <span className="text-white font-medium">
                                            {IMPACT_DOMAIN_LABELS[projection.domain] || projection.domain}
                                          </span>
                                          <Badge className={`ml-2 text-xs ${
                                            projection.impact_severity === 'high' ? 'bg-[#E5533D]/20 text-[#E5533D] border-[#E5533D]/40' :
                                            projection.impact_severity === 'moderate' ? 'bg-[#F4B400]/20 text-[#F4B400] border-[#F4B400]/40' :
                                            'bg-[#4F81BD]/20 text-[#4F81BD] border-[#4F81BD]/40'
                                          }`}>
                                            {projection.impact_severity.toUpperCase()}
                                          </Badge>
                                        </div>
                                        <div className="text-right">
                                          <div className="text-lg font-bold text-[#F4B400]">
                                            {(projection.impact_severity_score * 100).toFixed(0)}%
                                          </div>
                                          <div className="text-xs text-[#9FB0C7]">severity</div>
                                        </div>
                                      </div>
                                      <p className="text-sm text-[#9FB0C7] mb-1">{projection.current_assessment}</p>
                                      <p className="text-sm text-[#C9D4E3] leading-7 mb-2">{projection.projected_trajectory}</p>
                                      <div className="flex items-center gap-2 mb-2">
                                        <Progress value={projection.impact_severity_score * 100} className="h-1.5 flex-1" />
                                        <span className="text-xs text-[#9FB0C7]">
                                          {(projection.confidence * 100).toFixed(0)}% conf ({projection.confidence_band[0].toFixed(0)}-{projection.confidence_band[1].toFixed(0)}%)
                                        </span>
                                      </div>
                                      <div className="text-xs text-[#7A8CA3]">
                                        Time Horizon: {projection.time_horizon_hours[0]}-{projection.time_horizon_hours[1]} hours
                                      </div>
                                    </div>
                                  ))}
                                </div>

                                <Alert className="bg-[#0B1220] border-[#7A8CA3]/30">
                                  <Shield className="h-4 w-4 text-[#7A8CA3]" />
                                  <AlertTitle className="text-[#7A8CA3] text-sm">Forecast Disclaimer</AlertTitle>
                                  <AlertDescription className="text-[#9FB0C7] text-xs">
                                    {selectedThreat.decision_advantage_layer.impact_forecast.disclaimer}
                                  </AlertDescription>
                                </Alert>
                              </>
                            )}
                          </CardContent>
                        </Card>

                        <Card className="bg-[#121C2D] border-[#16233A]">
                          <CardHeader>
                            <div className="flex items-start justify-between">
                              <div>
                                <CardTitle className="text-lg text-white flex items-center gap-2">
                                  <Brain className="h-5 w-5 text-[#3EC1C9]" />
                                  Authority-Aware Recommendations
                                </CardTitle>
                                <CardDescription className="text-[#9FB0C7]">
                                  Leadership domains best positioned to respond - no individual naming
                                </CardDescription>
                              </div>
                              <Badge className="bg-[#3EC1C9]/20 text-[#3EC1C9] border-[#3EC1C9]/40">
                                Phase 3
                              </Badge>
                            </div>
                          </CardHeader>
                          <CardContent className="space-y-4">
                            {selectedThreat.decision_advantage_layer.authority_recommendations && (
                              <>
                                <div className="bg-[#16233A] rounded-lg p-4">
                                  <div className="text-sm text-[#C9D4E3] leading-7 mb-2">
                                    {selectedThreat.decision_advantage_layer.authority_recommendations.coordination_summary}
                                  </div>
                                  <div className="text-xs text-[#9FB0C7]">
                                    Context: {selectedThreat.decision_advantage_layer.authority_recommendations.context_applicability}
                                  </div>
                                </div>

                                <div className="space-y-3">
                                  {selectedThreat.decision_advantage_layer.authority_recommendations.recommendations.slice(0, 5).map((rec, idx) => (
                                    <div key={idx} className="bg-[#16233A] rounded-lg p-4 border-l-4" style={{ borderLeftColor: '#3EC1C9' }}>
                                      <div className="flex items-start justify-between mb-2">
                                        <span className="text-white font-medium">
                                          {AUTHORITY_DOMAIN_LABELS[rec.authority_domain] || rec.authority_domain}
                                        </span>
                                        <div className="text-right">
                                          <div className="text-lg font-bold text-[#3EC1C9]">
                                            {(rec.relevance_score * 100).toFixed(0)}%
                                          </div>
                                          <div className="text-xs text-[#9FB0C7]">positioning</div>
                                        </div>
                                      </div>
                                      <p className="text-sm text-[#C9D4E3] leading-7 mb-2">{rec.positioning_rationale}</p>
                                      <div className="flex items-center gap-2 mb-2">
                                        <Progress value={rec.relevance_score * 100} className="h-1.5 flex-1" />
                                        <span className="text-xs text-[#9FB0C7]">{(rec.confidence * 100).toFixed(0)}% conf</span>
                                      </div>
                                      {rec.suggested_awareness_areas.length > 0 && (
                                        <details className="mt-2">
                                          <summary className="text-xs text-[#9FB0C7] cursor-pointer hover:text-[#C9D4E3]">
                                            View awareness areas ({rec.suggested_awareness_areas.length})
                                          </summary>
                                          <div className="mt-2 space-y-1 pl-3 border-l border-[#7A8CA3]/30">
                                            {rec.suggested_awareness_areas.map((area, aIdx) => (
                                              <div key={aIdx} className="text-xs text-[#9FB0C7]">{area}</div>
                                            ))}
                                          </div>
                                        </details>
                                      )}
                                      <div className="flex flex-wrap gap-1 mt-2">
                                        {rec.context_applicability.map((ctx, ctxIdx) => (
                                          <Badge key={ctxIdx} variant="outline" className="border-[#3EC1C9]/30 text-[#3EC1C9] text-xs">
                                            {ctx}
                                          </Badge>
                                        ))}
                                      </div>
                                    </div>
                                  ))}
                                </div>

                                <Alert className="bg-[#0B1220] border-[#7A8CA3]/30">
                                  <Shield className="h-4 w-4 text-[#7A8CA3]" />
                                  <AlertTitle className="text-[#7A8CA3] text-sm">Authority Disclaimer</AlertTitle>
                                  <AlertDescription className="text-[#9FB0C7] text-xs">
                                    {selectedThreat.decision_advantage_layer.authority_recommendations.disclaimer}
                                  </AlertDescription>
                                </Alert>
                              </>
                            )}
                          </CardContent>
                        </Card>

                        <Card className="bg-[#121C2D] border-[#16233A]">
                          <CardHeader>
                            <CardTitle className="text-lg text-white flex items-center gap-2">
                              <Shield className="h-5 w-5 text-[#7A8CA3]" />
                              Decision Advantage Summary
                            </CardTitle>
                          </CardHeader>
                          <CardContent className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                              <div className="bg-[#16233A] rounded-lg p-4">
                                <div className="text-xs text-[#9FB0C7] mb-1">Overall Decision Posture</div>
                                <div className="text-sm text-[#C9D4E3] leading-7">
                                  {selectedThreat.decision_advantage_layer.overall_decision_posture}
                                </div>
                              </div>
                              <div className="bg-[#16233A] rounded-lg p-4">
                                <div className="text-xs text-[#9FB0C7] mb-1">Confidence-Weighted Priority</div>
                                <div className="text-2xl font-bold text-white">
                                  {(selectedThreat.decision_advantage_layer.confidence_weighted_priority * 100).toFixed(0)}%
                                </div>
                              </div>
                            </div>

                            <Alert className="bg-[#0B1220] border-[#F4B400]/30">
                              <AlertTriangle className="h-4 w-4 text-[#F4B400]" />
                              <AlertTitle className="text-[#F4B400] text-sm">Master Disclaimer</AlertTitle>
                              <AlertDescription className="text-[#9FB0C7] text-xs">
                                {selectedThreat.decision_advantage_layer.master_disclaimer}
                              </AlertDescription>
                            </Alert>

                            <div className="bg-[#16233A] rounded-lg p-3">
                              <div className="text-xs text-[#9FB0C7] mb-2">Policy Compliance</div>
                              <div className="flex flex-wrap gap-2">
                                {selectedThreat.decision_advantage_layer.policy_compliance.map((note, idx) => (
                                  <Badge key={idx} variant="outline" className="border-[#7A8CA3]/30 text-[#9FB0C7] text-xs">
                                    {note}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </>
                    )}

                    {!selectedThreat.region_context && !selectedThreat.escalation_pathway && !selectedThreat.threat_class_alignment && !selectedThreat.decision_advantage_layer && (
                      <Alert className="bg-[#16233A] border-[#16233A]">
                        <AlertTriangle className="h-4 w-4 text-[#F4B400]" />
                        <AlertTitle className="text-white">Situational Awareness Data Unavailable</AlertTitle>
                        <AlertDescription className="text-[#C9D4E3]">
                          Region context and escalation pathway data have not been generated for this threat.
                        </AlertDescription>
                      </Alert>
                    )}

                    {regionSummaries.length > 0 && (
                      <Card className="bg-[#121C2D] border-[#16233A]">
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Layers className="h-5 w-5 text-[#3EC1C9]" />
                              <CardTitle className="text-lg text-white">Multi-Context Regional Intelligence</CardTitle>
                            </div>
                            <Badge variant="outline" className="border-[#3EC1C9]/30 text-[#3EC1C9]">
                              {regionSummaries.length} Regions • {multiRegionIntelligence?.total_contexts || 0} Contexts
                            </Badge>
                          </div>
                          <CardDescription className="text-[#9FB0C7]">
                            Independent decision contexts per region — no merging, no compound threats
                          </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <div className="bg-[#16233A] rounded-lg p-4">
                            <div className="text-xs text-[#9FB0C7] mb-3">Regional Context Selector</div>
                            <div className="flex flex-wrap gap-2">
                              {regionSummaries.map((region) => {
                                const stageColors = region.highest_intent_stage ? 
                                  INTENT_STAGE_COLORS[region.highest_intent_stage] || INTENT_STAGE_COLORS.grievance_formation : 
                                  INTENT_STAGE_COLORS.grievance_formation;
                                return (
                                  <button
                                    key={region.region_id}
                                    onClick={() => handleSetActiveRegion(region.region_id)}
                                    className={`px-4 py-2 rounded-lg border transition-all ${
                                      region.is_active 
                                        ? 'bg-[#3EC1C9]/20 border-[#3EC1C9] text-white' 
                                        : 'bg-[#0B1220] border-[#16233A] text-[#C9D4E3] hover:border-[#3EC1C9]/50'
                                    }`}
                                  >
                                    <div className="flex items-center gap-2">
                                      <div 
                                        className="w-2 h-2 rounded-full" 
                                        style={{ backgroundColor: stageColors.accent }}
                                      />
                                      <span className="text-sm font-medium">{region.region_name}</span>
                                      <Badge variant="outline" className="border-[#7A8CA3]/30 text-[#9FB0C7] text-xs">
                                        {region.context_count} ctx
                                      </Badge>
                                    </div>
                                  </button>
                                );
                              })}
                            </div>
                          </div>

                          {activeRegion && (
                            <>
                              {activeRegion.confidence_bands && (
                                <div className="bg-[#16233A] rounded-lg p-4">
                                  <div className="text-xs text-[#9FB0C7] mb-3 flex items-center gap-2">
                                    Layered Region Confidence Bands
                                    <TooltipProvider>
                                      <UITooltip>
                                        <TooltipTrigger asChild>
                                          <Info className="w-3.5 h-3.5 text-[#9FB0C7] hover:text-[#C9D4E3] cursor-help" />
                                        </TooltipTrigger>
                                        <TooltipContent side="right" className="max-w-xs bg-[#121C2D] border border-[#16233A] text-[#C9D4E3] p-3">
                                          <p className="font-medium text-white mb-2">Regional Relevance Zones</p>
                                          <p className="text-xs leading-relaxed">
                                            These labels describe analytical relevance zones for the selected region. 
                                            They indicate where contextual conditions are most relevant based on converging indicators. 
                                            They do not represent event locations, actor activity, or precise geographic targeting, and they are not interactive. 
                                            The map provides spatial context only to support decision understanding.
                                          </p>
                                        </TooltipContent>
                                      </UITooltip>
                                    </TooltipProvider>
                                  </div>
                                  <div className="space-y-3">
                                    <div className="flex items-center gap-3 p-3 rounded-lg bg-[#0B1220] border-2 border-solid border-[#3EC1C9]">
                                      <div className="w-3 h-3 rounded-full bg-[#3EC1C9]" />
                                      <div className="flex-1">
                                        <div className="text-sm font-medium text-white">Core Region</div>
                                        <div className="text-xs text-[#9FB0C7]">{activeRegion.confidence_bands.core_band.region_name}</div>
                                      </div>
                                      <div className="text-right">
                                        <div className="text-lg font-bold text-[#3EC1C9]">
                                          {(activeRegion.confidence_bands.core_band.relevance_score * 100).toFixed(0)}%
                                        </div>
                                        <div className="text-xs text-[#9FB0C7]">relevance</div>
                                      </div>
                                    </div>
                                    
                                    {activeRegion.confidence_bands.adjacent_band && (
                                      <div className="flex items-center gap-3 p-3 rounded-lg bg-[#0B1220] border-2 border-dashed border-[#F4B400]/60">
                                        <div className="w-3 h-3 rounded-full bg-[#F4B400]/60" />
                                        <div className="flex-1">
                                          <div className="text-sm font-medium text-white">Adjacent Zone</div>
                                          <div className="text-xs text-[#9FB0C7]">{activeRegion.confidence_bands.adjacent_band.region_name}</div>
                                        </div>
                                        <div className="text-right">
                                          <div className="text-lg font-bold text-[#F4B400]">
                                            {(activeRegion.confidence_bands.adjacent_band.relevance_score * 100).toFixed(0)}%
                                          </div>
                                          <div className="text-xs text-[#9FB0C7]">relevance</div>
                                        </div>
                                      </div>
                                    )}
                                    
                                    {activeRegion.confidence_bands.peripheral_band && (
                                      <div className="flex items-center gap-3 p-3 rounded-lg bg-[#0B1220] border border-[#7A8CA3]/30 opacity-70">
                                        <div className="w-3 h-3 rounded-full bg-[#7A8CA3]/50" />
                                        <div className="flex-1">
                                          <div className="text-sm font-medium text-[#C9D4E3]">Peripheral Influence</div>
                                          <div className="text-xs text-[#9FB0C7]">{activeRegion.confidence_bands.peripheral_band.region_name}</div>
                                        </div>
                                        <div className="text-right">
                                          <div className="text-lg font-bold text-[#7A8CA3]">
                                            {(activeRegion.confidence_bands.peripheral_band.relevance_score * 100).toFixed(0)}%
                                          </div>
                                          <div className="text-xs text-[#9FB0C7]">relevance</div>
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                  <div className="mt-3 text-xs text-[#9FB0C7] italic">
                                    Bands represent analytical relevance only — not events, actors, or threats
                                  </div>
                                </div>
                              )}

                              <div className="bg-[#16233A] rounded-lg p-4">
                                <div className="flex items-center justify-between mb-3">
                                  <div className="text-xs text-[#9FB0C7]">Context Stack — {activeRegion.region_name}</div>
                                  <Badge variant="outline" className="border-[#7A8CA3]/30 text-[#9FB0C7] text-xs">
                                    {activeRegion.displayed_count} displayed / {activeRegion.total_count} total
                                  </Badge>
                                </div>
                                <div className="space-y-2">
                                  {activeRegion.contexts.map((context) => {
                                    const stageColors = INTENT_STAGE_COLORS[context.intent_stage] || INTENT_STAGE_COLORS.grievance_formation;
                                    const isExpanded = context.context_id === activeRegion.expanded_context_id;
                                    return (
                                      <div 
                                        key={context.context_id}
                                        className={`rounded-lg border transition-all cursor-pointer ${
                                          isExpanded 
                                            ? 'bg-[#0B1220] border-l-4' 
                                            : 'bg-[#0B1220]/50 border-[#16233A] hover:border-[#3EC1C9]/30'
                                        }`}
                                        style={isExpanded ? { borderLeftColor: stageColors.accent } : {}}
                                        onClick={() => handleExpandContext(activeRegion.region_id, context.context_id)}
                                      >
                                        <div className="p-3">
                                          <div className="flex items-center justify-between">
                                            <div className="flex items-center gap-2">
                                              <div 
                                                className="w-2 h-2 rounded-full" 
                                                style={{ backgroundColor: stageColors.accent }}
                                              />
                                              <span className="text-sm font-medium text-white">{context.context_name}</span>
                                              <Badge className={`${stageColors.bg} ${stageColors.text} ${stageColors.border} text-xs`}>
                                                {STAGE_LABELS[context.intent_stage] || context.intent_stage}
                                              </Badge>
                                            </div>
                                            <div className="flex items-center gap-3">
                                              <div className="text-right">
                                                <div className="text-sm font-bold text-white">
                                                  {(context.confidence_score * 100).toFixed(0)}%
                                                </div>
                                                <div className="text-xs text-[#9FB0C7]">confidence</div>
                                              </div>
                                              {isExpanded ? (
                                                <ChevronUp className="h-4 w-4 text-[#9FB0C7]" />
                                              ) : (
                                                <ChevronDown className="h-4 w-4 text-[#9FB0C7]" />
                                              )}
                                            </div>
                                          </div>
                                          
                                          {isExpanded && (
                                            <div className="mt-4 pt-4 border-t border-[#16233A] space-y-3">
                                              <p className="text-sm text-[#C9D4E3] leading-6">{context.context_description}</p>
                                              
                                              <div className="grid grid-cols-4 gap-3">
                                                <div className="bg-[#16233A] rounded p-2">
                                                  <div className="text-xs text-[#9FB0C7]">Intent Stage</div>
                                                  <div className="text-sm font-medium" style={{ color: stageColors.accent }}>
                                                    {(context.intent_stage_confidence * 100).toFixed(0)}%
                                                  </div>
                                                </div>
                                                <div className="bg-[#16233A] rounded p-2">
                                                  <div className="text-xs text-[#9FB0C7]">Persistence</div>
                                                  <div className="text-sm font-medium text-white">
                                                    {(context.persistence_score * 100).toFixed(0)}%
                                                  </div>
                                                </div>
                                                <div className="bg-[#16233A] rounded p-2">
                                                  <div className="text-xs text-[#9FB0C7]">Decision Impact</div>
                                                  <div className="text-sm font-medium text-white">
                                                    {(context.decision_impact_score * 100).toFixed(0)}%
                                                  </div>
                                                </div>
                                                <div className="bg-[#16233A] rounded p-2">
                                                  <div className="text-xs text-[#9FB0C7]">Signals</div>
                                                  <div className="text-sm font-medium text-white">
                                                    {context.signal_count}
                                                  </div>
                                                </div>
                                              </div>
                                              
                                              <div className="flex items-center gap-2">
                                                <Badge variant="outline" className="border-[#7A8CA3]/30 text-[#9FB0C7] text-xs">
                                                  Priority: {context.priority}
                                                </Badge>
                                                <Badge variant="outline" className="border-[#7A8CA3]/30 text-[#9FB0C7] text-xs">
                                                  Score: {(context.priority_score * 100).toFixed(0)}%
                                                </Badge>
                                              </div>
                                            </div>
                                          )}
                                        </div>
                                      </div>
                                    );
                                  })}
                                </div>
                                
                                {activeRegion.summarized_contexts && (
                                  <Alert className="mt-3 bg-[#0B1220] border-[#7A8CA3]/30">
                                    <AlertTriangle className="h-4 w-4 text-[#7A8CA3]" />
                                    <AlertDescription className="text-[#9FB0C7] text-xs">
                                      {activeRegion.summarized_contexts.summary_note} ({activeRegion.summarized_contexts.summarized_count} contexts, avg confidence: {(activeRegion.summarized_contexts.average_confidence * 100).toFixed(0)}%)
                                    </AlertDescription>
                                  </Alert>
                                )}
                              </div>

                              <Alert className="bg-[#0B1220] border-[#3EC1C9]/30">
                                <Lock className="h-4 w-4 text-[#3EC1C9]" />
                                <AlertTitle className="text-[#3EC1C9] text-sm">Multi-Context Safety Constraints</AlertTitle>
                                <AlertDescription className="text-[#9FB0C7] text-xs">
                                  {activeRegion.policy_notes.join(' • ')}
                                </AlertDescription>
                              </Alert>
                            </>
                          )}

                          {multiRegionIntelligence && (
                            <Alert className="bg-[#0B1220] border-[#F4B400]/30">
                              <Shield className="h-4 w-4 text-[#F4B400]" />
                              <AlertTitle className="text-[#F4B400] text-sm">Master Disclaimer</AlertTitle>
                              <AlertDescription className="text-[#9FB0C7] text-xs">
                                {multiRegionIntelligence.master_disclaimer}
                              </AlertDescription>
                            </Alert>
                          )}
                        </CardContent>
                      </Card>
                    )}

                    {decisionDiscipline && (
                      <Card className="bg-[#121C2D] border-[#16233A]">
                        <CardHeader>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Shield className="h-5 w-5 text-[#4F81BD]" />
                              <CardTitle className="text-lg text-white">Decision Discipline Layer</CardTitle>
                            </div>
                            {decisionDiscipline.drl && (
                              <Badge 
                                variant="outline" 
                                className={`border-[#4F81BD]/50 text-[#4F81BD] ${
                                  decisionDiscipline.drl === 'drl_0' ? 'border-[#7A8CA3]/50 text-[#7A8CA3]' :
                                  decisionDiscipline.drl === 'drl_1' ? 'border-[#4F81BD]/50 text-[#4F81BD]' :
                                  decisionDiscipline.drl === 'drl_2' ? 'border-[#F4B400]/50 text-[#F4B400]' :
                                  'border-[#F28C28]/50 text-[#F28C28]'
                                }`}
                              >
                                {decisionDiscipline.drl_details?.name || decisionDiscipline.drl?.toUpperCase().replace('_', '-')}
                              </Badge>
                            )}
                          </div>
                          <CardDescription className="text-[#9FB0C7]">
                            Confidence gating, readiness levels, and explainability for decision support
                          </CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          {decisionDiscipline.confidence_gate && (
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="flex items-center justify-between mb-3">
                                <div className="text-xs text-[#9FB0C7]">Decision Confidence Gate</div>
                                <Badge 
                                  variant="outline" 
                                  className={`${
                                    decisionDiscipline.confidence_gate.gate_status === 'open' 
                                      ? 'border-[#3EC1C9]/50 text-[#3EC1C9]' 
                                      : decisionDiscipline.confidence_gate.gate_status === 'limited'
                                      ? 'border-[#F4B400]/50 text-[#F4B400]'
                                      : 'border-[#7A8CA3]/50 text-[#7A8CA3]'
                                  }`}
                                >
                                  {decisionDiscipline.confidence_gate.gate_status.toUpperCase()}
                                </Badge>
                              </div>
                              
                              <div className="grid grid-cols-4 gap-3 mb-4">
                                <div className="bg-[#0B1220] rounded p-2">
                                  <div className="text-xs text-[#9FB0C7]">Signal Diversity</div>
                                  <div className="text-sm font-medium text-white">
                                    {(decisionDiscipline.confidence_gate.signal_diversity_score * 100).toFixed(0)}%
                                  </div>
                                </div>
                                <div className="bg-[#0B1220] rounded p-2">
                                  <div className="text-xs text-[#9FB0C7]">Persistence</div>
                                  <div className="text-sm font-medium text-white">
                                    {(decisionDiscipline.confidence_gate.persistence_score * 100).toFixed(0)}%
                                  </div>
                                </div>
                                <div className="bg-[#0B1220] rounded p-2">
                                  <div className="text-xs text-[#9FB0C7]">Cross-Domain</div>
                                  <div className="text-sm font-medium text-white">
                                    {(decisionDiscipline.confidence_gate.cross_domain_convergence * 100).toFixed(0)}%
                                  </div>
                                </div>
                                <div className="bg-[#0B1220] rounded p-2">
                                  <div className="text-xs text-[#9FB0C7]">Data Confidence</div>
                                  <div className="text-sm font-medium text-white">
                                    {(decisionDiscipline.confidence_gate.data_confidence * 100).toFixed(0)}%
                                  </div>
                                </div>
                              </div>

                              <div className="text-sm text-[#C9D4E3] leading-relaxed mb-3">
                                {decisionDiscipline.confidence_gate.gate_rationale}
                              </div>

                              {decisionDiscipline.confidence_gate.limiting_message && (
                                <Alert className="bg-[#0B1220] border-[#F4B400]/30">
                                  <AlertTriangle className="h-4 w-4 text-[#F4B400]" />
                                  <AlertDescription className="text-[#F4B400] text-sm">
                                    {decisionDiscipline.confidence_gate.limiting_message}
                                  </AlertDescription>
                                </Alert>
                              )}

                              {decisionDiscipline.confidence_gate.restricted_outputs.length > 0 && (
                                <div className="mt-3">
                                  <div className="text-xs text-[#9FB0C7] mb-2">Restricted Outputs</div>
                                  <div className="flex flex-wrap gap-2">
                                    {decisionDiscipline.confidence_gate.restricted_outputs.map((output, idx) => (
                                      <Badge key={idx} variant="outline" className="border-[#7A8CA3]/30 text-[#7A8CA3] text-xs">
                                        {output}
                                      </Badge>
                                    ))}
                                  </div>
                                </div>
                              )}
                            </div>
                          )}

                          {decisionDiscipline.drl_details && (
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-3">Decision Readiness Level</div>
                              <div className="flex items-center gap-3 mb-3">
                                <div className={`text-lg font-bold ${
                                  decisionDiscipline.drl === 'drl_0' ? 'text-[#7A8CA3]' :
                                  decisionDiscipline.drl === 'drl_1' ? 'text-[#4F81BD]' :
                                  decisionDiscipline.drl === 'drl_2' ? 'text-[#F4B400]' :
                                  'text-[#F28C28]'
                                }`}>
                                  {decisionDiscipline.drl_details.name}
                                </div>
                                <Badge variant="outline" className="border-[#7A8CA3]/30 text-[#9FB0C7] text-xs">
                                  {decisionDiscipline.drl_details.posture}
                                </Badge>
                              </div>
                              <p className="text-sm text-[#C9D4E3] leading-relaxed mb-3">
                                {decisionDiscipline.drl_details.description}
                              </p>
                              <div className="bg-[#0B1220] rounded p-3">
                                <div className="text-xs text-[#9FB0C7] mb-1">Action Guidance</div>
                                <p className="text-sm text-white">{decisionDiscipline.drl_details.action_guidance}</p>
                              </div>
                            </div>
                          )}

                          {decisionDiscipline.context_aging && (
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="flex items-center justify-between mb-3">
                                <div className="text-xs text-[#9FB0C7]">Context Aging Status</div>
                                <Badge 
                                  variant="outline" 
                                  className={`${
                                    decisionDiscipline.context_aging.aging_status === 'stable' 
                                      ? 'border-[#3EC1C9]/50 text-[#3EC1C9]' 
                                      : decisionDiscipline.context_aging.aging_status === 'cooling'
                                      ? 'border-[#4F81BD]/50 text-[#4F81BD]'
                                      : decisionDiscipline.context_aging.aging_status === 'decaying'
                                      ? 'border-[#F4B400]/50 text-[#F4B400]'
                                      : 'border-[#7A8CA3]/50 text-[#7A8CA3]'
                                  }`}
                                >
                                  {decisionDiscipline.context_aging.aging_status.toUpperCase()}
                                </Badge>
                              </div>
                              
                              <p className="text-sm text-[#C9D4E3] leading-relaxed mb-3">
                                {decisionDiscipline.context_aging.aging_message}
                              </p>

                              <div className="grid grid-cols-3 gap-3">
                                <div className="bg-[#0B1220] rounded p-2">
                                  <div className="text-xs text-[#9FB0C7]">Days Since Signal</div>
                                  <div className="text-sm font-medium text-white">
                                    {decisionDiscipline.context_aging.days_since_last_signal}
                                  </div>
                                </div>
                                <div className="bg-[#0B1220] rounded p-2">
                                  <div className="text-xs text-[#9FB0C7]">Decay Rate</div>
                                  <div className="text-sm font-medium text-white">
                                    {(decisionDiscipline.context_aging.decay_rate * 100).toFixed(1)}%
                                  </div>
                                </div>
                                <div className="bg-[#0B1220] rounded p-2">
                                  <div className="text-xs text-[#9FB0C7]">Velocity Trend</div>
                                  <div className="text-sm font-medium text-white">
                                    {decisionDiscipline.context_aging.velocity_trend}
                                  </div>
                                </div>
                              </div>

                              {decisionDiscipline.context_aging.removal_warning && (
                                <Alert className="mt-3 bg-[#0B1220] border-[#F4B400]/30">
                                  <AlertTriangle className="h-4 w-4 text-[#F4B400]" />
                                  <AlertDescription className="text-[#F4B400] text-sm">
                                    {decisionDiscipline.context_aging.removal_explanation || 'Context may be removed due to prolonged inactivity'}
                                  </AlertDescription>
                                </Alert>
                              )}
                            </div>
                          )}

                          {decisionDiscipline.explainability_panels && decisionDiscipline.explainability_panels.length > 0 && (
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-3">Explainability Panels</div>
                              <div className="space-y-2">
                                {decisionDiscipline.explainability_panels.map((panel, idx) => (
                                  <div key={idx} className="bg-[#0B1220] rounded-lg border border-[#16233A]">
                                    <button
                                      onClick={() => setExpandedExplainability(
                                        expandedExplainability === `${panel.panel_type}-${idx}` ? null : `${panel.panel_type}-${idx}`
                                      )}
                                      className="w-full p-3 flex items-center justify-between text-left hover:bg-[#16233A]/50 transition-colors rounded-lg"
                                    >
                                      <div className="flex items-center gap-2">
                                        <Info className="h-4 w-4 text-[#4F81BD]" />
                                        <span className="text-sm text-white">Why this is shown: {panel.panel_title}</span>
                                      </div>
                                      {expandedExplainability === `${panel.panel_type}-${idx}` ? (
                                        <ChevronUp className="h-4 w-4 text-[#9FB0C7]" />
                                      ) : (
                                        <ChevronDown className="h-4 w-4 text-[#9FB0C7]" />
                                      )}
                                    </button>
                                    
                                    {expandedExplainability === `${panel.panel_type}-${idx}` && (
                                      <div className="px-3 pb-3 space-y-3">
                                        <p className="text-sm text-[#C9D4E3] leading-relaxed">{panel.summary}</p>
                                        
                                        {panel.triggering_factors.length > 0 && (
                                          <div>
                                            <div className="text-xs text-[#9FB0C7] mb-2">Triggering Factors</div>
                                            <div className="space-y-1">
                                              {panel.triggering_factors.map((factor, fidx) => (
                                                <div key={fidx} className="flex items-start gap-2 text-sm">
                                                  <div className="w-1.5 h-1.5 rounded-full bg-[#3EC1C9] mt-1.5 flex-shrink-0" />
                                                  <span className="text-[#C9D4E3]">{factor.factor_description}</span>
                                                </div>
                                              ))}
                                            </div>
                                          </div>
                                        )}

                                        {panel.non_triggering_factors.length > 0 && (
                                          <div>
                                            <div className="text-xs text-[#9FB0C7] mb-2">Non-Triggering Factors</div>
                                            <div className="space-y-1">
                                              {panel.non_triggering_factors.map((factor, fidx) => (
                                                <div key={fidx} className="flex items-start gap-2 text-sm">
                                                  <div className="w-1.5 h-1.5 rounded-full bg-[#7A8CA3] mt-1.5 flex-shrink-0" />
                                                  <span className="text-[#9FB0C7]">{factor.factor_description}</span>
                                                </div>
                                              ))}
                                            </div>
                                          </div>
                                        )}

                                        {panel.explicit_non_claims.length > 0 && (
                                          <div>
                                            <div className="text-xs text-[#9FB0C7] mb-2">What This Does NOT Claim</div>
                                            <div className="space-y-1">
                                              {panel.explicit_non_claims.map((claim, cidx) => (
                                                <div key={cidx} className="flex items-start gap-2 text-sm">
                                                  <div className="w-1.5 h-1.5 rounded-full bg-[#F4B400] mt-1.5 flex-shrink-0" />
                                                  <span className="text-[#F4B400]/80">{claim}</span>
                                                </div>
                                              ))}
                                            </div>
                                          </div>
                                        )}

                                        <div className="text-xs text-[#9FB0C7] italic pt-2 border-t border-[#16233A]">
                                          {panel.confidence_note}
                                        </div>
                                      </div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {decisionDiscipline.decision_discipline && (
                            <>
                              <div className="bg-[#16233A] rounded-lg p-4">
                                <div className="text-xs text-[#9FB0C7] mb-3">Restraint Indicators</div>
                                <div className="flex flex-wrap gap-2">
                                  {decisionDiscipline.decision_discipline.restraint_indicators.map((indicator, idx) => (
                                    <Badge key={idx} variant="outline" className="border-[#4F81BD]/30 text-[#4F81BD] text-xs">
                                      {indicator}
                                    </Badge>
                                  ))}
                                </div>
                              </div>

                              <Alert className="bg-[#0B1220] border-[#4F81BD]/30">
                                <Shield className="h-4 w-4 text-[#4F81BD]" />
                                <AlertTitle className="text-[#4F81BD] text-sm">Decision Discipline Posture</AlertTitle>
                                <AlertDescription className="text-[#9FB0C7] text-xs">
                                  {decisionDiscipline.decision_discipline.overall_discipline_posture}
                                </AlertDescription>
                              </Alert>

                              <Alert className="bg-[#0B1220] border-[#F4B400]/30">
                                <Lock className="h-4 w-4 text-[#F4B400]" />
                                <AlertTitle className="text-[#F4B400] text-sm">Master Disclaimer</AlertTitle>
                                <AlertDescription className="text-[#9FB0C7] text-xs">
                                  {decisionDiscipline.decision_discipline.master_disclaimer}
                                </AlertDescription>
                              </Alert>
                            </>
                          )}

                          {decisionDiscipline.governance_compliance && decisionDiscipline.governance_compliance.length > 0 && (
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-xs text-[#9FB0C7] mb-3">Governance Compliance</div>
                              <div className="flex flex-wrap gap-2">
                                {decisionDiscipline.governance_compliance.map((item, idx) => (
                                  <Badge key={idx} variant="outline" className="border-[#3EC1C9]/30 text-[#3EC1C9] text-xs">
                                    {item}
                                  </Badge>
                                ))}
                              </div>
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    )}
                  </TabsContent>

                  <TabsContent value="signals" className="space-y-4">
                    <Card className="bg-[#121C2D] border-[#16233A]">
                      <CardHeader>
                        <CardTitle className="text-lg text-white">Probability Trend</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="h-64">
                          <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={historyData}>
                              <CartesianGrid strokeDasharray="3 3" stroke="#16233A" />
                              <XAxis dataKey="timestamp" stroke="#9FB0C7" fontSize={12} />
                              <YAxis domain={[0, 100]} stroke="#9FB0C7" fontSize={12} />
                              <Tooltip
                                contentStyle={{ backgroundColor: '#121C2D', border: '1px solid #16233A' }}
                                labelStyle={{ color: '#9FB0C7' }}
                              />
                              <Area
                                type="monotone"
                                dataKey="probability"
                                stroke="#4F81BD"
                                fill="#4F81BD"
                                fillOpacity={0.2}
                              />
                            </AreaChart>
                          </ResponsiveContainer>
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="bg-[#121C2D] border-[#16233A]">
                      <CardHeader>
                        <CardTitle className="text-lg text-white">Domain Coverage</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="grid grid-cols-3 gap-4">
                          {Object.entries(selectedThreat.probability_curve.domain_coverage).map(([domain, count]) => {
                            const domainColors = DOMAIN_COLORS[domain] || DOMAIN_COLORS.social_discourse;
                            return (
                            <div key={domain} className={`bg-[#16233A] rounded-lg p-4 border-l-4`} style={{ borderLeftColor: domainColors.accent }}>
                              <div className={`text-sm mb-1 ${domainColors.text}`}>{DOMAIN_LABELS[domain] || domain}</div>
                              <div className="text-2xl font-bold text-white">{count}</div>
                              <div className="text-xs text-[#9FB0C7]">signals</div>
                            </div>
                            );
                          })}
                        </div>
                      </CardContent>
                    </Card>

                    <Card className="bg-[#121C2D] border-[#16233A]">
                      <CardHeader>
                        <CardTitle className="text-lg text-white">Contributing Signals</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          {selectedThreat.signals.map((signal) => {
                            const domainColors = DOMAIN_COLORS[signal.domain] || DOMAIN_COLORS.social_discourse;
                            const confidenceOpacity = getConfidenceOpacity(signal.raw_confidence);
                            return (
                            <div key={signal.id} className={`bg-[#16233A] rounded-lg p-4 border-l-4 ${confidenceOpacity}`} style={{ borderLeftColor: domainColors.accent }}>
                              <div className="flex items-start justify-between mb-2">
                                <div>
                                  <Badge className={`mb-2 ${domainColors.bg} ${domainColors.text} ${domainColors.border}`}>
                                    {DOMAIN_LABELS[signal.domain] || signal.domain}
                                  </Badge>
                                  <h4 className="font-medium text-white">{signal.signal_type.replace(/_/g, ' ')}</h4>
                                </div>
                                <div className="text-right">
                                  <div className={`text-lg font-bold ${domainColors.text}`}>
                                    {(signal.raw_confidence * 100).toFixed(0)}%
                                  </div>
                                  <div className="text-xs text-[#9FB0C7]">confidence</div>
                                </div>
                              </div>
                              <p className="text-sm text-[#9FB0C7] mb-2">{signal.source_description}</p>
                              <p className="text-sm text-[#C9D4E3]">{signal.reasoning}</p>
                              <div className="flex items-center gap-4 mt-2 text-xs text-[#9FB0C7]">
                                <span>Weight: {signal.weight.toFixed(2)}</span>
                                <span>{formatDate(signal.timestamp)}</span>
                              </div>
                            </div>
                            );
                          })}
                        </div>
                      </CardContent>
                    </Card>
                  </TabsContent>

                  <TabsContent value="gradient" className="space-y-4">
                    <Card className="bg-[#121C2D] border-[#16233A]">
                      <CardHeader>
                        <div className="flex items-start justify-between">
                          <div>
                            <CardTitle className="text-lg text-white">Intent Gradient Visualization</CardTitle>
                            <CardDescription className="text-[#9FB0C7]">
                              Threat evolution modeled as a continuous gradient across four stages
                            </CardDescription>
                          </div>
                          <div className="flex items-center gap-3 text-xs">
                            <div className="flex items-center gap-1.5">
                              <div className="w-2.5 h-2.5 rounded-full bg-[#4F81BD]" />
                              <span className="text-[#9FB0C7]">Stage 1</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                              <div className="w-2.5 h-2.5 rounded-full bg-[#F4B400]" />
                              <span className="text-[#9FB0C7]">Stage 2</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                              <div className="w-2.5 h-2.5 rounded-full bg-[#F28C28]" />
                              <span className="text-[#9FB0C7]">Stage 3</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                              <div className="w-2.5 h-2.5 rounded-full bg-[#E5533D]" />
                              <span className="text-[#9FB0C7]">Stage 4</span>
                            </div>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-6">
                          <div className="grid grid-cols-4 gap-2">
                            {[
                              { key: 'grievance_formation', score: selectedThreat.intent_gradient.stage_1_score, label: 'Grievance Formation' },
                              { key: 'cognitive_fixation', score: selectedThreat.intent_gradient.stage_2_score, label: 'Cognitive Fixation' },
                              { key: 'behavioral_acceleration', score: selectedThreat.intent_gradient.stage_3_score, label: 'Behavioral Acceleration' },
                              { key: 'mobilization_risk', score: selectedThreat.intent_gradient.stage_4_score, label: 'Mobilization Risk' },
                            ].map((stage, idx) => {
                              const stageColors = INTENT_STAGE_COLORS[stage.key] || INTENT_STAGE_COLORS.grievance_formation;
                              const isCurrentStage = selectedThreat.intent_gradient.current_stage === stage.key;
                              return (
                              <div
                                key={stage.key}
                                className={`p-4 rounded-lg border-2 ${
                                  isCurrentStage
                                    ? `${stageColors.bg} border-l-4`
                                    : 'bg-[#16233A] border-[#16233A]'
                                }`}
                                style={isCurrentStage ? { borderLeftColor: stageColors.accent } : {}}
                              >
                                <div className={`text-xs mb-1 ${isCurrentStage ? stageColors.text : 'text-[#9FB0C7]'}`}>Stage {idx + 1}</div>
                                <div className={`font-medium text-sm mb-2 ${isCurrentStage ? 'text-white' : 'text-[#C9D4E3]'}`}>{stage.label}</div>
                                <Progress value={stage.score * 100} className="h-2 mb-1" style={{ '--progress-color': stageColors.accent } as React.CSSProperties} />
                                <div className={`text-xs ${isCurrentStage ? stageColors.text : 'text-[#9FB0C7]'}`}>{(stage.score * 100).toFixed(0)}%</div>
                              </div>
                              );
                            })}
                          </div>

                          <div className="grid grid-cols-3 gap-4">
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-sm text-[#9FB0C7] mb-1">Stage Confidence</div>
                              <div className={`text-2xl font-bold text-white ${getConfidenceOpacity(selectedThreat.intent_gradient.stage_confidence)}`}>
                                {(selectedThreat.intent_gradient.stage_confidence * 100).toFixed(0)}%
                              </div>
                            </div>
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-sm text-[#9FB0C7] mb-1">Velocity</div>
                              <div className={`text-2xl font-bold text-white ${getVelocityStyle(selectedThreat.intent_gradient.velocity)}`}>
                                {selectedThreat.intent_gradient.velocity > 0 ? '+' : ''}
                                {(selectedThreat.intent_gradient.velocity * 100).toFixed(1)}%
                              </div>
                            </div>
                            <div className="bg-[#16233A] rounded-lg p-4">
                              <div className="text-sm text-[#9FB0C7] mb-1">Time in Stage</div>
                              <div className="text-2xl font-bold text-white">
                                {selectedThreat.intent_gradient.time_in_stage.toFixed(1)}h
                              </div>
                            </div>
                          </div>
                        </div>
                      </CardContent>
                    </Card>

                    {selectedThreat.historical_analogs.length > 0 && (
                      <Card className="bg-[#121C2D] border-[#16233A]">
                        <CardHeader>
                          <CardTitle className="text-lg text-white">Historical Analogs</CardTitle>
                          <CardDescription className="text-[#9FB0C7]">
                            Similar historical patterns for context and lessons learned
                          </CardDescription>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-4">
                            {selectedThreat.historical_analogs.map((analog, idx) => (
                              <div key={idx} className="bg-[#16233A] rounded-lg p-4">
                                <div className="flex items-start justify-between mb-2">
                                  <div>
                                    <h4 className="font-medium text-white">{analog.name}</h4>
                                    <div className="text-xs text-[#9FB0C7]">{analog.date_range}</div>
                                  </div>
                                  <Badge className="bg-[#4F81BD]/10 text-[#4F81BD] border-[#4F81BD]/30">
                                    {(analog.similarity_score * 100).toFixed(0)}% similar
                                  </Badge>
                                </div>
                                <p className="text-sm text-[#9FB0C7] mb-2">{analog.description}</p>
                                <div className="grid grid-cols-2 gap-4 mt-3">
                                  <div>
                                    <div className="text-xs text-[#9FB0C7] mb-1">Outcome</div>
                                    <p className="text-sm text-[#C9D4E3]">{analog.outcome}</p>
                                  </div>
                                  <div>
                                    <div className="text-xs text-[#9FB0C7] mb-1">Lessons Learned</div>
                                    <p className="text-sm text-[#C9D4E3]">{analog.lessons_learned}</p>
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </CardContent>
                      </Card>
                    )}
                  </TabsContent>

                  <TabsContent value="feedback" className="space-y-4">
                    <Card className="bg-[#121C2D] border-[#16233A]">
                      <CardHeader>
                        <CardTitle className="text-lg text-white">Submit Analyst Feedback</CardTitle>
                        <CardDescription className="text-[#9FB0C7]">
                          Provide feedback to improve future convergence logic. Feedback is logged but never overrides historical data.
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div>
                          <label className="text-sm text-[#9FB0C7] mb-2 block">Feedback Type</label>
                          <Select value={feedbackType} onValueChange={setFeedbackType}>
                            <SelectTrigger className="bg-[#16233A] border-[#16233A] text-[#C9D4E3]">
                              <SelectValue placeholder="Select feedback type" />
                            </SelectTrigger>
                            <SelectContent className="bg-[#16233A] border-[#16233A]">
                              <SelectItem value="weight_adjustment" className="text-[#C9D4E3]">Weight Adjustment</SelectItem>
                              <SelectItem value="stage_correction" className="text-[#C9D4E3]">Stage Correction</SelectItem>
                              <SelectItem value="signal_validation" className="text-[#C9D4E3]">Signal Validation</SelectItem>
                              <SelectItem value="confidence_adjustment" className="text-[#C9D4E3]">Confidence Adjustment</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div>
                          <label className="text-sm text-[#9FB0C7] mb-2 block">Rationale</label>
                          <Textarea
                            value={feedbackRationale}
                            onChange={(e) => setFeedbackRationale(e.target.value)}
                            placeholder="Explain your reasoning for this feedback..."
                            className="bg-[#16233A] border-[#16233A] text-[#C9D4E3] min-h-32 placeholder:text-[#9FB0C7]/50"
                          />
                        </div>
                        <Button onClick={submitFeedback} disabled={!feedbackType || !feedbackRationale} className="bg-[#4F81BD] hover:bg-[#4F81BD]/80 text-white">
                          Submit Feedback
                        </Button>
                      </CardContent>
                    </Card>

                    <Alert className="bg-[#16233A] border-[#16233A]">
                      <Clock className="h-4 w-4 text-[#4F81BD]" />
                      <AlertTitle className="text-white">Human-in-the-Loop System</AlertTitle>
                      <AlertDescription className="text-[#C9D4E3]">
                        All feedback is logged with full audit trail. Feedback adjusts future weighting and convergence logic
                        but never modifies or overrides historical data. This ensures full accountability and explainability.
                      </AlertDescription>
                    </Alert>
                  </TabsContent>
                </Tabs>
              </div>
            ) : (
              <Card className="bg-[#121C2D] border-[#16233A]">
                <CardContent className="flex items-center justify-center h-96">
                  <div className="text-center text-[#9FB0C7]">
                    <Shield className="h-16 w-16 mx-auto mb-4 opacity-50 text-[#4F81BD]" />
                    <p>Select a threat from the list to view details</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>

      <footer className="border-t border-[#16233A] bg-[#121C2D]/50 py-4 mt-8">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between text-xs text-[#9FB0C7]">
            <div>AURORA Decision Intelligence Simulation v1.0.0-mvp | Global 3 Technology & Intelligence (G3TI)</div>
            <div>Pre-Patent Demo Environment | Synthetic Data Only | Full Audit Trail</div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App
