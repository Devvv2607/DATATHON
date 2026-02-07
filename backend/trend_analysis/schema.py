"""
Pydantic schemas for request/response validation
Ensures type safety and automatic API documentation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# ========== ENUMS ==========

class PlatformType(str, Enum):
    """Supported social media platforms"""
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    REDDIT = "reddit"
    YOUTUBE = "youtube"

class TrendStatus(str, Enum):
    """Trend lifecycle status"""
    EMERGING = "emerging"
    GROWING = "growing"
    PEAK = "peak"
    DECLINING = "declining"
    FADED = "faded"

class ConfidenceLevel(str, Enum):
    """Prediction confidence levels"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

# ========== RESPONSE MODELS ==========

class TrendMetrics(BaseModel):
    """Core trend metrics"""
    engagement_rate: float = Field(..., description="Engagement rate (0-100)")
    sentiment_score: float = Field(..., description="Sentiment score (0-1)")
    viral_coefficient: float = Field(..., description="Viral coefficient (shares per user)")
    health_score: float = Field(..., description="Overall health score (0-100)")

class TrendOverview(BaseModel):
    """Overview of a single trend"""
    id: str = Field(..., description="Unique trend identifier")
    name: str = Field(..., description="Trend name or hashtag")
    description: str = Field(..., description="Brief description")
    platforms: List[PlatformType] = Field(..., description="Active platforms")
    status: TrendStatus = Field(..., description="Current lifecycle status")
    metrics: TrendMetrics
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

class TimeSeriesPoint(BaseModel):
    """Single data point in time series"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    value: float = Field(..., description="Metric value")

class TrendDetails(BaseModel):
    """Detailed trend information"""
    id: str
    name: str
    description: str
    platforms: List[PlatformType]
    status: TrendStatus
    metrics: TrendMetrics
    engagement_history: List[TimeSeriesPoint]
    sentiment_history: List[TimeSeriesPoint]
    top_hashtags: List[str] = Field(default_factory=list)
    top_influencers: List[Dict[str, Any]] = Field(default_factory=list)
    geographic_spread: Dict[str, float] = Field(default_factory=dict)

class DeclinePrediction(BaseModel):
    """Decline prediction result"""
    trend_id: str
    decline_probability: float = Field(..., ge=0, le=1, description="Probability of decline (0-1)")
    is_declining: bool = Field(..., description="Whether trend is predicted to decline")
    days_until_decline: int = Field(..., description="Estimated days until decline")
    confidence_level: ConfidenceLevel
    prediction_date: datetime = Field(default_factory=datetime.now)
    model_version: str = Field(default="1.0.0")

class FeatureAttribution(BaseModel):
    """Feature importance for explainability"""
    feature: str
    impact: float
    impact_percentage: float
    direction: str  # "decline" or "growth"

class Counterfactual(BaseModel):
    """Counterfactual scenario"""
    scenario: str
    change: Dict[str, float]
    predicted_probability: float
    outcome: str

class ExplanationResponse(BaseModel):
    """Explanation for prediction"""
    summary: str
    detailed_explanation: str
    feature_attributions: List[FeatureAttribution]
    counterfactuals: List[Counterfactual]
    confidence: str
    recommendations: List[str]

class TrajectoryPoint(BaseModel):
    """Point in trend trajectory"""
    day: int
    date: str
    health_score: float
    engagement: float
    sentiment: float

class SimulationImpact(BaseModel):
    """Impact metrics from simulation"""
    health_improvement: float
    improvement_percentage: float
    days_extended: int
    engagement_lift: float

class ROIPrediction(BaseModel):
    """ROI prediction for intervention"""
    total_cost_usd: float
    estimated_benefit_usd: float
    roi_percentage: float
    recommendation: str

class SimulationResponse(BaseModel):
    """Simulation result"""
    baseline: Dict[str, Any]
    with_intervention: Dict[str, Any]
    impact: SimulationImpact
    recommendations: List[str]
    cost_estimate: Dict[str, Any]
    roi_prediction: ROIPrediction

# ========== REQUEST MODELS ==========

class SimulationRequest(BaseModel):
    """Request to simulate interventions"""
    trend_id: str
    interventions: Dict[str, float] = Field(
        ...,
        description="Intervention parameters (e.g., {'add_influencers': 5})"
    )
    forecast_days: int = Field(default=30, ge=7, le=90)

class TrendQuery(BaseModel):
    """Query parameters for trend search"""
    platforms: Optional[List[PlatformType]] = None
    status: Optional[TrendStatus] = None
    min_health_score: Optional[float] = Field(None, ge=0, le=100)
    limit: int = Field(default=20, ge=1, le=100)

# ========== LIST RESPONSES ==========

class TrendsListResponse(BaseModel):
    """Paginated list of trends"""
    trends: List[TrendOverview]
    total: int
    page: int = 1
    page_size: int = 20

class HealthCheckResponse(BaseModel):
    """API health check"""
    status: str
    service: str
    version: str
    endpoints: Dict[str, str]
