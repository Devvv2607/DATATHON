'use client';

import { useEffect, useState } from 'react';
import { fetchTrends, predictDecline, type TrendOverview, type DeclinePrediction } from '@/lib/api';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { ProbabilityGauge } from '@/components/dashboard/ProbabilityGauge';
import { TrendCard } from '@/components/dashboard/TrendCard';
import { TrendChart } from '@/components/dashboard/Charts';
import { TrendingUp, Users, BarChart3, AlertTriangle } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const [trends, setTrends] = useState<TrendOverview[]>([]);
  const [selectedTrend, setSelectedTrend] = useState<TrendOverview | null>(null);
  const [prediction, setPrediction] = useState<DeclinePrediction | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const { trends: data } = await fetchTrends();
      setTrends(data);
      if (data.length > 0) {
        setSelectedTrend(data[0]);
        const pred = await predictDecline(data[0].id);
        setPrediction(pred);
      }
      setLoading(false);
    }
    loadData();
  }, []);

  const avgHealthScore = trends.length > 0
    ? (trends.reduce((sum, t) => sum + t.metrics.health_score, 0) / trends.length).toFixed(1)
    : '0';

  const decliningTrends = trends.filter(t => t.status === 'declining').length;

  // Mock velocity data
  const velocityData = Array.from({ length: 7 }, (_, i) => ({
    date: new Date(Date.now() - (6 - i) * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    value: 65 + Math.sin(i / 2) * 15 + Math.random() * 10
  }));

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Trend Intelligence Dashboard</h1>
        <p className="text-gray-400">Real-time analysis and decline prediction powered by ML</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Average Health Score"
          value={avgHealthScore}
          change={2.3}
          trend="up"
          icon={<BarChart3 className="w-6 h-6" />}
        />
        <MetricCard
          title="Active Trends"
          value={trends.length}
          icon={<TrendingUp className="w-6 h-6" />}
        />
        <MetricCard
          title="At-Risk Trends"
          value={decliningTrends}
          trend="down"
          icon={<AlertTriangle className="w-6 h-6" />}
        />
        <MetricCard
          title="Total Reach"
          value="12.4M"
          change={8.5}
          trend="up"
          icon={<Users className="w-6 h-6" />}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Trends List */}
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
            <h2 className="text-2xl font-bold text-white mb-6">Trending Topics</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {trends.slice(0, 4).map((trend) => (
                <TrendCard
                  key={trend.id}
                  trend={trend}
                  onClick={() => router.push('/dashboard/trendLifecycle')}
                />
              ))}
            </div>
          </div>

          {/* Engagement Velocity Chart */}
          <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-bold text-white">Engagement Velocity</h2>
                <p className="text-sm text-gray-400 mt-1">7-day trend momentum</p>
              </div>
              <div className="flex gap-2">
                <button className="px-3 py-1 rounded-lg bg-blue-500/20 text-blue-400 text-sm font-medium">
                  7D
                </button>
                <button className="px-3 py-1 rounded-lg bg-white/5 text-gray-400 text-sm font-medium hover:bg-white/10">
                  30D
                </button>
              </div>
            </div>
            <TrendChart
              data={velocityData}
              color="rgb(96, 165, 250)"
              height={250}
              type="area"
            />
          </div>
        </div>

        {/* Right Column - Selected Trend Analysis */}
        <div className="space-y-6">
          {selectedTrend && prediction && (
            <>
              <div className="rounded-xl border border-white/10 bg-gradient-to-br from-red-950/30 to-orange-950/20 backdrop-blur-sm p-6">
                <h2 className="text-xl font-bold text-white mb-6 text-center">Decline Risk Analysis</h2>
                <ProbabilityGauge
                  value={prediction.decline_probability}
                  label={selectedTrend.name}
                  size="lg"
                />
                <div className="mt-6 p-4 rounded-lg bg-black/20 border border-white/10">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-400">Confidence</span>
                    <span className="text-sm font-bold text-white capitalize">
                      {prediction.confidence_level}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">Est. Days Until Decline</span>
                    <span className="text-sm font-bold text-orange-400">
                      {prediction.days_until_decline} days
                    </span>
                  </div>
                </div>
              </div>

              <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
                <h3 className="text-lg font-bold text-white mb-4">Key Risk Indicators</h3>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-gray-400">Audience Saturation</span>
                      <span className="text-sm font-bold text-red-400">High</span>
                    </div>
                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-red-500 to-orange-500" style={{ width: '78%' }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-gray-400">Content Novelty</span>
                      <span className="text-sm font-bold text-yellow-400">Medium</span>
                    </div>
                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-yellow-500 to-orange-500" style={{ width: '45%' }} />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-gray-400">Influencer Dependency</span>
                      <span className="text-sm font-bold text-green-400">Low</span>
                    </div>
                    <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-green-500 to-emerald-500" style={{ width: '32%' }} />
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
