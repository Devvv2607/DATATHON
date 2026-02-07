import { cn } from '@/lib/utils';

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon?: React.ReactNode;
  trend?: 'up' | 'down' | 'neutral';
  className?: string;
}

export function MetricCard({ title, value, change, icon, trend = 'neutral', className }: MetricCardProps) {
  const trendColor = {
    up: 'text-green-400',
    down: 'text-red-400',
    neutral: 'text-gray-400'
  }[trend];

  return (
    <div className={cn(
      'rounded-3xl glass-card p-6 group cursor-pointer',
      className
    )}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-400 font-medium mb-2">{title}</p>
          <p className="text-3xl font-bold text-white mb-1">{value}</p>
          {change !== undefined && (
            <p className={cn('text-sm font-medium', trendColor)}>
              {change > 0 && '+'}{change}%
            </p>
          )}
        </div>
        {icon && (
          <div className="flex-shrink-0 ml-4 p-3 rounded-2xl bg-blue-500/10 text-blue-400 group-hover:scale-110 group-hover:rotate-3 transition-all duration-300">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}
