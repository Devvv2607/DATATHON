"""Interpretation component for translating ranges into recommendations."""

import logging
from typing import List, Tuple

from .types import ScenarioInput, RangeValue
from .constants import (
    BREAK_EVEN_AGGRESSIVE_THRESHOLD,
    BREAK_EVEN_MODERATE_MIN,
    BREAK_EVEN_MODERATE_MAX,
    BREAK_EVEN_CONSERVATIVE_THRESHOLD,
    LOSS_PROBABILITY_AVOID_THRESHOLD,
)

logger = logging.getLogger(__name__)


class Interpreter:
    """Interprets numeric ranges into strategic recommendations."""

    @staticmethod
    def compute_recommended_posture(
        break_even_probability: float,
        loss_probability: float,
        risk_trend: str,
        lifecycle_stage: str,
    ) -> str:
        """
        Compute recommended posture based on metrics.
        
        Args:
            break_even_probability: Break-even probability (0-100)
            loss_probability: Loss probability (0-100)
            risk_trend: Risk trend ("improving", "stable", "worsening")
            lifecycle_stage: Lifecycle stage
            
        Returns:
            Recommended posture: "scale", "test_small", "monitor", or "avoid"
        """
        # Avoid posture: decline/dormant with high loss probability
        if lifecycle_stage in ["decline", "dormant"] and loss_probability > LOSS_PROBABILITY_AVOID_THRESHOLD:
            return "avoid"

        # Scale posture: high break-even probability with stable/improving risk
        if (break_even_probability >= BREAK_EVEN_AGGRESSIVE_THRESHOLD and
            risk_trend in ["stable", "improving"]):
            return "scale"

        # Monitor posture: moderate break-even probability with stable risk
        if (BREAK_EVEN_MODERATE_MIN <= break_even_probability <= BREAK_EVEN_MODERATE_MAX and
            risk_trend == "stable"):
            return "monitor"

        # Test_small posture: low break-even probability or worsening risk
        if (break_even_probability < BREAK_EVEN_CONSERVATIVE_THRESHOLD or
            risk_trend == "worsening"):
            return "test_small"

        # Default to monitor
        return "monitor"

    @staticmethod
    def identify_opportunities(
        engagement_growth_range: RangeValue,
        reach_growth_range: RangeValue,
        creator_participation_change_range: RangeValue,
        scenario: ScenarioInput,
    ) -> List[str]:
        """
        Identify primary opportunities.
        
        Args:
            engagement_growth_range: Engagement growth range
            reach_growth_range: Reach growth range
            creator_participation_change_range: Creator participation change range
            scenario: The scenario
            
        Returns:
            List of opportunity descriptions
        """
        opportunities: List[str] = []

        # High engagement growth potential
        if engagement_growth_range.max > 50:
            opportunities.append("High engagement growth potential")

        # High reach growth potential
        if reach_growth_range.max > 40:
            opportunities.append("Significant audience expansion opportunity")

        # Creator participation growth
        if creator_participation_change_range.max > 20:
            opportunities.append("Strong creator participation growth potential")

        # Early stage trends
        if scenario.trend_context.lifecycle_stage == "emerging":
            opportunities.append("Early-stage trend positioning advantage")

        # Growth stage trends
        if scenario.trend_context.lifecycle_stage == "growth":
            opportunities.append("Momentum in growth phase")

        # Low risk score
        if scenario.trend_context.current_risk_score < 30:
            opportunities.append("Low volatility environment")

        # Macro/mega creator tiers
        if scenario.campaign_strategy.creator_tier in ["macro", "mega"]:
            opportunities.append("High-reach creator network available")

        # Ensure at least one opportunity
        if not opportunities:
            opportunities.append("Baseline growth opportunity")

        return opportunities

    @staticmethod
    def identify_risks(
        engagement_growth_range: RangeValue,
        reach_growth_range: RangeValue,
        loss_probability: float,
        risk_trend: str,
        scenario: ScenarioInput,
    ) -> List[str]:
        """
        Identify primary risks.
        
        Args:
            engagement_growth_range: Engagement growth range
            reach_growth_range: Reach growth range
            loss_probability: Loss probability
            risk_trend: Risk trend
            scenario: The scenario
            
        Returns:
            List of risk descriptions
        """
        risks: List[str] = []

        # Low engagement growth potential
        if engagement_growth_range.max < 20:
            risks.append("Limited engagement growth potential")

        # Low reach growth potential
        if reach_growth_range.max < 15:
            risks.append("Constrained audience expansion")

        # High loss probability
        if loss_probability > 60:
            risks.append("High probability of financial loss")

        # Worsening risk trend
        if risk_trend == "worsening":
            risks.append("Risk trajectory deteriorating")

        # Decline/dormant stages
        if scenario.trend_context.lifecycle_stage in ["decline", "dormant"]:
            risks.append("Trend in late lifecycle stage")

        # High current risk score
        if scenario.trend_context.current_risk_score > 70:
            risks.append("High trend volatility")

        # Nano/micro creator tiers
        if scenario.campaign_strategy.creator_tier in ["nano", "micro"]:
            risks.append("Limited creator reach capacity")

        # Long campaign duration
        if scenario.campaign_strategy.campaign_duration_days > 180:
            risks.append("Extended campaign duration increases uncertainty")

        # Ensure at least one risk
        if not risks:
            risks.append("Baseline execution risk")

        return risks

    @staticmethod
    def compute_overall_outlook(
        break_even_probability: float,
        loss_probability: float,
        risk_trend: str,
    ) -> str:
        """
        Compute overall outlook.
        
        Args:
            break_even_probability: Break-even probability
            loss_probability: Loss probability
            risk_trend: Risk trend
            
        Returns:
            Overall outlook: "favorable", "risky", or "unfavorable"
        """
        if break_even_probability >= 70 and risk_trend in ["stable", "improving"]:
            return "favorable"
        elif loss_probability > 60 or risk_trend == "worsening":
            return "unfavorable"
        else:
            return "risky"

    @staticmethod
    def compute_confidence_level(
        data_coverage: float,
        original_confidence: str,
    ) -> str:
        """
        Compute confidence level for output.
        
        Args:
            data_coverage: Data coverage percentage
            original_confidence: Original confidence level
            
        Returns:
            Confidence level: "low", "medium", or "high"
        """
        if data_coverage < 50:
            return "low"
        elif data_coverage < 75:
            return "medium" if original_confidence != "high" else "medium"
        else:
            return original_confidence
