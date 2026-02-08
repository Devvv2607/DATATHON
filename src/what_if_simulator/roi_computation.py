"""ROI and probability computation component."""

import logging
from typing import Optional

from .types import RangeValue, ScenarioInput, ROIAttributionResponse
from .external_systems import ExternalSystemsClient
from .utils import calculate_probability_from_range, clamp

logger = logging.getLogger(__name__)


class ROIComputation:
    """Computes ROI ranges and probabilities."""

    def __init__(self, external_systems: ExternalSystemsClient):
        """
        Initialize ROI computation.
        
        Args:
            external_systems: Client for accessing external systems
        """
        self.external_systems = external_systems

    def compute_roi_range(
        self,
        engagement_growth_range: RangeValue,
        reach_growth_range: RangeValue,
        scenario: ScenarioInput,
    ) -> Optional[RangeValue]:
        """
        Compute ROI range using ROI Attribution system.
        
        Args:
            engagement_growth_range: Engagement growth range
            reach_growth_range: Reach growth range
            scenario: The scenario
            
        Returns:
            ROI range as percentage, or None if unavailable
        """
        campaign_budget = scenario.campaign_strategy.budget_range.get("max", 10000)
        campaign_duration = scenario.campaign_strategy.campaign_duration_days

        roi_response = self.external_systems.get_roi_projection(
            engagement_growth_range,
            reach_growth_range,
            campaign_budget,
            campaign_duration,
        )

        if roi_response:
            roi_range = roi_response.roi_percent_range
            logger.info(f"ROI range: {roi_range.min:.1f}% to {roi_range.max:.1f}%")
            return roi_range

        # Fallback: compute simple ROI estimate
        logger.warning("ROI Attribution unavailable, using fallback computation")
        return self._compute_roi_fallback(
            engagement_growth_range,
            reach_growth_range,
            campaign_budget,
        )

    @staticmethod
    def _compute_roi_fallback(
        engagement_growth_range: RangeValue,
        reach_growth_range: RangeValue,
        campaign_budget: float,
    ) -> RangeValue:
        """
        Fallback ROI computation when external system unavailable.
        
        Args:
            engagement_growth_range: Engagement growth range
            reach_growth_range: Reach growth range
            campaign_budget: Campaign budget
            
        Returns:
            ROI range as percentage
        """
        # Simple model: average engagement and reach growth, scale by budget efficiency
        avg_engagement = (engagement_growth_range.min + engagement_growth_range.max) / 2
        avg_reach = (reach_growth_range.min + reach_growth_range.max) / 2
        avg_growth = (avg_engagement + avg_reach) / 2

        # Budget efficiency: assume $1000 budget generates 10% ROI baseline
        budget_efficiency = (campaign_budget / 1000) * 0.1
        roi_min = avg_growth * 0.5 - budget_efficiency - 15
        roi_max = avg_growth * 1.2 - budget_efficiency + 10

        return RangeValue(min=roi_min, max=roi_max)

    @staticmethod
    def compute_break_even_probability(roi_range: RangeValue) -> float:
        """
        Compute break-even probability (likelihood that ROI >= 0).
        
        Args:
            roi_range: ROI range
            
        Returns:
            Probability as percentage (0-100)
        """
        probability = calculate_probability_from_range(roi_range, threshold=0, above_threshold=True)
        return clamp(probability, 0, 100)

    @staticmethod
    def compute_loss_probability(roi_range: RangeValue) -> float:
        """
        Compute loss probability (likelihood that ROI < 0).
        
        Args:
            roi_range: ROI range
            
        Returns:
            Probability as percentage (0-100)
        """
        probability = calculate_probability_from_range(roi_range, threshold=0, above_threshold=False)
        return clamp(probability, 0, 100)

    @staticmethod
    def adjust_probabilities_for_scenario(
        break_even_probability: float,
        loss_probability: float,
        scenario: ScenarioInput,
    ) -> tuple[float, float]:
        """
        Adjust probabilities based on scenario characteristics.
        
        Args:
            break_even_probability: Initial break-even probability
            loss_probability: Initial loss probability
            scenario: The scenario
            
        Returns:
            Tuple of (adjusted_break_even, adjusted_loss)
        """
        # High budget relative to baseline reduces break-even probability
        campaign_budget = scenario.campaign_strategy.budget_range.get("max", 10000)
        if campaign_budget > 50000:
            break_even_probability *= 0.85
            loss_probability *= 1.15

        # Decline/dormant stages increase loss probability
        if scenario.trend_context.lifecycle_stage in ["decline", "dormant"]:
            loss_probability = min(loss_probability * 1.3, 100)
            break_even_probability = max(break_even_probability * 0.7, 0)

        # Ensure complementarity (approximately)
        if abs(break_even_probability + loss_probability - 100) > 5:
            # Normalize to ensure they sum to 100
            total = break_even_probability + loss_probability
            if total > 0:
                break_even_probability = (break_even_probability / total) * 100
                loss_probability = (loss_probability / total) * 100

        return clamp(break_even_probability, 0, 100), clamp(loss_probability, 0, 100)
