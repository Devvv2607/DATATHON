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

      {decision && (
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">Decision Analysis</h2>
          <pre className="text-gray-300 text-sm overflow-auto">
            {JSON.stringify(decision, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
