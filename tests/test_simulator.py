"""Basic tests for the What-If Trend Adoption Simulator."""

import sys
sys.path.insert(0, 'src')

from what_if_simulator.types import (
    ScenarioInput,
    TrendContext,
    CampaignStrategy,
    Assumptions,
    Constraints,
)
from what_if_simulator.external_systems import (
    MockTrendLifecycleEngine,
    MockEarlyDeclineDetection,
    MockROIAttribution,
    ExternalSystemsClient,
)
from what_if_simulator.simulator import WhatIfSimulator


def test_basic_simulation():
    """Test basic simulation flow."""
    # Create mock external systems
    external_systems = ExternalSystemsClient(
        trend_lifecycle_engine=MockTrendLifecycleEngine(),
        early_decline_detection=MockEarlyDeclineDetection(),
        roi_attribution=MockROIAttribution(),
    )

    # Create simulator
    simulator = WhatIfSimulator(external_systems)

    # Create test scenario
    scenario = ScenarioInput(
        trend_context=TrendContext(
            trend_id="trend_123",
            trend_name="TikTok Dance Challenge",
            platform="tiktok",
            lifecycle_stage="growth",
            current_risk_score=45.0,
            confidence="medium",
        ),
        campaign_strategy=CampaignStrategy(
            campaign_type="short_term_influencer",
            budget_range={"min": 5000, "max": 15000},
            campaign_duration_days=30,
            creator_tier="macro",
            content_intensity="high",
        ),
        assumptions=Assumptions(
            engagement_trend="optimistic",
            creator_participation="increasing",
            market_noise="low",
        ),
        constraints=Constraints(
            risk_tolerance="medium",
            max_budget_cap=50000,
        ),
    )

    # Run simulation
    result = simulator.simulate(scenario)

    # Verify result structure
    assert hasattr(result, "scenario_id")
    assert hasattr(result, "trend_id")
    assert hasattr(result, "simulation_summary")
    assert hasattr(result, "expected_growth_metrics")
    assert hasattr(result, "expected_roi_metrics")
    assert hasattr(result, "risk_projection")
    assert hasattr(result, "decision_interpretation")
    assert hasattr(result, "assumption_sensitivity")
    assert hasattr(result, "guardrails")

    # Verify output values are in expected ranges
    assert 0 <= result.expected_growth_metrics.engagement_growth_percent.min <= 300
    assert 0 <= result.expected_growth_metrics.engagement_growth_percent.max <= 300
    assert result.expected_growth_metrics.engagement_growth_percent.min <= result.expected_growth_metrics.engagement_growth_percent.max

    assert 0 <= result.expected_roi_metrics.break_even_probability <= 100
    assert 0 <= result.expected_roi_metrics.loss_probability <= 100

    assert 0 <= result.risk_projection.current_risk_score <= 100
    assert 0 <= result.risk_projection.projected_risk_score.min <= 100
    assert 0 <= result.risk_projection.projected_risk_score.max <= 100

    assert result.decision_interpretation.recommended_posture in ["scale", "test_small", "monitor", "avoid"]
    assert len(result.decision_interpretation.primary_opportunities) > 0
    assert len(result.decision_interpretation.primary_risks) > 0

    assert result.assumption_sensitivity.most_sensitive_factor in ["engagement_trend", "creator_participation", "market_noise"]
    assert result.assumption_sensitivity.impact_if_wrong in ["low", "medium", "high"]

    assert 0 <= result.guardrails.data_coverage <= 100
    assert len(result.guardrails.system_note) > 0

    print("✓ Basic simulation test passed")
    print(f"  Scenario ID: {result.scenario_id}")
    print(f"  Overall Outlook: {result.simulation_summary.overall_outlook}")
    print(f"  Recommended Posture: {result.decision_interpretation.recommended_posture}")
    print(f"  Break-Even Probability: {result.expected_roi_metrics.break_even_probability:.1f}%")
    print(f"  Data Coverage: {result.guardrails.data_coverage:.1f}%")


def test_validation_error():
    """Test validation error handling."""
    external_systems = ExternalSystemsClient(
        trend_lifecycle_engine=MockTrendLifecycleEngine(),
        early_decline_detection=MockEarlyDeclineDetection(),
        roi_attribution=MockROIAttribution(),
    )

    simulator = WhatIfSimulator(external_systems)

    # Create invalid scenario (budget exceeds cap)
    scenario = ScenarioInput(
        trend_context=TrendContext(
            trend_id="trend_123",
            trend_name="Test Trend",
            platform="tiktok",
            lifecycle_stage="growth",
            current_risk_score=45.0,
            confidence="medium",
        ),
        campaign_strategy=CampaignStrategy(
            campaign_type="short_term_influencer",
            budget_range={"min": 5000, "max": 100000},  # Exceeds max_budget_cap
            campaign_duration_days=30,
            creator_tier="macro",
            content_intensity="high",
        ),
        assumptions=Assumptions(),
        constraints=Constraints(
            risk_tolerance="medium",
            max_budget_cap=50000,  # Budget exceeds this
        ),
    )

    result = simulator.simulate(scenario)

    # Verify error response
    assert hasattr(result, "error_code")
    assert result.error_code == "VALIDATION_ERROR"
    assert len(result.validation_failures) > 0

    print("✓ Validation error test passed")
    print(f"  Error: {result.error_message}")
    print(f"  Failures: {len(result.validation_failures)}")


if __name__ == "__main__":
    test_basic_simulation()
    test_validation_error()
    print("\n✓ All tests passed!")
