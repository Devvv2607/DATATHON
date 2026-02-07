"""
Pydantic schemas for request/response validation (Twitter/X Edition).
Defines the structure of X/Twitter trend metrics input and analysis output.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class PeriodMetric(BaseModel):
    """Metric comparing current and previous periods."""
    current: float = Field(..., description="Current period value")
    previous_period: float = Field(..., description="Previous period value for comparison")


class XMetrics(BaseModel):
    """X/Twitter platform metrics (all optional but at least one should be provided)."""
    tweet_volume: Optional[PeriodMetric] = Field(None, description="Number of tweets with trend")
    weekly_engagement_velocity: Optional[float] = Field(None, description="Weekly % change in engagement (-0.15 = 15% decline)")
    unique_content_ratio: Optional[float] = Field(None, ge=0, le=1, description="0-1, % of posts that are unique (novelty)")
    posts_per_day: Optional[PeriodMetric] = Field(None, description="Daily posting volume")
    reach_per_tweet: Optional[PeriodMetric] = Field(None, description="Average reach per tweet")
    impression_velocity: Optional[float] = Field(None, description="Daily % change in impressions")
    top_accounts_participation: Optional[PeriodMetric] = Field(None, description="Number of top accounts posting")
    top_influencer_engagement: Optional[PeriodMetric] = Field(None, description="Engagement from top influencers")
    sentiment_score: Optional[PeriodMetric] = Field(None, description="Sentiment (-1 to 1, negative = bad)")
    days_since_peak: Optional[int] = Field(None, ge=0, description="Days since trend peaked")


class TrendMetricsInput(BaseModel):
    """Complete input schema for trend analysis (Twitter/X only)."""
    trend_name: str = Field(..., description="Name of trend, hashtag, or topic")
    x: Optional[XMetrics] = Field(None, description="X/Twitter metrics (required)")

    class Config:
        json_schema_extra = {
            "example": {
                "trend_name": "#TechTok",
                "x": {
                    "tweet_volume": {"current": 45000, "previous_period": 52000},
                    "weekly_engagement_velocity": -0.15,
                    "unique_content_ratio": 0.25,
                    "posts_per_day": {"current": 2800, "previous_period": 3200},
                    "reach_per_tweet": {"current": 850, "previous_period": 1100},
                }
            }
        }


class DeclineCauseOutput(BaseModel):
    """Single detected cause in output."""
    cause_type: str
    confidence: float
    severity_contribution: float
    evidence: List[str]
    affected_platforms: List[str]
    business_explanation: str


class RecommendedActionOutput(BaseModel):
    """Actionable recommendation in output."""
    action_type: str
    priority: str
    description: str
    expected_impact: str
    timeframe: str
    platforms_targeted: List[str]


class TrendAnalysisOutput(BaseModel):
    """Complete analysis output."""
    trend_name: str
    analysis_timestamp: str
    trend_status: str
    decline_probability: float
    severity_level: str
    root_causes: List[DeclineCauseOutput]
    cross_platform_summary: Dict[str, Any]
    recommended_actions: List[RecommendedActionOutput]
    confidence_in_analysis: float

    class Config:
        json_schema_extra = {
            "example": {
                "trend_name": "#TechTok",
                "analysis_timestamp": "2026-02-07T14:30:00Z",
                "trend_status": "DECLINING",
                "decline_probability": 0.72,
                "severity_level": "WARNING",
                "root_causes": [
                    {
                        "cause_type": "Engagement Decay",
                        "confidence": 0.85,
                        "severity_contribution": 0.68,
                        "evidence": ["X engagement declining at -15.0% per week"],
                        "affected_platforms": ["X"],
                        "business_explanation": "Users are interacting less...",
                    }
                ],
                "cross_platform_summary": {
                    "X": {
                        "tweet_volume": 45000,
                        "engagement_velocity": -0.15,
                        "health_status": "Declining"
                    }
                },
                "recommended_actions": [],
                "confidence_in_analysis": 0.65,
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    details: Optional[str] = None
    timestamp: str
