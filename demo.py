"""Demo script showcasing the What-If Trend Adoption Simulator."""

import sys
import json
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
from what_if_simulator.explainability import format_executive_summary


def format_result(result):
    """Format simulation result for display."""
    output = []
    output.append("\n" + "="*80)
    output.append("WHAT-IF TREND ADOPTION SIMULATOR - RESULTS")
    output.append("="*80)
    
    output.append(f"\nScenario ID: {result.scenario_id}")
    output.append(f"Trend: {result.trend_name}")
    
    output.append("\n--- SIMULATION SUMMARY ---")
    output.append(f"Overall Outlook: {result.simulation_summary.overall_outlook.upper()}")
    output.append(f"Confidence: {result.simulation_summary.confidence}")
    output.append(f"Scenario Label: {result.simulation_summary.scenario_label}")
    
    output.append("\n--- EXPECTED GROWTH METRICS ---")
    eng = result.expected_growth_metrics.engagement_growth_percent
    output.append(f"Engagement Growth: {eng.min:.1f}% to {eng.max:.1f}%")
    reach = result.expected_growth_metrics.reach_growth_percent
    output.append(f"Reach Growth: {reach.min:.1f}% to {reach.max:.1f}%")
    creator = result.expected_growth_metrics.creator_participation_change_percent
    output.append(f"Creator Participation Change: {creator.min:.1f}% to {creator.max:.1f}%")
    
    output.append("\n--- EXPECTED ROI METRICS ---")
    roi = result.expected_roi_metrics.roi_percent
    output.append(f"ROI Range: {roi.min:.1f}% to {roi.max:.1f}%")
    output.append(f"Break-Even Probability: {result.expected_roi_metrics.break_even_probability:.1f}%")
    output.append(f"Loss Probability: {result.expected_roi_metrics.loss_probability:.1f}%")
    
    output.append("\n--- RISK PROJECTION ---")
    output.append(f"Current Risk Score: {result.risk_projection.current_risk_score:.1f}")
    proj = result.risk_projection.projected_risk_score
    output.append(f"Projected Risk Score: {proj.min:.1f} to {proj.max:.1f}")
    output.append(f"Risk Trend: {result.risk_projection.risk_trend.upper()}")
    
    output.append("\n--- DECISION INTERPRETATION ---")
    output.append(f"Recommended Posture: {result.decision_interpretation.recommended_posture.upper()}")
    output.append("\nPrimary Opportunities:")
    for opp in result.decision_interpretation.primary_opportunities:
        output.append(f"  • {opp}")
    output.append("\nPrimary Risks:")
    for risk in result.decision_interpretation.primary_risks:
        output.append(f"  • {risk}")
    
    output.append("\n--- ASSUMPTION SENSITIVITY ---")
    output.append(f"Most Sensitive Factor: {result.assumption_sensitivity.most_sensitive_factor}")
    output.append(f"Impact If Wrong: {result.assumption_sensitivity.impact_if_wrong.upper()}")
    
    output.append("\n--- GUARDRAILS ---")
    output.append(f"Data Coverage: {result.guardrails.data_coverage:.1f}%")
    output.append(f"System Note: {result.guardrails.system_note}")
    
    output.append("\n" + "="*80)
    
    return "\n".join(output)


