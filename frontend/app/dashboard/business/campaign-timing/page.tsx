'use client';

import { useState, useEffect } from 'react';
import { Calendar, Clock, Hash } from 'lucide-react';
import { useDomain } from '@/contexts/DomainContext';
import DomainAndTrendSelector from '@/components/DomainAndTrendSelector';

export default function CampaignTimingPage() {
  const [loading, setLoading] = useState(false);
  const [timing, setTiming] = useState<any>(null);
  const { selectedDomain, selectedTrend } = useDomain();

  const getTiming = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `http://localhost:8000/api/business/campaign-timing?domain=${selectedDomain}&trend_id=${selectedTrend}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      setTiming(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getTiming();
  }, [selectedDomain, selectedTrend]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Campaign Timing</h1>
          <p className="text-gray-400 mt-2">
            {timing ? `${timing.domain}: ${timing.trend}` : 'Optimal posting times & hashtags'}
          </p>
        </div>
        <button
          onClick={getTiming}
          disabled={loading}
          className="px-6 py-3 rounded-xl glass-card text-blue-400 hover:text-white transition-all duration-300"
        >
          {loading ? 'Calculating...' : 'Refresh Timing'}
        </button>
      </div>

      <DomainAndTrendSelector />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-6">
            <Clock className="w-6 h-6 text-blue-400" />
            <h2 className="text-xl font-bold text-white">Best Posting Times</h2>
          </div>
          <div className="space-y-4">
            {timing?.timing?.optimal_times ? (
              timing.timing.optimal_times.map((time: string, i: number) => (
                <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/5">
                  <span className="text-gray-300">{time}</span>
                  <span className="text-green-400 text-sm font-medium">High Engagement</span>
                </div>
              ))
            ) : (
              ['Monday 9-11 AM EST', 'Wednesday 1-3 PM EST', 'Friday 5-7 PM EST'].map((time, i) => (
                <div key={i} className="flex items-center justify-between p-4 rounded-xl bg-white/5">
                  <span className="text-gray-300">{time}</span>
                  <span className="text-green-400 text-sm font-medium">High Engagement</span>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-6">
            <Hash className="w-6 h-6 text-purple-400" />
            <h2 className="text-xl font-bold text-white">Recommended Hashtags</h2>
          </div>
          <div className="flex flex-wrap gap-3">
            {timing?.timing?.recommended_hashtags ? (
              timing.timing.recommended_hashtags.slice(0, 8).map((tag: string, i: number) => (
                <span key={i} className="px-4 py-2 rounded-xl glass-card text-blue-400 text-sm">
                  {tag}
                </span>
              ))
            ) : (
              ['#AIRevolution', '#TechTrends', '#Innovation', '#FutureTech', '#MachineLearning', '#DigitalTransformation'].map((tag, i) => (
                <span key={i} className="px-4 py-2 rounded-xl glass-card text-blue-400 text-sm">
                  {tag}
                </span>
              ))
            )}
          </div>
        </div>
      </div>

      {timing && (
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">Timing Analysis</h2>
          <pre className="text-gray-300 text-sm overflow-auto">
            {JSON.stringify(timing, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
