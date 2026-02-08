/**
 * CinematicMetric Component
 * Premium metric display with animated counter and micro-sparkline
 * Replaces the generic MetricCard
 */

'use client';

import { motion, useSpring, useTransform } from 'framer-motion';
import { useEffect, ReactNode } from 'react';
import { fadeInUp } from '@/lib/motion-config';
import { ArrowUp, ArrowDown, Minus, TrendingUp } from 'lucide-react';

interface CinematicMetricProps {
  label: string;
  value: number | string;
  unit?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: number;
  trendLabel?: string;
  color?: 'growth' | 'alert' | 'insight' | 'pulse' | 'forecast' | 'warning';
  icon?: ReactNode;
  isLive?: boolean;
  recentData?: number[]; // For mini sparkline
  animated?: boolean;
}

const colorMap = {
  growth: {
    text: 'text-[#10B981]',
    bg: 'bg-[#10B981]/10',
    glow: 'rgba(16, 185, 129, 0.1)',
    border: 'rgba(16, 185, 129, 0.3)',
  },
  alert: {
    text: 'text-[#EF4444]',
    bg: 'bg-[#EF4444]/10',
    glow: 'rgba(239, 68, 68, 0.1)',
    border: 'rgba(239, 68, 68, 0.3)',
  },
  insight: {
    text: 'text-[#3B82F6]',
    bg: 'bg-[#3B82F6]/10',
    glow: 'rgba(59, 130, 246, 0.1)',
    border: 'rgba(59, 130, 246, 0.3)',
  },
  pulse: {
    text: 'text-[#06B6D4]',
    bg: 'bg-[#06B6D4]/10',
    glow: 'rgba(6, 182, 212, 0.1)',
    border: 'rgba(6, 182, 212, 0.3)',
  },
  forecast: {
    text: 'text-[#8B5CF6]',
    bg: 'bg-[#8B5CF6]/10',
    glow: 'rgba(139, 92, 246, 0.1)',
    border: 'rgba(139, 92, 246, 0.3)',
  },
  warning: {
    text: 'text-[#F59E0B]',
    bg: 'bg-[#F59E0B]/10',
    glow: 'rgba(245, 158, 11, 0.1)',
    border: 'rgba(245, 158, 11, 0.3)',
  },
};

const trendConfig = {
  up: {
    color: 'text-[#10B981]',
    bg: 'bg-[#10B981]/10',
    icon: ArrowUp,
  },
  down: {
    color: 'text-[#EF4444]',
    bg: 'bg-[#EF4444]/10',
    icon: ArrowDown,
  },
  neutral: {
    color: 'text-[#94A3B8]',
    bg: 'bg-[#94A3B8]/10',
    icon: Minus,
  },
};

function AnimatedNumber({ value }: { value: number }) {
  const spring = useSpring(0, {
    stiffness: 60,
    damping: 25,
  });

  const display = useTransform(spring, (current) => Math.floor(current).toLocaleString());

  useEffect(() => {
    const timer = setTimeout(() => {
      spring.set(value);
    }, 300);

    return () => clearTimeout(timer);
  }, [value, spring]);

  return <motion.span>{display}</motion.span>;
}

function MiniSparkline({ data, color }: { data: number[]; color: string }) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min;

  const points = data
    .map((value, index) => {
      const x = (index / (data.length - 1)) * 100;
      const y = 100 - ((value - min) / range) * 100;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg viewBox="0 0 100 100" className="w-full h-full" preserveAspectRatio="none">
      <motion.polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 0.6 }}
        transition={{ duration: 1.5, ease: [0.43, 0.13, 0.23, 0.96] }}
      />
    </svg>
  );
}

export function CinematicMetric({
  label,
  value,
  unit,
  trend,
  trendValue,
  trendLabel = 'vs last week',
  color = 'insight',
  icon,
  isLive = false,
  recentData,
  animated = true,
}: CinematicMetricProps) {
  const colors = colorMap[color];
  const TrendIcon = trend ? trendConfig[trend].icon : null;
  const trendColors = trend ? trendConfig[trend] : null;

  return (
    <motion.div
      variants={fadeInUp}
      initial="initial"
      animate="animate"
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className="group relative overflow-hidden"
    >
      {/* Animated glow on hover */}
      <motion.div
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-xl -z-10"
        style={{
          background: `radial-gradient(circle at top right, ${colors.glow}, transparent)`,
        }}
      />

      {/* Card container */}
      <div
        className="relative p-6 rounded-xl border transition-all duration-300"
        style={{
          background: 'linear-gradient(180deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0) 100%), #161B26',
          borderColor: colors.border,
        }}
      >
        {/* Header: Label + Live indicator */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            {isLive && (
              <motion.div
                animate={{
                  scale: [1, 1.3, 1],
                  opacity: [1, 0.4, 1],
                }}
                transition={{
                  repeat: Infinity,
                  duration: 2,
                  ease: 'easeInOut',
                }}
                className="w-2 h-2 rounded-full"
                style={{ backgroundColor: colors.text.replace('text-', '') }}
              />
            )}
            <span className="text-xs uppercase tracking-wider text-[#94A3B8] font-medium">
              {label}
            </span>
          </div>
          {icon && <div className={`${colors.text} opacity-40`}>{icon}</div>}
        </div>

        {/* Main value - Cinematic counter */}
        <div className="flex items-baseline gap-2 mb-4">
          <motion.div
            className={`text-4xl font-display font-bold ${colors.text} tabular-nums`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.6 }}
          >
            {typeof value === 'number' && animated ? <AnimatedNumber value={value} /> : value}
          </motion.div>
          {unit && <span className="text-lg text-[#CBD5E1]">{unit}</span>}
        </div>

        {/* Mini sparkline (if data provided) */}
        {recentData && recentData.length > 0 && (
          <div className="h-12 mb-4 opacity-50 group-hover:opacity-100 transition-opacity duration-300">
            <MiniSparkline data={recentData} color={colors.text.replace('text-', '')} />
          </div>
        )}

        {/* Trend indicator */}
        {trend && trendColors && (
          <div
            className={`flex items-center gap-2 pt-3 border-t`}
            style={{ borderColor: 'rgba(255,255,255,0.05)' }}
          >
            <div className={`${trendColors.bg} ${trendColors.color} p-1 rounded`}>
              {TrendIcon && <TrendIcon size={12} strokeWidth={2.5} />}
            </div>
            <span className={`text-sm font-semibold ${trendColors.color}`}>
              {trendValue !== undefined && `${trendValue > 0 ? '+' : ''}${trendValue}%`}
            </span>
            <span className="text-xs text-[#94A3B8]">{trendLabel}</span>
          </div>
        )}
      </div>
    </motion.div>
  );
}

/**
 * Compact version for smaller spaces
 */
export function CinematicMetricCompact({
  label,
  value,
  color = 'insight',
  icon,
}: Pick<CinematicMetricProps, 'label' | 'value' | 'color' | 'icon'>) {
  const colors = colorMap[color];

  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="flex items-center gap-3 p-4 rounded-lg border"
      style={{
        background: '#161B26',
        borderColor: colors.border,
      }}
    >
      {icon && (
        <div
          className={`p-2 rounded-lg ${colors.bg}`}
          style={{ color: colors.text.replace('text-', '') }}
        >
          {icon}
        </div>
      )}
      <div>
        <p className="text-xs uppercase tracking-wider text-[#94A3B8] mb-1">{label}</p>
        <p className={`text-2xl font-display font-bold ${colors.text} tabular-nums`}>
          {typeof value === 'number' ? value.toLocaleString() : value}
        </p>
      </div>
    </motion.div>
  );
}
