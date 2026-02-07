'use client';

import { useEffect, useState } from 'react';
import { fetchTrendDetails, fetchTrajectory, type TrendDetails } from '@/lib/api';
import { MultiLineChart } from '@/components/dashboard/Charts';
import { TrendingUp, TrendingDown, Activity, Users, Target } from 'lucide-react';

export default function TrendLifecyclePage() {
  const [trendData, setTrendData] = useState<TrendDetails | null>(null);
  const [trajectoryData, setTrajectoryData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const details = await fetchTrendDetails('trend_1');
      const trajectory = await fetchTrajectory('trend_1', 60);
      setTrendData(details);
      setTrajectoryData(trajectory);
      setLoading(false);
    }
    loadData();
  }, []);

  if (loading || !trendData) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Create lifecycle stages data
  const lifecycleData = trendData.engagement_history.map((point, index) => {
    const totalDays = trendData.engagement_history.length;
    const dayNum = index + 1;
    
    let stage = 'Emerging';
    if (dayNum > totalDays * 0.2 && dayNum <= totalDays * 0.5) stage = 'Growing';
    else if (dayNum > totalDays * 0.5 && dayNum <= totalDays * 0.7) stage = 'Peak';
    else if (dayNum > totalDays * 0.7) stage = 'Declining';

    return {
      date: point.date,
      engagement: point.value,
      sentiment: trendData.sentiment_history[index]?.value || 50,
      stage
    };
  });

  // Calculate stage metrics
  const currentStage = lifecycleData[lifecycleData.length - 1].stage;
  const peakValue = Math.max(...lifecycleData.map(d => d.engagement));
  const currentValue = lifecycleData[lifecycleData.length - 1].engagement;
  const declineRate = ((peakValue - currentValue) / peakValue * 100).toFixed(1);

  // Audience fatigue indicator (mock calculation)
  const audienceFatigue = 68; // Higher = more fatigue
  
  // Influencer dependency score (mock)
  const influencerDependency = 42; // 0-100

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Trend Lifecycle Analysis</h1>
        <p className="text-gray-400">Track trend evolution from emergence to decline</p>
      </div>

      {/* Current Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-purple-950/30 to-blue-950/20 p-6 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="w-5 h-5 text-purple-400" />
            <span className="text-sm text-gray-400">Current Stage</span>
          </div>
          <p className="text-2xl font-bold text-white">{currentStage}</p>
          <p className="text-xs text-purple-400 mt-1">Day {lifecycleData.length} of lifecycle</p>
        </div>

        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-cyan-950/20 p-6 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-2">
            <TrendingUp className="w-5 h-5 text-blue-400" />
            <span className="text-sm text-gray-400">Peak Value</span>
          </div>
          <p className="text-2xl font-bold text-white">{peakValue.toFixed(1)}</p>
          <p className="text-xs text-blue-400 mt-1">Highest engagement reached</p>
        </div>

        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-orange-950/30 to-red-950/20 p-6 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-2">
            <TrendingDown className="w-5 h-5 text-orange-400" />
            <span className="text-sm text-gray-400">Decline Rate</span>
          </div>
          <p className="text-2xl font-bold text-white">{declineRate}%</p>
          <p className="text-xs text-orange-400 mt-1">From peak to current</p>
        </div>

        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-green-950/30 to-emerald-950/20 p-6 backdrop-blur-sm">
          <div className="flex items-center gap-3 mb-2">
            <Users className="w-5 h-5 text-green-400" />
            <span className="text-sm text-gray-400">Current Engagement</span>
          </div>
          <p className="text-2xl font-bold text-white">{currentValue.toFixed(1)}</p>
          <p className="text-xs text-green-400 mt-1">Real-time metric</p>
        </div>
      </div>

      {/* Main Lifecycle Chart */}
      <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">Growth → Peak → Decline Visualization</h2>
          <p className="text-sm text-gray-400">Complete trend lifecycle with stage transitions</p>
        </div>

        {/* Stage Indicators */}
        <div className="flex gap-4 mb-6">
          {['Emerging', 'Growing', 'Peak', 'Declining'].map((stage, idx) => (
            <div
              key={stage}
              className={`flex-1 p-3 rounded-lg border ${
                currentStage === stage
                  ? 'bg-blue-500/20 border-blue-500/50'
                  : 'bg-white/5 border-white/10'
              }`}
            >
              <div className="flex items-center gap-2">
                <div className={`w-3 h-3 rounded-full ${
                  idx === 0 ? 'bg-green-500' :
                  idx === 1 ? 'bg-blue-500' :
                  idx === 2 ? 'bg-purple-500' :
                  'bg-red-500'
                }`} />
                <span className={`text-sm font-medium ${
                  currentStage === stage ? 'text-white' : 'text-gray-400'
                }`}>
                  {stage}
                </span>
              </div>
            </div>
          ))}
        </div>

        <MultiLineChart
          data={lifecycleData}
          lines={[
            { dataKey: 'engagement', color: 'rgb(96, 165, 250)', name: 'Engagement' },
            { dataKey: 'sentiment', color: 'rgb(168, 85, 247)', name: 'Sentiment' }
          ]}
          height={350}
        />
      </div>

      {/* Bottom Grid - Indicators */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Audience Fatigue */}
        <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
          <div className="flex items-center gap-3 mb-6">
            <Target className="w-6 h-6 text-orange-400" />
            <div>
              <h3 className="text-xl font-bold text-white">Audience Fatigue Indicator</h3>
              <p className="text-sm text-gray-400">How burned out is your audience?</p>
            </div>
          </div>

          <div className="relative pt-8">
            <div className="h-8 bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 rounded-full relative overflow-hidden">
              <div
                className="absolute top-0 bottom-0 bg-white/20"
                style={{ left: `${audienceFatigue}%`, width: '4px' }}
              />
            </div>
            <div
              className="absolute top-0 flex flex-col items-center"
              style={{ left: `${audienceFatigue}%`, transform: 'translateX(-50%)' }}
            >
              <div className="bg-white text-gray-900 px-3 py-1 rounded-lg text-sm font-bold mb-1">
                {audienceFatigue}%
              </div>
            </div>
          </div>

          <div className="mt-8 space-y-3">
            <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
              <span className="text-sm text-gray-400">Repetition Index</span>
              <span className="text-sm font-bold text-orange-400">High (72%)</span>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
              <span className="text-sm text-gray-400">Novelty Depletion</span>
              <span className="text-sm font-bold text-red-400">Critical (85%)</span>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg bg-white/5">
              <span className="text-sm text-gray-400">Audience Overlap</span>
              <span className="text-sm font-bold text-yellow-400">Medium (58%)</span>
            </div>
          </div>
        </div>

        {/* Influencer Dependency */}
        <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
          <div className="flex items-center gap-3 mb-6">
            <Users className="w-6 h-6 text-purple-400" />
            <div>
              <h3 className="text-xl font-bold text-white">Influencer Dependency Score</h3>
              <p className="text-sm text-gray-400">Reliance on key influencers</p>
            </div>
          </div>

          <div className="flex items-center justify-center mb-8">
            <div className="relative w-48 h-48">
              <svg className="transform -rotate-90" width="192" height="192">
                <circle
                  cx="96"
                  cy="96"
                  r="80"
                  stroke="rgba(255,255,255,0.1)"
                  strokeWidth="16"
                  fill="none"
                />
                <circle
                  cx="96"
                  cy="96"
                  r="80"
                  stroke="rgb(168, 85, 247)"
                  strokeWidth="16"
                  fill="none"
                  strokeDasharray={`${2 * Math.PI * 80}`}
                  strokeDashoffset={`${2 * Math.PI * 80 * (1 - influencerDependency / 100)}`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-4xl font-bold text-purple-400">{influencerDependency}%</span>
                <span className="text-sm text-gray-400 mt-1">Dependency</span>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <div className="p-3 rounded-lg bg-white/5 border border-white/10">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-gray-400">Top 5 Influencers</span>
                <span className="text-sm font-bold text-white">35% of traffic</span>
              </div>
              <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-purple-500 to-pink-500" style={{ width: '35%' }} />
              </div>
            </div>

            <div className="p-3 rounded-lg bg-white/5 border border-white/10">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-gray-400">Organic Growth</span>
                <span className="text-sm font-bold text-white">58% contribution</span>
              </div>
              <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-green-500 to-emerald-500" style={{ width: '58%' }} />
              </div>
            </div>

            <div className="p-3 rounded-lg bg-green-500/10 border border-green-500/30 mt-4">
              <p className="text-sm text-green-400">
                ✓ Low dependency indicates sustainable organic growth
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
