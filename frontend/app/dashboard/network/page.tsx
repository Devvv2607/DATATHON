'use client';

import { Network, MapPin, Users, Share2, TrendingDown } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

export default function NetworkPage() {
  // Mock network data
  const propagationData = [
    { node: 'Influencer A', connections: 45, engagement: 12500 },
    { node: 'Influencer B', connections: 38, engagement: 9800 },
    { node: 'Community Hub 1', connections: 62, engagement: 18200 },
    { node: 'Community Hub 2', connections: 51, engagement: 15600 },
    { node: 'Organic Users', connections: 124, engagement: 28900 }
  ];

  const geoData = [
    { region: 'North America', engagement: 35.2, decline: -8.5 },
    { region: 'Europe', engagement: 28.1, decline: -12.3 },
    { region: 'Asia Pacific', engagement: 22.4, decline: -5.2 },
    { region: 'Latin America', engagement: 10.8, decline: -15.7 },
    { region: 'Other', engagement: 3.5, decline: -18.2 }
  ];

  const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-4xl font-bold text-white mb-2">Network & Geographic Analysis</h1>
        <p className="text-gray-400">Understand trend propagation patterns and geographic engagement</p>
      </div>

      {/* Network Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-cyan-950/20 p-6 backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <Network className="w-5 h-5 text-blue-400" />
            <span className="text-sm text-gray-400">Network Density</span>
          </div>
          <p className="text-3xl font-bold text-white">0.42</p>
          <p className="text-xs text-blue-400 mt-1">Well-connected</p>
        </div>

        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-purple-950/30 to-pink-950/20 p-6 backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <Users className="w-5 h-5 text-purple-400" />
            <span className="text-sm text-gray-400">Key Nodes</span>
          </div>
          <p className="text-3xl font-bold text-white">28</p>
          <p className="text-xs text-purple-400 mt-1">High-influence users</p>
        </div>

        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-green-950/30 to-emerald-950/20 p-6 backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <Share2 className="w-5 h-5 text-green-400" />
            <span className="text-sm text-gray-400">Cascade Depth</span>
          </div>
          <p className="text-3xl font-bold text-white">5.2</p>
          <p className="text-xs text-green-400 mt-1">Avg. shares chain</p>
        </div>

        <div className="rounded-xl border border-white/10 bg-gradient-to-br from-orange-950/30 to-red-950/20 p-6 backdrop-blur-sm">
          <div className="flex items-center gap-2 mb-2">
            <MapPin className="w-5 h-5 text-orange-400" />
            <span className="text-sm text-gray-400">Active Regions</span>
          </div>
          <p className="text-3xl font-bold text-white">42</p>
          <p className="text-xs text-orange-400 mt-1">Countries</p>
        </div>
      </div>

      {/* Trend Propagation Network */}
      <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">Trend Propagation Network</h2>
          <p className="text-sm text-gray-400">Key influencers and community hubs driving trend spread</p>
        </div>

        {/* Network Visualization Placeholder */}
        <div className="relative h-96 rounded-xl bg-gradient-to-br from-blue-950/20 to-purple-950/20 border border-white/5 overflow-hidden mb-6">
          {/* Simulated network nodes */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="relative w-full h-full p-12">
              {/* Center node */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center shadow-lg shadow-blue-500/50 z-10">
                <span className="text-white font-bold text-sm">#Trend</span>
              </div>

              {/* Connected nodes */}
              {[...Array(8)].map((_, i) => {
                const angle = (i * 360) / 8;
                const radius = 150;
                const x = Math.cos((angle * Math.PI) / 180) * radius;
                const y = Math.sin((angle * Math.PI) / 180) * radius;
                
                return (
                  <div key={i}>
                    {/* Connection line */}
                    <svg className="absolute top-1/2 left-1/2 -z-10" width="400" height="400" style={{ marginLeft: '-200px', marginTop: '-200px' }}>
                      <line
                        x1="200"
                        y1="200"
                        x2={200 + x}
                        y2={200 + y}
                        stroke="rgba(96, 165, 250, 0.2)"
                        strokeWidth="2"
                      />
                    </svg>
                    {/* Node */}
                    <div
                      className="absolute w-12 h-12 rounded-full bg-gradient-to-br from-cyan-500/80 to-blue-500/80 flex items-center justify-center shadow-lg"
                      style={{
                        left: `calc(50% + ${x}px)`,
                        top: `calc(50% + ${y}px)`,
                        transform: 'translate(-50%, -50%)'
                      }}
                    >
                      <Users className="w-6 h-6 text-white" />
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Node Details */}
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={propagationData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis 
              dataKey="node" 
              stroke="rgba(255,255,255,0.3)"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="rgba(255,255,255,0.3)"
              style={{ fontSize: '12px' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(17, 24, 39, 0.95)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '8px',
                padding: '12px'
              }}
            />
            <Bar dataKey="connections" fill="rgb(96, 165, 250)" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Geographic Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Geographic Spread */}
        <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
          <div className="flex items-center gap-3 mb-6">
            <MapPin className="w-6 h-6 text-orange-400" />
            <div>
              <h2 className="text-xl font-bold text-white">Geographic Distribution</h2>
              <p className="text-sm text-gray-400">Engagement by region</p>
            </div>
          </div>

          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={geoData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ region, engagement }) => `${region}: ${engagement}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="engagement"
              >
                {geoData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(17, 24, 39, 0.95)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '8px',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Engagement Decay by Region */}
        <div className="rounded-xl border border-white/10 bg-black/20 backdrop-blur-sm p-6">
          <div className="flex items-center gap-3 mb-6">
            <TrendingDown className="w-6 h-6 text-red-400" />
            <div>
              <h2 className="text-xl font-bold text-white">Regional Decay Rates</h2>
              <p className="text-sm text-gray-400">Engagement decline by geography</p>
            </div>
          </div>

          <div className="space-y-4">
            {geoData.map((region, index) => (
              <div key={region.region}>
                <div className="flex justify-between mb-2">
                  <span className="text-sm text-gray-300">{region.region}</span>
                  <span className="text-sm font-bold text-red-400">{region.decline}%</span>
                </div>
                <div className="h-3 bg-white/5 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-orange-500 to-red-500 rounded-full"
                    style={{ width: `${Math.abs(region.decline) * 5}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 rounded-lg bg-red-500/10 border border-red-500/30">
            <p className="text-sm text-red-400">
              ⚠️ Latin America showing highest decay rate - consider regional targeting
            </p>
          </div>
        </div>
      </div>

      {/* Insights */}
      <div className="rounded-xl border border-white/10 bg-gradient-to-br from-blue-950/30 to-purple-950/20 backdrop-blur-sm p-6">
        <h3 className="text-xl font-bold text-white mb-4">Network Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-lg bg-white/5 border border-white/10">
            <h4 className="font-semibold text-white mb-2">Propagation Pattern</h4>
            <p className="text-sm text-gray-300">
              Trend spreading primarily through influencer-driven cascades with strong community hub amplification.
            </p>
          </div>
          <div className="p-4 rounded-lg bg-white/5 border border-white/10">
            <h4 className="font-semibold text-white mb-2">Geographic Concentration</h4>
            <p className="text-sm text-gray-300">
              North America and Europe dominate engagement, but showing faster decay. APAC emerging as growth opportunity.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
