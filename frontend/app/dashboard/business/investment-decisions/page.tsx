'use client';

import { useState, useEffect } from 'react';
import { Target, AlertCircle } from 'lucide-react';
import { useDomain } from '@/contexts/DomainContext';
import DomainAndTrendSelector from '@/components/DomainAndTrendSelector';

export default function InvestmentDecisionsPage() {
  const [loading, setLoading] = useState(false);
  const [decision, setDecision] = useState<any>(null);
  const { selectedDomain, selectedTrend } = useDomain();

  const getDecision = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `http://localhost:8000/api/business/investment-decision?domain=${selectedDomain}&trend_id=${selectedTrend}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      setDecision(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getDecision();
  }, [selectedDomain, selectedTrend]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Investment Decisions</h1>
          <p className="text-gray-400 mt-2">
            {decision ? `${decision.domain}: ${decision.trend}` : 'Risk × ROI matrix analysis'}
          </p>
        </div>
        <button
          onClick={getDecision}
          disabled={loading}
          className="px-6 py-3 rounded-xl glass-card text-blue-400 hover:text-white transition-all duration-300"
        >
          {loading ? 'Analyzing...' : 'Refresh Analysis'}
        </button>
      </div>

      <DomainAndTrendSelector />

      <div className="glass-card p-8 rounded-2xl">
        <div className="grid grid-cols-2 gap-8">
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Target className="w-8 h-8 text-green-400" />
              <div>
                <h3 className="text-lg font-bold text-white">Scale</h3>
                <p className="text-sm text-gray-400">High ROI, Low Risk</p>
              </div>
            </div>
            <p className="text-gray-300">Invest heavily and expand operations</p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Target className="w-8 h-8 text-blue-400" />
              <div>
                <h3 className="text-lg font-bold text-white">Tactical</h3>
                <p className="text-sm text-gray-400">High ROI, High Risk</p>
              </div>
            </div>
            <p className="text-gray-300">Proceed with caution and monitoring</p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <Target className="w-8 h-8 text-yellow-400" />
              <div>
                <h3 className="text-lg font-bold text-white">Monitor</h3>
                <p className="text-sm text-gray-400">Low ROI, Low Risk</p>
              </div>
            </div>
            <p className="text-gray-300">Watch and optimize performance</p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <AlertCircle className="w-8 h-8 text-red-400" />
              <div>
                <h3 className="text-lg font-bold text-white">Exit</h3>
                <p className="text-sm text-gray-400">Low ROI, High Risk</p>
              </div>
            </div>
            <p className="text-gray-300">Discontinue or divest immediately</p>
          </div>
        </div>
      </div>

      {decision?.decision && (
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-6">Decision Analysis</h2>
          <div className="space-y-4">
            <div className="p-6 rounded-xl bg-gradient-to-br from-blue-500/10 to-blue-600/5 border border-blue-500/20">
              <div className="flex items-center justify-between mb-4">
                <div className="text-sm text-gray-400 uppercase tracking-wider">Recommended Action</div>
                <div className="text-2xl">🎯</div>
              </div>
              <div className="text-2xl font-bold text-blue-400 mb-2">
                {decision.decision.investment_decision?.recommended_action || 'N/A'}
              </div>
              <div className="text-gray-300 leading-relaxed">
                {decision.decision.investment_decision?.explanation || 'No explanation available'}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-slate-800/50">
                <div className="text-sm text-gray-400 uppercase tracking-wider mb-2">ROI</div>
                <div className="text-2xl font-bold text-green-400">
                  {decision.decision.investment_decision?.roi ? `${(decision.decision.investment_decision.roi * 100).toFixed(1)}%` : 'N/A'}
                </div>
              </div>
              <div className="p-4 rounded-xl bg-slate-800/50">
                <div className="text-sm text-gray-400 uppercase tracking-wider mb-2">Risk Level</div>
                <div className="text-2xl font-bold text-orange-400">
                  {decision.decision.investment_decision?.risk_level ? `${(decision.decision.investment_decision.risk_level * 100).toFixed(0)}%` : 'N/A'}
                </div>
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-800/50">
              <div className="text-sm text-gray-400 uppercase tracking-wider mb-2">Domain & Trend</div>
              <div className="text-white font-medium">{decision.domain} · {decision.trend}</div>
            </div>

            {decision.success !== undefined && (
              <div className="p-4 rounded-xl bg-slate-800/50">
                <div className="text-sm text-gray-400 uppercase tracking-wider mb-2">Status</div>
                <div className={`inline-flex px-3 py-1 rounded-full text-sm font-medium ${
                  decision.success ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                }`}>
                  {decision.success ? 'Analysis Complete' : 'Analysis Failed'}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
