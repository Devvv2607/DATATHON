'use client';

import { ComebackResponse } from '@/lib/comeback-api';

interface Props {
  result: ComebackResponse;
}

export default function ComebackContentDisplay({ result }: Props) {
  const modeColor = result.mode.includes('COMEBACK') ? 'red' : 'green';
  const alertColor = {
    red: 'bg-red-500',
    orange: 'bg-orange-500',
    yellow: 'bg-yellow-500',
    green: 'bg-green-500',
  }[result.alert_level] || 'bg-gray-500';

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2">
              {result.trend_name}
            </h2>
            <div className="flex items-center gap-4 text-sm">
              <span className={`px-4 py-2 ${alertColor} text-white font-semibold rounded-full`}>
                {result.alert_level.toUpperCase()} ALERT
              </span>
              <span className="px-4 py-2 bg-purple-600 text-white font-semibold rounded-full">
                {result.mode}
              </span>
              <span className="text-gray-300">
                Stage {result.lifecycle_stage}: {result.stage_name}
              </span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-4xl font-bold text-white">
              {result.decline_risk_score.toFixed(0)}
            </div>
            <div className="text-sm text-gray-400">Risk Score</div>
          </div>
        </div>

        <div className="bg-white/5 rounded-xl p-4">
          <h3 className="font-semibold text-white mb-2">
            📋 Content Strategy
          </h3>
          <p className="text-gray-300">{result.content_strategy}</p>
        </div>

        {/* Decline Drivers or Growth Opportunities */}
        {result.decline_drivers && (
          <div className="mt-4 bg-red-500/10 border border-red-500/30 rounded-xl p-4">
            <h3 className="font-semibold text-red-400 mb-2">
              ⚠️ Decline Drivers Addressed
            </h3>
            <ul className="space-y-1">
              {result.decline_drivers.map((driver, idx) => (
                <li key={idx} className="text-gray-300 text-sm">
                  • {driver}
                </li>
              ))}
            </ul>
          </div>
        )}

        {result.growth_opportunities && (
          <div className="mt-4 bg-green-500/10 border border-green-500/30 rounded-xl p-4">
            <h3 className="font-semibold text-green-400 mb-2">
              🚀 Growth Opportunities
            </h3>
            <ul className="space-y-1">
              {result.growth_opportunities.map((opp, idx) => (
                <li key={idx} className="text-gray-300 text-sm">
                  • {opp}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Reel Ideas */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          📹 Reel Ideas
          <span className="text-sm font-normal text-gray-400">
            ({result.content.reels.length} ideas)
          </span>
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          {result.content.reels.map((reel) => (
            <div
              key={reel.id}
              className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-xl p-6 hover:border-purple-500/60 transition-all"
            >
              <div className="text-purple-400 font-bold text-sm mb-2">
                REEL #{reel.id}
              </div>
              <h4 className="text-xl font-bold text-white mb-3">
                {reel.title}
              </h4>
              <p className="text-gray-300 text-sm mb-4">
                {reel.description}
              </p>
              <div className="bg-white/10 rounded-lg p-3 mb-3">
                <div className="text-xs font-semibold text-purple-400 mb-1">
                  HOOK:
                </div>
                <div className="text-white text-sm italic">
                  "{reel.hook}"
                </div>
              </div>
              <div className="bg-white/10 rounded-lg p-3">
                <div className="text-xs font-semibold text-green-400 mb-1">
                  WHY IT WORKS:
                </div>
                <div className="text-gray-300 text-xs">
                  {reel.why_it_works}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Captions */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          📝 Captions & Hooks
          <span className="text-sm font-normal text-gray-400">
            ({result.content.captions.length} captions)
          </span>
        </h3>
        <div className="grid md:grid-cols-3 gap-6">
          {result.content.captions.map((caption) => (
            <div
              key={caption.id}
              className="bg-blue-600/10 border border-blue-500/30 rounded-xl p-6 hover:border-blue-500/60 transition-all"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-blue-400 font-bold text-sm">
                  CAPTION #{caption.id}
                </span>
                <span className="px-3 py-1 bg-blue-600/30 text-blue-300 text-xs font-semibold rounded-full">
                  {caption.language}
                </span>
              </div>
              <p className="text-white text-lg font-medium">
                "{caption.caption}"
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Remix Formats */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
        <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
          🎬 Remix Formats
          <span className="text-sm font-normal text-gray-400">
            ({result.content.remixes.length} formats)
          </span>
        </h3>
        <div className="grid md:grid-cols-2 gap-6">
          {result.content.remixes.map((remix) => (
            <div
              key={remix.id}
              className="bg-gradient-to-br from-orange-600/20 to-yellow-600/20 border border-orange-500/30 rounded-xl p-6 hover:border-orange-500/60 transition-all"
            >
              <div className="text-orange-400 font-bold text-sm mb-2">
                FORMAT #{remix.id}
              </div>
              <h4 className="text-2xl font-bold text-white mb-3">
                {remix.format}
              </h4>
              <div className="bg-white/10 rounded-lg p-4 mb-3">
                <div className="text-xs font-semibold text-orange-400 mb-2">
                  STRUCTURE:
                </div>
                <p className="text-gray-300 text-sm">
                  {remix.structure}
                </p>
              </div>
              <div className="bg-white/10 rounded-lg p-4">
                <div className="text-xs font-semibold text-yellow-400 mb-2">
                  EXAMPLE:
                </div>
                <p className="text-gray-300 text-sm italic">
                  {remix.example}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Metadata */}
      <div className="bg-white/5 backdrop-blur-lg rounded-xl p-4 border border-white/10 text-center text-sm text-gray-400">
        Generated at {new Date(result.generated_at).toLocaleString()} · Confidence: {result.confidence}
      </div>
    </div>
  );
}
