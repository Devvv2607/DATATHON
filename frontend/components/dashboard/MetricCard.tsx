'use client';

import { motion, useSpring, useTransform } from 'framer-motion';
import { useEffect, ReactNode } from 'react';
import { fadeInUp } from '@/lib/motion-config';
import { ArrowUp, ArrowDown, Minus } from 'lucide-react';

interface MetricCardProps {
  label: string;
  value: number | string;
  unit?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: number;
  color?: 'amber' | 'coral' | 'acid' | 'cyan' | 'electric' | 'violet';
  icon?: ReactNode;
  animated?: boolean;
}

const colorClasses = {
  amber: 'text-[#F59E0B]',
  coral: 'text-[#F97316]',
  acid: 'text-[#84CC16]',
  cyan: 'text-[#06B6D4]',
  electric: 'text-[#3B82F6]',
  violet: 'text-[#8B5CF6]',
};

const trendColors = {
  up: 'text-[#84CC16]',
  down: 'text-[#F97316]',
  neutral: 'text-[#9CA3AF]',
};

const trendIcons = {
  up: ArrowUp,
  down: ArrowDown,
  neutral: Minus,
};

export function MetricCard({
  label,
  value,
  unit,
  trend,
  trendValue,
  color = 'electric',
  icon,
  animated = true,
}: MetricCardProps) {
  const spring = useSpring(0, { stiffness: 50, damping: 20 });
  const display = useTransform(spring, (current) => {
    if (typeof value === 'number') {
      return Math.floor(current).toLocaleString();
    }
    return value;
  });

  useEffect(() => {
    if (animated && typeof value === 'number') {
      spring.set(value);
    }
  }, [value, spring, animated]);

  const TrendIcon = trend ? trendIcons[trend] : null;

  return (
    <motion.div
      variants={fadeInUp}
      initial="initial"
      animate="animate"
      className="group relative"
    >
      {/* Hover glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg pointer-events-none" />
      
      <div className="relative p-6 border border-[#374151] rounded-lg bg-[#151922] hover:border-[#3B82F6] transition-all duration-200">
        {/* Header with icon */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <p className="text-xs font-medium text-[#9CA3AF] uppercase tracking-wider">
              {label}
            </p>
          </div>
          {icon && (
            <div className={`${colorClasses[color]} opacity-60`}>
              {icon}
            </div>
          )}
        </div>
        
        {/* Value */}
        <div className="flex items-baseline gap-2 mb-2">
          {animated && typeof value === 'number' ? (
            <motion.span 
              className={`text-4xl font-bold font-display ${colorClasses[color]}`}
            >
              {display}
            </motion.span>
          ) : (
            <span className={`text-4xl font-bold font-display ${colorClasses[color]}`}>
              {value}
            </span>
          )}
          {unit && (
            <span className="text-lg text-[#D1D5DB] font-mono opacity-70">
              {unit}
            </span>
          )}
        </div>
        
        {/* Trend Indicator */}
        {trend && trendValue !== undefined && TrendIcon && (
          <div className={`flex items-center gap-1.5 text-sm ${trendColors[trend]}`}>
            <TrendIcon className="w-4 h-4" />
            <span className="font-mono font-medium">
              {trendValue > 0 ? '+' : ''}{trendValue}%
            </span>
            <span className="text-xs text-[#9CA3AF] ml-1">
              vs last period
            </span>
          </div>
        )}
      </div>
    </motion.div>
  );
}
