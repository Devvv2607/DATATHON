/**
 * API Client for Comeback AI Content Generation
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ComebackRequest {
  trend_name: string;
  alert_level?: string;
  lifecycle_stage?: number;
  decline_risk_score?: number;
}

export interface ReelIdea {
  id: number;
  title: string;
  description: string;
  hook: string;
  why_it_works: string;
}

export interface Caption {
  id: number;
  caption: string;
  language: string;
}

export interface RemixFormat {
  id: number;
  format: string;
  structure: string;
  example: string;
}

export interface ContentIdeas {
  reels: ReelIdea[];
  captions: Caption[];
  remixes: RemixFormat[];
}

export interface ComebackResponse {
  trend_name: string;
  alert_level: string;
  mode: string;
  decline_risk_score: number;
  lifecycle_stage: number;
  stage_name: string;
  decline_drivers?: string[];
  growth_opportunities?: string[];
  content_strategy: string;
  content: ContentIdeas;
  generated_at: string;
  confidence: string;
}

/**
 * Generate comeback/growth content for a trend
 */
export async function generateComebackContent(
  request: ComebackRequest
): Promise<ComebackResponse> {
  const response = await fetch(`${API_BASE_URL}/api/comeback/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to generate content');
  }

  return response.json();
}

/**
 * Check Comeback AI health status
 */
export async function checkComebackHealth() {
  const response = await fetch(`${API_BASE_URL}/api/comeback/health`);
  
  if (!response.ok) {
    throw new Error('Health check failed');
  }

  return response.json();
}

/**
 * Quick test endpoint
 */
export async function quickTest(trendName: string = 'AI memes') {
  const response = await fetch(
    `${API_BASE_URL}/api/comeback/quick-test?trend_name=${encodeURIComponent(trendName)}`,
    { method: 'POST' }
  );

  if (!response.ok) {
    throw new Error('Quick test failed');
  }

  return response.json();
}
