/**
 * API Service Layer for Frontend
 * Handles all backend communication with type safety
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// ========== TYPES ==========

export interface TrendMetrics {
  engagement_rate: number;
  sentiment_score: number;
  viral_coefficient: number;
  health_score: number;
}

export interface TrendOverview {
  id: string;
  name: string;
  description: string;
  platforms: string[];
  status: string;
  metrics: TrendMetrics;
  created_at: string;
  last_updated: string;
}

export interface TimeSeriesPoint {
  date: string;
  value: number;
}

export interface TrendDetails extends TrendOverview {
  engagement_history: TimeSeriesPoint[];
  sentiment_history: TimeSeriesPoint[];
  top_hashtags: string[];
  top_influencers: Array<{
    name: string;
    followers: number;
    engagement: number;
  }>;
  geographic_spread: Record<string, number>;
}

export interface DeclinePrediction {
  trend_id: string;
  decline_probability: number;
  is_declining: boolean;
  days_until_decline: number;
  confidence_level: string;
  prediction_date: string;
  model_version: string;
}

export interface FeatureAttribution {
  feature: string;
  impact: number;
  impact_percentage: number;
  direction: string;
}

export interface ExplanationResponse {
  summary: string;
  detailed_explanation: string;
  feature_attributions: FeatureAttribution[];
  counterfactuals: Array<{
    scenario: string;
    change: Record<string, number>;
    predicted_probability: number;
    outcome: string;
  }>;
  confidence: string;
  recommendations: string[];
}

export interface SimulationRequest {
  trend_id: string;
  interventions: Record<string, number>;
  forecast_days?: number;
}

export interface SimulationResponse {
  baseline: {
    features: Record<string, number>;
    trajectory: Array<{
      day: number;
      date: string;
      health_score: number;
      engagement: number;
      sentiment: number;
    }>;
    final_health: number;
  };
  with_intervention: {
    features: Record<string, number>;
    trajectory: Array<{
      day: number;
      date: string;
      health_score: number;
      engagement: number;
      sentiment: number;
    }>;
    final_health: number;
  };
  impact: {
    health_improvement: number;
    improvement_percentage: number;
    days_extended: number;
    engagement_lift: number;
  };
  recommendations: string[];
  cost_estimate: {
    breakdown: Record<string, number>;
    total_usd: number;
  };
  roi_prediction: {
    total_cost_usd: number;
    estimated_benefit_usd: number;
    roi_percentage: number;
    recommendation: string;
  };
}

// ========== API FUNCTIONS ==========

export async function fetchTrends(
  platforms?: string[],
  status?: string,
  limit: number = 20
): Promise<{ trends: TrendOverview[]; total: number }> {
  try {
    const params = new URLSearchParams();
    if (platforms) platforms.forEach(p => params.append('platforms', p));
    if (status) params.append('status', status);
    params.append('limit', limit.toString());

    const response = await fetch(`${API_BASE_URL}/trends?${params}`);
    if (!response.ok) throw new Error('Failed to fetch trends');
    return await response.json();
  } catch (error) {
    console.error('Error fetching trends:', error);
    // Return mock data on error
    return import('./mockData').then(m => ({ trends: m.mockTrends.slice(0, limit), total: m.mockTrends.length }));
  }
}

export async function fetchTrendDetails(trendId: string): Promise<TrendDetails> {
  try {
    const response = await fetch(`${API_BASE_URL}/trends/${trendId}`);
    if (!response.ok) throw new Error('Failed to fetch trend details');
    return await response.json();
  } catch (error) {
    console.error('Error fetching trend details:', error);
    return import('./mockData').then(m => m.mockTrendDetails);
  }
}

export async function predictDecline(trendId: string): Promise<DeclinePrediction> {
  try {
    const response = await fetch(`${API_BASE_URL}/trends/predict/decline?trend_id=${trendId}`, {
      method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to predict decline');
    return await response.json();
  } catch (error) {
    console.error('Error predicting decline:', error);
    return import('./mockData').then(m => m.mockDeclinePrediction);
  }
}

export async function getExplanation(trendId: string): Promise<ExplanationResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/trends/explain/${trendId}`);
    if (!response.ok) throw new Error('Failed to fetch explanation');
    return await response.json();
  } catch (error) {
    console.error('Error fetching explanation:', error);
    return import('./mockData').then(m => m.mockExplanation);
  }
}

export async function simulateIntervention(request: SimulationRequest): Promise<SimulationResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/trends/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });
    if (!response.ok) throw new Error('Failed to simulate intervention');
    return await response.json();
  } catch (error) {
    console.error('Error simulating intervention:', error);
    return import('./mockData').then(m => m.mockSimulation);
  }
}

export async function fetchTrajectory(trendId: string, days: number = 30) {
  try {
    const response = await fetch(`${API_BASE_URL}/trends/${trendId}/trajectory?days=${days}`);
    if (!response.ok) throw new Error('Failed to fetch trajectory');
    return await response.json();
  } catch (error) {
    console.error('Error fetching trajectory:', error);
    return import('./mockData').then(m => ({ trajectory: m.mockTrajectory }));
  }
}
