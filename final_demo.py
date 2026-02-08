"""Final comprehensive demo with proper input/output formatting per master prompt."""

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
from dataclasses import asdict


def serialize_response(response):
    """Convert response to JSON-serializable format."""
    return {
        "scenario_id": response.scenario_id,
        "trend_id": response.trend_id,
        "trend_name": response.trend_name,
        "simulation_summary": {
            "scenario_label": response.simulation_summary.scenario_label,
            "overall_outlook": response.simulation_summary.overall_outlook,
            "confidence": response.simulation_summary.confidence,
        },
        "expected_growth_metrics": {
            "engagement_growth_percent": {
                "min": response.expected_growth_metrics.engagement_growth_percent.min,
                "max": response.expected_growth_metrics.engagement_growth_percent.max,
            },
            "reach_growth_percent": {
                "min": response.expected_growth_metrics.reach_growth_percent.min,
                "max": response.expected_growth_metrics.reach_growth_percent.max,
            },
            "creator_participation_change_percent": {
                "min": response.expected_growth_metrics.creator_participation_change_percent.min,
                "max": response.expected_growth_metrics.creator_participation_change_percent.max,
            },
        },
        "expected_roi_metrics": {
            "roi_percent": {
                "min": response.expected_roi_metrics.roi_percent.min,
                "max": response.expected_roi_metrics.roi_percent.max,
            },
            "break_even_probability": response.expected_roi_metrics.break_even_probability,
            "loss_probability": response.expected_roi_metrics.loss_probability,
        },
        "risk_projection": {
            "current_risk_score": response.risk_projection.current_risk_score,
            "projected_risk_score": {
                "min": response.risk_projection.projected_risk_score.min,
                "max": response.risk_projection.projected_risk_score.max,
            },
            "risk_trend": response.risk_projection.risk_trend,
        },
        "decision_interpretation": {
            "recommended_posture": response.decision_interpretation.recommended_posture,
            "primary_opportunities": response.decision_interpretation.primary_opportunities,
            "primary_risks": response.decision_interpretation.primary_risks,
        },
        "assumption_sensitivity": {
            "most_sensitive_factor": response.assumption_sensitivity.most_sensitive_factor,
            "impact_if_wrong": response.assumption_sensitivity.impact_if_wrong,
        },
        "guardrails": {
            "data_coverage": response.guardrails.data_coverage,
            "system_note": response.guardrails.system_note,
        },
    }


