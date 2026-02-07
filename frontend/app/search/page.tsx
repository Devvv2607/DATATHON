'use client';

import { useState } from 'react';
import { Search, TrendingUp, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface LifecycleResult {
  trend_id: string;
  trend_name: string;
  lifecycle_stage: number;
  stage_name: string;
  days_in_stage: number;
  confidence: number;
}

const STAGE_COLORS = {
  1: 'text-green-400 bg-green-500/10',
  2: 'text-blue-400 bg-blue-500/10',
  3: 'text-yellow-400 bg-yellow-500/10',
  4: 'text-orange-400 bg-orange-500/10',
  5: 'text-red-400 bg-red-500/10',
};

const STAGE_ICONS = {
  1: '🌱',
  2: '🚀',
  3: '📊',
  4: '📉',
  5: '🪦',
};

export default function TrendSearchPage() {
  const router = useRouter();
  const [keyword, setKeyword] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<LifecycleResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!keyword.trim()) {
      setError('Please enter a trend keyword');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Call lifecycle detection API
      const response = await fetch('http://localhost:8000/api/trend/lifecycle', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          trend_name: keyword,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to analyze trend');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const viewDetails = () => {
    if (result) {
      // Navigate to dashboard with trend data
      router.push(`/dashboard/trendLifecycle?trend=${encodeURIComponent(result.trend_name)}`);
    }
  };

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Animated background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 -left-1/4 w-1/2 h-1/2 bg-blue-600/20 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-0 -right-1/4 w-1/2 h-1/2 bg-purple-600/20 rounded-full blur-[120px] animate-pulse" style={{animationDelay: '1s'}} />
      </div>

      <div className="relative max-w-4xl mx-auto px-6 py-24">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-3 mb-6">
            <div className="p-3 rounded-2xl glass-strong">
              <TrendingUp className="w-8 h-8 text-blue-400" />
            </div>
            <h1 className="text-4xl font-bold gradient-text">Trend Analysis</h1>
          </div>
          <p className="text-xl text-slate-300">
            Enter a trend keyword to analyze its lifecycle stage and predict decline
          </p>
        </div>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="mb-12">
          <div className="relative">
            <input
              type="text"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              placeholder="Enter trend keyword (e.g., 'Grimace Shake', 'Wednesday Dance')"
              className="w-full px-6 py-5 pl-14 rounded-3xl glass-strong text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-lg"
              disabled={loading}
            />
            <Search className="absolute left-5 top-1/2 -translate-y-1/2 w-6 h-6 text-gray-400" />
            <button
              type="submit"
              disabled={loading || !keyword.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 px-8 py-3 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 hover:shadow-[0_0_40px_rgba(96,165,250,0.4)] hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 font-semibold"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing...
                </span>
              ) : (
                'Analyze'
              )}
            </button>
          </div>
        </form>

        {/* Error Message */}
        {error && (
          <div className="p-6 rounded-3xl glass-card border border-red-500/30 mb-8">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-6 h-6 text-red-400" />
              <div>
                <h3 className="font-semibold text-red-400 mb-1">Analysis Failed</h3>
                <p className="text-sm text-slate-300">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Result Card */}
        {result && (
          <div className="space-y-6">
            {/* Success Banner */}
            <div className="p-4 rounded-2xl glass-strong border border-green-500/30">
              <div className="flex items-center gap-3">
                <CheckCircle className="w-5 h-5 text-green-400" />
                <p className="text-sm text-green-400 font-medium">
                  Trend analysis complete! Click "View Full Analysis" for detailed insights.
                </p>
              </div>
            </div>

            {/* Main Result */}
            <div className="p-8 rounded-3xl glass-card">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-3xl font-bold mb-2">{result.trend_name}</h2>
                  <p className="text-slate-400">Trend ID: {result.trend_id}</p>
                </div>
                <div className="text-6xl">{STAGE_ICONS[result.lifecycle_stage as keyof typeof STAGE_ICONS]}</div>
              </div>

              <div className="grid md:grid-cols-3 gap-6 mb-8">
                {/* Lifecycle Stage */}
                <div className="p-6 rounded-2xl glass-strong">
                  <p className="text-sm text-slate-400 mb-2">Lifecycle Stage</p>
                  <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full ${STAGE_COLORS[result.lifecycle_stage as keyof typeof STAGE_COLORS]}`}>
                    <span className="text-2xl">{STAGE_ICONS[result.lifecycle_stage as keyof typeof STAGE_ICONS]}</span>
                    <span className="font-semibold">{result.stage_name}</span>
                  </div>
                </div>

                {/* Days in Stage */}
                <div className="p-6 rounded-2xl glass-strong">
                  <p className="text-sm text-slate-400 mb-2">Days in Stage</p>
                  <p className="text-3xl font-bold text-white">{result.days_in_stage}</p>
                  <p className="text-xs text-slate-500 mt-1">days</p>
                </div>

                {/* Confidence */}
                <div className="p-6 rounded-2xl glass-strong">
                  <p className="text-sm text-slate-400 mb-2">Confidence</p>
                  <p className="text-3xl font-bold text-blue-400">{(result.confidence * 100).toFixed(0)}%</p>
                  <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-500"
                      style={{ width: `${result.confidence * 100}%` }}
                    />
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4">
                <button
                  onClick={viewDetails}
                  className="flex-1 px-6 py-4 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 hover:shadow-[0_0_40px_rgba(96,165,250,0.4)] hover:scale-105 transition-all duration-300 font-semibold"
                >
                  View Full Analysis
                </button>
                <button
                  onClick={() => {
                    setKeyword('');
                    setResult(null);
                    setError(null);
                  }}
                  className="px-6 py-4 rounded-full glass-strong hover:scale-105 transition-all duration-300"
                >
                  New Search
                </button>
              </div>
            </div>

            {/* Stage Description */}
            <div className="p-6 rounded-3xl glass-strong">
              <h3 className="font-semibold mb-3">What does {result.stage_name} mean?</h3>
              <p className="text-slate-300 leading-relaxed">
                {result.lifecycle_stage === 1 && "This trend is in its early growth phase with low-to-moderate activity. It's gaining initial traction but hasn't reached viral status yet."}
                {result.lifecycle_stage === 2 && "This trend is experiencing explosive viral growth! High momentum and rapid engagement indicate peak virality."}
                {result.lifecycle_stage === 3 && "This trend has stabilized at high engagement levels. Growth has flattened, but activity remains strong and consistent."}
                {result.lifecycle_stage === 4 && "This trend is declining with sustained negative growth. Engagement is dropping, and the trend is losing momentum."}
                {result.lifecycle_stage === 5 && "This trend is dead with near-zero activity across all platforms. It's no longer generating significant engagement."}
              </p>
            </div>
          </div>
        )}

        {/* Example Trends */}
        {!result && !loading && (
          <div className="mt-16">
            <h3 className="text-center text-slate-400 mb-6">Try analyzing these trends:</h3>
            <div className="flex flex-wrap justify-center gap-3">
              {['Grimace Shake', 'Wednesday Dance', 'Barbie Movie', 'Ice Bucket Challenge', 'Gangnam Style'].map((trend) => (
                <button
                  key={trend}
                  onClick={() => setKeyword(trend)}
                  className="px-6 py-3 rounded-full glass-strong hover:scale-105 hover:glass-card transition-all duration-300 text-sm"
                >
                  {trend}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
