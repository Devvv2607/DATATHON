'use client';

import { useState } from 'react';
import { Sparkles, Search, TrendingUp, Video, MessageSquare, Repeat, Target, Shield } from 'lucide-react';
import { generateComebackContent, ComebackResponse } from '@/lib/comeback-api';

export default function ComebackAIPage() {
  const getCachedResult = (trendName: string) => {
    if (typeof window === 'undefined') return null;
    const cached = localStorage.getItem(`comeback_${trendName}`);
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
  const [result, setResult] = useState<ComebackResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setError('Please enter a trend name');
      return;
    }

    const trendName = searchQuery.trim();
    
    // Check cache first
    const cachedResult = getCachedResult(trendName);
    if (cachedResult) {
      setResult(cachedResult);
      setError(null);
    }

    setLoading(!cachedResult);
    setError(null);

    try {
      const response = await generateComebackContent({
        trend_name: trendName,
      });
      setResult(response);
      
      // Cache the result
      localStorage.setItem(`comeback_${trendName}`, JSON.stringify({
        result: response,
        timestamp: Date.now()
      }));
    } catch (err: any) {
      if (!cachedResult) {
        setError(err.message || 'Failed to generate content');
      }
      console.error('Comeback generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getAlertColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'green':
        return {
          bg: 'from-green-950/30 to-emerald-950/20',
          border: 'border-green-500/50',
          text: 'text-green-400',
          badge: 'bg-green-500/20 text-green-300'
        };
      case 'yellow':
        return {
          bg: 'from-yellow-950/30 to-amber-950/20',
          border: 'border-yellow-500/50',
          text: 'text-yellow-400',
          badge: 'bg-yellow-500/20 text-yellow-300'
        };
      case 'orange':
        return {
          bg: 'from-orange-950/30 to-red-950/20',
          border: 'border-orange-500/50',
          text: 'text-orange-400',
          badge: 'bg-orange-500/20 text-orange-300'
        };
      case 'red':
        return {
          bg: 'from-red-950/30 to-rose-950/20',
          border: 'border-red-500/50',
          text: 'text-red-400',
          badge: 'bg-red-500/20 text-red-300'
        };
      default:
        return {
          bg: 'from-gray-950/30 to-slate-950/20',
          border: 'border-gray-500/50',
          text: 'text-gray-400',
          badge: 'bg-gray-500/20 text-gray-300'
        };
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 rounded-2xl glass-card">
            <Sparkles className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <h1 className="text-4xl font-bold gradient-text">Comeback AI</h1>
            <p className="text-gray-400 mt-1">
              AI-powered creative content generation for declining or rising trends
            </p>
          </div>
        </div>
      </div>

      {/* Search Section */}
      <div className="mb-8">
        <form onSubmit={handleGenerate} className="glass-card p-6">
          <div className="flex gap-4">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Enter trend name (e.g., fidget spinner, AI memes)"
                className="w-full pl-12 pr-4 py-4 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50 focus:ring-2 focus:ring-purple-500/20 transition-all"
                disabled={loading}
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  Generating...
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  <Sparkles className="w-5 h-5" />
                  Generate Content
                </span>
              )}
            </button>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-300 flex items-center gap-2">
              <Shield className="w-5 h-5" />
              {error}
            </div>
          )}
        </form>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="glass-card p-12 text-center">
          <div className="flex flex-col items-center gap-4">
            <div className="w-16 h-16 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin" />
            <h3 className="text-2xl font-semibold text-white">Analyzing Trend...</h3>
            <p className="text-gray-400">
              Fetching lifecycle data → Analyzing decline signals → Generating creative content
            </p>
          </div>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="space-y-6">
          {/* Overview Card */}
          <div className={`glass-card p-6 border bg-gradient-to-br ${getAlertColor(result.alert_level).bg} ${getAlertColor(result.alert_level).border}`}>
            <div className="flex items-start justify-between mb-6">
              <div>
                <h2 className="text-3xl font-bold text-white mb-3">{result.trend_name}</h2>
                <div className="flex items-center gap-3 flex-wrap">
                  <span className={`px-4 py-2 ${getAlertColor(result.alert_level).badge} font-semibold rounded-full text-sm`}>
                    {result.alert_level.toUpperCase()} ALERT
                  </span>
                  <span className={`px-4 py-2 ${result.mode.includes('COMEBACK') ? 'bg-red-500/20 text-red-300' : 'bg-green-500/20 text-green-300'} font-semibold rounded-full text-sm`}>
                    {result.mode}
                  </span>
                  <span className="px-4 py-2 bg-white/10 text-gray-300 rounded-full text-sm">
                    Stage {result.lifecycle_stage}: {result.stage_name}
                  </span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-4xl font-bold text-white">{result.decline_risk_score.toFixed(0)}</div>
                <div className="text-sm text-gray-400">Risk Score</div>
              </div>
            </div>

            <div className="glass p-4 rounded-xl mb-4">
              <h3 className="font-semibold text-white mb-2 flex items-center gap-2">
                <Target className="w-5 h-5 text-purple-400" />
                Content Strategy
              </h3>
              <p className="text-gray-300">{result.content_strategy}</p>
            </div>

            {result.decline_drivers && (
              <div className="glass p-4 rounded-xl border border-red-500/20">
                <h3 className="font-semibold text-red-400 mb-3 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  Decline Drivers Addressed
                </h3>
                <ul className="space-y-2">
                  {result.decline_drivers.map((driver, idx) => (
                    <li key={idx} className="text-gray-300 text-sm flex items-start gap-2">
                      <span className="text-red-400 mt-1">•</span>
                      <span>{driver}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.growth_opportunities && (
              <div className="glass p-4 rounded-xl border border-green-500/20">
                <h3 className="font-semibold text-green-400 mb-3 flex items-center gap-2">
                  <TrendingUp className="w-5 h-5" />
                  Growth Opportunities
                </h3>
                <ul className="space-y-2">
                  {result.growth_opportunities.map((opp, idx) => (
                    <li key={idx} className="text-gray-300 text-sm flex items-start gap-2">
                      <span className="text-green-400 mt-1">•</span>
                      <span>{opp}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Reel Ideas */}
          <div className="glass-card p-6">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <Video className="w-6 h-6 text-purple-400" />
              Reel Ideas
              <span className="text-sm font-normal text-gray-400">
                ({result.content.reels.length} ideas)
              </span>
            </h3>
            <div className="grid md:grid-cols-3 gap-6">
              {result.content.reels.map((reel) => (
                <div
                  key={reel.id}
                  className="glass-card p-6 hover:border-purple-500/50 transition-all group"
                >
                  <div className="text-purple-400 font-bold text-sm mb-3">REEL #{reel.id}</div>
                  <h4 className="text-xl font-bold text-white mb-3 group-hover:text-purple-400 transition-colors">
                    {reel.title}
                  </h4>
                  <p className="text-gray-400 text-sm mb-4">{reel.description}</p>
                  <div className="glass p-3 rounded-lg mb-3">
                    <div className="text-xs font-semibold text-purple-400 mb-1">HOOK:</div>
                    <div className="text-white text-sm italic">"{reel.hook}"</div>
                  </div>
                  <div className="glass p-3 rounded-lg">
                    <div className="text-xs font-semibold text-green-400 mb-1">WHY IT WORKS:</div>
                    <div className="text-gray-300 text-xs">{reel.why_it_works}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Captions */}
          <div className="glass-card p-6">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <MessageSquare className="w-6 h-6 text-blue-400" />
              Captions & Hooks
              <span className="text-sm font-normal text-gray-400">
                ({result.content.captions.length} captions)
              </span>
            </h3>
            <div className="grid md:grid-cols-3 gap-6">
              {result.content.captions.map((caption) => (
                <div
                  key={caption.id}
                  className="glass-card p-6 hover:border-blue-500/50 transition-all"
                >
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-blue-400 font-bold text-sm">CAPTION #{caption.id}</span>
                    <span className="px-3 py-1 bg-blue-600/20 text-blue-300 text-xs font-semibold rounded-full">
                      {caption.language}
                    </span>
                  </div>
                  <p className="text-white text-lg font-medium">"{caption.caption}"</p>
                </div>
              ))}
            </div>
          </div>

          {/* Remix Formats */}
          <div className="glass-card p-6">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
              <Repeat className="w-6 h-6 text-orange-400" />
              Remix Formats
              <span className="text-sm font-normal text-gray-400">
                ({result.content.remixes.length} formats)
              </span>
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              {result.content.remixes.map((remix) => (
                <div
                  key={remix.id}
                  className="glass-card p-6 hover:border-orange-500/50 transition-all"
                >
                  <div className="text-orange-400 font-bold text-sm mb-3">FORMAT #{remix.id}</div>
                  <h4 className="text-2xl font-bold text-white mb-4">{remix.format}</h4>
                  <div className="glass p-4 rounded-lg mb-3">
                    <div className="text-xs font-semibold text-orange-400 mb-2">STRUCTURE:</div>
                    <p className="text-gray-300 text-sm">{remix.structure}</p>
                  </div>
                  <div className="glass p-4 rounded-lg">
                    <div className="text-xs font-semibold text-yellow-400 mb-2">EXAMPLE:</div>
                    <p className="text-gray-300 text-sm italic">{remix.example}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Metadata */}
          <div className="text-center text-sm text-gray-500">
            Generated {new Date(result.generated_at).toLocaleString()} · Confidence: {result.confidence}
          </div>
        </div>
      )}

      {/* Empty State */}
      {!result && !loading && (
        <div className="glass-card p-12 text-center">
          <div className="max-w-2xl mx-auto">
            <Sparkles className="w-16 h-16 text-purple-400 mx-auto mb-6" />
            <h3 className="text-2xl font-semibold text-white mb-4">How It Works</h3>
            <div className="grid md:grid-cols-2 gap-6 text-left">
              <div className="glass p-4 rounded-xl">
                <h4 className="font-semibold text-red-400 mb-2 flex items-center gap-2">
                  🔴 COMEBACK MODE
                </h4>
                <p className="text-sm text-gray-400">
                  For declining trends (Red/Orange alerts). Generates fresh angles, remix formats to combat fatigue and re-engage audiences.
                </p>
              </div>
              <div className="glass p-4 rounded-xl">
                <h4 className="font-semibold text-green-400 mb-2 flex items-center gap-2">
                  🟢 GROWTH MODE
                </h4>
                <p className="text-sm text-gray-400">
                  For rising trends (Green/Yellow alerts). Generates strategies to maximize reach and scale across platforms.
                </p>
              </div>
              <div className="glass p-4 rounded-xl">
                <h4 className="font-semibold text-blue-400 mb-2 flex items-center gap-2">
                  📊 Automatic Analysis
                </h4>
                <p className="text-sm text-gray-400">
                  Fetches lifecycle stage and decline risk automatically. Generates contextual decline drivers or growth opportunities.
                </p>
              </div>
              <div className="glass p-4 rounded-xl">
                <h4 className="font-semibold text-purple-400 mb-2 flex items-center gap-2">
                  🎨 AI-Powered Content
                </h4>
                <p className="text-sm text-gray-400">
                  Get 3 reels, 3 captions (English + Hinglish), and 2 remixes - all tailored to your trend's lifecycle.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
