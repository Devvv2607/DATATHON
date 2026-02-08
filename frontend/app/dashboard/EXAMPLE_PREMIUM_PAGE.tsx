/**
 * Premium Dashboard Overview Page - EXAMPLE IMPLEMENTATION
 * Copy and adapt this pattern for your actual dashboard/page.tsx
 * 
 * Key Features:
 * - Dramatic hero section with live stats
 * - Cinematic metrics with animated counters
 * - Staggered card animations
 * - Asymmetric editorial layout
 * - Purposeful motion language
 */

'use client';

import { useEffect, useState } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';
import { 
  TrendingUp, 
  Users, 
  Activity, 
  AlertTriangle, 
  Zap,
  Eye,
  ArrowRight 
} from 'lucide-react';
import { fetchTrends, type TrendOverview } from '@/lib/api';
import { CinematicMetric } from '@/components/premium/CinematicMetric';
import { staggerContainer, fadeInUp } from '@/lib/motion-config';

// Animated number component
function AnimatedNumber({ value, suffix = '' }: { value: number; suffix?: string }) {
  const spring = useSpring(0, { stiffness: 60, damping: 25 });
  const display = useTransform(spring, (current) => 
    Math.floor(current).toLocaleString() + suffix
  );

  useEffect(() => {
    setTimeout(() => spring.set(value), 300);
  }, [value, spring]);

  return <motion.span>{display}</motion.span>;
}

