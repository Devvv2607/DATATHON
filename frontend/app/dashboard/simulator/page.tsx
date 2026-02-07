'use client';

import { useState } from 'react';
import { simulateIntervention, type SimulationResponse } from '@/lib/api';
import { Sliders, Play, RotateCcw, TrendingUp, DollarSign } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { formatCurrency } from '@/lib/utils';

export default function SimulatorPage() {
  const [simulation, setSimulation] = useState<SimulationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  
  // Intervention sliders state
  const [addInfluencers, setAddInfluencers] = useState(0);
  const [increaseNovelty, setIncreaseNovelty] = useState(0);
  const [expandPlatforms, setExpandPlatforms] = useState(0);
  const [boostEngagement, setBoostEngagement] = useState(0);

  const runSimulation = async () => {
    setLoading(true);
    const interventions: Record<string, number> = {};
    if (addInfluencers > 0) interventions.add_influencers = addInfluencers;
    if (increaseNovelty > 0) interventions.increase_content_novelty = increaseNovelty / 100;
    if (expandPlatforms > 0) interventions.expand_platforms = expandPlatforms;
    if (boostEngagement > 0) interventions.boost_engagement = boostEngagement / 10;

    const result = await simulateIntervention({
      trend_id: 'trend_1',
      interventions,
      forecast_days: 30
    });
    
    setSimulation(result);
    setLoading(false);
  };

  const resetSimulation = () => {
    setAddInfluencers(0);
    setIncreaseNovelty(0);
    setExpandPlatforms(0);
    setBoostEngagement(0);
    setSimulation(null);
  };

  // Combine baseline and intervention data for comparison chart
  const comparisonData = simulation
    ? simulation.baseline.trajectory.map((point, idx) => ({
        date: point.date,
        baseline: point.health_score,
        intervention: simulation.with_intervention.trajectory[idx]?.health_score || 0
      }))
    : [];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">What-If Simulator</h1>
        <p className="text-gray-400">Model intervention outcomes and predict impact on trend health</p>
      </div>

      {/* Control Panel */}
      <div className="rounded-xl border border-white/10 bg-gradient-to-br from-purple-950/30 to-blue-950/20 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-6">
          <Sliders className="w-6 h-6 text-purple-400" />
          <h2 className="text-2xl font-bold text-white">Intervention Controls</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Add Influencers */}
          <div>
            <div className="flex justify-between mb-3">
              <label className="text-sm font-medium text-gray-300">Add Influencers</label>
              <span className="text-sm font-bold text-blue-400">{addInfluencers} influencers</span>
            </div>
            <input
              type="range"
              min="0"
              max="10"
              value={addInfluencers}
              onChange={(e) => setAddInfluencers(Number(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <p className="text-xs text-gray-400 mt-2">Estimated cost: ${(addInfluencers * 5000).toLocaleString()}</p>
          </div>

          {/* Increase Content Novelty */}
          <div>
            <div className="flex justify-between mb-3">
              <label className="text-sm font-medium text-gray-300">Increase Content Novelty</label>
              <span className="text-sm font-bold text-purple-400">+{increaseNovelty}%</span>
            </div>
            <input
              type="range"
              min="0"
              max="50"
              value={increaseNovelty}
              onChange={(e) => setIncreaseNovelty(Number(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-purple-500"
            />
            <p className="text-xs text-gray-400 mt-2">Requires fresh content production</p>
          </div>

          {/* Expand Platforms */}
          <div>
            <div className="flex justify-between mb-3">
              <label className="text-sm font-medium text-gray-300">Expand to New Platforms</label>
              <span className="text-sm font-bold text-green-400">{expandPlatforms} platforms</span>
            </div>
            <input
              type="range"
              min="0"
              max="3"
              value={expandPlatforms}
              onChange={(e) => setExpandPlatforms(Number(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-green-500"
            />
            <p className="text-xs text-gray-400 mt-2">Cross-platform reach expansion</p>
          </div>

          {/* Boost Engagement */}
          <div>
            <div className="flex justify-between mb-3">
              <label className="text-sm font-medium text-gray-300">Boost Engagement Campaigns</label>
              <span className="text-sm font-bold text-orange-400">+{boostEngagement} units</span>
            </div>
            <input
              type="range"
              min="0"
              max="20"
              value={boostEngagement}
              onChange={(e) => setBoostEngagement(Number(e.target.value))}
              className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-orange-500"
            />
            <p className="text-xs text-gray-400 mt-2">Ad spend and promotion intensity</p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={runSimulation}
            disabled={loading}
            className="flex items-center gap-2 px-6 py-3 rounded-lg bg-blue-500 hover:bg-blue-600 text-white font-medium transition-colors disabled:opacity-50"
          >
            <Play className="w-5 h-5" />
            {loading ? 'Running Simulation...' : 'Run Simulation'}
          </button>
          <button
            onClick={resetSimulation}
            className="flex items-center gap-2 px-6 py-3 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium transition-colors"
          >
            <RotateCcw className="w-5 h-5" />
            Reset
          </button>
        </div>
      </div>

      {/* Simulation Results */}
      {simulation && (
        <>
          {/* Impact Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="rounded-xl border border-white/10 bg-gradient-to-br from-green-950/30 to-emerald-950/20 p-6 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-green-400" />
                <span className="text-sm text-gray-400">Health Improvement</span>
              </div>
              <p className="text-3xl font-bold text-green-400">
                +{simulation.impact.health_improvement.toFixed(1)}
              </p>
              <p className="text-xs text-gray-400 mt-1">
                {simulation.impact.improvement_percentage.toFixed(1)}% increase
              </p>
            </div>

            <div className="rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-cyan-950/20 p-6 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-2">
                <Activity className="w-5 h-5 text-blue-400" />
                <span className="text-sm text-gray-400">Engagement Lift</span>
              </div>
              <p className="text-3xl font-bold text-blue-400">
                +{simulation.impact.engagement_lift.toFixed(1)}%
              </p>
              <p className="text-xs text-gray-400 mt-1">Expected increase</p>
            </div>

            <div className="rounded-xl border border-white/10 bg-gradient-to-br from-purple-950/30 to-pink-950/20 p-6 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5 text-purple-400" />
                <span className="text-sm text-gray-400">Lifespan Extended</span>
              </div>
              <p className="text-3xl font-bold text-purple-400">
                {simulation.impact.days_extended} days
              </p>
              <p className="text-xs text-gray-400 mt-1">Additional runway</p>
            </div>

            <div className="rounded-xl border border-white/10 bg-gradient-to-br from-orange-950/30 to-yellow-950/20 p-6 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-2">
                <DollarSign className="w-5 h-5 text-orange-400" />
                <span className="text-sm text-gray-400">Total Cost</span>
              </div>
              <p className="text-3xl font-bold text-orange-400">
                {formatCurrency(simulation.cost_estimate.total_usd)}
              </p>
              <p className="text-xs text-gray-400 mt-1">Investment required</p>
            </div>
          </div>

          {/* Comparison Chart */}
          <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-white mb-2">Projected Impact Comparison</h2>
              <p className="text-sm text-gray-400">Baseline vs. With Interventions (30-day forecast)</p>
            </div>

            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={comparisonData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis 
                  dataKey="date" 
                  stroke="rgba(255,255,255,0.3)"
                  style={{ fontSize: '12px' }}
                  tickLine={false}
                />
                <YAxis 
                  stroke="rgba(255,255,255,0.3)"
                  style={{ fontSize: '12px' }}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(17, 24, 39, 0.95)',
                    border: '1px solid rgba(255,255,255,0.1)',
                    borderRadius: '8px',
                    padding: '12px'
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="baseline"
                  stroke="rgb(239, 68, 68)"
                  strokeWidth={2}
                  name="Baseline (No Action)"
                  dot={false}
                  strokeDasharray="5 5"
                />
                <Line
                  type="monotone"
                  dataKey="intervention"
                  stroke="rgb(34, 197, 94)"
                  strokeWidth={3}
                  name="With Interventions"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* ROI Analysis */}
          <div className="rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-purple-950/20 backdrop-blur-sm p-6">
            <div className="flex items-center gap-3 mb-6">
              <DollarSign className="w-6 h-6 text-green-400" />
              <h2 className="text-2xl font-bold text-white">ROI Prediction</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="p-5 rounded-xl bg-white/5 border border-white/10">
                <p className="text-sm text-gray-400 mb-2">Total Investment</p>
                <p className="text-2xl font-bold text-white">
                  {formatCurrency(simulation.roi_prediction.total_cost_usd)}
                </p>
              </div>
              <div className="p-5 rounded-xl bg-white/5 border border-white/10">
                <p className="text-sm text-gray-400 mb-2">Estimated Benefit</p>
                <p className="text-2xl font-bold text-green-400">
                  {formatCurrency(simulation.roi_prediction.estimated_benefit_usd)}
                </p>
              </div>
              <div className="p-5 rounded-xl bg-green-500/10 border border-green-500/30">
                <p className="text-sm text-gray-400 mb-2">ROI</p>
                <p className="text-2xl font-bold text-green-400">
                  {simulation.roi_prediction.roi_percentage.toFixed(1)}%
                </p>
              </div>
            </div>

            <div className={`p-4 rounded-lg border ${
              simulation.roi_prediction.roi_percentage > 50
                ? 'bg-green-500/10 border-green-500/30'
                : 'bg-yellow-500/10 border-yellow-500/30'
            }`}>
              <p className={`font-medium ${
                simulation.roi_prediction.roi_percentage > 50 ? 'text-green-400' : 'text-yellow-400'
              }`}>
                ✓ {simulation.roi_prediction.recommendation}
              </p>
            </div>
          </div>

          {/* Insights */}
          <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
            <h3 className="text-xl font-bold text-white mb-4">Key Insights</h3>
            <div className="space-y-3">
              {simulation.recommendations.map((rec, index) => (
                <div key={index} className="flex items-start gap-3 p-4 rounded-lg bg-white/5">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 text-sm font-bold">
                    {index + 1}
                  </div>
                  <p className="text-gray-300">{rec}</p>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
