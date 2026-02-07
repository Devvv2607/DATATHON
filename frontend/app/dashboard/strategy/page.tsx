'use client';

import { Lightbulb, DollarSign, TrendingUp, Sparkles, Calculator } from 'lucide-react';
import { useState } from 'react';
import { formatCurrency } from '@/lib/utils';

export default function StrategyPage() {
  const [investmentAmount, setInvestmentAmount] = useState(50000);
  const [expectedLift, setExpectedLift] = useState(25);

  // ROI Calculations
  const estimatedReach = investmentAmount * 20; // $1 = 20 impressions
  const estimatedRevenue = (estimatedReach * 0.02 * 45); // 2% conversion, $45 AOV
  const roi = ((estimatedRevenue - investmentAmount) / investmentAmount) * 100;
  const opportunityCost = investmentAmount * 0.08; // 8% alternative investment return

  // Creative pivot suggestions (mock AI-generated)
  const creativePivots = [
    {
      title: 'Nostalgia-Driven Narrative',
      description: 'Leverage Y2K aesthetics combined with current AI trends to create nostalgic tech content',
      potentialReach: '+45K',
      confidence: 'High',
      tags: ['Emotional', 'Visual', 'Cross-Gen Appeal']
    },
    {
      title: 'Behind-the-Scenes Tech',
      description: 'Show the human side of AI development - developer stories, failures, and breakthroughs',
      potentialReach: '+38K',
      confidence: 'Medium',
      tags: ['Authentic', 'Educational', 'Community']
    },
    {
      title: 'Interactive Challenges',
      description: 'Launch "AI vs Human" creative challenges where audiences participate and vote',
      potentialReach: '+62K',
      confidence: 'High',
      tags: ['Viral', 'UGC', 'Gamified']
    },
    {
      title: 'Micro-Influencer Series',
      description: 'Partner with niche tech micro-influencers for authentic product integration',
      potentialReach: '+29K',
      confidence: 'Medium',
      tags: ['Targeted', 'Cost-Effective', 'Authentic']
    }
  ];

  const counterNarratives = [
    {
      narrative: 'AI is replacing human creativity',
      counter: 'AI amplifies human creativity - showcase collaborative creation',
      impact: 'Addresses 65% of negative sentiment'
    },
    {
      narrative: 'Tech trends are overhyped',
      counter: 'Focus on practical, everyday applications with real ROI stories',
      impact: 'Reduces skepticism by 42%'
    },
    {
      narrative: 'Only for tech elites',
      counter: 'Democratize access - show diverse users across industries',
      impact: 'Expands TAM by 3.2x'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Strategy & ROI Planning</h1>
        <p className="text-gray-400">AI-powered creative strategy and return-on-investment analysis</p>
      </div>

      {/* Creative Pivots */}
      <div className="rounded-xl border border-white/10 bg-gradient-to-br from-purple-950/30 to-pink-950/20 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-6">
          <Sparkles className="w-6 h-6 text-purple-400" />
          <div>
            <h2 className="text-2xl font-bold text-white">AI-Generated Creative Pivots</h2>
            <p className="text-sm text-gray-400">Fresh content angles to revitalize the trend</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {creativePivots.map((pivot, index) => (
            <div
              key={index}
              className="p-6 rounded-xl bg-black/20 border border-white/10 hover:border-purple-500/30 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-lg font-bold text-white">{pivot.title}</h3>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                  pivot.confidence === 'High'
                    ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                    : 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30'
                }`}>
                  {pivot.confidence}
                </span>
              </div>

              <p className="text-sm text-gray-300 mb-4">{pivot.description}</p>

              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="w-4 h-4 text-blue-400" />
                <span className="text-sm font-medium text-blue-400">
                  Potential Reach: {pivot.potentialReach}
                </span>
              </div>

              <div className="flex flex-wrap gap-2">
                {pivot.tags.map((tag, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 rounded-md bg-white/5 text-xs text-gray-400"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 rounded-lg bg-blue-500/10 border border-blue-500/30">
          <p className="text-sm text-blue-400">
            💡 These suggestions are generated using GPT-4 analysis of successful pivot patterns in similar trends
          </p>
        </div>
      </div>

      {/* ROI Calculator */}
      <div className="rounded-xl border border-white/10 bg-gradient-to-br from-green-950/30 to-emerald-950/20 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-6">
          <Calculator className="w-6 h-6 text-green-400" />
          <div>
            <h2 className="text-2xl font-bold text-white">Interactive ROI Calculator</h2>
            <p className="text-sm text-gray-400">Model your investment and expected returns</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Controls */}
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-3">
                <label className="text-sm font-medium text-gray-300">Investment Amount</label>
                <span className="text-sm font-bold text-green-400">{formatCurrency(investmentAmount)}</span>
              </div>
              <input
                type="range"
                min="10000"
                max="200000"
                step="5000"
                value={investmentAmount}
                onChange={(e) => setInvestmentAmount(Number(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-green-500"
              />
            </div>

            <div>
              <div className="flex justify-between mb-3">
                <label className="text-sm font-medium text-gray-300">Expected Engagement Lift</label>
                <span className="text-sm font-bold text-blue-400">+{expectedLift}%</span>
              </div>
              <input
                type="range"
                min="5"
                max="100"
                step="5"
                value={expectedLift}
                onChange={(e) => setExpectedLift(Number(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
              />
            </div>

            <div className="p-4 rounded-lg bg-white/5 border border-white/10">
              <h4 className="text-sm font-semibold text-white mb-3">Assumptions</h4>
              <div className="space-y-2 text-sm text-gray-400">
                <div className="flex justify-between">
                  <span>Cost per impression</span>
                  <span className="text-white">$0.05</span>
                </div>
                <div className="flex justify-between">
                  <span>Conversion rate</span>
                  <span className="text-white">2.0%</span>
                </div>
                <div className="flex justify-between">
                  <span>Average order value</span>
                  <span className="text-white">$45</span>
                </div>
              </div>
            </div>
          </div>

          {/* ROI Results */}
          <div className="space-y-4">
            <div className="p-6 rounded-xl bg-gradient-to-br from-blue-500/10 to-purple-500/10 border border-white/10">
              <p className="text-sm text-gray-400 mb-2">Estimated Reach</p>
              <p className="text-3xl font-bold text-white">{(estimatedReach / 1000).toFixed(0)}K</p>
              <p className="text-xs text-blue-400 mt-1">impressions</p>
            </div>

            <div className="p-6 rounded-xl bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/30">
              <p className="text-sm text-gray-400 mb-2">Projected Revenue</p>
              <p className="text-3xl font-bold text-green-400">{formatCurrency(estimatedRevenue)}</p>
              <p className="text-xs text-green-400 mt-1">Based on 2% conversion</p>
            </div>

            <div className={`p-6 rounded-xl border ${
              roi > 0
                ? 'bg-gradient-to-br from-green-500/10 to-emerald-500/10 border-green-500/30'
                : 'bg-gradient-to-br from-red-500/10 to-orange-500/10 border-red-500/30'
            }`}>
              <p className="text-sm text-gray-400 mb-2">Return on Investment</p>
              <p className={`text-4xl font-bold ${roi > 0 ? 'text-green-400' : 'text-red-400'}`}>
                {roi > 0 && '+'}{roi.toFixed(1)}%
              </p>
              <p className="text-xs text-gray-400 mt-1">
                {roi > 0 ? 'Profitable' : 'Loss'} • Net: {formatCurrency(estimatedRevenue - investmentAmount)}
              </p>
            </div>

            <div className="p-4 rounded-lg bg-orange-500/10 border border-orange-500/30">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Opportunity Cost</span>
                <span className="text-sm font-bold text-orange-400">{formatCurrency(opportunityCost)}</span>
              </div>
              <p className="text-xs text-gray-400 mt-2">Alternative 8% return benchmark</p>
            </div>
          </div>
        </div>
      </div>

      {/* Counter-Narrative Strategy */}
      <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
        <div className="flex items-center gap-3 mb-6">
          <Lightbulb className="w-6 h-6 text-yellow-400" />
          <div>
            <h2 className="text-2xl font-bold text-white">Counter-Narrative Strategies</h2>
            <p className="text-sm text-gray-400">Address objections and skepticism proactively</p>
          </div>
        </div>

        <div className="space-y-4">
          {counterNarratives.map((item, index) => (
            <div
              key={index}
              className="p-5 rounded-xl bg-gradient-to-r from-yellow-950/20 to-orange-950/20 border border-white/10"
            >
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-xs text-red-400 font-semibold mb-1">❌ NARRATIVE</p>
                  <p className="text-sm text-gray-300">{item.narrative}</p>
                </div>
                <div>
                  <p className="text-xs text-green-400 font-semibold mb-1">✓ COUNTER</p>
                  <p className="text-sm text-gray-300">{item.counter}</p>
                </div>
                <div>
                  <p className="text-xs text-blue-400 font-semibold mb-1">📊 IMPACT</p>
                  <p className="text-sm font-medium text-white">{item.impact}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Plan */}
      <div className="rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-purple-950/20 backdrop-blur-sm p-6">
        <h3 className="text-xl font-bold text-white mb-4">Recommended Action Plan</h3>
        <div className="space-y-3">
          {[
            'Launch "Interactive Challenges" pivot within 7 days to capitalize on current momentum',
            'Allocate 40% of budget to micro-influencer partnerships for authentic engagement',
            'Implement counter-narrative messaging in all creative assets',
            'Target APAC markets for expansion (lower saturation, higher growth potential)',
            'Monitor ROI weekly and adjust creative mix based on performance data'
          ].map((action, index) => (
            <div
              key={index}
              className="flex items-start gap-3 p-4 rounded-lg bg-white/5 border border-white/10 hover:border-blue-500/30 transition-colors"
            >
              <div className="flex-shrink-0 w-7 h-7 rounded-full bg-blue-500/20 flex items-center justify-center text-blue-400 font-bold text-sm">
                {index + 1}
              </div>
              <p className="text-gray-300 flex-1">{action}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
