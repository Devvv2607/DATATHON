'use client';

import { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, TrendingDown, BarChart as BarChartIcon } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';
import DomainAndTrendSelector from '@/components/DomainAndTrendSelector';
import { useDomain } from '@/contexts/DomainContext';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function ROIAnalysisPage() {
  const [loading, setLoading] = useState(false);
  const [roiData, setRoiData] = useState<any>(null);
  const { selectedDomain, selectedTrend } = useDomain();

  const analyzeROI = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(
        `http://localhost:8000/api/business/roi-analysis?domain=${selectedDomain}&trend_id=${selectedTrend}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        }
      );
      const data = await response.json();
      setRoiData(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    analyzeROI();
  }, [selectedDomain, selectedTrend]);

  // Extract real data from API response or use defaults
  const summary = roiData?.data?.summary || {};
  const contentBreakdown = roiData?.data?.profitable_content || [];
  const unprofitableContent = roiData?.data?.unprofitable_content || [];

  // Sample data for charts
  const profitabilityData = [
    { name: 'AI Tutorial', revenue: 2500, cost: 500, profit: 2000 },
    { name: 'Tech Review', revenue: 1200, cost: 300, profit: 900 },
    { name: 'News Update', revenue: 400, cost: 600, profit: -200 },
    { name: 'Deep Dive', revenue: 1800, cost: 400, profit: 1400 },
    { name: 'Quick Tips', revenue: 800, cost: 250, profit: 550 },
  ];

  const monthlyTrend = [
    { month: 'Jan', profit: 8500, revenue: 12000 },
    { month: 'Feb', profit: 10200, revenue: 14500 },
    { month: 'Mar', profit: 12450, revenue: 17200 },
    { month: 'Apr', profit: 11800, revenue: 16000 },
    { month: 'May', profit: 13900, revenue: 18500 },
    { month: 'Jun', profit: 15200, revenue: 20000 },
  ];

  const contentPieData = [
    { name: 'Profitable', value: 65, count: 13 },
    { name: 'Breakeven', value: 20, count: 4 },
    { name: 'Loss', value: 15, count: 3 },
  ];

  const roiByCategory = [
    { category: 'Tutorials', roi: 450, engagement: 15000 },
    { category: 'Reviews', roi: 320, engagement: 8000 },
    { category: 'News', roi: -50, engagement: 5000 },
    { category: 'Analysis', roi: 380, engagement: 12000 },
    { category: 'Tips', roi: 280, engagement: 6500 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">ROI Dashboard</h1>
          <p className="text-gray-400 mt-2">
            {roiData ? `Analyzing: ${roiData.trend_analyzed} in ${roiData.domain}` : 'Content profitability analysis with AI trends'}
          </p>
        </div>
        <button
          onClick={analyzeROI}
          disabled={loading}
          className="px-6 py-3 rounded-xl glass-card text-blue-400 hover:text-white transition-all duration-300 disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Refresh Analysis'}
        </button>
      </div>

      {/* Domain Selector */}
      <DomainAndTrendSelector />

      {/* Data Source Banner */}
      {roiData && (
        <div className={`glass-card p-4 rounded-xl ${roiData.personalized ? 'bg-green-500/10 border border-green-500/20' : 'bg-yellow-500/10 border border-yellow-500/20'}`}>
          <p className={`font-medium ${roiData.personalized ? 'text-green-400' : 'text-yellow-400'}`}>
            {roiData.personalized ? '✓ Using your business data' : '⚠️ Using sample data'}
          </p>
          <p className="text-sm text-gray-400 mt-1">{roiData.data_source}</p>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 rounded-xl bg-green-500/10">
              <TrendingUp className="w-6 h-6 text-green-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Total Revenue</p>
              <p className="text-2xl font-bold text-white">
                ${summary.total_revenue?.toLocaleString() || '20,000'}
              </p>
            </div>
          </div>
          <div className="text-sm text-green-400">+32% from last month</div>
        </div>

        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 rounded-xl bg-red-500/10">
              <TrendingDown className="w-6 h-6 text-red-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Total Cost</p>
              <p className="text-2xl font-bold text-white">
                ${summary.total_cost?.toLocaleString() || '4,800'}
              </p>
            </div>
          </div>
          <div className="text-sm text-red-400">+8% from last month</div>
        </div>

        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 rounded-xl bg-blue-500/10">
              <DollarSign className="w-6 h-6 text-blue-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">Net Profit</p>
              <p className="text-2xl font-bold text-white">$15,200</p>
            </div>
          </div>
          <div className="text-sm text-blue-400">+42% from last month</div>
        </div>

        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 rounded-xl bg-purple-500/10">
              <BarChartIcon className="w-6 h-6 text-purple-400" />
            </div>
            <div>
              <p className="text-sm text-gray-400">ROI Ratio</p>
              <p className="text-2xl font-bold text-white">4.2x</p>
            </div>
          </div>
          <div className="text-sm text-purple-400">Excellent performance</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue vs Cost vs Profit Bar Chart */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">Content Performance</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={profitabilityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="name" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333', borderRadius: '8px' }}
              />
              <Legend />
              <Bar dataKey="revenue" fill="#3b82f6" name="Revenue" />
              <Bar dataKey="cost" fill="#ef4444" name="Cost" />
              <Bar dataKey="profit" fill="#10b981" name="Profit" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Monthly Trend Line Chart */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">6-Month Profit Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={monthlyTrend}>
              <defs>
                <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis dataKey="month" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333', borderRadius: '8px' }}
              />
              <Legend />
              <Area type="monotone" dataKey="profit" stroke="#3b82f6" fillOpacity={1} fill="url(#colorProfit)" name="Net Profit" />
              <Line type="monotone" dataKey="revenue" stroke="#10b981" name="Revenue" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Content Distribution Pie Chart */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">Content Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={contentPieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {contentPieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333', borderRadius: '8px' }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            {contentPieData.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[idx] }} />
                  <span className="text-gray-300">{item.name}</span>
                </div>
                <span className="text-white font-medium">{item.count} posts</span>
              </div>
            ))}
          </div>
        </div>

        {/* ROI by Category */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">ROI by Category</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={roiByCategory} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis type="number" stroke="#888" />
              <YAxis dataKey="category" type="category" stroke="#888" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #333', borderRadius: '8px' }}
              />
              <Bar dataKey="roi" fill="#8b5cf6" name="ROI %">
                {roiByCategory.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.roi >= 0 ? '#10b981' : '#ef4444'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Trend Analysis Section */}
      <div className="glass-card p-6 rounded-2xl">
        <h2 className="text-xl font-bold text-white mb-4">AI Trend Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="p-4 rounded-xl bg-blue-500/10">
            <p className="text-gray-400 mb-2">Analyzing Trends:</p>
            <ul className="space-y-1 text-blue-400">
              <li>• #AIRevolution2026</li>
              <li>• #SustainableFashion</li>
              <li>• #MetaverseLife</li>
            </ul>
          </div>
          <div className="p-4 rounded-xl bg-green-500/10">
            <p className="text-gray-400 mb-2">Top Platforms:</p>
            <ul className="space-y-1 text-green-400">
              <li>• Twitter: 45% engagement</li>
              <li>• Instagram: 32% engagement</li>
              <li>• TikTok: 23% engagement</li>
            </ul>
          </div>
          <div className="p-4 rounded-xl bg-purple-500/10">
            <p className="text-gray-400 mb-2">Trend Status:</p>
            <ul className="space-y-1 text-purple-400">
              <li>• 4 Growing trends</li>
              <li>• 3 Peak trends</li>
              <li>• 2 Declining trends</li>
            </ul>
          </div>
        </div>
      </div>

      {roiData && (
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-4">Live API Response</h2>
          <pre className="text-gray-300 text-sm overflow-auto p-4 rounded-xl bg-black/30">
            {JSON.stringify(roiData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
