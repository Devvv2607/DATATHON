'use client';

import { useState } from 'react';
import { Database, Save, Upload } from 'lucide-react';
import { useDomain } from '@/contexts/DomainContext';
import DomainAndTrendSelector from '@/components/DomainAndTrendSelector';
import { useAuth } from '@/contexts/AuthContext';

// Pre-filled templates for quick demo
const TEMPLATES = {
  fashion_startup: {
    business_name: 'TrendyStyle Fashion',
    monthly_revenue: '45000',
    monthly_costs: '18000',
    content_pieces: '25',
    avg_engagement_rate: '6.2',
    avg_reach: '12000',
    campaigns_running: '3',
    avg_campaign_cost: '3500',
    conversion_rate: '3.2',
    total_followers: '48000',
    monthly_growth_rate: '12.5',
    target_audience: 'Women 18-35, fashion enthusiasts, urban millennials',
    revenue_goal: '60000',
    growth_goal: '20',
    notes: 'Focusing on sustainable fashion and influencer partnerships'
  },
  tech_company: {
    business_name: 'CloudTech Solutions',
    monthly_revenue: '120000',
    monthly_costs: '45000',
    content_pieces: '40',
    avg_engagement_rate: '8.5',
    avg_reach: '35000',
    campaigns_running: '5',
    avg_campaign_cost: '8000',
    conversion_rate: '4.8',
    total_followers: '125000',
    monthly_growth_rate: '15.2',
    target_audience: 'Tech professionals, developers, CTOs, IT managers 25-45',
    revenue_goal: '150000',
    growth_goal: '25',
    notes: 'B2B SaaS platform, targeting enterprise clients'
  }
};

