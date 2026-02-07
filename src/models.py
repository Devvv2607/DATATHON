"""Data models for Brand Trend Revenue Intelligence Agent"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import pandas as pd


@dataclass
class TrendData:
    """Represents trend data from Google Trends"""
    keyword: str
    domain: str
    interest_over_time: pd.DataFrame
    current_interest: int
    peak_interest: int
    related_queries: List[str] = field(default_factory=list)


@dataclass
class TrendMetrics:
    """Calculated metrics for a trend"""
    growth_slope: float  # Percentage per month
    current_interest: int  # 0-100 scale
    peak_interest: int
    average_interest: float
    volatility: float
    trend_direction: str  # "up", "down", "flat"


@dataclass
class TrendClassification:
    """Classification result for a trend"""
    category: str  # "growing", "stable", "declining"
    confidence: float  # 0.0 to 1.0
    growth_rate: float  # Percentage
    reasoning: str


@dataclass
class BudgetStrategy:
    """Budget scaling recommendations"""
    recommendation: str
    scaling_percentage: str
    rationale: str


@dataclass
class ImpactMetrics:
    """Expected business impact metrics"""
    reach_increase: str
    conversion_impact: str
    revenue_potential: str


@dataclass
class GrowthAction:
    """Individual growth action recommendation"""
    title: str
    description: str
    expected_reach_increase: str  # e.g., "15-25%"
    expected_conversion_impact: str  # e.g., "10-15% lift"
    implementation_priority: str  # "high", "medium", "low"


@dataclass
class GrowthRecommendations:
    """Complete growth recommendations for a growing trend"""
    actions: List[GrowthAction]  # Exactly 3 actions
    content_angles: List[str]
    budget_strategy: BudgetStrategy
    estimated_impact: ImpactMetrics


@dataclass
class PivotStrategy:
    """Content strategy for pivoting to new trends"""
    approach: str
    timeline: str
    key_actions: List[str]


@dataclass
class AlternativeTrend:
    """Alternative trend suggestion"""
    keyword: str
    growth_rate: float
    relevance_to_domain: str
    entry_difficulty: str  # "low", "medium", "high"


@dataclass
class DeclineAnalysis:
    """Analysis and recommendations for declining trends"""
    days_until_collapse: int
    projected_marketing_burn: float
    recommendation: str  # "EXIT" or "TRY REVIVAL"
    revival_conditions: Optional[List[str]]
    alternative_trends: List[AlternativeTrend]  # 2-3 alternatives
    pivot_strategy: PivotStrategy


@dataclass
class ValidationResult:
    """Result of input validation"""
    is_valid: bool
    error_message: Optional[str] = None
    normalized_value: Optional[str] = None


@dataclass
class ErrorResponse:
    """Structured error response"""
    status: str = "error"
    error_type: str = ""
    message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    retry_possible: bool = False
