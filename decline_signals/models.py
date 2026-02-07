"""Pydantic Models for Request/Response"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ============================================================================
# INPUT MODELS
# ============================================================================

class LifecycleInfo(BaseModel):
    """Data from Feature #1: Lifecycle Classification"""
    trend_id: str
    trend_name: str
    lifecycle_stage: int  # 1-5
    stage_name: str
    days_in_stage: int
    confidence: float = Field(0.85, ge=0.0, le=1.0)

class DailyMetric(BaseModel):
    """Single day's metrics for a trend"""
    date: str  # ISO format: "2026-02-07"
    total_engagement: int
    views: int
    posts_count: int
    creators_count: int
    avg_creator_followers: float
    avg_comments_per_post: float
    avg_engagement_per_post: float

class DeclineSignalRequest(BaseModel):
    """Request body for decline signal computation"""
    trend_id: str
    trend_name: str
    lifecycle_info: Optional[LifecycleInfo] = None  # May be None if Feature #1 fails
    daily_metrics: List[DailyMetric]

# ============================================================================
# OUTPUT MODELS
# ============================================================================

class SignalBreakdown(BaseModel):
    """Individual signal scores (0-100)"""
    engagement_drop: float
    velocity_decline: float
    creator_decline: float
    quality_decline: float

class DeclineSignalResponse(BaseModel):
    """Main response for decline signal detection"""
    trend_id: str
    decline_risk_score: float  # 0-100
    alert_level: str  # "green", "yellow", "orange", "red"
    signal_breakdown: SignalBreakdown
    timestamp: str  # ISO format with Z
    confidence: str  # "high", "medium", "low"
    data_quality: str = "complete"  # "complete" or "degraded"
    time_to_die: Optional[int] = None  # Days until RED alert (if declining)

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    database_connected: bool
    timestamp: str
