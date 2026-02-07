'use client';

import { useEffect, useState } from 'react';
import { getExplanation, type ExplanationResponse } from '@/lib/api';
import { Brain, AlertCircle, TrendingUp, TrendingDown, Lightbulb } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function ExplainabilityPage() {
  const [explanation, setExplanation] = useState<ExplanationResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const data = await getExplanation('trend_1');
      setExplanation(data);
      setLoading(false);
    }
    loadData();
  }, []);

  if (loading || !explanation) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  const chartData = explanation.feature_attributions.map(attr => ({
    name: attr.feature,
    value: Math.abs(attr.impact),
    impact: attr.impact,
    direction: attr.direction
  }));

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Explainable AI Insights</h1>
        <p className="text-gray-400">Understanding why trends decline through feature attribution</p>
      </div>

      {/* Summary Card */}
      <div className="rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-purple-950/20 backdrop-blur-sm p-8">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-14 h-14 rounded-xl bg-blue-500/20 flex items-center justify-center">
            <Brain className="w-7 h-7 text-blue-400" />
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-white mb-3">{explanation.summary}</h2>
            <p className="text-gray-300 leading-relaxed mb-4">{explanation.detailed_explanation}</p>
            <div className="flex items-center gap-2 text-sm">
              <AlertCircle className="w-4 h-4 text-yellow-400" />
              <span className="text-yellow-400 font-medium">{explanation.confidence}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Feature Attribution Chart */}
      <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">Feature Attribution Analysis</h2>
          <p className="text-sm text-gray-400">SHAP values showing impact of each factor on decline prediction</p>
        </div>

        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData} layout="vertical" margin={{ left: 150, right: 30 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis 
              type="number" 
              stroke="rgba(255,255,255,0.3)"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              type="category" 
              dataKey="name" 
              stroke="rgba(255,255,255,0.3)"
              style={{ fontSize: '12px' }}
              width={140}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(17, 24, 39, 0.95)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '8px',
                padding: '12px'
              }}
              formatter={(value: any, name: any, props: any) => [
                `${(props.payload.impact * 100).toFixed(1)}%`,
                props.payload.direction === 'decline' ? 'Increases Risk' : 'Decreases Risk'
              ]}
            />
            <Bar dataKey="value" radius={[0, 8, 8, 0]}>
              {chartData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.direction === 'decline' ? 'rgb(239, 68, 68)' : 'rgb(34, 197, 94)'} 
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        <div className="mt-6 grid grid-cols-2 gap-4">
          <div className="flex items-center gap-2 p-3 rounded-lg bg-red-500/10 border border-red-500/30">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <span className="text-sm text-gray-300">Increases Decline Risk</span>
          </div>
          <div className="flex items-center gap-2 p-3 rounded-lg bg-green-500/10 border border-green-500/30">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span className="text-sm text-gray-300">Decreases Decline Risk</span>
          </div>
        </div>
      </div>

      {/* Detailed Attribution Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {explanation.feature_attributions.slice(0, 6).map((attr) => {
          const isNegative = attr.direction === 'decline';
          return (
            <div
              key={attr.feature}
              className={`rounded-xl border p-5 backdrop-blur-sm ${
                isNegative
                  ? 'bg-gradient-to-br from-red-950/30 to-orange-950/20 border-red-500/30'
                  : 'bg-gradient-to-br from-green-950/30 to-emerald-950/20 border-green-500/30'
              }`}
            >
              <div className="flex items-center gap-2 mb-3">
                {isNegative ? (
                  <TrendingDown className="w-5 h-5 text-red-400" />
                ) : (
                  <TrendingUp className="w-5 h-5 text-green-400" />
                )}
                <h3 className="font-semibold text-white text-sm">{attr.feature}</h3>
              </div>
              <div className="mb-2">
                <span className={`text-3xl font-bold ${isNegative ? 'text-red-400' : 'text-green-400'}`}>
                  {attr.impact > 0 ? '+' : ''}{(attr.impact * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-xs text-gray-400">
                {isNegative ? 'Contributing to decline risk' : 'Mitigating decline risk'}
              </p>
            </div>
          );
        })}
      </div>

      {/* Counterfactual Scenarios */}
      <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">What-If Counterfactual Scenarios</h2>
          <p className="text-sm text-gray-400">Explore how changes would affect the prediction</p>
        </div>

        <div className="space-y-4">
          {explanation.counterfactuals.map((cf, index) => (
            <div
              key={index}
              className="p-5 rounded-xl bg-gradient-to-r from-blue-950/30 to-purple-950/20 border border-white/10"
            >
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center text-purple-400 font-bold">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-white mb-2">{cf.scenario}</h4>
                  <div className="grid grid-cols-2 gap-4 mb-3">
                    <div className="p-3 rounded-lg bg-white/5">
                      <p className="text-xs text-gray-400 mb-1">Current Probability</p>
                      <p className="text-xl font-bold text-red-400">72%</p>
                    </div>
                    <div className="p-3 rounded-lg bg-green-500/10">
                      <p className="text-xs text-gray-400 mb-1">New Probability</p>
                      <p className="text-xl font-bold text-green-400">
                        {(cf.predicted_probability * 100).toFixed(0)}%
                      </p>
                    </div>
                  </div>
                  <p className="text-sm text-gray-300">{cf.outcome}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="rounded-xl border border-white/10 bg-gradient-to-br from-green-950/30 to-emerald-950/20 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-6">
          <Lightbulb className="w-6 h-6 text-green-400" />
          <h2 className="text-2xl font-bold text-white">Actionable Recommendations</h2>
        </div>

        <div className="space-y-3">
          {explanation.recommendations.map((rec, index) => (
            <div
              key={index}
              className="flex items-start gap-3 p-4 rounded-lg bg-white/5 border border-white/10 hover:border-green-500/30 transition-colors"
            >
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500/20 flex items-center justify-center text-green-400 text-sm font-bold">
                {index + 1}
              </div>
              <p className="text-gray-300 flex-1">{rec}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
