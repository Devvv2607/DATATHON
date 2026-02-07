import { cn } from '@/lib/utils';

interface TrendCardProps {
  trend: {
    id: string;
    name: string;
    status: string;
    platforms: string[];
    metrics: {
      health_score: number;
      engagement_rate: number;
      sentiment_score: number;
    };
  };
  onClick?: () => void;
  className?: string;
}

export function TrendCard({ trend, onClick, className }: TrendCardProps) {
  const statusColors = {
    emerging: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    growing: 'bg-green-500/10 text-green-400 border-green-500/30',
    peak: 'bg-purple-500/10 text-purple-400 border-purple-500/30',
    declining: 'bg-red-500/10 text-red-400 border-red-500/30',
    faded: 'bg-gray-500/10 text-gray-400 border-gray-500/30'
  };

  const statusColor = statusColors[trend.status as keyof typeof statusColors] || statusColors.emerging;

  return (
    <div
      onClick={onClick}
      className={cn(
        'rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-purple-950/20 p-5',
        'hover:border-blue-500/50 hover:shadow-xl hover:shadow-blue-500/10 transition-all duration-300',
        'cursor-pointer backdrop-blur-sm',
        className
      )}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-white mb-2">{trend.name}</h3>
          <span className={cn('inline-block px-3 py-1 rounded-full text-xs font-semibold border', statusColor)}>
            {trend.status.toUpperCase()}
          </span>
        </div>
      </div>

      <div className="flex gap-2 mb-4">
        {trend.platforms.slice(0, 3).map((platform) => (
          <span
            key={platform}
            className="px-2 py-1 rounded-md bg-white/5 text-xs text-gray-400 capitalize"
          >
            {platform}
          </span>
        ))}
        {trend.platforms.length > 3 && (
          <span className="px-2 py-1 rounded-md bg-white/5 text-xs text-gray-400">
            +{trend.platforms.length - 3}
          </span>
        )}
      </div>

      <div className="grid grid-cols-3 gap-3">
        <div>
          <p className="text-xs text-gray-400 mb-1">Health</p>
          <p className="text-sm font-bold text-white">{trend.metrics.health_score.toFixed(1)}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400 mb-1">Engagement</p>
          <p className="text-sm font-bold text-white">{trend.metrics.engagement_rate.toFixed(1)}%</p>
        </div>
        <div>
          <p className="text-xs text-gray-400 mb-1">Sentiment</p>
          <p className="text-sm font-bold text-white">{(trend.metrics.sentiment_score * 100).toFixed(0)}%</p>
        </div>
      </div>
    </div>
  );
}
