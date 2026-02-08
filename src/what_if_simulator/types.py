"""Core type definitions for the What-If Trend Adoption Simulator."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional, Dict, Any
from datetime import datetime


# Input Types
@dataclass
class TrendContext:
    """Metadata about the trend being analyzed."""
    trend_id: str
    trend_name: str
    platform: str
    lifecycle_stage: Literal["emerging", "growth", "peak", "decline", "dormant"]
    current_risk_score: float  # 0-100
    confidence: Literal["low", "medium", "high"]


@dataclass
class CampaignStrategy:
    """User-specified campaign parameters."""
    campaign_type: Literal["short_term_influencer", "long_term_paid", "organic_only", "mixed"]
    budget_range: Dict[str, float]  # {"min": float, "max": float}
    campaign_duration_days: int
    creator_tier: Literal["nano", "micro", "macro", "mixed"]
    content_intensity: Literal["low", "medium", "high"]


@dataclass
class Assumptions:
    """User-provided beliefs about market conditions."""
    engagement_trend: Literal["optimistic", "neutral", "pessimistic"] = "neutral"
    creator_participation: Literal["increasing", "stable", "declining"] = "stable"
    market_noise: Literal["low", "medium", "high"] = "medium"


@dataclass
class Constraints:
    """User-specified boundaries for simulation."""
    risk_tolerance: Literal["low", "medium", "high"]
    max_budget_cap: float


@dataclass
class ScenarioInput:
    """Complete scenario input for simulation."""
    trend_context: TrendContext
    campaign_strategy: CampaignStrategy
    assumptions: Assumptions
    constraints: Constraints
    scenario_id: Optional[str] = None


# Output Types
@dataclass
class SimulationSummary:
    """High-level summary of simulation results."""
    scenario_label: str
    overall_outlook: Literal["favorable", "risky", "unfavorable"]
    confidence: Literal["low", "medium", "high"]


@dataclass
class RangeValue:
    """A min-max range representing uncertainty."""
    min: float
    max: float


@dataclass
class ExpectedGrowthMetrics:
    """Range-based growth projections."""
    engagement_growth_percent: RangeValue
    reach_growth_percent: RangeValue
    creator_participation_change_percent: RangeValue


@dataclass
class ExpectedROIMetrics:
    """Range-based ROI projections with probabilities."""
    roi_percent: RangeValue
    break_even_probability: float  # 0-100
    loss_probability: float  # 0-100


@dataclass
class RiskProjection:
    """Risk score evolution."""
    current_risk_score: float  # 0-100
    projected_risk_score: RangeValue
    risk_trend: Literal["improving", "stable", "worsening"]


@dataclass
class DecisionInterpretation:
    """Strategic recommendations based on numeric ranges."""
    recommended_posture: Literal["scale", "test_small", "monitor", "avoid"]
    primary_opportunities: list[str]
    primary_risks: list[str]


@dataclass
class AssumptionSensitivity:
    """Sensitivity analysis results."""
    most_sensitive_factor: str
    impact_if_wrong: Literal["low", "medium", "high"]


@dataclass
class Guardrails:
    """Data limitations and transparency notes."""
    data_coverage: float  # 0-100
    system_note: str


@dataclass
class SimulationResponse:
    """Complete simulation output."""
    scenario_id: str
    trend_id: str
    trend_name: str
    simulation_summary: SimulationSummary
    expected_growth_metrics: ExpectedGrowthMetrics
    expected_roi_metrics: ExpectedROIMetrics
    risk_projection: RiskProjection
    decision_interpretation: DecisionInterpretation
    assumption_sensitivity: AssumptionSensitivity
    guardrails: Guardrails
    executive_summary: Optional[Dict[str, Any]] = None


# Error Types
@dataclass
class ValidationFailure:
    """A single validation failure."""
    field: str
    message: str
    guidance: str


@dataclass
class ErrorResponse:
    """Structured error response."""
    error_code: str
    error_message: str
    validation_failures: list[ValidationFailure] = field(default_factory=list)


# External System Response Types
@dataclass
class TrendLifecycleEngineResponse:
    """Response from Trend Lifecycle Engine."""
    lifecycle_stage: Literal["emerging", "growth", "peak", "decline", "dormant"]
    engagement_trend: float  # 0-100
    roi_trend: float  # 0-100
    historical_volatility: float  # 0-100


@dataclass
class EarlyDeclineDetectionResponse:
    """Response from Early Decline Detection system."""
    current_risk_score: float  # 0-100
    risk_indicators: list[str]
    risk_trajectory: Literal["increasing", "stable", "decreasing"]


@dataclass
class ROIAttributionResponse:
    """Response from ROI Attribution system."""
    roi_percent_range: RangeValue
    confidence: float  # 0-100


# Scenario Persistence Types
@dataclass
class ScenarioMetadata:
    """Metadata for persisted scenarios."""
    scenario_id: str
    created_timestamp: datetime
    last_modified_timestamp: datetime
    created_by_user_id: str


@dataclass
class PersistedScenario:
    """Complete persisted scenario with results."""
    metadata: ScenarioMetadata
    input: ScenarioInput
    result: Optional[SimulationResponse] = None
