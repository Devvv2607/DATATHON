"""
MongoDB Schemas and Pydantic Models for Trend Lifecycle Detection
"""

from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId


class LifecycleStage(int, Enum):
    """Fixed lifecycle stages - DO NOT CHANGE"""
    EMERGENCE = 1
    VIRAL_EXPLOSION = 2
    PLATEAU = 3
    DECLINE = 4
    DEATH = 5


STAGE_NAMES = {
    LifecycleStage.EMERGENCE: "Emergence",
    LifecycleStage.VIRAL_EXPLOSION: "Viral Explosion",
    LifecycleStage.PLATEAU: "Plateau",
    LifecycleStage.DECLINE: "Decline",
    LifecycleStage.DEATH: "Death"
}


# === API Request/Response Models ===

class TrendLifecycleRequest(BaseModel):
    """Input contract for lifecycle detection"""
    trend_name: str = Field(..., min_length=1, max_length=200)


class TrendLifecycleResponse(BaseModel):
    """Output contract - STRICT FORMAT"""
    trend_id: str
    trend_name: str
    lifecycle_stage: int = Field(..., ge=1, le=5)
    stage_name: str
    days_in_stage: int = Field(..., ge=0)
    confidence: float = Field(..., ge=0.0, le=1.0)


# === Feature Engineering Models ===

class GoogleTrendsSignals(BaseModel):
    """Google Trends extracted features"""
    interest_score: float = Field(..., ge=0, le=100)
    interest_slope: float
    rolling_mean_interest: float = Field(..., ge=0, le=100)
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class TwitterSignals(BaseModel):
    """Twitter/X extracted features"""
    post_volume: int = Field(..., ge=0)
    engagement_rate: float = Field(..., ge=0)
    velocity: float  # day-over-day change
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class RedditSignals(BaseModel):
    """Reddit extracted features"""
    post_count: int = Field(..., ge=0)
    comment_count: int = Field(..., ge=0)
    discussion_growth_rate: float
    raw_data: Dict[str, Any] = Field(default_factory=dict)


class AggregatedSignals(BaseModel):
    """Computed cross-platform signals"""
    growth_rate: float
    momentum: float  # rolling average momentum
    decay_signal: float  # sustained negative momentum indicator
    engagement_saturation: float = Field(..., ge=0, le=1)


# === MongoDB Document Model ===

class TrendLifecycleDocument(BaseModel):
    """MongoDB document structure"""
    trend_id: str = Field(default_factory=lambda: str(ObjectId()))
    trend_name: str
    lifecycle_stage: int
    stage_name: str
    days_in_stage: int
    confidence: float
    
    # Raw signals
    google_signals: Optional[GoogleTrendsSignals] = None
    twitter_signals: Optional[TwitterSignals] = None
    reddit_signals: Optional[RedditSignals] = None
    aggregated_signals: Optional[AggregatedSignals] = None
    
    # Metadata
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            ObjectId: lambda v: str(v)
        }
