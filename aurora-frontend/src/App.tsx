import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { Separator } from '@/components/ui/separator';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertTriangle, TrendingUp, TrendingDown, Minus, Shield, Activity, FileText, MessageSquare, Clock, Target, Brain, Eye } from 'lucide-react';
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
}

interface JurisdictionListResponse {
  jurisdictions: JurisdictionSummary[];
  total: number;
  current_jurisdiction: string;
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

const getConfidenceOpacity = (confidence: number): string => {
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

  useEffect(() => {
    fetchThreats();
    fetchSystemStatus();
    fetchJurisdictions();
  }, []);

  useEffect(() => {
    if (selectedThreat) {
      fetchThreatHistory(selectedThreat.id);
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
                  <SelectTrigger className="w-48 h-8 bg-[#16233A] border-[#16233A] text-sm text-[#C9D4E3]">
                    <SelectValue placeholder="Select jurisdiction" />
                  </SelectTrigger>
                  <SelectContent className="bg-[#16233A] border-[#16233A] max-h-80">
                    {Object.entries(
                      jurisdictions.reduce((acc, j) => {
                        if (!acc[j.region]) acc[j.region] = [];
                        acc[j.region].push(j);
                        return acc;
                      }, {} as Record<string, JurisdictionSummary[]>)
                    ).map(([region, items]) => (
                      <div key={region}>
                        <div className="px-2 py-1 text-xs font-semibold text-[#9FB0C7] bg-[#121C2D]">{region}</div>
                        {items.map((j) => (
                          <SelectItem key={j.code} value={j.code} className="text-sm text-[#C9D4E3]">
                            {j.name}
                          </SelectItem>
                        ))}
                      </div>
                    ))}
                  </SelectContent>
                </Select>
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
