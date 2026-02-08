"""Sensitivity analysis component for identifying assumption impact."""

import logging
from typing import Dict, Tuple

from .types import ScenarioInput, RangeValue
from .range_computation import RangeComputation
from .utils import get_range_width

logger = logging.getLogger(__name__)


class SensitivityAnalyzer:
    """Analyzes sensitivity of outputs to assumption changes."""

    @staticmethod
    def analyze_assumption_sensitivity(
        baseline_engagement_trend: float,
        scenario: ScenarioInput,
    ) -> Tuple[str, str]:
        """
        Analyze which assumption has the greatest impact on outputs.
        
        Args:
            baseline_engagement_trend: Baseline engagement trend
            scenario: The scenario
            
        Returns:
            Tuple of (most_sensitive_factor, impact_if_wrong)
        """
        # Compute baseline ranges
        baseline_engagement = RangeComputation.compute_engagement_growth_range(
            baseline_engagement_trend, scenario
        )
        baseline_reach = RangeComputation.compute_reach_growth_range(
            baseline_engagement_trend, scenario
        )

        # Vary each assumption and measure impact
        sensitivity_scores: Dict[str, float] = {}

        # Test engagement_trend sensitivity
        engagement_trend_impact = SensitivityAnalyzer._test_engagement_trend_sensitivity(
            baseline_engagement_trend, scenario
        )
        sensitivity_scores["engagement_trend"] = engagement_trend_impact

        # Test creator_participation sensitivity
        creator_participation_impact = SensitivityAnalyzer._test_creator_participation_sensitivity(
            baseline_engagement_trend, scenario
        )
        sensitivity_scores["creator_participation"] = creator_participation_impact

        # Test market_noise sensitivity
        market_noise_impact = SensitivityAnalyzer._test_market_noise_sensitivity(
            baseline_engagement_trend, scenario
        )
        sensitivity_scores["market_noise"] = market_noise_impact

        # Find most sensitive factor
        most_sensitive = max(sensitivity_scores, key=sensitivity_scores.get)
        impact_magnitude = sensitivity_scores[most_sensitive]

        # Determine impact level
        if impact_magnitude > 30:
            impact_level = "high"
        elif impact_magnitude > 15:
            impact_level = "medium"
        else:
            impact_level = "low"

        logger.info(
            f"Most sensitive factor: {most_sensitive} (impact: {impact_level}, "
            f"magnitude: {impact_magnitude:.1f}%)"
        )

        return most_sensitive, impact_level

    @staticmethod
    def _test_engagement_trend_sensitivity(
        baseline_engagement_trend: float,
        scenario: ScenarioInput,
    ) -> float:
        """Test sensitivity to engagement_trend assumption."""
        # Compute range with current assumption
        current_range = RangeComputation.compute_engagement_growth_range(
            baseline_engagement_trend, scenario
        )
        current_width = get_range_width(current_range)

        # Compute range with opposite assumption
        original_assumption = scenario.assumptions.engagement_trend
        if original_assumption == "optimistic":
            scenario.assumptions.engagement_trend = "pessimistic"
        elif original_assumption == "pessimistic":
            scenario.assumptions.engagement_trend = "optimistic"
        else:
            scenario.assumptions.engagement_trend = "optimistic"

        opposite_range = RangeComputation.compute_engagement_growth_range(
            baseline_engagement_trend, scenario
        )
        opposite_width = get_range_width(opposite_range)

        # Restore original
        scenario.assumptions.engagement_trend = original_assumption

        # Calculate impact as percentage change in range width
        impact = abs(opposite_width - current_width) / current_width * 100 if current_width > 0 else 0
        return impact

    @staticmethod
    def _test_creator_participation_sensitivity(
        baseline_engagement_trend: float,
        scenario: ScenarioInput,
    ) -> float:
        """Test sensitivity to creator_participation assumption."""
        # Compute range with current assumption
        current_range = RangeComputation.compute_engagement_growth_range(
            baseline_engagement_trend, scenario
        )
        current_width = get_range_width(current_range)

        # Compute range with opposite assumption
        original_assumption = scenario.assumptions.creator_participation
        if original_assumption == "increasing":
            scenario.assumptions.creator_participation = "declining"
        elif original_assumption == "declining":
            scenario.assumptions.creator_participation = "increasing"
        else:
            scenario.assumptions.creator_participation = "increasing"

        opposite_range = RangeComputation.compute_engagement_growth_range(
            baseline_engagement_trend, scenario
        )
        opposite_width = get_range_width(opposite_range)

        # Restore original
        scenario.assumptions.creator_participation = original_assumption

        # Calculate impact
        impact = abs(opposite_width - current_width) / current_width * 100 if current_width > 0 else 0
        return impact

    @staticmethod
    def _test_market_noise_sensitivity(
        baseline_engagement_trend: float,
        scenario: ScenarioInput,
    ) -> float:
        """Test sensitivity to market_noise assumption."""
        # Compute range with current assumption
        current_range = RangeComputation.compute_engagement_growth_range(
            baseline_engagement_trend, scenario
        )
        current_width = get_range_width(current_range)

        # Compute range with opposite assumption
        original_assumption = scenario.assumptions.market_noise
        if original_assumption == "low":
            scenario.assumptions.market_noise = "high"
        elif original_assumption == "high":
            scenario.assumptions.market_noise = "low"
        else:
            scenario.assumptions.market_noise = "high"

        opposite_range = RangeComputation.compute_engagement_growth_range(
            baseline_engagement_trend, scenario
        )
        opposite_width = get_range_width(opposite_range)

        # Restore original
        scenario.assumptions.market_noise = original_assumption

        # Calculate impact
        impact = abs(opposite_width - current_width) / current_width * 100 if current_width > 0 else 0
        return impact