export default function BusinessDataPage() {
  const { token } = useAuth();
  const { selectedDomain } = useDomain();
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const [businessData, setBusinessData] = useState({
    // Basic Info
    business_name: '',
    monthly_revenue: '',
    monthly_costs: '',
    
    // Content Metrics
    content_pieces: '',
    avg_engagement_rate: '',
    avg_reach: '',
    
    // Campaign Data
    campaigns_running: '',
    avg_campaign_cost: '',
    conversion_rate: '',
    
    // Audience Metrics
    total_followers: '',
    monthly_growth_rate: '',
    target_audience: '',
    
    // Goals
    revenue_goal: '',
    growth_goal: '',
    notes: ''
  });

  const applyTemplate = (templateKey: string) => {
    setBusinessData(TEMPLATES[templateKey as keyof typeof TEMPLATES]);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setBusinessData({
      ...businessData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(false);

    try {
      const response = await fetch('http://localhost:8000/api/business/user-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          domain: selectedDomain,
          data: businessData
        })
      });

      if (response.ok) {
        setSuccess(true);
        // Store in localStorage as backup
        localStorage.setItem(`business_data_${selectedDomain}`, JSON.stringify(businessData));
        setTimeout(() => setSuccess(false), 3000);
      }
    } catch (error) {
      console.error('Error saving data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Business Data Collection</h1>
          <p className="text-gray-400 mt-2">Input your metrics for personalized insights</p>
        </div>
      </div>

      <DomainAndTrendSelector />

      {/* Quick Templates */}
      <div className="glass-card p-6 rounded-2xl bg-purple-500/5 border border-purple-500/20">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold text-purple-400">⚡ Quick Start Templates</h3>
            <p className="text-sm text-gray-400">Fill form instantly with realistic demo data</p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            type="button"
            onClick={() => applyTemplate('fashion_startup')}
            className="p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-pink-500/50 transition-all duration-300 text-left group"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-gradient-to-br from-pink-500 to-purple-500">
                <span className="text-2xl">👗</span>
              </div>
              <div>
                <h4 className="font-bold text-white group-hover:text-pink-400">Fashion Startup</h4>
                <p className="text-xs text-gray-400">$45K revenue, 48K followers, 6.2% engagement</p>
              </div>
            </div>
            <p className="text-sm text-gray-300">Perfect for fashion brands, e-commerce, retail businesses</p>
          </button>

          <button
            type="button"
            onClick={() => applyTemplate('tech_company')}
            className="p-4 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 hover:border-blue-500/50 transition-all duration-300 text-left group"
          >
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500">
                <span className="text-2xl">💻</span>
              </div>
              <div>
                <h4 className="font-bold text-white group-hover:text-blue-400">Tech Company</h4>
                <p className="text-xs text-gray-400">$120K revenue, 125K followers, 8.5% engagement</p>
              </div>
            </div>
            <p className="text-sm text-gray-300">Ideal for SaaS, software companies, tech startups</p>
          </button>
        </div>
      </div>

      {success && (
        <div className="glass-card p-4 rounded-xl bg-green-500/10 border border-green-500/20">
          <p className="text-green-400 font-medium">✓ Data saved successfully! Your insights will now be personalized.</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Business Info */}
        <div className="glass-card p-6 rounded-2xl">
          <div className="flex items-center gap-3 mb-6">
            <Database className="w-6 h-6 text-blue-400" />
            <h2 className="text-xl font-bold text-white">Basic Information</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Business Name</label>
              <input
                type="text"
                name="business_name"
                value={businessData.business_name}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., TrendyFashion Co."
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Monthly Revenue ($)</label>
              <input
                type="number"
                name="monthly_revenue"
                value={businessData.monthly_revenue}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 50000"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Monthly Costs ($)</label>
              <input
                type="number"
                name="monthly_costs"
                value={businessData.monthly_costs}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 15000"
              />
            </div>
          </div>
        </div>

        {/* Content Metrics */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-6">Content Metrics</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Content Pieces/Month</label>
              <input
                type="number"
                name="content_pieces"
                value={businessData.content_pieces}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 20"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Avg Engagement Rate (%)</label>
              <input
                type="number"
                step="0.1"
                name="avg_engagement_rate"
                value={businessData.avg_engagement_rate}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 5.2"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Avg Reach per Post</label>
              <input
                type="number"
                name="avg_reach"
                value={businessData.avg_reach}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 10000"
              />
            </div>
          </div>
        </div>

        {/* Campaign Data */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-6">Campaign Data</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Active Campaigns</label>
              <input
                type="number"
                name="campaigns_running"
                value={businessData.campaigns_running}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 3"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Avg Campaign Cost ($)</label>
              <input
                type="number"
                name="avg_campaign_cost"
                value={businessData.avg_campaign_cost}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 2000"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Conversion Rate (%)</label>
              <input
                type="number"
                step="0.1"
                name="conversion_rate"
                value={businessData.conversion_rate}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 2.5"
              />
            </div>
          </div>
        </div>

        {/* Audience Metrics */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-6">Audience Metrics</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Total Followers</label>
              <input
                type="number"
                name="total_followers"
                value={businessData.total_followers}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 50000"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Monthly Growth Rate (%)</label>
              <input
                type="number"
                step="0.1"
                name="monthly_growth_rate"
                value={businessData.monthly_growth_rate}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 8.5"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm text-gray-400 mb-2">Target Audience</label>
              <input
                type="text"
                name="target_audience"
                value={businessData.target_audience}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., Women 25-35, Fashion enthusiasts, Urban professionals"
              />
            </div>
          </div>
        </div>

        {/* Goals */}
        <div className="glass-card p-6 rounded-2xl">
          <h2 className="text-xl font-bold text-white mb-6">Business Goals</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-2">Revenue Goal (Next Month) ($)</label>
              <input
                type="number"
                name="revenue_goal"
                value={businessData.revenue_goal}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 75000"
              />
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-2">Growth Goal (%)</label>
              <input
                type="number"
                step="0.1"
                name="growth_goal"
                value={businessData.growth_goal}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none"
                placeholder="e.g., 15"
              />
            </div>

            <div className="md:col-span-2">
              <label className="block text-sm text-gray-400 mb-2">Additional Notes</label>
              <textarea
                name="notes"
                value={businessData.notes}
                onChange={handleChange}
                rows={4}
                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-blue-500 focus:outline-none resize-none"
                placeholder="Any specific challenges, opportunities, or context about your business..."
              />
            </div>
          </div>
        </div>

        <div className="flex items-center justify-end gap-4">
          <button
            type="submit"
            disabled={loading}
            className="flex items-center gap-3 px-8 py-4 rounded-xl glass-card text-blue-400 hover:text-white transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <Save className="w-5 h-5" />
                Save Business Data
              </>
            )}
          </button>
        </div>
      </form>

      <div className="glass-card p-6 rounded-2xl bg-blue-500/5 border border-blue-500/20">
        <h3 className="text-lg font-bold text-blue-400 mb-2">💡 Why provide this data?</h3>
        <ul className="space-y-2 text-gray-300 text-sm">
          <li>• Get personalized ROI calculations based on YOUR actual revenue and costs</li>
          <li>• Receive investment recommendations tailored to YOUR business performance</li>
          <li>• Compare YOUR metrics against industry trends and benchmarks</li>
          <li>• Get accurate campaign timing suggestions for YOUR audience</li>
          <li>• Find alternative trends that match YOUR business goals</li>
        </ul>
      </div>
    </div>
  );
}
