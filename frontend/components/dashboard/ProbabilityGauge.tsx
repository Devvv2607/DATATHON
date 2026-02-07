'use client';

import { cn } from '@/lib/utils';

interface ProbabilityGaugeProps {
  value: number; // 0-1
  label?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function ProbabilityGauge({ value, label = 'Decline Probability', size = 'md', className }: ProbabilityGaugeProps) {
  const percentage = Math.round(value * 100);
  
  // Determine color based on risk level
  const getColor = () => {
    if (value >= 0.7) return { stroke: 'rgb(239, 68, 68)', bg: 'rgba(239, 68, 68, 0.1)' };
    if (value >= 0.5) return { stroke: 'rgb(251, 191, 36)', bg: 'rgba(251, 191, 36, 0.1)' };
    return { stroke: 'rgb(34, 197, 94)', bg: 'rgba(34, 197, 94, 0.1)' };
  };

  const colors = getColor();
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (value * circumference);

  const sizeMap = {
    sm: { width: 120, fontSize: 'text-2xl', labelSize: 'text-xs' },
    md: { width: 160, fontSize: 'text-3xl', labelSize: 'text-sm' },
    lg: { width: 200, fontSize: 'text-4xl', labelSize: 'text-base' }
  };

  const { width, fontSize, labelSize } = sizeMap[size];

  return (
    <div className={cn('flex flex-col items-center', className)}>
      <div className="relative" style={{ width, height: width }}>
        <svg className="transform -rotate-90" width={width} height={width}>
          {/* Background circle */}
          <circle
            cx={width / 2}
            cy={width / 2}
            r={45}
            stroke={colors.bg}
            strokeWidth="10"
            fill="none"
          />
          {/* Progress circle */}
          <circle
            cx={width / 2}
            cy={width / 2}
            r={45}
            stroke={colors.stroke}
            strokeWidth="10"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={cn('font-bold', fontSize)} style={{ color: colors.stroke }}>
            {percentage}%
          </span>
          <span className="text-xs text-gray-400 mt-1">Risk</span>
        </div>
      </div>
      <p className={cn('mt-4 text-gray-300 font-medium text-center', labelSize)}>{label}</p>
    </div>
  );
}
