"""Validation component for scenario inputs."""

from typing import List, Tuple
import logging

from .types import ScenarioInput, ValidationFailure
from .constants import (
    LIFECYCLE_STAGES,
    CAMPAIGN_TYPES,
    CREATOR_TIERS,
    CONFIDENCE_LEVELS,
    RISK_TOLERANCE_LEVELS,
    ENGAGEMENT_TRENDS,
    CREATOR_PARTICIPATION,
    MARKET_NOISE,
    CONTENT_INTENSITY,
    COMPATIBILITY_MATRIX,
    DEFAULT_ASSUMPTIONS,
)
from .errors import ValidationException

logger = logging.getLogger(__name__)


class ScenarioValidator:
    """Validates scenario inputs against predefined rules."""

    @staticmethod
    def validate(scenario: ScenarioInput) -> Tuple[bool, List[ValidationFailure]]:
        """
        Validate a scenario input.
        
        Args:
            scenario: The scenario to validate
            
        Returns:
            Tuple of (is_valid, list of failures)
        """
        failures: List[ValidationFailure] = []

        # Validate trend context
        failures.extend(ScenarioValidator._validate_trend_context(scenario.trend_context))

        # Validate campaign strategy
        failures.extend(
            ScenarioValidator._validate_campaign_strategy(scenario.campaign_strategy)
        )

        # Validate assumptions
        failures.extend(ScenarioValidator._validate_assumptions(scenario.assumptions))

        # Validate constraints
        failures.extend(ScenarioValidator._validate_constraints(scenario.constraints))

        # Validate lifecycle-campaign compatibility
        failures.extend(
            ScenarioValidator._validate_compatibility(
                scenario.trend_context.lifecycle_stage,
                scenario.campaign_strategy.campaign_type,
            )
        )

        # Validate budget constraint
        failures.extend(
            ScenarioValidator._validate_budget_constraint(
                scenario.campaign_strategy.budget_range,
                scenario.constraints.max_budget_cap,
            )
        )

        is_valid = len(failures) == 0
        return is_valid, failures

    @staticmethod
    def _validate_trend_context(trend_context) -> List[ValidationFailure]:
        """Validate trend context fields."""
        failures: List[ValidationFailure] = []

        if not trend_context.trend_id or not isinstance(trend_context.trend_id, str):
            failures.append(
                ValidationFailure(
                    field="trend_context.trend_id",
                    message="trend_id must be a non-empty string",
                    guidance="Provide a valid trend identifier",
                )
            )

        if not trend_context.trend_name or not isinstance(trend_context.trend_name, str):
            failures.append(
                ValidationFailure(
                    field="trend_context.trend_name",
                    message="trend_name must be a non-empty string",
                    guidance="Provide a descriptive trend name",
                )
            )

        if trend_context.lifecycle_stage not in LIFECYCLE_STAGES:
            failures.append(
                ValidationFailure(
                    field="trend_context.lifecycle_stage",
                    message=f"lifecycle_stage must be one of {LIFECYCLE_STAGES}",
                    guidance=f"Valid values: {', '.join(sorted(LIFECYCLE_STAGES))}",
                )
            )

        if not (0 <= trend_context.current_risk_score <= 100):
            failures.append(
                ValidationFailure(
                    field="trend_context.current_risk_score",
                    message="current_risk_score must be between 0 and 100",
                    guidance="Provide a risk score as a percentage (0-100)",
                )
            )

        if trend_context.confidence not in CONFIDENCE_LEVELS:
            failures.append(
                ValidationFailure(
                    field="trend_context.confidence",
                    message=f"confidence must be one of {CONFIDENCE_LEVELS}",
                    guidance=f"Valid values: {', '.join(sorted(CONFIDENCE_LEVELS))}",
                )
            )

        return failures

    @staticmethod
    def _validate_campaign_strategy(campaign_strategy) -> List[ValidationFailure]:
        """Validate campaign strategy fields."""
        failures: List[ValidationFailure] = []

        if campaign_strategy.campaign_type not in CAMPAIGN_TYPES:
            failures.append(
                ValidationFailure(
                    field="campaign_strategy.campaign_type",
                    message=f"campaign_type must be one of {CAMPAIGN_TYPES}",
                    guidance=f"Valid values: {', '.join(sorted(CAMPAIGN_TYPES))}",
                )
            )

        if not isinstance(campaign_strategy.budget_range, dict):
            failures.append(
                ValidationFailure(
                    field="campaign_strategy.budget_range",
                    message="budget_range must be a dict with 'min' and 'max' keys",
                    guidance="Provide budget_range as {'min': float, 'max': float}",
                )
            )
        else:
            if "min" not in campaign_strategy.budget_range or "max" not in campaign_strategy.budget_range:
                failures.append(
                    ValidationFailure(
                        field="campaign_strategy.budget_range",
                        message="budget_range must have 'min' and 'max' keys",
                        guidance="Provide budget_range as {'min': float, 'max': float}",
                    )
                )
            elif campaign_strategy.budget_range["min"] > campaign_strategy.budget_range["max"]:
                failures.append(
                    ValidationFailure(
                        field="campaign_strategy.budget_range",
                        message="budget_range min must be <= max",
                        guidance="Ensure min <= max in budget_range",
                    )
                )

        if campaign_strategy.campaign_duration_days <= 0:
            failures.append(
                ValidationFailure(
                    field="campaign_strategy.campaign_duration_days",
                    message="campaign_duration_days must be positive",
                    guidance="Provide a positive number of days",
                )
            )

        if campaign_strategy.creator_tier not in CREATOR_TIERS:
            failures.append(
                ValidationFailure(
                    field="campaign_strategy.creator_tier",
                    message=f"creator_tier must be one of {CREATOR_TIERS}",
                    guidance=f"Valid values: {', '.join(sorted(CREATOR_TIERS))}",
                )
            )

        if campaign_strategy.content_intensity not in CONTENT_INTENSITY:
            failures.append(
                ValidationFailure(
                    field="campaign_strategy.content_intensity",
                    message=f"content_intensity must be one of {CONTENT_INTENSITY}",
                    guidance=f"Valid values: {', '.join(sorted(CONTENT_INTENSITY))}",
                )
            )

        return failures

    @staticmethod
    def _validate_assumptions(assumptions) -> List[ValidationFailure]:
        """Validate assumptions fields."""
        failures: List[ValidationFailure] = []

        if assumptions.engagement_trend not in ENGAGEMENT_TRENDS:
            failures.append(
                ValidationFailure(
                    field="assumptions.engagement_trend",
                    message=f"engagement_trend must be one of {ENGAGEMENT_TRENDS}",
                    guidance=f"Valid values: {', '.join(sorted(ENGAGEMENT_TRENDS))}",
                )
            )

        if assumptions.creator_participation not in CREATOR_PARTICIPATION:
            failures.append(
                ValidationFailure(
                    field="assumptions.creator_participation",
                    message=f"creator_participation must be one of {CREATOR_PARTICIPATION}",
                    guidance=f"Valid values: {', '.join(sorted(CREATOR_PARTICIPATION))}",
                )
            )

        if assumptions.market_noise not in MARKET_NOISE:
            failures.append(
                ValidationFailure(
                    field="assumptions.market_noise",
                    message=f"market_noise must be one of {MARKET_NOISE}",
                    guidance=f"Valid values: {', '.join(sorted(MARKET_NOISE))}",
                )
            )

        return failures

    @staticmethod
    def _validate_constraints(constraints) -> List[ValidationFailure]:
        """Validate constraints fields."""
        failures: List[ValidationFailure] = []

        if constraints.risk_tolerance not in RISK_TOLERANCE_LEVELS:
            failures.append(
                ValidationFailure(
                    field="constraints.risk_tolerance",
                    message=f"risk_tolerance must be one of {RISK_TOLERANCE_LEVELS}",
                    guidance=f"Valid values: {', '.join(sorted(RISK_TOLERANCE_LEVELS))}",
                )
            )

        if constraints.max_budget_cap <= 0:
            failures.append(
                ValidationFailure(
                    field="constraints.max_budget_cap",
                    message="max_budget_cap must be positive",
                    guidance="Provide a positive budget cap",
                )
            )

        return failures

    @staticmethod
    def _validate_compatibility(
        lifecycle_stage: str,
        campaign_type: str,
    ) -> List[ValidationFailure]:
        """Validate lifecycle-campaign type compatibility."""
        failures: List[ValidationFailure] = []

        key = (lifecycle_stage, campaign_type)
        if key in COMPATIBILITY_MATRIX:
            is_compatible, is_high_risk = COMPATIBILITY_MATRIX[key]
            if not is_compatible:
                failures.append(
                    ValidationFailure(
                        field="compatibility",
                        message=f"Campaign type '{campaign_type}' is not compatible with lifecycle stage '{lifecycle_stage}'",
                        guidance=f"Consider using a different campaign type for the {lifecycle_stage} stage",
                    )
                )
            elif is_high_risk:
                logger.warning(
                    f"High-risk combination: {lifecycle_stage} + {campaign_type}. "
                    "User should acknowledge this risk."
                )

        return failures

    @staticmethod
    def _validate_budget_constraint(
        budget_range: dict,
        max_budget_cap: float,
    ) -> List[ValidationFailure]:
        """Validate budget constraint."""
        failures: List[ValidationFailure] = []

        if "max" in budget_range and budget_range["max"] > max_budget_cap:
            failures.append(
                ValidationFailure(
                    field="budget_constraint",
                    message=f"Budget range max ({budget_range['max']}) exceeds max_budget_cap ({max_budget_cap})",
                    guidance=f"Reduce budget_range.max to be <= {max_budget_cap}",
                )
            )

        return failures


def apply_assumption_defaults(assumptions) -> None:
    """
    Apply default assumptions to missing values.
    
    Args:
        assumptions: The assumptions object to update (modified in place)
    """
    if assumptions.engagement_trend is None:
        assumptions.engagement_trend = DEFAULT_ASSUMPTIONS["engagement_trend"]
        logger.info(f"Applied default engagement_trend: {assumptions.engagement_trend}")

    if assumptions.creator_participation is None:
        assumptions.creator_participation = DEFAULT_ASSUMPTIONS["creator_participation"]
        logger.info(f"Applied default creator_participation: {assumptions.creator_participation}")

    if assumptions.market_noise is None:
        assumptions.market_noise = DEFAULT_ASSUMPTIONS["market_noise"]
        logger.info(f"Applied default market_noise: {assumptions.market_noise}")