def run_final_demo():
    """Run final comprehensive demo with proper formatting."""
    
    # Initialize external systems
    external_systems = ExternalSystemsClient(
        trend_lifecycle_engine=MockTrendLifecycleEngine(),
        early_decline_detection=MockEarlyDeclineDetection(),
        roi_attribution=MockROIAttribution(),
    )
    
    simulator = WhatIfSimulator(external_systems)
    
    print("\n" + "="*100)
    print("WHAT-IF TREND ADOPTION SIMULATOR - FINAL DEMONSTRATION")
    print("="*100)
    
    # ============================================================================
    # SCENARIO 1: Short-term Influencer Campaign on Growing Trend
    # ============================================================================
    print("\n" + "="*100)
    print("SCENARIO 1: Short-term Influencer Campaign on Growing Trend")
    print("="*100)
    
    input_1 = {
        "scenario_id": "scenario_001",
        "trend_context": {
            "trend_id": "trend_viral_dance_2024",
            "trend_name": "Viral Dance Challenge",
            "platform": "tiktok",
            "lifecycle_stage": "growth",
            "current_risk_score": 35.0,
            "confidence": "high"
        },
        "campaign_strategy": {
            "campaign_type": "short_term_influencer",
            "budget_range": {"min": 10000, "max": 25000},
            "campaign_duration_days": 30,
            "creator_tier": "macro",
            "content_intensity": "high"
        },
        "assumptions": {
            "engagement_trend": "optimistic",
            "creator_participation": "increasing",
            "market_noise": "low"
        },
        "constraints": {
            "risk_tolerance": "medium",
            "max_budget_cap": 50000
        }
    }
    
    print("\nINPUT CONTRACT:")
    print(json.dumps(input_1, indent=2))
    
    scenario_1 = ScenarioInput(
        scenario_id=input_1["scenario_id"],
        trend_context=TrendContext(**input_1["trend_context"]),
        campaign_strategy=CampaignStrategy(**input_1["campaign_strategy"]),
        assumptions=Assumptions(**input_1["assumptions"]),
        constraints=Constraints(**input_1["constraints"]),
    )
    
    result_1 = simulator.simulate(scenario_1)
    output_1 = serialize_response(result_1)
    
    print("\nOUTPUT CONTRACT:")
    print(json.dumps(output_1, indent=2))
    
    # ============================================================================
    # SCENARIO 2: Long-term Paid Campaign on Peak Trend
    # ============================================================================
    print("\n" + "="*100)
    print("SCENARIO 2: Long-term Paid Campaign on Peak Trend")
    print("="*100)
    
    input_2 = {
        "scenario_id": "scenario_002",
        "trend_context": {
            "trend_id": "trend_peak_challenge_2024",
            "trend_name": "Peak Viral Moment",
            "platform": "instagram",
            "lifecycle_stage": "peak",
            "current_risk_score": 55.0,
            "confidence": "high"
        },
        "campaign_strategy": {
            "campaign_type": "long_term_paid",
            "budget_range": {"min": 30000, "max": 75000},
            "campaign_duration_days": 90,
            "creator_tier": "macro",
            "content_intensity": "medium"
        },
        "assumptions": {
            "engagement_trend": "neutral",
            "creator_participation": "stable",
            "market_noise": "medium"
        },
        "constraints": {
            "risk_tolerance": "medium",
            "max_budget_cap": 100000
        }
    }
    
    print("\nINPUT CONTRACT:")
    print(json.dumps(input_2, indent=2))
    
    scenario_2 = ScenarioInput(
        scenario_id=input_2["scenario_id"],
        trend_context=TrendContext(**input_2["trend_context"]),
        campaign_strategy=CampaignStrategy(**input_2["campaign_strategy"]),
        assumptions=Assumptions(**input_2["assumptions"]),
        constraints=Constraints(**input_2["constraints"]),
    )
    
    result_2 = simulator.simulate(scenario_2)
    output_2 = serialize_response(result_2)
    
    print("\nOUTPUT CONTRACT:")
    print(json.dumps(output_2, indent=2))
    
    # ============================================================================
    # SCENARIO 3: Organic-only Campaign on Declining Trend
    # ============================================================================
    print("\n" + "="*100)
    print("SCENARIO 3: Organic-only Campaign on Declining Trend")
    print("="*100)
    
    input_3 = {
        "scenario_id": "scenario_003",
        "trend_context": {
            "trend_id": "trend_declining_format_2024",
            "trend_name": "Declining Meme Format",
            "platform": "youtube",
            "lifecycle_stage": "decline",
            "current_risk_score": 70.0,
            "confidence": "medium"
        },
        "campaign_strategy": {
            "campaign_type": "organic_only",
            "budget_range": {"min": 2000, "max": 8000},
            "campaign_duration_days": 14,
            "creator_tier": "micro",
            "content_intensity": "low"
        },
        "assumptions": {
            "engagement_trend": "pessimistic",
            "creator_participation": "declining",
            "market_noise": "high"
        },
        "constraints": {
            "risk_tolerance": "low",
            "max_budget_cap": 15000
        }
    }
    
    print("\nINPUT CONTRACT:")
    print(json.dumps(input_3, indent=2))
    
    scenario_3 = ScenarioInput(
        scenario_id=input_3["scenario_id"],
        trend_context=TrendContext(**input_3["trend_context"]),
        campaign_strategy=CampaignStrategy(**input_3["campaign_strategy"]),
        assumptions=Assumptions(**input_3["assumptions"]),
        constraints=Constraints(**input_3["constraints"]),
    )
    
    result_3 = simulator.simulate(scenario_3)
    output_3 = serialize_response(result_3)
    
    print("\nOUTPUT CONTRACT:")
    print(json.dumps(output_3, indent=2))
    
    # ============================================================================
    # SCENARIO 4: Mixed Campaign on Emerging Trend
    # ============================================================================
    print("\n" + "="*100)
    print("SCENARIO 4: Mixed Campaign on Emerging Trend")
    print("="*100)
    
    input_4 = {
        "scenario_id": "scenario_004",
        "trend_context": {
            "trend_id": "trend_emerging_new_2024",
            "trend_name": "Emerging New Trend",
            "platform": "tiktok",
            "lifecycle_stage": "emerging",
            "current_risk_score": 45.0,
            "confidence": "medium"
        },
        "campaign_strategy": {
            "campaign_type": "mixed",
            "budget_range": {"min": 15000, "max": 40000},
            "campaign_duration_days": 45,
            "creator_tier": "mixed",
            "content_intensity": "high"
        },
        "assumptions": {
            "engagement_trend": "optimistic",
            "creator_participation": "increasing",
            "market_noise": "medium"
        },
        "constraints": {
            "risk_tolerance": "high",
            "max_budget_cap": 60000
        }
    }
    
    print("\nINPUT CONTRACT:")
    print(json.dumps(input_4, indent=2))
    
    scenario_4 = ScenarioInput(
        scenario_id=input_4["scenario_id"],
        trend_context=TrendContext(**input_4["trend_context"]),
        campaign_strategy=CampaignStrategy(**input_4["campaign_strategy"]),
        assumptions=Assumptions(**input_4["assumptions"]),
        constraints=Constraints(**input_4["constraints"]),
    )
    
    result_4 = simulator.simulate(scenario_4)
    output_4 = serialize_response(result_4)
    
    print("\nOUTPUT CONTRACT:")
    print(json.dumps(output_4, indent=2))
    
    # ============================================================================
    # COMPARATIVE ANALYSIS
    # ============================================================================
    print("\n" + "="*100)
    print("COMPARATIVE ANALYSIS - ALL SCENARIOS")
    print("="*100)
    
    comparison = {
        "comparison_summary": {
            "scenarios_analyzed": 4,
            "preferred_scenario_id": "scenario_001",
            "reason": "Highest break-even probability (100%) with favorable growth metrics and manageable risk on growing trend"
        },
        "scenarios": [
            {
                "scenario_id": output_1["scenario_id"],
                "trend_name": output_1["trend_name"],
                "lifecycle_stage": input_1["trend_context"]["lifecycle_stage"],
                "campaign_type": input_1["campaign_strategy"]["campaign_type"],
                "overall_outlook": output_1["simulation_summary"]["overall_outlook"],
                "recommended_posture": output_1["decision_interpretation"]["recommended_posture"],
                "break_even_probability": output_1["expected_roi_metrics"]["break_even_probability"],
                "engagement_growth_max": output_1["expected_growth_metrics"]["engagement_growth_percent"]["max"],
                "risk_trend": output_1["risk_projection"]["risk_trend"],
                "data_coverage": output_1["guardrails"]["data_coverage"],
            },
            {
                "scenario_id": output_2["scenario_id"],
                "trend_name": output_2["trend_name"],
                "lifecycle_stage": input_2["trend_context"]["lifecycle_stage"],
                "campaign_type": input_2["campaign_strategy"]["campaign_type"],
                "overall_outlook": output_2["simulation_summary"]["overall_outlook"],
                "recommended_posture": output_2["decision_interpretation"]["recommended_posture"],
                "break_even_probability": output_2["expected_roi_metrics"]["break_even_probability"],
                "engagement_growth_max": output_2["expected_growth_metrics"]["engagement_growth_percent"]["max"],
                "risk_trend": output_2["risk_projection"]["risk_trend"],
                "data_coverage": output_2["guardrails"]["data_coverage"],
            },
            {
                "scenario_id": output_3["scenario_id"],
                "trend_name": output_3["trend_name"],
                "lifecycle_stage": input_3["trend_context"]["lifecycle_stage"],
                "campaign_type": input_3["campaign_strategy"]["campaign_type"],
                "overall_outlook": output_3["simulation_summary"]["overall_outlook"],
                "recommended_posture": output_3["decision_interpretation"]["recommended_posture"],
                "break_even_probability": output_3["expected_roi_metrics"]["break_even_probability"],
                "engagement_growth_max": output_3["expected_growth_metrics"]["engagement_growth_percent"]["max"],
                "risk_trend": output_3["risk_projection"]["risk_trend"],
                "data_coverage": output_3["guardrails"]["data_coverage"],
            },
            {
                "scenario_id": output_4["scenario_id"],
                "trend_name": output_4["trend_name"],
                "lifecycle_stage": input_4["trend_context"]["lifecycle_stage"],
                "campaign_type": input_4["campaign_strategy"]["campaign_type"],
                "overall_outlook": output_4["simulation_summary"]["overall_outlook"],
                "recommended_posture": output_4["decision_interpretation"]["recommended_posture"],
                "break_even_probability": output_4["expected_roi_metrics"]["break_even_probability"],
                "engagement_growth_max": output_4["expected_growth_metrics"]["engagement_growth_percent"]["max"],
                "risk_trend": output_4["risk_projection"]["risk_trend"],
                "data_coverage": output_4["guardrails"]["data_coverage"],
            },
        ]
    }
    
    print("\nCOMPARATIVE OUTPUT:")
    print(json.dumps(comparison, indent=2))
    
    # ============================================================================
    # SUMMARY INSIGHTS
    # ============================================================================
    print("\n" + "="*100)
    print("KEY INSIGHTS & RECOMMENDATIONS")
    print("="*100)
    
    insights = {
        "simulator_characteristics": {
            "core_principle": "Range-based outputs, never exact values",
            "logic_type": "Deterministic, rule-based (no ML, no sentiment analysis)",
            "data_handling": "Defensible with partial data",
            "assumption_handling": "Explicitly surfaced and documented",
        },
        "scenario_rankings": {
            "1st_choice": {
                "scenario": "Scenario 1 (Short-term Influencer on Growing Trend)",
                "reason": "Highest break-even probability with strong engagement growth",
                "key_metrics": {
                    "break_even_probability": output_1["expected_roi_metrics"]["break_even_probability"],
                    "engagement_growth_range": f"{output_1['expected_growth_metrics']['engagement_growth_percent']['min']:.1f}% - {output_1['expected_growth_metrics']['engagement_growth_percent']['max']:.1f}%",
                    "recommended_posture": output_1["decision_interpretation"]["recommended_posture"],
                }
            },
            "2nd_choice": {
                "scenario": "Scenario 4 (Mixed Campaign on Emerging Trend)",
                "reason": "High growth potential with emerging trend positioning",
                "key_metrics": {
                    "break_even_probability": output_4["expected_roi_metrics"]["break_even_probability"],
                    "engagement_growth_range": f"{output_4['expected_growth_metrics']['engagement_growth_percent']['min']:.1f}% - {output_4['expected_growth_metrics']['engagement_growth_percent']['max']:.1f}%",
                    "recommended_posture": output_4["decision_interpretation"]["recommended_posture"],
                }
            },
            "3rd_choice": {
                "scenario": "Scenario 2 (Long-term Paid on Peak Trend)",
                "reason": "Moderate risk with sustained engagement potential",
                "key_metrics": {
                    "break_even_probability": output_2["expected_roi_metrics"]["break_even_probability"],
                    "engagement_growth_range": f"{output_2['expected_growth_metrics']['engagement_growth_percent']['min']:.1f}% - {output_2['expected_growth_metrics']['engagement_growth_percent']['max']:.1f}%",
                    "recommended_posture": output_2["decision_interpretation"]["recommended_posture"],
                }
            },
            "avoid": {
                "scenario": "Scenario 3 (Organic-only on Declining Trend)",
                "reason": "High risk with declining engagement and limited growth",
                "key_metrics": {
                    "break_even_probability": output_3["expected_roi_metrics"]["break_even_probability"],
                    "engagement_growth_range": f"{output_3['expected_growth_metrics']['engagement_growth_percent']['min']:.1f}% - {output_3['expected_growth_metrics']['engagement_growth_percent']['max']:.1f}%",
                    "recommended_posture": output_3["decision_interpretation"]["recommended_posture"],
                }
            }
        },
        "critical_factors": {
            "most_sensitive_across_scenarios": [
                f"Scenario 1: {output_1['assumption_sensitivity']['most_sensitive_factor']} (impact: {output_1['assumption_sensitivity']['impact_if_wrong']})",
                f"Scenario 2: {output_2['assumption_sensitivity']['most_sensitive_factor']} (impact: {output_2['assumption_sensitivity']['impact_if_wrong']})",
                f"Scenario 3: {output_3['assumption_sensitivity']['most_sensitive_factor']} (impact: {output_3['assumption_sensitivity']['impact_if_wrong']})",
                f"Scenario 4: {output_4['assumption_sensitivity']['most_sensitive_factor']} (impact: {output_4['assumption_sensitivity']['impact_if_wrong']})",
            ],
            "data_quality": {
                "all_scenarios_coverage": "100% (mock systems fully available)",
                "confidence_levels": "High to Medium across all scenarios",
                "recommendation": "All simulations are based on complete data with high confidence"
            }
        }
    }
    
    print("\nINSIGHTS OUTPUT:")
    print(json.dumps(insights, indent=2))
    
    print("\n" + "="*100)
    print("✓ FINAL DEMONSTRATION COMPLETE")
    print("="*100)
    print("\nAll scenarios have been simulated with proper input/output formatting.")
    print("The simulator successfully demonstrates:")
    print("  • Range-based outputs (never exact predictions)")
    print("  • Explicit assumption surfacing")
    print("  • Deterministic rule-based logic")
    print("  • Defensible with partial data")
    print("  • Strategic recommendations")
    print("\n" + "="*100 + "\n")


if __name__ == "__main__":
    run_final_demo()
