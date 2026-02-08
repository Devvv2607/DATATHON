'use client';

import { useState, useEffect } from 'react';
import { Zap, Target, TrendingUp, AlertTriangle, Settings, Activity, DollarSign, Shield, Info } from 'lucide-react';
import { useDomain } from '@/contexts/DomainContext';
import DomainAndTrendSelector from '@/components/DomainAndTrendSelector';

export default function WhatIfSimulatorPage() {
  const [loading, setLoading] = useState(false);
  const [simulation, setSimulation] = useState<any>(null);
  const { selectedDomain, selectedTrend } = useDomain();
  
  // Campaign Strategy inputs
  const [campaignType, setCampaignType] = useState('mixed');
  const [budgetRange, setBudgetRange] = useState('medium');
  const [duration, setDuration] = useState(30);
  const [creatorTier, setCreatorTier] = useState('mixed');
  const [contentIntensity, setContentIntensity] = useState('medium');
  
  // Assumptions inputs
  const [engagementTrend, setEngagementTrend] = useState('neutral');
  const [creatorParticipation, setCreatorParticipation] = useState('stable');
  const [marketNoise, setMarketNoise] = useState('medium');
  
  // Constraints inputs
  const [riskTolerance, setRiskTolerance] = useState('medium');
  const [maxBudgetCap, setMaxBudgetCap] = useState(50000);
  
  // UI state
  const [showAdvanced, setShowAdvanced] = useState(false);

  const runSimulation = async () => {
    setLoading(true);
    try {
      // Convert budget range string to min/max object
      const budgetRangeMap: Record<string, {min: number, max: number}> = {
        'low': { min: 1000, max: 5000 },
        'medium': { min: 10000, max: 50000 },
        'high': { min: 50000, max: 200000 }
      };
      
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `http://localhost:8000/api/business/what-if-simulator?domain=${selectedDomain}&trend_id=${selectedTrend}&include_executive_summary=true`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            scenario_id: `${selectedTrend}_${Date.now()}`,
            campaign_type: campaignType,
            budget_range: budgetRangeMap[budgetRange],
            campaign_duration_days: duration,
            creator_tier: creatorTier,
            content_intensity: contentIntensity,
            engagement_trend: engagementTrend,
            creator_participation: creatorParticipation,
            market_noise: marketNoise,
            risk_tolerance: riskTolerance,
            max_budget_cap: maxBudgetCap
          })
        }
      );
      const data = await response.json();
      console.log('Simulation response:', JSON.stringify(data, null, 2));
      setSimulation(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (preset: string) => {
    if (preset === 'conservative') {
      setCampaignType('organic_only');
      setBudgetRange('low');
      setDuration(14);
      setCreatorTier('nano');
      setContentIntensity('low');
      setEngagementTrend('pessimistic');
      setCreatorParticipation('declining');
      setMarketNoise('high');
      setRiskTolerance('low');
      setMaxBudgetCap(10000);
    } else if (preset === 'balanced') {
      setCampaignType('mixed');
      setBudgetRange('medium');
      setDuration(30);
      setCreatorTier('mixed');
      setContentIntensity('medium');
      setEngagementTrend('neutral');
      setCreatorParticipation('stable');
      setMarketNoise('medium');
      setRiskTolerance('medium');
      setMaxBudgetCap(50000);
    } else if (preset === 'aggressive') {
      setCampaignType('long_term_paid');
      setBudgetRange('high');
      setDuration(60);
      setCreatorTier('macro');
      setContentIntensity('high');
      setEngagementTrend('optimistic');
      setCreatorParticipation('increasing');
      setMarketNoise('low');
      setRiskTolerance('high');
      setMaxBudgetCap(100000);
    }
  };

  const getPostureColor = (posture: string) => {
    switch (posture?.toLowerCase()) {
      case 'scale': return 'text-green-400';
      case 'test_small': return 'text-blue-400';
      case 'monitor': return 'text-yellow-400';
      case 'avoid': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getPostureIcon = (posture: string) => {
    switch (posture?.toLowerCase()) {
      case 'scale': return <Target className="w-6 h-6 text-green-400" />;
      case 'test_small': return <Activity className="w-6 h-6 text-blue-400" />;
      case 'monitor': return <Shield className="w-6 h-6 text-yellow-400" />;
      case 'avoid': return <AlertTriangle className="w-6 h-6 text-red-400" />;
      default: return <Info className="w-6 h-6 text-gray-400" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text flex items-center gap-3">
            <Zap className="w-8 h-8 text-blue-400" />
            What-If Simulator
          </h1>
          <p className="text-gray-400 mt-2">
            Campaign scenario planning with risk-adjusted projections
          </p>
        </div>
        <button
          onClick={runSimulation}
          disabled={loading}
          className="px-6 py-3 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:opacity-90 transition-all duration-300 disabled:opacity-50"
        >
          {loading ? 'Simulating...' : 'Run Simulation'}
        </button>
      </div>

      <DomainAndTrendSelector />

      {/* Preset Scenarios */}
      <div className="glass-card p-4 rounded-2xl">
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-400">Quick Presets:</span>
          <button
            onClick={() => loadPreset('conservative')}
            className="px-4 py-2 rounded-lg bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 transition-all"
          >
            🛡️ Conservative
          </button>
          <button
            onClick={() => loadPreset('balanced')}
            className="px-4 py-2 rounded-lg bg-purple-500/10 text-purple-400 hover:bg-purple-500/20 transition-all"
          >
            ⚖️ Balanced
          </button>
          <button
            onClick={() => loadPreset('aggressive')}
            className="px-4 py-2 rounded-lg bg-green-500/10 text-green-400 hover:bg-green-500/20 transition-all"
          >
            🚀 Aggressive
          </button>
        </div>
      </div>

      {/* Input Configuration Panel */}
      <div className="glass-card p-6 rounded-2xl">
        <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <Settings className="w-6 h-6 text-blue-400" />
          Scenario Configuration
        </h2>

        {/* Campaign Strategy Section */}
        <div className="space-y-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-300 border-b border-gray-700 pb-2">
            Campaign Strategy
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-sm text-gray-400 mb-2 block">Campaign Type</label>
              <select
                value={campaignType}
                onChange={(e) => setCampaignType(e.target.value)}
                className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
              >
                <option value="short_term_influencer">Short-term Influencer</option>
                <option value="long_term_paid">Long-term Paid</option>
                <option value="organic_only">Organic Only</option>
                <option value="mixed">Mixed</option>
              </select>
            </div>

            <div>
              <label className="text-sm text-gray-400 mb-2 block">Budget Range</label>
              <select
                value={budgetRange}
                onChange={(e) => setBudgetRange(e.target.value)}
                className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
              >
                <option value="low">Low ($1K-$10K)</option>
                <option value="medium">Medium ($10K-$50K)</option>
                <option value="high">High ($50K+)</option>
              </select>
            </div>

            <div>
              <label className="text-sm text-gray-400 mb-2 block">Campaign Duration (Days)</label>
              <input
                type="number"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                min="7"
                max="180"
                className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="text-sm text-gray-400 mb-2 block">Creator Tier</label>
              <select
                value={creatorTier}
                onChange={(e) => setCreatorTier(e.target.value)}
                className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
              >
                <option value="nano">Nano (1K-10K)</option>
                <option value="micro">Micro (10K-100K)</option>
                <option value="macro">Macro (100K+)</option>
                <option value="mixed">Mixed</option>
              </select>
            </div>

            <div>
              <label className="text-sm text-gray-400 mb-2 block">Content Intensity</label>
              <select
                value={contentIntensity}
                onChange={(e) => setContentIntensity(e.target.value)}
                className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
              >
                <option value="low">Low (1-2 posts/week)</option>
                <option value="medium">Medium (3-5 posts/week)</option>
                <option value="high">High (Daily+)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Advanced Options Toggle */}
        <button
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-blue-400 hover:text-blue-300 text-sm mb-4 flex items-center gap-2"
        >
          {showAdvanced ? '▼' : '▶'} Advanced Options (Assumptions & Constraints)
        </button>

        {showAdvanced && (
          <>
            {/* Assumptions Section */}
            <div className="space-y-6 mb-8">
              <h3 className="text-lg font-semibold text-gray-300 border-b border-gray-700 pb-2">
                Market Assumptions
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Engagement Trend</label>
                  <select
                    value={engagementTrend}
                    onChange={(e) => setEngagementTrend(e.target.value)}
                    className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
                  >
                    <option value="optimistic">Optimistic (Growing)</option>
                    <option value="neutral">Neutral (Stable)</option>
                    <option value="pessimistic">Pessimistic (Declining)</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Creator Participation</label>
                  <select
                    value={creatorParticipation}
                    onChange={(e) => setCreatorParticipation(e.target.value)}
                    className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
                  >
                    <option value="increasing">Increasing</option>
                    <option value="stable">Stable</option>
                    <option value="declining">Declining</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Market Noise</label>
                  <select
                    value={marketNoise}
                    onChange={(e) => setMarketNoise(e.target.value)}
                    className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
                  >
                    <option value="low">Low (Clear signal)</option>
                    <option value="medium">Medium</option>
                    <option value="high">High (Noisy market)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Constraints Section */}
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-gray-300 border-b border-gray-700 pb-2">
                Business Constraints
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Risk Tolerance</label>
                  <select
                    value={riskTolerance}
                    onChange={(e) => setRiskTolerance(e.target.value)}
                    className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
                  >
                    <option value="low">Low (Conservative)</option>
                    <option value="medium">Medium (Balanced)</option>
                    <option value="high">High (Aggressive)</option>
                  </select>
                </div>

                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Max Budget Cap ($)</label>
                  <input
                    type="number"
                    value={maxBudgetCap}
                    onChange={(e) => setMaxBudgetCap(Number(e.target.value))}
                    min="1000"
                    max="1000000"
                    step="1000"
                    className="w-full p-3 rounded-lg bg-slate-800 text-white border border-slate-700 focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Validation Errors */}
      {simulation?.success === false && simulation?.validation_failures && (
        <div className="glass-card p-6 rounded-2xl bg-red-500/10 border border-red-500/20">
          <div className="flex items-center gap-3 mb-4">
            <AlertTriangle className="w-6 h-6 text-red-400" />
            <h2 className="text-xl font-bold text-red-400">Validation Errors</h2>
          </div>
          <div className="space-y-3">
            {simulation.validation_failures.map((failure: any, i: number) => (
              <div key={i} className="p-4 rounded-lg bg-red-500/5 border border-red-500/10">
                <div className="font-semibold text-red-400">{failure.field}</div>
                <div className="text-gray-300 text-sm mt-1">{failure.message}</div>
                {failure.guidance && (
                  <div className="text-gray-400 text-xs mt-2 italic">{failure.guidance}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Generic Error */}
      {simulation?.success === false && simulation?.error && !simulation?.validation_failures && (
        <div className="glass-card p-6 rounded-2xl bg-red-500/10 border border-red-500/20">
          <div className="flex items-center gap-3 mb-2">
            <AlertTriangle className="w-6 h-6 text-red-400" />
            <h2 className="text-xl font-bold text-red-400">Simulation Error</h2>
          </div>
          <p className="text-gray-300">{simulation.error}</p>
        </div>
      )}

      {/* Results Display */}
      {simulation?.success && simulation?.simulation && (
        <>
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* Recommended Posture */}
            <div className="glass-card p-6 rounded-2xl">
              <div className="flex items-center gap-3 mb-4">
                {getPostureIcon(simulation.simulation.decision_interpretation?.recommended_posture)}
                <div className="text-sm text-gray-400">Strategic Posture</div>
              </div>
              <div className={`text-2xl font-bold capitalize ${getPostureColor(simulation.simulation.decision_interpretation?.recommended_posture)}`}>
                {simulation.simulation.decision_interpretation?.recommended_posture?.replace('_', ' ')}
              </div>
            </div>

            {/* ROI Range */}
            <div className="glass-card p-6 rounded-2xl">
              <div className="flex items-center gap-3 mb-4">
                <DollarSign className="w-6 h-6 text-green-400" />
                <div className="text-sm text-gray-400">ROI Range</div>
              </div>
              <div className="text-2xl font-bold text-green-400">
                {simulation.simulation.expected_roi_metrics?.roi_percent?.min?.toFixed(1)}% - 
                {simulation.simulation.expected_roi_metrics?.roi_percent?.max?.toFixed(1)}%
              </div>
              <div className="text-xs text-gray-500 mt-2">
                Break-even: {simulation.simulation.expected_roi_metrics?.break_even_probability}
              </div>
            </div>

            {/* Engagement Growth */}
            <div className="glass-card p-6 rounded-2xl">
              <div className="flex items-center gap-3 mb-4">
                <TrendingUp className="w-6 h-6 text-blue-400" />
                <div className="text-sm text-gray-400">Engagement Growth</div>
              </div>
              <div className="text-2xl font-bold text-blue-400">
                {simulation.simulation.expected_growth_metrics?.engagement_growth_percent?.min?.toFixed(0)}% - 
                {simulation.simulation.expected_growth_metrics?.engagement_growth_percent?.max?.toFixed(0)}%
              </div>
            </div>

            {/* Risk Projection */}
            <div className="glass-card p-6 rounded-2xl">
              <div className="flex items-center gap-3 mb-4">
                <Shield className="w-6 h-6 text-orange-400" />
                <div className="text-sm text-gray-400">Risk Trend</div>
              </div>
              <div className={`text-2xl font-bold capitalize ${
                simulation.simulation.risk_projection?.risk_trend === 'improving' ? 'text-green-400' :
                simulation.simulation.risk_projection?.risk_trend === 'worsening' ? 'text-red-400' :
                'text-yellow-400'
              }`}>
                {simulation.simulation.risk_projection?.risk_trend}
              </div>
              <div className="text-xs text-gray-500 mt-2">
                Current: {simulation.simulation.risk_projection?.current_risk_score?.toFixed(0)}
              </div>
            </div>
          </div>

          {/* Detailed Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Growth Projections */}
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-400" />
                Growth Projections
              </h3>
              <div className="space-y-4">
                <div className="p-4 rounded-lg bg-slate-800/50">
                  <div className="text-sm text-gray-400 mb-1">Engagement Growth</div>
                  <div className="text-xl font-bold text-blue-400">
                    {simulation.simulation.expected_growth_metrics?.engagement_growth_percent?.min?.toFixed(1)}% - 
                    {simulation.simulation.expected_growth_metrics?.engagement_growth_percent?.max?.toFixed(1)}%
                  </div>
                </div>
                <div className="p-4 rounded-lg bg-slate-800/50">
                  <div className="text-sm text-gray-400 mb-1">Reach Growth</div>
                  <div className="text-xl font-bold text-purple-400">
                    {simulation.simulation.expected_growth_metrics?.reach_growth_percent?.min?.toFixed(1)}% - 
                    {simulation.simulation.expected_growth_metrics?.reach_growth_percent?.max?.toFixed(1)}%
                  </div>
                </div>
                <div className="p-4 rounded-lg bg-slate-800/50">
                  <div className="text-sm text-gray-400 mb-1">Creator Participation Change</div>
                  <div className="text-xl font-bold text-green-400">
                    {simulation.simulation.expected_growth_metrics?.creator_participation_change_percent?.min?.toFixed(1)}% - 
                    {simulation.simulation.expected_growth_metrics?.creator_participation_change_percent?.max?.toFixed(1)}%
                  </div>
                </div>
              </div>
            </div>

            {/* Decision Interpretation */}
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <Target className="w-5 h-5 text-green-400" />
                Strategic Recommendations
              </h3>
              
              {simulation.simulation.decision_interpretation?.primary_opportunities?.length > 0 && (
                <div className="mb-4">
                  <div className="text-sm text-green-400 font-semibold mb-2">✓ Opportunities</div>
                  <ul className="space-y-2">
                    {simulation.simulation.decision_interpretation.primary_opportunities.map((opp: string, i: number) => (
                      <li key={i} className="text-gray-300 text-sm pl-4 border-l-2 border-green-500/50">
                        {opp}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {simulation.simulation.decision_interpretation?.primary_risks?.length > 0 && (
                <div>
                  <div className="text-sm text-red-400 font-semibold mb-2">⚠️ Risks</div>
                  <ul className="space-y-2">
                    {simulation.simulation.decision_interpretation.primary_risks.map((risk: string, i: number) => (
                      <li key={i} className="text-gray-300 text-sm pl-4 border-l-2 border-red-500/50">
                        {risk}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Sensitivity Analysis */}
          {simulation.simulation.assumption_sensitivity && (
            <div className="glass-card p-6 rounded-2xl">
              <h3 className="text-lg font-bold text-white mb-4">Sensitivity Analysis</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-slate-800/50">
                  <div className="text-sm text-gray-400 mb-1">Most Sensitive Factor</div>
                  <div className="text-xl font-bold text-yellow-400 capitalize">
                    {simulation.simulation.assumption_sensitivity.most_sensitive_factor}
                  </div>
                </div>
                <div className="p-4 rounded-lg bg-slate-800/50">
                  <div className="text-sm text-gray-400 mb-1">Impact If Wrong</div>
                  <div className={`text-xl font-bold capitalize ${
                    simulation.simulation.assumption_sensitivity.impact_if_wrong === 'high' ? 'text-red-400' :
                    simulation.simulation.assumption_sensitivity.impact_if_wrong === 'medium' ? 'text-yellow-400' :
                    'text-green-400'
                  }`}>
                    {simulation.simulation.assumption_sensitivity.impact_if_wrong}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Executive Summary */}
          {simulation.simulation.executive_summary && (
            <div className="glass-card p-6 rounded-2xl">
              <h2 className="text-xl font-bold text-white mb-6">Executive Summary</h2>
              
              <div className="space-y-6">
                {/* Trend Analysis */}
                {simulation.simulation.executive_summary.trend_analysis && (
                  <div>
                    <h4 className="text-sm text-blue-400 font-semibold uppercase tracking-wider mb-2">Trend Analysis</h4>
                    <div className="text-gray-300 leading-relaxed space-y-2">
                      {typeof simulation.simulation.executive_summary.trend_analysis === 'string' ? (
                        <p>{simulation.simulation.executive_summary.trend_analysis}</p>
                      ) : (
                        <>
                          <p><strong>Stage:</strong> {simulation.simulation.executive_summary.trend_analysis.stage} ({simulation.simulation.executive_summary.trend_analysis.stage_description})</p>
                          <p><strong>Risk Level:</strong> {simulation.simulation.executive_summary.trend_analysis.risk_level} ({simulation.simulation.executive_summary.trend_analysis.current_risk_score?.toFixed(1)} score, {simulation.simulation.executive_summary.trend_analysis.risk_trend})</p>
                          <p className="italic">{simulation.simulation.executive_summary.trend_analysis.interpretation}</p>
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* Success Probability */}
                {simulation.simulation.executive_summary.success_probability && (
                  <div>
                    <h4 className="text-sm text-green-400 font-semibold uppercase tracking-wider mb-2">Success Probability</h4>
                    <div className="text-gray-300 leading-relaxed space-y-2">
                      {typeof simulation.simulation.executive_summary.success_probability === 'string' ? (
                        <p>{simulation.simulation.executive_summary.success_probability}</p>
                      ) : (
                        <>
                          <p><strong>Success Level:</strong> {simulation.simulation.executive_summary.success_probability.success_level}</p>
                          <p><strong>Break-even Probability:</strong> {simulation.simulation.executive_summary.success_probability.break_even_probability?.toFixed(0)}%</p>
                          <p><strong>Loss Probability:</strong> {simulation.simulation.executive_summary.success_probability.loss_probability?.toFixed(0)}%</p>
                          <p className="italic">{simulation.simulation.executive_summary.success_probability.interpretation}</p>
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* Financial Outlook */}
                {simulation.simulation.executive_summary.financial_outlook && (
                  <div>
                    <h4 className="text-sm text-purple-400 font-semibold uppercase tracking-wider mb-2">Financial Outlook</h4>
                    <div className="text-gray-300 leading-relaxed">
                      {typeof simulation.simulation.executive_summary.financial_outlook === 'string' ? (
                        <p>{simulation.simulation.executive_summary.financial_outlook}</p>
                      ) : (
                        <>
                          <p><strong>Outlook:</strong> {simulation.simulation.executive_summary.financial_outlook.outlook}</p>
                          <p className="italic">{simulation.simulation.executive_summary.financial_outlook.interpretation}</p>
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* Risk Assessment */}
                {simulation.simulation.executive_summary.risk_assessment && (
                  <div>
                    <h4 className="text-sm text-orange-400 font-semibold uppercase tracking-wider mb-2">Risk Assessment</h4>
                    <div className="text-gray-300 leading-relaxed">
                      {typeof simulation.simulation.executive_summary.risk_assessment === 'string' ? (
                        <p>{simulation.simulation.executive_summary.risk_assessment}</p>
                      ) : (
                        <>
                          <p><strong>Alignment:</strong> {simulation.simulation.executive_summary.risk_assessment.alignment_with_tolerance}</p>
                          <p className="italic">{simulation.simulation.executive_summary.risk_assessment.interpretation}</p>
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* Strategic Recommendation */}
                {simulation.simulation.executive_summary.strategic_recommendation && (
                  <div>
                    <h4 className="text-sm text-cyan-400 font-semibold uppercase tracking-wider mb-2">Strategic Recommendation</h4>
                    <div className="text-gray-300 leading-relaxed">
                      {typeof simulation.simulation.executive_summary.strategic_recommendation === 'string' ? (
                        <p>{simulation.simulation.executive_summary.strategic_recommendation}</p>
                      ) : (
                        <>
                          <p><strong>Posture:</strong> {simulation.simulation.executive_summary.strategic_recommendation.recommended_posture}</p>
                          <p className="italic">{simulation.simulation.executive_summary.strategic_recommendation.rationale}</p>
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* Key Drivers */}
                {simulation.simulation.executive_summary.key_drivers && (
                  <div>
                    <h4 className="text-sm text-yellow-400 font-semibold uppercase tracking-wider mb-2">Key Drivers</h4>
                    <div className="space-y-3">
                      {simulation.simulation.executive_summary.key_drivers.opportunities?.length > 0 && (
                        <div>
                          <p className="text-green-400 font-semibold mb-1">Opportunities:</p>
                          <ul className="list-disc list-inside text-gray-300 space-y-1">
                            {simulation.simulation.executive_summary.key_drivers.opportunities.map((item: string, i: number) => (
                              <li key={i}>{item}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      {simulation.simulation.executive_summary.key_drivers.risks?.length > 0 && (
                        <div>
                          <p className="text-red-400 font-semibold mb-1">Risks:</p>
                          <ul className="list-disc list-inside text-gray-300 space-y-1">
                            {simulation.simulation.executive_summary.key_drivers.risks.map((item: string, i: number) => (
                              <li key={i}>{item}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Critical Assumptions */}
                {simulation.simulation.executive_summary.critical_assumptions && (
                  <div>
                    <h4 className="text-sm text-pink-400 font-semibold uppercase tracking-wider mb-2">Critical Assumptions</h4>
                    <div className="text-gray-300">
                      {typeof simulation.simulation.executive_summary.critical_assumptions === 'string' ? (
                        <p>{simulation.simulation.executive_summary.critical_assumptions}</p>
                      ) : (
                        <ul className="list-disc list-inside space-y-1">
                          {simulation.simulation.executive_summary.critical_assumptions.assumptions?.map((item: string, i: number) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                )}

                {/* Action Items */}
                {simulation.simulation.executive_summary.action_items?.length > 0 && (
                  <div>
                    <h4 className="text-sm text-yellow-400 font-semibold uppercase tracking-wider mb-2">Action Items</h4>
                    <div className="space-y-3">
                      {simulation.simulation.executive_summary.action_items.map((item: any, i: number) => (
                        <div key={i} className="p-4 rounded-lg bg-slate-800/50 border-l-4 border-yellow-500">
                          {typeof item === 'string' ? (
                            <div className="flex items-start gap-2 text-gray-300">
                              <span className="text-yellow-400 mt-1">→</span>
                              <span>{item}</span>
                            </div>
                          ) : (
                            <>
                              <div className="flex items-center gap-2 mb-2">
                                <span className={`px-2 py-1 rounded text-xs font-semibold uppercase ${
                                  item.priority === 'high' ? 'bg-red-500/20 text-red-400' :
                                  item.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                  'bg-blue-500/20 text-blue-400'
                                }`}>
                                  {item.priority} Priority
                                </span>
                              </div>
                              <div className="text-white font-medium mb-1">{item.action}</div>
                              <div className="text-gray-400 text-sm italic">{item.rationale}</div>
                            </>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Guardrails */}
          {simulation.simulation.guardrails && (
            <div className="glass-card p-4 rounded-2xl bg-yellow-500/5 border border-yellow-500/20">
              <div className="flex items-center gap-2 text-yellow-400 text-sm">
                <Info className="w-4 h-4" />
                <span className="font-semibold">Note:</span>
                <span className="text-gray-400">
                  {simulation.simulation.guardrails.system_note} 
                  (Data Coverage: {(simulation.simulation.guardrails.data_coverage * 100).toFixed(0)}%)
                </span>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
