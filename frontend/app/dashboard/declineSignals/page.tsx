'use client';

import { useState } from 'react';
import { AlertTriangle, Activity, Users, TrendingDown, Target, Search, Shield } from 'lucide-react';

interface SignalBreakdown {
  engagement_drop: number;
  velocity_decline: number;
  creator_decline: number;
  quality_decline: number;
}

interface DeclineSignalResponse {
  trend_id: string;
  decline_risk_score: number;
  alert_level: string;
  signal_breakdown: SignalBreakdown;
  timestamp: string;
  confidence: string;
  data_quality: string;
  time_to_die: number | null;
}

export default function DeclineSignalsPage() {
  const getCachedResult = (trendName: string) => {
    if (typeof window === 'undefined') return null;
    const cached = localStorage.getItem(`decline_signals_${trendName}`);
    if (cached) {
      try {
        const { result, timestamp } = JSON.parse(cached);
        // Use cache if less than 1 hour old
        if (Date.now() - timestamp < 60 * 60 * 1000) {
          return result;
        }
      } catch (e) {
        return null;
      }
    }
    return null;
  };

  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<DeclineSignalResponse | null>(null);
  const [trendName, setTrendName] = useState('');

  const getAlertColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'green':
        return {
          bg: 'from-green-950/30 to-emerald-950/20',
          border: 'border-green-500/50',
          text: 'text-green-400',
          glow: 'shadow-green-500/20',
          badge: 'bg-green-500/20 text-green-300'
        };
      case 'yellow':
        return {
          bg: 'from-yellow-950/30 to-amber-950/20',
          border: 'border-yellow-500/50',
          text: 'text-yellow-400',
          glow: 'shadow-yellow-500/20',
          badge: 'bg-yellow-500/20 text-yellow-300'
        };
      case 'orange':
        return {
          bg: 'from-orange-950/30 to-red-950/20',
          border: 'border-orange-500/50',
          text: 'text-orange-400',
          glow: 'shadow-orange-500/20',
          badge: 'bg-orange-500/20 text-orange-300'
        };
      case 'red':
        return {
          bg: 'from-red-950/30 to-rose-950/20',
          border: 'border-red-500/50',
          text: 'text-red-400',
          glow: 'shadow-red-500/20',
          badge: 'bg-red-500/20 text-red-300'
        };
      default:
        return {
          bg: 'from-gray-950/30 to-slate-950/20',
          border: 'border-gray-500/50',
          text: 'text-gray-400',
          glow: 'shadow-gray-500/20',
          badge: 'bg-gray-500/20 text-gray-300'
        };
    }
  };

  const getAlertMessage = (level: string, score: number) => {
    switch (level.toLowerCase()) {
      case 'green':
        return { title: '✅ Safe', message: 'All signals are healthy. No immediate concerns.' };
      case 'yellow':
        return { title: '⚠️ Watch', message: 'Early warning signs detected. Monitor closely.' };
      case 'orange':
        return { title: '🚨 Alert', message: 'Significant decline detected. Take action soon.' };
      case 'red':
        return { title: '🔴 Critical', message: 'Multiple system failures. Immediate action required.' };
      default:
        return { title: 'Unknown', message: 'Unable to determine status.' };
    }
  };

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    const trendName = searchQuery.trim();
    setTrendName(trendName);
    
    // Check cache first
    const cachedResult = getCachedResult(trendName);
    if (cachedResult) {
      setResult(cachedResult);
    }

    setLoading(!cachedResult);
    
    try {
      // First, get lifecycle data
      const lifecycleResponse = await fetch('http://localhost:8000/api/trend/lifecycle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ trend_name: trendName })
      });

      if (!lifecycleResponse.ok) throw new Error('Lifecycle analysis failed');
      
      const lifecycleData = await lifecycleResponse.json();
      
      // Then analyze decline signals
      const declineResponse = await fetch('http://localhost:8000/api/decline-signals/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          trend_name: lifecycleData.trend_name,
          lifecycle_stage: lifecycleData.lifecycle_stage,
          stage_name: lifecycleData.stage_name,
          confidence: lifecycleData.confidence
        })
      });

      if (!declineResponse.ok) throw new Error('Decline signal analysis failed');
      
      const declineData = await declineResponse.json();
      setResult(declineData);
      
      // Cache the result
      localStorage.setItem(`decline_signals_${trendName}`, JSON.stringify({
        result: declineData,
        timestamp: Date.now()
      }));
      
    } catch (error) {
      console.error('Analysis failed:', error);
      if (!cachedResult) {
        alert('Analysis failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const colors = result ? getAlertColor(result.alert_level) : getAlertColor('gray');
  const alertInfo = result ? getAlertMessage(result.alert_level, result.decline_risk_score) : null;

  return (
    <div className="min-h-screen bg-black text-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <Shield className="w-10 h-10 text-purple-400" />
            <div>
              <h1 className="text-4xl font-bold text-white">Early Decline Detection</h1>
              <p className="text-gray-400 mt-1">Real-time warning system for trend health monitoring</p>
            </div>
          </div>

          {/* Search Bar */}
          <form onSubmit={handleAnalyze} className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Enter trend name to analyze..."
                className="w-full pl-12 pr-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:bg-white/10 transition-all"
              />
            </div>
            <button
              type="submit"
              disabled={loading || !searchQuery.trim()}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl font-semibold hover:from-purple-500 hover:to-blue-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </form>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Alert Status Card */}
            <div className={`rounded-2xl border ${colors.border} bg-gradient-to-br ${colors.bg} p-8 backdrop-blur-sm ${colors.glow} shadow-2xl`}>
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-3xl font-bold text-white mb-2">{trendName}</h2>
                  <div className="flex items-center gap-3">
                    <span className={`px-4 py-1 rounded-full text-sm font-semibold ${colors.badge}`}>
                      {result.alert_level.toUpperCase()}
                    </span>
                    <span className="text-sm text-gray-400">
                      Confidence: {result.confidence} | Quality: {result.data_quality}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-6xl font-bold ${colors.text}`}>
                    {result.decline_risk_score.toFixed(0)}
                  </div>
                  <div className="text-sm text-gray-400 mt-1">Risk Score</div>
                </div>
              </div>

              {alertInfo && (
                <div className="bg-black/30 rounded-xl p-6 backdrop-blur-sm">
                  <h3 className={`text-xl font-bold ${colors.text} mb-2`}>{alertInfo.title}</h3>
                  <p className="text-gray-300">{alertInfo.message}</p>
                  {result.time_to_die && (
                    <p className="text-sm text-gray-400 mt-3">
                      ⏱️ Estimated time to critical: <span className="font-bold">{result.time_to_die} days</span>
                    </p>
                  )}
                </div>
              )}
            </div>

            {/* Signal Breakdown */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Engagement Drop */}
              <div className="rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-cyan-950/20 p-6 backdrop-blur-sm">
                <div className="flex items-center gap-3 mb-3">
                  <Activity className="w-5 h-5 text-blue-400" />
                  <span className="text-sm text-gray-400">Engagement Drop</span>
                </div>
                <div className="text-3xl font-bold text-white mb-2">
                  {result.signal_breakdown.engagement_drop.toFixed(1)}
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all"
                    style={{ width: `${result.signal_breakdown.engagement_drop}%` }}
                  />
                </div>
              </div>

              {/* Velocity Decline */}
              <div className="rounded-xl border border-white/10 bg-gradient-to-br from-purple-950/30 to-pink-950/20 p-6 backdrop-blur-sm">
                <div className="flex items-center gap-3 mb-3">
                  <TrendingDown className="w-5 h-5 text-purple-400" />
                  <span className="text-sm text-gray-400">Velocity Decline</span>
                </div>
                <div className="text-3xl font-bold text-white mb-2">
                  {result.signal_breakdown.velocity_decline.toFixed(1)}
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div 
                    className="bg-purple-500 h-2 rounded-full transition-all"
                    style={{ width: `${result.signal_breakdown.velocity_decline}%` }}
                  />
                </div>
              </div>

              {/* Creator Decline */}
              <div className="rounded-xl border border-white/10 bg-gradient-to-br from-orange-950/30 to-red-950/20 p-6 backdrop-blur-sm">
                <div className="flex items-center gap-3 mb-3">
                  <Users className="w-5 h-5 text-orange-400" />
                  <span className="text-sm text-gray-400">Creator Decline</span>
                </div>
                <div className="text-3xl font-bold text-white mb-2">
                  {result.signal_breakdown.creator_decline.toFixed(1)}
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div 
                    className="bg-orange-500 h-2 rounded-full transition-all"
                    style={{ width: `${result.signal_breakdown.creator_decline}%` }}
                  />
                </div>
              </div>

              {/* Quality Decline */}
              <div className="rounded-xl border border-white/10 bg-gradient-to-br from-green-950/30 to-emerald-950/20 p-6 backdrop-blur-sm">
                <div className="flex items-center gap-3 mb-3">
                  <Target className="w-5 h-5 text-green-400" />
                  <span className="text-sm text-gray-400">Quality Decline</span>
                </div>
                <div className="text-3xl font-bold text-white mb-2">
                  {result.signal_breakdown.quality_decline.toFixed(1)}
                </div>
                <div className="w-full bg-white/10 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full transition-all"
                    style={{ width: `${result.signal_breakdown.quality_decline}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Info Panel */}
            <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
              <h3 className="text-lg font-bold text-white mb-4">📊 Signal Interpretation</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-semibold text-green-400">GREEN (0-30):</span>
                  <span className="text-gray-300 ml-2">All signals healthy</span>
                </div>
                <div>
                  <span className="font-semibold text-yellow-400">YELLOW (30-57):</span>
                  <span className="text-gray-300 ml-2">Early warning signs</span>
                </div>
                <div>
                  <span className="font-semibold text-orange-400">ORANGE (57-80):</span>
                  <span className="text-gray-300 ml-2">Significant decline</span>
                </div>
                <div>
                  <span className="font-semibold text-red-400">RED (80-100):</span>
                  <span className="text-gray-300 ml-2">Critical failure</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!result && !loading && (
          <div className="text-center py-20">
            <Shield className="w-20 h-20 text-gray-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-400 mb-2">No Analysis Yet</h3>
            <p className="text-gray-500">Enter a trend name above to detect early decline signals</p>
          </div>
        )}
      </div>
    </div>
  );
}
