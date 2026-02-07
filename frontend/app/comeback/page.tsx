'use client';

import { useState } from 'react';
import { generateComebackContent, ComebackResponse } from '@/lib/comeback-api';
import ComebackContentDisplay from '@/components/comeback/ComebackContentDisplay';

export default function ComebackPage() {
  const [trendName, setTrendName] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ComebackResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!trendName.trim()) {
      setError('Please enter a trend name');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await generateComebackContent({
        trend_name: trendName.trim(),
      });
      setResult(response);
    } catch (err: any) {
      setError(err.message || 'Failed to generate content');
      console.error('Comeback generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !loading) {
      handleGenerate();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            🎬 Comeback AI
          </h1>
          <p className="text-xl text-gray-300">
            Generate strategic content for declining or rising trends
          </p>
          <p className="text-sm text-gray-400 mt-2">
            Powered by AI · Lifecycle Detection · Decline Signal Analysis
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-8 border border-white/20">
          <div className="flex gap-4">
            <input
              type="text"
              value={trendName}
              onChange={(e) => setTrendName(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Enter trend name (e.g., fidget spinner, AI memes)"
              className="flex-1 px-6 py-4 bg-white/10 border border-white/30 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
              disabled={loading}
            />
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Generating...
                </span>
              ) : (
                '✨ Generate Content'
              )}
            </button>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-300">
              ⚠️ {error}
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-12 border border-white/20 text-center">
            <div className="flex flex-col items-center gap-4">
              <div className="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin" />
              <h3 className="text-2xl font-semibold text-white">
                Analyzing Trend...
              </h3>
              <p className="text-gray-400">
                Fetching lifecycle data → Analyzing decline signals → Generating creative content
              </p>
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <ComebackContentDisplay result={result} />
        )}

        {/* Instructions */}
        {!result && !loading && (
          <div className="bg-white/5 backdrop-blur-lg rounded-2xl p-8 border border-white/10">
            <h3 className="text-2xl font-semibold text-white mb-4">
              How It Works
            </h3>
            <div className="grid md:grid-cols-2 gap-6 text-gray-300">
              <div>
                <h4 className="font-semibold text-purple-400 mb-2">
                  🔴 COMEBACK MODE (Red/Orange Alert)
                </h4>
                <p className="text-sm">
                  For declining or saturated trends. Generates fresh angles, remix formats, and strategies to combat audience fatigue and re-engage viewers.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-green-400 mb-2">
                  🟢 GROWTH MODE (Green/Yellow Alert)
                </h4>
                <p className="text-sm">
                  For rising or emerging trends. Generates strategies to maximize reach, capture viral momentum, and scale content across platforms.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-blue-400 mb-2">
                  📊 Automatic Analysis
                </h4>
                <p className="text-sm">
                  System automatically fetches lifecycle stage, decline risk score, and generates contextual decline drivers or growth opportunities.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-yellow-400 mb-2">
                  🎨 AI-Powered Content
                </h4>
                <p className="text-sm">
                  Get 3 reel ideas, 3 captions (English + Hinglish), and 2 remix formats - all tailored to your trend's current lifecycle state.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
