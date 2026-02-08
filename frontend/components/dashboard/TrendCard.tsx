'use client';

import { motion } from 'framer-motion';
import { fadeInUp } from '@/lib/motion-config';
import { TrendingUp, TrendingDown, Activity } from 'lucide-react';
import type { TrendOverview } from '@/lib/api';

interface TrendCardProps {
  trend: TrendOverview;
  onClick?: () => void;
}

const statusConfig = {
  emerging: {
    color: '#84CC16',
    bg: 'bg-[#84CC16]/10',
    border: 'border-[#84CC16]/30',
    label: 'Emerging',
    icon: TrendingUp,
  },
  peak: {
    color: '#3B82F6',
    bg: 'bg-[#3B82F6]/10',
    border: 'border-[#3B82F6]/30',
    label: 'Peak',
    icon: Activity,
  },
  declining: {
    color: '#F97316',
    bg: 'bg-[#F97316]/10',
    border: 'border-[#F97316]/30',
    label: 'Declining',
    icon: TrendingDown,
  },
  stable: {
    color: '#06B6D4',
    bg: 'bg-[#06B6D4]/10',
    border: 'border-[#06B6D4]/30',
    label: 'Stable',
    icon: Activity,
  },
};

export function TrendCard({ trend, onClick }: TrendCardProps) {
  const config = statusConfig[trend.status as keyof typeof statusConfig] || statusConfig.stable;
  const StatusIcon = config.icon;

  return (
    <motion.div
      variants={fadeInUp}
      whileHover={{ y: -4 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="group relative cursor-pointer"
    >
      {/* Glow effect on hover */}
      <div 
        className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg blur-xl"
        style={{ backgroundColor: `${config.color}20` }}
      />
      
      <div className="relative p-5 border border-[#374151] rounded-lg bg-[#151922] group-hover:border-[#3B82F6] transition-all duration-200">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="text-lg font-bold text-[#F9FAFB] mb-1 line-clamp-1">
              {trend.name}
            </h3>
            <p className="text-sm text-[#9CA3AF] line-clamp-2">
              {trend.description || 'No description available'}
            </p>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div>
            <p className="text-xs text-[#9CA3AF] uppercase tracking-wider mb-1">
              Engagement
            </p>
            <p className="text-xl font-bold font-mono text-[#F9FAFB]">
              {trend.metrics.engagement_rate?.toFixed(1) ?? '0.0'}%
            </p>
          </div>
          <div>
            <p className="text-xs text-[#9CA3AF] uppercase tracking-wider mb-1">
              Health
            </p>
            <p className="text-xl font-bold font-mono text-[#F9FAFB]">
              {trend.metrics.health_score?.toFixed(0) ?? '0'}
            </p>
          </div>
        </div>

        {/* Status Badge */}
        <div className="flex items-center justify-between">
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full ${config.bg} ${config.border} border`}>
            <StatusIcon className="w-3.5 h-3.5" style={{ color: config.color }} />
            <span className="text-xs font-medium" style={{ color: config.color }}>
              {config.label}
            </span>
          </div>
          
          {/* Velocity indicator */}
          {(trend.metrics as any).velocity !== undefined && (
            <div className="flex items-center gap-1">
              <div className="w-1.5 h-1.5 rounded-full bg-[#84CC16] animate-pulse" />
              <span className="text-xs text-[#9CA3AF] font-mono">
                {(trend.metrics as any).velocity.toFixed(1)}
              </span>
            </div>
          )}
        </div>

        {/* Hover indicator */}
        <div className="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity">
          <div className="text-[#3B82F6] text-xs font-medium">
            View details →
          </div>
        </div>
      </div>
    </motion.div>
  );
}
