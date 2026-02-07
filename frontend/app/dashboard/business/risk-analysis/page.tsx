'use client';

import { useState, useEffect } from 'react';
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react';
import { useDomain } from '@/contexts/DomainContext';
import DomainAndTrendSelector from '@/components/DomainAndTrendSelector';

export default function RiskAnalysisPage() {
  const [loading, setLoading] = useState(false);
  const [scenarios, setScenarios] = useState<any>(null);
  const { selectedDomain, selectedTrend } = useDomain();

  const analyzeRisk = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `http://localhost:8000/api/business/risk-analysis?domain=${selectedDomain}&trend_id=${selectedTrend}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      setScenarios(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    analyzeRisk();
  }, [selectedDomain, selectedTrend]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Risk Analysis</h1>
          <p className="text-gray-400 mt-2">
            {scenarios ? `${scenarios.domain}: ${scenarios.trend} (Risk: ${scenarios.current_risk?.toFixed(1)}%)` : 'What-if scenario planning'}
          </p>
        </div>
        <button
          onClick={analyzeRisk}
          disabled={loading}
          className="px-6 py-3 rounded-xl glass-card text-blue-400 hover:text-white transition-all duration-300"
        >
          {loading ? 'Analyzing...' : 'Refresh Scenarios'}
        </button>
      </div>

      <DomainAndTrendSelector />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-4">
            <CheckCircle className="w-8 h-8 text-green-400" />
            <h3 className="text-lg font-bold text-white">Best Case</h3>
          </div>
          <div className="space-y-3 text-gray-300">
            <div className="flex justify-between">
              <span>ROI:</span>
              <span className="text-green-400 font-bold">6.2x</span>
            </div>
            <div className="flex justify-between">
              <span>Growth:</span>
              <span className="text-green-400">+180%</span>
            </div>
            <div className="flex justify-between">
              <span>Risk:</span>
              <span className="text-green-400">Low</span>
            </div>
          </div>
        </div>

        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-4">
            <Shield className="w-8 h-8 text-blue-400" />
            <h3 className="text-lg font-bold text-white">Expected Case</h3>
          </div>
          <div className="space-y-3 text-gray-300">
            <div className="flex justify-between">
              <span>ROI:</span>
              <span className="text-blue-400 font-bold">4.5x</span>
            </div>
            <div className="flex justify-between">
              <span>Growth:</span>
              <span className="text-blue-400">+120%</span>
            </div>
            <div className="flex justify-between">
              <span>Risk:</span>
              <span className="text-blue-400">Medium</span>
            </div>
          </div>
        </div>

        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-4">
            <AlertTriangle className="w-8 h-8 text-red-400" />
            <h3 className="text-lg font-bold text-white">Worst Case</h3>
          </div>
          <div className="space-y-3 text-gray-300">
            <div className="flex justify-between">
              <span>ROI:</span>
              <span className="text-red-400 font-bold">2.1x</span>
            </div>
            <div className="flex justify-between">
              <span>Growth:</span>
              <span className="text-red-400">+45%</span>
            </div>
            <div className="flex justify-between">
              <span>Risk:</span>
              <span className="text-red-400">High</span>
            </div>
          </div>
        </div>
      </div>

      {scenarios && (
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">Scenario Analysis</h2>
          <pre className="text-gray-300 text-sm overflow-auto">
            {JSON.stringify(scenarios, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
