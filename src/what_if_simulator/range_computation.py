"""Range computation component for calculating output ranges."""

import logging
from typing import Dict, Any

from .types import RangeValue, ScenarioInput
from .utils import (
    apply_multiplier_to_range,
    widen_range,
    clamp,
)
from .constants import (
    ENGAGEMENT_TREND_MODIFIERS,
    CREATOR_PARTICIPATION_MODIFIERS,
    MARKET_NOISE_RANGE_WIDENING,
    CAMPAIGN_BUDGET_MULTIPLIERS,
    CREATOR_TIER_REACH_MULTIPLIERS,
    CONTENT_INTENSITY_MULTIPLIERS,
    DIMINISHING_RETURNS_THRESHOLD_DAYS,
    MIN_RISK_SCORE,
    MAX_RISK_SCORE,
)

logger = logging.getLogger(__name__)


class RangeComputation:
    """Computes range-based outputs using deterministic rules."""

    @staticmethod
    def compute_engagement_growth_range(
        baseline_engagement_trend: float,
        scenario: ScenarioInput,
    ) -> RangeValue:
        """
        Compute engagement growth range.
        
        Args:
            baseline_engagement_trend: Baseline engagement trend (0-100)
            scenario: The scenario
            
        Returns:
            Engagement growth range as percentage
        """
        # Start with baseline as a range
        base_range = RangeValue(
            min=baseline_engagement_trend * 0.8,
            max=baseline_engagement_trend * 1.2,
        )

        # Apply campaign budget multiplier
        budget_key = "medium"  # Default
        if scenario.campaign_strategy.budget_range["max"] < 5000:
            budget_key = "low"
        elif scenario.campaign_strategy.budget_range["max"] > 20000:
            budget_key = "high"

        budget_mult_min, budget_mult_max = CAMPAIGN_BUDGET_MULTIPLIERS[budget_key]
        base_range = apply_multiplier_to_range(base_range, budget_mult_min, budget_mult_max)

        # Apply content intensity multiplier
        intensity_key = scenario.campaign_strategy.content_intensity
        intensity_mult_min, intensity_mult_max = CONTENT_INTENSITY_MULTIPLIERS[intensity_key]
        base_range = apply_multiplier_to_range(base_range, intensity_mult_min, intensity_mult_max)

        # Apply engagement trend assumption modifier
        engagement_trend_key = scenario.assumptions.engagement_trend
        eng_mod_min, eng_mod_max = ENGAGEMENT_TREND_MODIFIERS[engagement_trend_key]
        base_range = apply_multiplier_to_range(base_range, eng_mod_min, eng_mod_max)

        # Apply creator participation modifier
        creator_part_key = scenario.assumptions.creator_participation
        creator_mod_min, creator_mod_max = CREATOR_PARTICIPATION_MODIFIERS[creator_part_key]
        base_range = apply_multiplier_to_range(base_range, creator_mod_min, creator_mod_max)

        # Apply market noise widening
        market_noise_key = scenario.assumptions.market_noise
        noise_widening = MARKET_NOISE_RANGE_WIDENING[market_noise_key]
        base_range = widen_range(base_range, noise_widening)

        # Clamp to reasonable bounds
        return RangeValue(
            min=clamp(base_range.min, 0, 200),
            max=clamp(base_range.max, 0, 300),
        )

    @staticmethod
    def compute_reach_growth_range(
        baseline_engagement_trend: float,
        scenario: ScenarioInput,
    ) -> RangeValue:
        """
        Compute reach growth range.
        
        Args:
            baseline_engagement_trend: Baseline engagement trend (0-100)
            scenario: The scenario
            
        Returns:
            Reach growth range as percentage
        """
        # Start with baseline
        base_range = RangeValue(
            min=baseline_engagement_trend * 0.6,
            max=baseline_engagement_trend * 1.4,
        )

        # Apply creator tier multiplier
        creator_tier_key = scenario.campaign_strategy.creator_tier
        tier_mult_min, tier_mult_max = CREATOR_TIER_REACH_MULTIPLIERS[creator_tier_key]
        base_range = apply_multiplier_to_range(base_range, tier_mult_min, tier_mult_max)

        # Apply campaign duration diminishing returns
        duration = scenario.campaign_strategy.campaign_duration_days
        if duration > DIMINISHING_RETURNS_THRESHOLD_DAYS:
            # Reduce upper bound for long campaigns
            diminishing_factor = 1.0 - ((duration - DIMINISHING_RETURNS_THRESHOLD_DAYS) / 365) * 0.3
            base_range = RangeValue(
                min=base_range.min,
                max=base_range.max * diminishing_factor,
            )

        # Apply peak stage saturation reduction
        if scenario.trend_context.lifecycle_stage == "peak":
            base_range = apply_multiplier_to_range(base_range, 0.7, 0.85)

        # Clamp to reasonable bounds
        return RangeValue(
            min=clamp(base_range.min, 0, 200),
            max=clamp(base_range.max, 0, 250),
        )

    @staticmethod
    def compute_creator_participation_change_range(
        scenario: ScenarioInput,
    ) -> RangeValue:
        """
        Compute creator participation change range.
        
        Args:
            scenario: The scenario
            
        Returns:
            Creator participation change range as percentage
        """
        # Base on creator participation assumption
        creator_part_key = scenario.assumptions.creator_participation
        creator_mod_min, creator_mod_max = CREATOR_PARTICIPATION_MODIFIERS[creator_part_key]

        # Scale by campaign intensity
        intensity_key = scenario.campaign_strategy.content_intensity
        intensity_mult_min, intensity_mult_max = CONTENT_INTENSITY_MULTIPLIERS[intensity_key]

        min_change = 10 * creator_mod_min * intensity_mult_min
        max_change = 30 * creator_mod_max * intensity_mult_max

        return RangeValue(
            min=clamp(min_change, -50, 100),
            max=clamp(max_change, -50, 150),
        )

    @staticmethod
    def compute_projected_risk_score(
        current_risk_score: float,
        scenario: ScenarioInput,
    ) -> RangeValue:
        """
        Compute projected risk score range.
        
        Args:
            current_risk_score: Current risk score (0-100)
            scenario: The scenario
            
        Returns:
            Projected risk score range
        """
        # Base on campaign type and lifecycle stage
        risk_adjustment = 0

        # Aggressive growth + peak = higher risk
        if (scenario.campaign_strategy.campaign_type == "short_term_influencer" and
            scenario.trend_context.lifecycle_stage == "peak"):
            risk_adjustment = 15

        # Sustainable engagement + growth = lower risk
        elif (scenario.campaign_strategy.campaign_type == "organic_only" and
              scenario.trend_context.lifecycle_stage == "growth"):
            risk_adjustment = -10

        # Decline/dormant stages increase risk
        if scenario.trend_context.lifecycle_stage in ["decline", "dormant"]:
            risk_adjustment += 20

        # Apply content intensity
        intensity_key = scenario.campaign_strategy.content_intensity
        if intensity_key == "high":
            risk_adjustment += 5
        elif intensity_key == "low":
            risk_adjustment -= 5

        # Compute range
        min_risk = clamp(current_risk_score + risk_adjustment - 5, MIN_RISK_SCORE, MAX_RISK_SCORE)
        max_risk = clamp(current_risk_score + risk_adjustment + 10, MIN_RISK_SCORE, MAX_RISK_SCORE)

        return RangeValue(min=min_risk, max=max_risk)

    @staticmethod
    def compute_risk_trend(
        current_risk_score: float,
        projected_risk_range: RangeValue,
    ) -> str:
        """
        Determine risk trend.
        
        Args:
            current_risk_score: Current risk score
            projected_risk_range: Projected risk score range
            
        Returns:
            Risk trend: "improving", "stable", or "worsening"
        """
        projected_midpoint = (projected_risk_range.min + projected_risk_range.max) / 2

        if projected_midpoint > current_risk_score + 2:
            return "worsening"
        elif projected_midpoint < current_risk_score - 2:
            return "improving"
        else:
            return "stable"
