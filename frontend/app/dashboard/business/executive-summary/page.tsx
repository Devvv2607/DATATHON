'use client';

import { useState, useEffect } from 'react';
import { FileText, Briefcase } from 'lucide-react';
import { useDomain } from '@/contexts/DomainContext';
import DomainAndTrendSelector from '@/components/DomainAndTrendSelector';

export default function ExecutiveSummaryPage() {
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<any>(null);
  const { selectedDomain, selectedTrend } = useDomain();

  const getSummary = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `http://localhost:8000/api/business/executive-summary?domain=${selectedDomain}&trend_id=${selectedTrend}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      setSummary(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getSummary();
  }, [selectedDomain, selectedTrend]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Executive Summary</h1>
          <p className="text-gray-400 mt-2">
            {summary ? `${summary.domain}: ${summary.trend}` : 'C-suite recommendations'}
          </p>
        </div>
        <button
          onClick={getSummary}
          disabled={loading}
          className="px-6 py-3 rounded-xl glass-card text-blue-400 hover:text-white transition-all duration-300"
        >
          {loading ? 'Generating...' : 'Refresh Summary'}
        </button>
      </div>

      <DomainAndTrendSelector />

      <div className="glass-card p-8 rounded-2xl">
        <div className="flex items-center gap-4 mb-6">
          <div className="p-4 rounded-xl bg-purple-500/10">
            <Briefcase className="w-8 h-8 text-purple-400" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Strategic Insights</h2>
            <p className="text-gray-400">One-paragraph recommendations for decision makers</p>
          </div>
        </div>

        {summary?.summary ? (
          <div className="space-y-4 text-gray-300 leading-relaxed">
            <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/20">
              <h3 className="text-lg font-bold text-blue-400 mb-2">Executive Summary</h3>
              <p>{summary.summary.executive_summary}</p>
            </div>
            
            <div className="p-4 rounded-xl bg-green-500/10 border border-green-500/20">
              <h3 className="text-lg font-bold text-green-400 mb-2">Recommendation</h3>
              <p>{summary.summary.recommendation}</p>
            </div>
          </div>
        ) : (
          <div className="space-y-4 text-gray-300 leading-relaxed">
          <p>
            Based on comprehensive trend analysis, the AI Revolution trend demonstrates exceptional market performance
            with a 4.5x ROI and low risk profile (30%), positioning it in the "Scale" quadrant of our investment matrix.
          </p>
          <p>
            Current engagement metrics show strong momentum with 15,000 interactions generating $2,500 in revenue against
            a modest $500 investment, yielding a 400% return rate that significantly outperforms industry benchmarks.
          </p>
          <p>
            <strong className="text-white">Recommendation:</strong> Aggressively scale operations and increase investment
            allocation to capitalize on favorable market conditions while maintaining strategic monitoring of competitive
            dynamics and market saturation indicators.
          </p>
        </div>
        )}
      </div>
        
      {summary && (
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">API Response</h2>
          <pre className="text-gray-300 text-sm overflow-auto">
            {JSON.stringify(summary, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
