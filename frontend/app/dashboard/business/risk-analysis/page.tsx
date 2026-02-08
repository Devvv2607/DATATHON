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

      {scenarios && scenarios.scenarios?.decision_levers && (
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-3">
            <Shield className="w-6 h-6 text-blue-400" />
            Risk Management Strategy
          </h2>
          <div className="space-y-4">
            {scenarios.scenarios.decision_levers.risk_reduction && (
              <div className="p-6 rounded-xl bg-green-500/10 border border-green-500/20">
                <div className="text-sm text-green-400 font-semibold uppercase tracking-wider mb-2">Risk Reduction</div>
                <div className="text-gray-200 text-lg leading-relaxed">
                  {scenarios.scenarios.decision_levers.risk_reduction.join(', ')}
                </div>
              </div>
            )}
            {scenarios.scenarios.decision_levers.risk_escalation && (
              <div className="p-6 rounded-xl bg-red-500/10 border border-red-500/20">
                <div className="text-sm text-red-400 font-semibold uppercase tracking-wider mb-2">Risk Escalation</div>
                <div className="text-gray-200 text-lg leading-relaxed">
                  {scenarios.scenarios.decision_levers.risk_escalation.join(', ')}
                </div>
              </div>
            )}
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-slate-800/50">
                <div className="text-sm text-gray-400 uppercase tracking-wider mb-2">Domain</div>
                <div className="text-white font-medium">{scenarios.domain}</div>
              </div>
              <div className="p-4 rounded-xl bg-slate-800/50">
                <div className="text-sm text-gray-400 uppercase tracking-wider mb-2">Trend</div>
                <div className="text-white font-medium">{scenarios.trend}</div>
              </div>
            </div>
            {scenarios.success !== undefined && (
              <div className="inline-flex px-3 py-1 rounded-full text-sm font-medium ${
                scenarios.success ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
              }">
                {scenarios.success ? 'Analysis Complete' : 'Analysis Failed'}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