def run_demo():
    """Run demonstration scenarios."""
    # Create external systems client
    external_systems = ExternalSystemsClient(
        trend_lifecycle_engine=MockTrendLifecycleEngine(),
        early_decline_detection=MockEarlyDeclineDetection(),
        roi_attribution=MockROIAttribution(),
    )

    # Create simulator
    simulator = WhatIfSimulator(external_systems)

    # Scenario 1: Aggressive Growth Strategy on Growing Trend
    print("\n" + "="*80)
    print("SCENARIO 1: Aggressive Growth Strategy on Growing Trend")
    print("="*80)
    
    scenario1 = ScenarioInput(
        trend_context=TrendContext(
            trend_id="trend_001",
            trend_name="TikTok Dance Challenge",
            platform="tiktok",
            lifecycle_stage="growth",
            current_risk_score=35.0,
            confidence="high",
        ),
        campaign_strategy=CampaignStrategy(
            campaign_type="short_term_influencer",
            budget_range={"min": 10000, "max": 25000},
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

    result1 = simulator.simulate(scenario1)
    print(format_result(result1))
    if result1.executive_summary:
        print(format_executive_summary(result1.executive_summary))

    # Scenario 2: Conservative Strategy on Declining Trend
    print("\n" + "="*80)
    print("SCENARIO 2: Conservative Strategy on Declining Trend")
    print("="*80)
    
    scenario2 = ScenarioInput(
        trend_context=TrendContext(
            trend_id="trend_002",
            trend_name="Outdated Meme Format",
            platform="instagram",
            lifecycle_stage="decline",
            current_risk_score=75.0,
            confidence="medium",
        ),
        campaign_strategy=CampaignStrategy(
            campaign_type="organic_only",
            budget_range={"min": 2000, "max": 5000},
            campaign_duration_days=14,
            creator_tier="nano",
            content_intensity="low",
        ),
        assumptions=Assumptions(
            engagement_trend="pessimistic",
            creator_participation="declining",
            market_noise="high",
        ),
        constraints=Constraints(
            risk_tolerance="low",
            max_budget_cap=10000,
        ),
    )

    result2 = simulator.simulate(scenario2)
    print(format_result(result2))
    if result2.executive_summary:
        print(format_executive_summary(result2.executive_summary))

    # Scenario 3: Balanced Strategy on Peak Trend
    print("\n" + "="*80)
    print("SCENARIO 3: Balanced Strategy on Peak Trend")
    print("="*80)
    
    scenario3 = ScenarioInput(
        trend_context=TrendContext(
            trend_id="trend_003",
            trend_name="Viral Challenge at Peak",
            platform="youtube",
            lifecycle_stage="peak",
            current_risk_score=55.0,
            confidence="high",
        ),
        campaign_strategy=CampaignStrategy(
            campaign_type="mixed",
            budget_range={"min": 15000, "max": 40000},
            campaign_duration_days=60,
            creator_tier="macro",
            content_intensity="medium",
        ),
        assumptions=Assumptions(
            engagement_trend="neutral",
            creator_participation="stable",
            market_noise="medium",
        ),
        constraints=Constraints(
            risk_tolerance="medium",
            max_budget_cap=75000,
        ),
    )

    result3 = simulator.simulate(scenario3)
    print(format_result(result3))
    if result3.executive_summary:
        print(format_executive_summary(result3.executive_summary))

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\nScenario 1 (Aggressive Growth):")
    print(f"  Posture: {result1.decision_interpretation.recommended_posture}")
    print(f"  Outlook: {result1.simulation_summary.overall_outlook}")
    print(f"  Break-Even Probability: {result1.expected_roi_metrics.break_even_probability:.1f}%")
    
    print("\nScenario 2 (Conservative Decline):")
    print(f"  Posture: {result2.decision_interpretation.recommended_posture}")
    print(f"  Outlook: {result2.simulation_summary.overall_outlook}")
    print(f"  Break-Even Probability: {result2.expected_roi_metrics.break_even_probability:.1f}%")
    
    print("\nScenario 3 (Balanced Peak):")
    print(f"  Posture: {result3.decision_interpretation.recommended_posture}")
    print(f"  Outlook: {result3.simulation_summary.overall_outlook}")
    print(f"  Break-Even Probability: {result3.expected_roi_metrics.break_even_probability:.1f}%")
    
    print("\n" + "="*80)
    print("✓ Demo completed successfully!")
    print("="*80 + "\n")


if __name__ == "__main__":
    run_demo()