export default function PremiumDashboard() {
  const [trends, setTrends] = useState<TrendOverview[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      const { trends: data } = await fetchTrends();
      setTrends(data);
      setLoading(false);
    }
    loadData();
  }, []);

  // Calculate aggregated metrics
  const activeTrends = trends.length;
  const avgHealthScore = trends.length > 0
    ? Math.round(trends.reduce((sum, t) => sum + t.metrics.health_score, 0) / trends.length)
    : 0;
  const decliningTrends = trends.filter(t => t.status === 'declining').length;
  const totalReach = 12400000; // 12.4M
  const avgEngagement = 6.8;
  const criticalSignals = 3;

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 border-4 border-[#3B82F6] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-[#94A3B8] font-medium">Loading intelligence...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, filter: 'blur(10px)' }}
      animate={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
      transition={{ duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] }}
      className="space-y-12 pb-12"
    >
      {/* ============================================ */}
      {/* SECTION 1: HERO - What's Happening Right Now */}
      {/* ============================================ */}
      
      <motion.section
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="relative h-[450px] rounded-2xl overflow-hidden border border-[#2D3447]"
        style={{
          background: 'linear-gradient(135deg, #0B0F19 0%, #1E2433 100%)',
        }}
      >
        {/* Live indicator badge */}
        <div className="absolute top-6 right-6 z-20">
          <div className="flex items-center gap-2 px-4 py-2 rounded-full backdrop-blur-xl bg-[#10B981]/10 border border-[#10B981]/30">
            <motion.div
              animate={{
                scale: [1, 1.3, 1],
                opacity: [1, 0.4, 1]
              }}
              transition={{ repeat: Infinity, duration: 2, ease: 'easeInOut' }}
              className="w-2 h-2 rounded-full bg-[#10B981]"
            />
            <span className="text-xs font-semibold text-[#10B981] uppercase tracking-wider">
              Live
            </span>
          </div>
        </div>

        {/* Main content */}
        <div className="relative z-10 p-12 h-full flex flex-col justify-between">
          {/* Top: Title */}
          <div>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="flex items-center gap-3 mb-4"
            >
              <Zap size={24} className="text-[#3B82F6]" strokeWidth={2} />
              <span className="text-sm font-medium text-[#94A3B8] uppercase tracking-wider">
                Intelligence Hub
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5, duration: 0.6 }}
              className="text-6xl md:text-7xl font-display font-bold text-[#F8FAFC] tracking-tight leading-tight"
            >
              Trend Intelligence
              <br />
              <span className="text-[#3B82F6]">Command Center</span>
            </motion.h1>
          </div>

          {/* Bottom: Large stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.6 }}
            className="grid grid-cols-3 gap-8"
          >
            <div>
              <div className="text-6xl font-display font-bold text-[#3B82F6] tabular-nums mb-2">
                <AnimatedNumber value={activeTrends} />
              </div>
              <p className="text-sm text-[#94A3B8] uppercase tracking-wider">
                Active Trends
              </p>
            </div>

            <div>
              <div className="text-6xl font-display font-bold text-[#10B981] tabular-nums mb-2">
                <AnimatedNumber value={avgHealthScore} suffix="%" />
              </div>
              <p className="text-sm text-[#94A3B8] uppercase tracking-wider">
                Avg Health Score
              </p>
            </div>

            <div>
              <div className="text-6xl font-display font-bold text-[#06B6D4] tabular-nums mb-2">
                <AnimatedNumber value={Math.floor(totalReach / 1000000)} suffix="M" />
              </div>
              <p className="text-sm text-[#94A3B8] uppercase tracking-wider">
                Total Reach
              </p>
            </div>
          </motion.div>
        </div>

        {/* Decorative gradient orbs (depth) */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-[#3B82F6]/15 rounded-full blur-3xl opacity-50" />
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-[#10B981]/15 rounded-full blur-3xl opacity-50" />
      </motion.section>

      {/* ============================================ */}
      {/* SECTION 2: KEY METRICS - Cinematic Display */}
      {/* ============================================ */}

      <section>
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.8 }}
          className="mb-6"
        >
          <h2 className="text-3xl font-display font-bold text-[#F8FAFC] mb-2">
            Key Metrics
          </h2>
          <p className="text-[#94A3B8]">
            Real-time performance indicators across all platforms
          </p>
        </motion.div>

        <motion.div
          variants={staggerContainer}
          initial="initial"
          animate="animate"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          <CinematicMetric
            label="Avg Health Score"
            value={avgHealthScore}
            unit="%"
            trend="up"
            trendValue={2.3}
            color="insight"
            icon={<Activity size={20} />}
            isLive={true}
            animated={true}
            recentData={[65, 68, 70, 69, 72, 75, avgHealthScore]}
          />

          <CinematicMetric
            label="Total Reach"
            value={Math.floor(totalReach / 1000)}
            unit="K"
            trend="up"
            trendValue={5.7}
            color="pulse"
            icon={<Users size={20} />}
            isLive={true}
            animated={true}
          />

          <CinematicMetric
            label="Avg Engagement"
            value={avgEngagement}
            unit="%"
            trend="up"
            trendValue={1.2}
            color="growth"
            icon={<TrendingUp size={20} />}
            animated={true}
          />

          <CinematicMetric
            label="Declining Trends"
            value={decliningTrends}
            trend="down"
            trendValue={-8}
            color="alert"
            icon={<AlertTriangle size={20} />}
            animated={true}
          />

          <CinematicMetric
            label="Active Monitoring"
            value={activeTrends}
            trend="neutral"
            color="forecast"
            icon={<Eye size={20} />}
            animated={true}
          />

          <CinematicMetric
            label="Critical Signals"
            value={criticalSignals}
            trend="up"
            trendValue={50}
            trendLabel="requires attention"
            color="warning"
            icon={<Zap size={20} />}
            isLive={true}
            animated={true}
          />
        </motion.div>
      </section>

      {/* ============================================ */}
      {/* SECTION 3: FEATURED INSIGHT - Asymmetric Layout */}
      {/* ============================================ */}

      <section>
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 1 }}
          className="mb-6"
        >
          <h2 className="text-3xl font-display font-bold text-[#F8FAFC] mb-2">
            Critical Insights
          </h2>
          <p className="text-[#94A3B8]">
            AI-detected patterns requiring immediate attention
          </p>
        </motion.div>

        <div className="grid grid-cols-12 gap-6">
          {/* Large featured insight (8 columns) */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1, duration: 0.6 }}
            className="col-span-12 lg:col-span-8"
          >
            <motion.div
              whileHover={{ y: -4 }}
              transition={{ duration: 0.3 }}
              className="relative group h-full"
            >
              {/* Hover glow */}
              <motion.div
                className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-xl -z-10"
                style={{
                  background: 'radial-gradient(circle at top right, rgba(239, 68, 68, 0.1), transparent)',
                }}
              />

              <div className="p-8 h-full rounded-xl border border-[#2D3447] bg-gradient-to-br from-[#161B26] to-[#0B0F19]">
                {/* Priority badge */}
                <div className="flex items-center gap-2 mb-4">
                  <div className="px-3 py-1 rounded-full bg-[#EF4444]/10 border border-[#EF4444]/30">
                    <span className="text-xs font-semibold text-[#EF4444] uppercase tracking-wider">
                      High Priority
                    </span>
                  </div>
                  <span className="text-xs text-[#94A3B8]">2 hours ago</span>
                </div>

                <h3 className="text-2xl font-display font-bold text-[#F8FAFC] mb-3">
                  3 Trends Show Early Decline Signals
                </h3>

                <p className="text-[#CBD5E1] mb-6 leading-relaxed">
                  Machine learning model detected anomalous engagement drops in emerging trends. 
                  Immediate analysis recommended to prevent cascading effects.
                </p>

                {/* Mini metrics */}
                <div className="grid grid-cols-3 gap-4 mb-6">
                  <div>
                    <p className="text-3xl font-display font-bold text-[#EF4444] mb-1">72%</p>
                    <p className="text-xs text-[#94A3B8] uppercase tracking-wider">Decline Risk</p>
                  </div>
                  <div>
                    <p className="text-3xl font-display font-bold text-[#F59E0B] mb-1">-23%</p>
                    <p className="text-xs text-[#94A3B8] uppercase tracking-wider">Velocity Drop</p>
                  </div>
                  <div>
                    <p className="text-3xl font-display font-bold text-[#3B82F6] mb-1">8.2M</p>
                    <p className="text-xs text-[#94A3B8] uppercase tracking-wider">At Risk Reach</p>
                  </div>
                </div>

                {/* CTA */}
                <motion.button
                  whileHover={{ x: 4 }}
                  className="flex items-center gap-2 text-[#3B82F6] font-semibold group/btn"
                >
                  <span>Investigate Trends</span>
                  <ArrowRight size={16} className="group-hover/btn:translate-x-1 transition-transform" />
                </motion.button>
              </div>
            </motion.div>
          </motion.div>

          {/* Smaller insights (4 columns) */}
          <div className="col-span-12 lg:col-span-4 space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.2, duration: 0.6 }}
              whileHover={{ y: -4 }}
              className="p-6 rounded-xl border border-[#2D3447] bg-[#161B26]"
            >
              <div className="flex items-center gap-2 mb-3">
                <div className="p-2 rounded-lg bg-[#10B981]/10">
                  <TrendingUp size={20} className="text-[#10B981]" />
                </div>
                <span className="text-xs text-[#94A3B8] uppercase tracking-wider">Opportunity</span>
              </div>
              <h4 className="text-lg font-bold text-[#F8FAFC] mb-2">
                Emerging Niche Detected
              </h4>
              <p className="text-sm text-[#CBD5E1] mb-3">
                New micro-trend gaining 300% velocity in target demo
              </p>
              <div className="text-2xl font-display font-bold text-[#10B981]">
                +300%
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.3, duration: 0.6 }}
              whileHover={{ y: -4 }}
              className="p-6 rounded-xl border border-[#2D3447] bg-[#161B26]"
            >
              <div className="flex items-center gap-2 mb-3">
                <div className="p-2 rounded-lg bg-[#8B5CF6]/10">
                  <Activity size={20} className="text-[#8B5CF6]" />
                </div>
                <span className="text-xs text-[#94A3B8] uppercase tracking-wider">Forecast</span>
              </div>
              <h4 className="text-lg font-bold text-[#F8FAFC] mb-2">
                Platform Shift Predicted
              </h4>
              <p className="text-sm text-[#CBD5E1] mb-3">
                TikTok engagement expected to peak within 48 hours
              </p>
              <div className="text-2xl font-display font-bold text-[#8B5CF6]">
                48 hrs
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* ============================================ */}
      {/* SECTION 4: QUICK ACTIONS - CTA Strip */}
      {/* ============================================ */}

      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.4 }}
        className="grid grid-cols-1 md:grid-cols-3 gap-4"
      >
        {[
          { label: 'Analyze Decline', icon: AlertTriangle, color: '#EF4444' },
          { label: 'Run Simulation', icon: Zap, color: '#3B82F6' },
          { label: 'View Network', icon: Users, color: '#06B6D4' },
        ].map((action, i) => (
          <motion.button
            key={action.label}
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            className="p-6 rounded-xl border border-[#2D3447] bg-[#161B26] text-left group"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div
                  className="p-3 rounded-lg"
                  style={{ backgroundColor: `${action.color}20` }}
                >
                  <action.icon size={24} style={{ color: action.color }} strokeWidth={2} />
                </div>
                <span className="font-semibold text-[#F8FAFC]">{action.label}</span>
              </div>
              <ArrowRight
                size={20}
                className="text-[#94A3B8] group-hover:translate-x-1 transition-transform"
              />
            </div>
          </motion.button>
        ))}
      </motion.section>
    </motion.div>
  );
}
