"""Guardrails and system notes generation."""

import logging
from typing import List

from .types import ScenarioInput

logger = logging.getLogger(__name__)


class GuardrailsGenerator:
    """Generates guardrails and system notes."""

    @staticmethod
    def generate_system_note(
        data_coverage: float,
        scenario: ScenarioInput,
        missing_data_points: List[str],
        default_assumptions_applied: List[str],
    ) -> str:
        """
        Generate system note explaining limitations and assumptions.
        
        Args:
            data_coverage: Data coverage percentage
            scenario: The scenario
            missing_data_points: List of missing data points
            default_assumptions_applied: List of default assumptions applied
            
        Returns:
            System note string
        """
        notes: List[str] = []

        # Base note
        notes.append("This is a conditional simulation, not a guaranteed outcome.")

        # Low data coverage warning
        if data_coverage < 50:
            notes.append(
                f"Results are based on partial data ({data_coverage:.0f}% coverage). "
                "Ranges are widened to reflect increased uncertainty."
            )
            if missing_data_points:
                notes.append(f"Missing data points: {', '.join(missing_data_points)}")

        # Emerging/dormant stage note
        if scenario.trend_context.lifecycle_stage in ["emerging", "dormant"]:
            notes.append(
                f"Trend is in {scenario.trend_context.lifecycle_stage} stage with limited historical precedent. "
                "Projections are based on limited comparable data."
            )

        # Extreme budget note
        campaign_budget = scenario.campaign_strategy.budget_range.get("max", 10000)
        if campaign_budget < 1000 or campaign_budget > 100000:
            notes.append(
                f"Campaign budget ({campaign_budget}) is outside typical range. "
                "Extrapolation limits apply."
            )

        # Risk tolerance conflict
        if scenario.constraints.risk_tolerance == "low":
            notes.append(
                "Risk tolerance is set to 'low'. Review projected risk scores carefully."
            )

        # Default assumptions note
        if default_assumptions_applied:
            notes.append(
                f"Default assumptions applied for: {', '.join(default_assumptions_applied)}"
            )

        # High confidence note
        if scenario.trend_context.confidence == "high" and data_coverage >= 80:
            notes.append("High confidence in baseline data supports these projections.")

        return " ".join(notes)

    @staticmethod
    def identify_default_assumptions_applied(
        scenario: ScenarioInput,
    ) -> List[str]:
        """
        Identify which default assumptions were applied.
        
        Args:
            scenario: The scenario
            
        Returns:
            List of assumption names that used defaults
        """
        defaults_applied: List[str] = []

        # Note: In practice, this would check if user provided values
        # For now, we assume all are provided by the user
        # This would be enhanced when integrating with actual input handling

        return defaults_applied
