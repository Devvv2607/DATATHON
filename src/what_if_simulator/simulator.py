"""Core simulation orchestration."""

import logging
from typing import Union

from .types import (
    ScenarioInput,
    SimulationResponse,
    SimulationSummary,
    ExpectedGrowthMetrics,
    ExpectedROIMetrics,
    RiskProjection,
    DecisionInterpretation,
    AssumptionSensitivity,
    Guardrails,
    ErrorResponse,
)
from .validation import ScenarioValidator, apply_assumption_defaults
from .baseline_extraction import BaselineExtractor
from .range_computation import RangeComputation
from .roi_computation import ROIComputation
from .interpretation import Interpreter
from .sensitivity_analysis import SensitivityAnalyzer
from .guardrails import GuardrailsGenerator
from .explainability import ExecutiveSummaryGenerator
from .external_systems import ExternalSystemsClient
from .errors import ValidationException
from .utils import generate_scenario_id, widen_range

logger = logging.getLogger(__name__)


class WhatIfSimulator:
    """Main simulator orchestrating all components."""

    def __init__(self, external_systems: ExternalSystemsClient):
        """
        Initialize simulator.
        
        Args:
            external_systems: Client for accessing external systems
        """
        self.external_systems = external_systems
        self.baseline_extractor = BaselineExtractor(external_systems)
        self.roi_computation = ROIComputation(external_systems)

    def simulate(
        self,
        scenario: ScenarioInput,
        include_executive_summary: bool = True,
    ) -> Union[SimulationResponse, ErrorResponse]:
        """
        Execute complete simulation.
        
        Args:
            scenario: The scenario to simulate
            include_executive_summary: Whether to include executive summary
            
        Returns:
            SimulationResponse on success, ErrorResponse on failure
        """
        logger.info(f"Starting simulation for trend_id={scenario.trend_context.trend_id}")

        # Assign scenario ID if not provided
        if not scenario.scenario_id:
            scenario.scenario_id = generate_scenario_id()

        # Step 1: Validate scenario
        logger.info("Step 1: Validating scenario")
        is_valid, validation_failures = ScenarioValidator.validate(scenario)
        if not is_valid:
            logger.error(f"Validation failed with {len(validation_failures)} errors")
            error_response = ErrorResponse(
                error_code="VALIDATION_ERROR",
                error_message="Scenario validation failed",
                validation_failures=validation_failures,
            )
            return error_response

        # Apply assumption defaults
        apply_assumption_defaults(scenario.assumptions)

        # Step 2: Extract baseline
        logger.info("Step 2: Extracting baseline metrics")
        baseline = self.baseline_extractor.extract_baseline(scenario)

        # Adjust confidence based on data coverage
        adjusted_confidence = BaselineExtractor.adjust_confidence_for_data_coverage(
            scenario.trend_context.confidence,
            baseline["data_coverage"],
        )

        # Step 3: Compute ranges
        logger.info("Step 3: Computing output ranges")
        engagement_growth_range = RangeComputation.compute_engagement_growth_range(
            baseline["engagement_trend"] or 50,
            scenario,
        )
        reach_growth_range = RangeComputation.compute_reach_growth_range(
            baseline["engagement_trend"] or 50,
            scenario,
        )
        creator_participation_range = RangeComputation.compute_creator_participation_change_range(
            scenario
        )
        projected_risk_range = RangeComputation.compute_projected_risk_score(
            baseline["current_risk_score"],
            scenario,
        )

        # Apply range widening if needed
        if BaselineExtractor.should_widen_ranges(baseline["data_coverage"], adjusted_confidence):
            widening_factor = BaselineExtractor.get_range_widening_factor(
                baseline["data_coverage"],
                adjusted_confidence,
            )
            logger.info(f"Widening ranges by factor {widening_factor:.2f}")
            engagement_growth_range = widen_range(engagement_growth_range, widening_factor)
            reach_growth_range = widen_range(reach_growth_range, widening_factor)
            creator_participation_range = widen_range(creator_participation_range, widening_factor)
            projected_risk_range = widen_range(projected_risk_range, widening_factor)

        # Step 4: Compute ROI and probabilities
        logger.info("Step 4: Computing ROI and probabilities")
        roi_range = self.roi_computation.compute_roi_range(
            engagement_growth_range,
            reach_growth_range,
            scenario,
        )
        if not roi_range:
            logger.error("Failed to compute ROI range")
            return ErrorResponse(
                error_code="ROI_COMPUTATION_ERROR",
                error_message="Failed to compute ROI projections",
            )

        break_even_probability = ROIComputation.compute_break_even_probability(roi_range)
        loss_probability = ROIComputation.compute_loss_probability(roi_range)

        # Adjust probabilities for scenario
        break_even_probability, loss_probability = ROIComputation.adjust_probabilities_for_scenario(
            break_even_probability,
            loss_probability,
            scenario,
        )

        # Step 5: Determine risk trend
        logger.info("Step 5: Determining risk trend")
        risk_trend = RangeComputation.compute_risk_trend(
            baseline["current_risk_score"],
            projected_risk_range,
        )

        # Step 6: Sensitivity analysis
        logger.info("Step 6: Analyzing assumption sensitivity")
        most_sensitive_factor, impact_if_wrong = SensitivityAnalyzer.analyze_assumption_sensitivity(
            baseline["engagement_trend"] or 50,
            scenario,
        )

        # Step 7: Interpretation
        logger.info("Step 7: Interpreting results")
        recommended_posture = Interpreter.compute_recommended_posture(
            break_even_probability,
            loss_probability,
            risk_trend,
            scenario.trend_context.lifecycle_stage,
        )
        opportunities = Interpreter.identify_opportunities(
            engagement_growth_range,
            reach_growth_range,
            creator_participation_range,
            scenario,
        )
        risks = Interpreter.identify_risks(
            engagement_growth_range,
            reach_growth_range,
            loss_probability,
            risk_trend,
            scenario,
        )
        overall_outlook = Interpreter.compute_overall_outlook(
            break_even_probability,
            loss_probability,
            risk_trend,
        )

        # Step 8: Generate guardrails
        logger.info("Step 8: Generating guardrails")
        default_assumptions = GuardrailsGenerator.identify_default_assumptions_applied(scenario)
        system_note = GuardrailsGenerator.generate_system_note(
            baseline["data_coverage"],
            scenario,
            baseline["missing_data_points"],
            default_assumptions,
        )

        # Step 9: Assemble response
        logger.info("Step 9: Assembling response")
        response = SimulationResponse(
            scenario_id=scenario.scenario_id,
            trend_id=scenario.trend_context.trend_id,
            trend_name=scenario.trend_context.trend_name,
            simulation_summary=SimulationSummary(
                scenario_label=f"{scenario.trend_context.trend_name} - {scenario.campaign_strategy.campaign_type}",
                overall_outlook=overall_outlook,
                confidence=adjusted_confidence,
            ),
            expected_growth_metrics=ExpectedGrowthMetrics(
                engagement_growth_percent=engagement_growth_range,
                reach_growth_percent=reach_growth_range,
                creator_participation_change_percent=creator_participation_range,
            ),
            expected_roi_metrics=ExpectedROIMetrics(
                roi_percent=roi_range,
                break_even_probability=break_even_probability,
                loss_probability=loss_probability,
            ),
            risk_projection=RiskProjection(
                current_risk_score=baseline["current_risk_score"],
                projected_risk_score=projected_risk_range,
                risk_trend=risk_trend,
            ),
            decision_interpretation=DecisionInterpretation(
                recommended_posture=recommended_posture,
                primary_opportunities=opportunities,
                primary_risks=risks,
            ),
            assumption_sensitivity=AssumptionSensitivity(
                most_sensitive_factor=most_sensitive_factor,
                impact_if_wrong=impact_if_wrong,
            ),
            guardrails=Guardrails(
                data_coverage=baseline["data_coverage"],
                system_note=system_note,
            ),
        )

        logger.info(f"Simulation completed successfully for scenario_id={scenario.scenario_id}")
        
        # Add executive summary if requested
        if include_executive_summary:
            response.executive_summary = ExecutiveSummaryGenerator.generate_executive_summary(
                response, scenario
            )
        
        return response
