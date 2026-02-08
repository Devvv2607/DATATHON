'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { fetchTrends, predictDecline, type TrendOverview, type DeclinePrediction } from '@/lib/api';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { ProbabilityGauge } from '@/components/dashboard/ProbabilityGauge';
import { TrendCard } from '@/components/dashboard/TrendCard';
import { TrendChart } from '@/components/dashboard/Charts';
import { staggerContainer, fadeInUp, pageTransition } from '@/lib/motion-config';
import { TrendingUp, Users, BarChart3, AlertTriangle, Activity, Zap } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const [trends, setTrends] = useState<TrendOverview[]>([]);
  const [selectedTrend, setSelectedTrend] = useState<TrendOverview | null>(null);
  const [prediction, setPrediction] = useState<DeclinePrediction | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function loadData() {
      // Try to load cached data first
      const cachedTrends = localStorage.getItem('dashboard_trends');
      const cachedPrediction = localStorage.getItem('dashboard_prediction');
      const cachedTimestamp = localStorage.getItem('dashboard_timestamp');
      
      // Show cached data immediately if available
      if (cachedTrends) {
        const parsedTrends = JSON.parse(cachedTrends);
        setTrends(parsedTrends);
        if (parsedTrends.length > 0) {
          setSelectedTrend(parsedTrends[0]);
          if (cachedPrediction) {
            setPrediction(JSON.parse(cachedPrediction));
          }
        }
        setLoading(false);
      }

      // Fetch fresh data in background
      try {
        const { trends: data } = await fetchTrends();
        setTrends(data);
        
        // Cache the fresh data
        localStorage.setItem('dashboard_trends', JSON.stringify(data));
        localStorage.setItem('dashboard_timestamp', Date.now().toString());
        
        if (data.length > 0) {
          setSelectedTrend(data[0]);
          const pred = await predictDecline(data[0].id);
          setPrediction(pred);
          
          // Cache prediction
          localStorage.setItem('dashboard_prediction', JSON.stringify(pred));
        }
      } catch (error) {
        console.error('Error loading trends:', error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const avgHealthScore = trends.length > 0
    ? Math.round(trends.reduce((sum, t) => sum + t.metrics.health_score, 0) / trends.length)
    : 0;

  const decliningTrends = trends.filter(t => t.status === 'declining').length;
  const totalReach = 12400000; // 12.4M

  // Mock velocity data
  const velocityData = Array.from({ length: 7 }, (_, i) => ({
    date: new Date(Date.now() - (6 - i) * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    value: 65 + Math.sin(i / 2) * 15 + Math.random() * 10
  }));

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 border-4 border-[#3B82F6] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-[#9CA3AF] font-medium">Loading intelligence...</p>
        </motion.div>
      </div>
    );
  }

  return (
    <motion.div
      variants={pageTransition}
      initial="initial"
      animate="animate"
      exit="exit"
      className="space-y-12 pb-12"
    >
      {/* Header Section */}
      <motion.div variants={fadeInUp} className="space-y-3">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-2 h-2 rounded-full bg-[#84CC16] animate-pulse" />
          <span className="text-sm font-medium text-[#84CC16] uppercase tracking-wider">
            Live Intelligence
          </span>
        </div>
        <h1 className="text-5xl md:text-6xl font-display font-bold text-[#F9FAFB] tracking-tight">
          Trend Intelligence
        </h1>
        <p className="text-xl text-[#9CA3AF] max-w-2xl">
          Real-time analysis and decline prediction powered by machine learning
        </p>
      </motion.div>

      {/* Key Metrics - Redesigned */}
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        <MetricCard
          label="Avg Health Score"
          value={avgHealthScore}
          trend="up"
          trendValue={2.3}
          color="electric"
          icon={<BarChart3 className="w-5 h-5" />}
          animated
        />
        <MetricCard
          label="Active Trends"
          value={trends.length}
          color="cyan"
          icon={<TrendingUp className="w-5 h-5" />}
          animated
        />
        <MetricCard
          label="At-Risk Trends"
          value={decliningTrends}
          trend="down"
          color="coral"
          icon={<AlertTriangle className="w-5 h-5" />}
          animated
        />
        <MetricCard
          label="Total Reach"
          value={totalReach}
          unit="users"
          trend="up"
          trendValue={8.5}
          color="acid"
          icon={<Users className="w-5 h-5" />}
          animated
        />
      </motion.div>

      {/* Main Content - Asymmetric Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column - 8 cols */}
        <motion.div
          variants={fadeInUp}
          className="lg:col-span-8 space-y-8"
        >
          {/* Trending Topics Section */}
          <div className="panel p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-3xl font-display font-bold text-[#F9FAFB] mb-2">
                  What's Happening
                </h2>
                <p className="text-sm text-[#9CA3AF]">
                  {trends.length} trends analyzed in real-time
                </p>
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => router.push('/dashboard/trendLifecycle')}
                className="px-4 py-2 rounded-lg bg-[#3B82F6] text-white text-sm font-medium hover:bg-[#2563EB] transition-colors"
              >
                View All
              </motion.button>
            </div>
            
            <motion.div
              variants={staggerContainer}
              initial="initial"
              animate="animate"
              className="grid grid-cols-1 md:grid-cols-2 gap-4"
            >
              {trends.slice(0, 4).map((trend) => (
                <TrendCard
                  key={trend.id}
                  trend={trend}
                  onClick={() => router.push('/dashboard/trendLifecycle')}
                />
              ))}
            </motion.div>
          </div>

          {/* Engagement Velocity Chart */}
          <div className="panel p-8">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-2xl font-display font-bold text-[#F9FAFB] mb-2">
                  Engagement Velocity
                </h2>
                <p className="text-sm text-[#9CA3AF]">
                  7-day trend momentum analysis
                </p>
              </div>
              <div className="flex gap-2">
                <button className="px-3 py-1.5 rounded-lg bg-[#3B82F6]/20 text-[#3B82F6] text-sm font-medium border border-[#3B82F6]/30">
                  7D
                </button>
                <button className="px-3 py-1.5 rounded-lg bg-transparent text-[#9CA3AF] text-sm font-medium border border-[#374151] hover:border-[#3B82F6]/30 transition-colors">
                  30D
                </button>
              </div>
            </div>
            <TrendChart
              data={velocityData}
              color="rgb(59, 130, 246)"
              height={280}
              type="area"
            />
          </div>
        </motion.div>

        {/* Right Column - 4 cols */}
        <motion.div
          variants={fadeInUp}
          className="lg:col-span-4 space-y-6"
        >
          {selectedTrend && prediction && (
            <>
              {/* Decline Risk Analysis */}
              <div className="panel-elevated p-6 border-[#F97316]/30">
                <div className="flex items-center gap-2 mb-6">
                  <Zap className="w-5 h-5 text-[#F97316]" />
                  <h2 className="text-xl font-display font-bold text-[#F9FAFB]">
                    Risk Analysis
                  </h2>
                </div>
                
                <ProbabilityGauge
                  value={prediction.decline_probability}
                  label={selectedTrend.name}
                  size="lg"
                />
                
                <div className="mt-6 p-4 rounded-lg bg-[#0A0E14] border border-[#374151]">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-sm text-[#9CA3AF]">Confidence</span>
                    <span className="text-sm font-bold text-[#F9FAFB] capitalize">
                      {prediction.confidence_level}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-[#9CA3AF]">Days Until Decline</span>
                    <span className="text-sm font-bold text-[#F97316]">
                      ~{prediction.days_until_decline}d
                    </span>
                  </div>
                </div>
              </div>

              {/* Key Risk Indicators */}
              <div className="panel p-6">
                <div className="flex items-center gap-2 mb-6">
                  <Activity className="w-5 h-5 text-[#3B82F6]" />
                  <h3 className="text-lg font-display font-bold text-[#F9FAFB]">
                    Risk Indicators
                  </h3>
                </div>
                
                <div className="space-y-5">
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-[#D1D5DB] font-medium">Audience Saturation</span>
                      <span className="text-sm font-bold text-[#F97316]">High</span>
                    </div>
                    <div className="h-2 bg-[#0A0E14] rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: '78%' }}
                        transition={{ duration: 1, delay: 0.2 }}
                        className="h-full bg-gradient-to-r from-[#F97316] to-[#F59E0B]"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-[#D1D5DB] font-medium">Content Novelty</span>
                      <span className="text-sm font-bold text-[#F59E0B]">Medium</span>
                    </div>
                    <div className="h-2 bg-[#0A0E14] rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: '45%' }}
                        transition={{ duration: 1, delay: 0.4 }}
                        className="h-full bg-gradient-to-r from-[#F59E0B] to-[#F97316]"
                      />
                    </div>
                  </div>
                  
                  <div>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-[#D1D5DB] font-medium">Influencer Dependency</span>
                      <span className="text-sm font-bold text-[#84CC16]">Low</span>
                    </div>
                    <div className="h-2 bg-[#0A0E14] rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: '32%' }}
                        transition={{ duration: 1, delay: 0.6 }}
                        className="h-full bg-gradient-to-r from-[#84CC16] to-[#06B6D4]"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </motion.div>
      </div>
    </motion.div>
  );
}
