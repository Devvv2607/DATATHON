'use client';

import { useState, useEffect } from 'react';
import { GitBranch, TrendingUp, ArrowRight } from 'lucide-react';
import { useDomain } from '@/contexts/DomainContext';
import DomainAndTrendSelector from '@/components/DomainAndTrendSelector';

export default function AlternativeTrendsPage() {
  const [loading, setLoading] = useState(false);
  const [alternatives, setAlternatives] = useState<any>(null);
  const { selectedDomain, selectedTrend } = useDomain();

  const findAlternatives = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `http://localhost:8000/api/business/alternative-trends?domain=${selectedDomain}&trend_id=${selectedTrend}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      setAlternatives(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    findAlternatives();
  }, [selectedDomain, selectedTrend]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Alternative Trends</h1>
          <p className="text-gray-400 mt-2">
            {alternatives ? `${alternatives.domain}: Pivoting from ${alternatives.current_trend}` : 'Discover pivot opportunities'}
          </p>
        </div>
        <button
          onClick={findAlternatives}
          disabled={loading}
          className="px-6 py-3 rounded-xl glass-card text-blue-400 hover:text-white transition-all duration-300"
        >
          {loading ? 'Searching...' : 'Refresh Alternatives'}
        </button>
      </div>

      <DomainAndTrendSelector />

      <div className="space-y-4">
        {alternatives?.alternatives?.alternatives?.pivot_targets?.length > 0 ? (
          alternatives.alternatives.alternatives.pivot_targets.map((trend: any, i: number) => (
            <div key={i} className="glass-card p-6 rounded-2xl hover:border-blue-500/30 transition-all duration-300 border border-transparent">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="p-3 rounded-xl bg-blue-500/10">
                    <GitBranch className="w-6 h-6 text-blue-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white">{trend.keyword || 'Alternative Trend'}</h3>
                    <p className="text-sm text-gray-400">
                      Growth: {trend.growth_rate ? `${trend.growth_rate > 0 ? '+' : ''}${trend.growth_rate}%` : 'N/A'} • 
                      Difficulty: {trend.difficulty || 'Unknown'}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-2xl font-bold ${trend.growth_rate > 50 ? 'text-green-400' : 'text-blue-400'}`}>
                    {trend.growth_rate ? `${trend.growth_rate > 0 ? '+' : ''}${trend.growth_rate}%` : 'N/A'}
                  </div>
                  <div className={`text-sm ${
                    trend.difficulty === 'low' ? 'text-green-400' : 
                    trend.difficulty === 'medium' ? 'text-yellow-400' : 'text-red-400'
                  }`}>
                    {trend.difficulty ? trend.difficulty.charAt(0).toUpperCase() + trend.difficulty.slice(1) : 'Unknown'} Risk
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          [
            { name: 'Quantum Computing', growth: '+145%', risk: 'Medium' },
            { name: 'Edge AI', growth: '+98%', risk: 'Low' },
            { name: 'Neural Interfaces', growth: '+76%', risk: 'High' },
            { name: 'Green Tech AI', growth: '+62%', risk: 'Low' }
          ].map((trend, i) => (
            <div key={i} className="glass-card p-6 rounded-2xl hover:border-blue-500/30 transition-all duration-300 border border-transparent">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="p-3 rounded-xl bg-blue-500/10">
                    <GitBranch className="w-6 h-6 text-blue-400" />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white">{trend.name}</h3>
                    <div className="flex items-center gap-4 mt-1">
                      <span className="text-sm text-gray-400">Risk: {trend.risk}</span>
                      <span className="text-sm text-green-400">{trend.growth}</span>
                    </div>
                  </div>
                </div>
                <button className="p-3 rounded-xl glass-card hover:text-blue-400 transition-all">
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {alternatives && alternatives.alternatives?.strategy && (
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-3">
            <TrendingUp className="w-6 h-6 text-blue-400" />
            Pivot Strategy
          </h2>
          <div className="space-y-4">
            <div className="p-6 rounded-xl bg-gradient-to-br from-purple-500/10 to-blue-500/5 border border-purple-500/20">
              <div className="text-gray-300 text-lg leading-relaxed">
                {alternatives.alternatives.strategy}
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-slate-800/50">
                <div className="text-sm text-gray-400 uppercase tracking-wider mb-2">Current Domain</div>
                <div className="text-white font-medium">{alternatives.domain}</div>
              </div>
              <div className="p-4 rounded-xl bg-slate-800/50">
                <div className="text-sm text-gray-400 uppercase tracking-wider mb-2">Current Trend</div>
                <div className="text-white font-medium">{alternatives.current_trend}</div>
              </div>
            </div>
            {alternatives.success !== undefined && (
              <div className="inline-flex px-3 py-1 rounded-full text-sm font-medium ${
                alternatives.success ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              }">
                {alternatives.success ? 'Analysis Complete' : 'Analysis Failed'}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
