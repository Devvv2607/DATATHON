/**
 * Mock data for development and fallback
 * Realistic data that matches API response structure
 */

import type { 
  TrendOverview, 
  TrendDetails, 
  DeclinePrediction, 
  ExplanationResponse,
  SimulationResponse 
} from './api';

export const mockTrends: TrendOverview[] = [
  {
    id: 'trend_1',
    name: '#AIRevolution2026',
    description: 'Analysis of AI Revolution trend across social media platforms',
    platforms: ['twitter', 'instagram'],
    status: 'peak',
    metrics: {
      engagement_rate: 8.5,
      sentiment_score: 0.82,
      viral_coefficient: 1.8,
      health_score: 85.3
    },
    created_at: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString(),
    last_updated: new Date().toISOString()
  },
  {
    id: 'trend_2',
    name: '#SustainableFashion',
    description: 'Sustainable fashion movement gaining momentum',
    platforms: ['instagram', 'tiktok'],
    status: 'growing',
    metrics: {
      engagement_rate: 6.2,
      sentiment_score: 0.75,
      viral_coefficient: 1.4,
      health_score: 72.1
    },
    created_at: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString(),
    last_updated: new Date().toISOString()
  },
  {
    id: 'trend_3',
    name: '#MetaverseLife',
    description: 'Metaverse lifestyle and virtual experiences',
    platforms: ['twitter', 'tiktok', 'youtube'],
    status: 'declining',
    metrics: {
      engagement_rate: 4.8,
      sentiment_score: 0.62,
      viral_coefficient: 0.9,
      health_score: 58.4
    },
    created_at: new Date(Date.now() - 35 * 24 * 60 * 60 * 1000).toISOString(),
    last_updated: new Date().toISOString()
  },
  {
    id: 'trend_4',
    name: '#WebThreeDev',
    description: 'Web3 development and decentralized applications',
    platforms: ['twitter', 'reddit'],
    status: 'growing',
    metrics: {
      engagement_rate: 7.1,
      sentiment_score: 0.78,
      viral_coefficient: 1.6,
      health_score: 76.8
    },
    created_at: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(),
    last_updated: new Date().toISOString()
  }
];

export const mockTrendDetails: TrendDetails = {
  ...mockTrends[0],
  engagement_history: Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    value: 40 + Math.sin(i / 5) * 30 + Math.random() * 20
  })),
  sentiment_history: Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    value: 60 + Math.cos(i / 7) * 20 + Math.random() * 10
  })),
  top_hashtags: ['#AIRevolution2026', '#AIRev', '#FutureTech', '#MachineLearning'],
  top_influencers: [
    { name: '@techinfluencer', followers: 1_200_000, engagement: 8.5 },
    { name: '@aiexpert', followers: 850_000, engagement: 12.3 },
    { name: '@futuretech', followers: 650_000, engagement: 9.8 }
  ],
  geographic_spread: {
    'US': 35.2,
    'UK': 18.5,
    'India': 15.3,
    'Canada': 8.7,
    'Australia': 7.1,
    'Others': 15.2
  }
};

export const mockDeclinePrediction: DeclinePrediction = {
  trend_id: 'trend_1',
  decline_probability: 0.72,
  is_declining: true,
  days_until_decline: 12,
  confidence_level: 'high',
  prediction_date: new Date().toISOString(),
  model_version: '1.0.0'
};

export const mockExplanation: ExplanationResponse = {
  summary: 'This trend shows strong signs of decline (72% probability).',
  detailed_explanation: 'Audience Saturation is increasing decline risk by 28.0 percentage points. Content Diversity is decreasing decline risk by 18.0 percentage points. Influencer Penetration is increasing decline risk by 15.0 percentage points.',
  feature_attributions: [
    { feature: 'Audience Saturation', impact: 0.28, impact_percentage: 28, direction: 'decline' },
    { feature: 'Content Diversity', impact: -0.18, impact_percentage: 18, direction: 'growth' },
    { feature: 'Influencer Penetration', impact: 0.15, impact_percentage: 15, direction: 'decline' },
    { feature: 'Novelty Score', impact: -0.11, impact_percentage: 11, direction: 'growth' },
    { feature: 'Engagement Rate', impact: -0.08, impact_percentage: 8, direction: 'growth' }
  ],
  counterfactuals: [
    {
      scenario: 'If audience saturation decreased to 40%',
      change: { audience_saturation: 0.40 },
      predicted_probability: 0.57,
      outcome: 'Trend would have lower decline risk'
    },
    {
      scenario: 'If content novelty increased to 75%',
      change: { novelty_score: 0.75 },
      predicted_probability: 0.60,
      outcome: 'Fresh content would reduce decline risk'
    }
  ],
  confidence: 'Prediction confidence: high',
  recommendations: [
    'Target new audience segments to reduce saturation',
    'Introduce fresh content angles and creative variations',
    'Reduce influencer dependency through organic community growth'
  ]
};

export const mockSimulation: SimulationResponse = {
  baseline: {
    features: {
      engagement_rate: 8.5,
      sentiment_score: 0.82,
      audience_saturation: 0.75
    },
    trajectory: Array.from({ length: 30 }, (_, i) => ({
      day: i,
      date: new Date(Date.now() + i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      health_score: 85 - i * 2 + Math.random() * 5,
      engagement: 8.5 - i * 0.15,
      sentiment: 82 - i * 1.2
    })),
    final_health: 35.2
  },
  with_intervention: {
    features: {
      engagement_rate: 10.2,
      sentiment_score: 0.87,
      audience_saturation: 0.60
    },
    trajectory: Array.from({ length: 30 }, (_, i) => ({
      day: i,
      date: new Date(Date.now() + i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      health_score: 85 - i * 1.2 + Math.random() * 5,
      engagement: 10.2 - i * 0.08,
      sentiment: 87 - i * 0.8
    })),
    final_health: 58.7
  },
  impact: {
    health_improvement: 23.5,
    improvement_percentage: 66.8,
    days_extended: 14,
    engagement_lift: 20.0
  },
  recommendations: [
    'This intervention shows significant positive impact on trend health',
    'Expected engagement lift is substantial',
    'Projected to extend trend lifespan by 14 days'
  ],
  cost_estimate: {
    breakdown: {
      add_influencers: 25000,
      increase_content_novelty: 10000
    },
    total_usd: 35000
  },
  roi_prediction: {
    total_cost_usd: 35000,
    estimated_benefit_usd: 68000,
    roi_percentage: 94.3,
    recommendation: 'Recommended'
  }
};

export const mockTrajectory = Array.from({ length: 30 }, (_, i) => ({
  date: new Date(Date.now() + i * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
  predicted_value: 85 - i * 1.8 + Math.random() * 5,
  confidence_lower: 75 - i * 1.8,
  confidence_upper: 95 - i * 1.8
}));
