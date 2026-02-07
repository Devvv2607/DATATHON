"""
Test Suite - Explainable AI Engine (Feature #3)
Tests gold-standard explanation generation for decline scenarios
"""

import sys
import os
from datetime import datetime

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))

from explainer import generate_explanation, explain_multiple_trends

# ============================================================================
# TEST 1: Scenario 2 - Sharp Collapse (Orange Alert)
# ============================================================================

def test_scenario_2_sharp_collapse():
    """Test explanation for sharp engagement collapse"""
    print("\n" + "="*80)
    print("TEST 1: Feature #3 - Sharp Collapse Explanation (Gold-Standard)")
    print("="*80)
    
    # Mock Feature #2 output
    feature2_output = {
        "trend_id": "trend_abc_123",
        "trend_name": "#BeautyTok Challenge",
        "decline_risk_score": 67.5,
        "alert_level": "orange",
        "lifecycle_stage": 3,
        "stage_name": "Plateau",
        "confidence": "high",
        "data_quality": "complete",
        "signal_breakdown": {
            "engagement_drop": 72,
            "velocity_decline": 65,
            "creator_decline": 58,
            "quality_decline": 45
        },
        "historical_risk_scores": [
            {"date": "2026-02-05", "risk": 42.0},
            {"date": "2026-02-06", "risk": 55.2},
            {"date": "2026-02-07", "risk": 67.5}
        ],
        "data_completeness": {
            "available_days": 7,
            "expected_days": 7
        }
    }
    
    analysis_date = "2026-02-07T14:30:00Z"
    
    explanation = generate_explanation(feature2_output, analysis_date)
    
    print(f"\n📋 TREND: {explanation['trend_name']} (ID: {explanation['trend_id']})")
    print(f"📅 ANALYSIS DATE: {explanation['analysis_date']}")
    print(f"📊 RISK SCORE: {explanation['risk_score']}/100 [{explanation['alert_level'].upper()}]")
    print(f"🎬 LIFECYCLE STAGE: {explanation['stage_name']}")
    print(f"🎯 CONFIDENCE: {explanation['confidence'].upper()}")
    
    print(f"\n📌 DECISION SUMMARY:")
    print(f"   Status: {explanation['decision_summary']['status']}")
    print(f"   Message: {explanation['decision_summary']['message']}")
    
    print(f"\n📊 SIGNAL CONTRIBUTIONS (Top 3):")
    for contrib in explanation['signal_contributions']:
        print(f"   - {contrib['signal']}: {contrib['signal_score']}/100")
        print(f"     Impact: {contrib['impact_on_risk']} points on risk")
        print(f"     Reason: {contrib['reason']}")
    
    print(f"\n📈 DECISION DELTA (Temporal Change):")
    print(f"   Previous Risk: {explanation['decision_delta']['previous_risk_score']}")
    print(f"   Current Risk: {explanation['decision_delta']['current_risk_score']}")
    print(f"   Change: {explanation['decision_delta']['primary_change']}")
    
    print(f"\n❓ COUNTERFACTUALS (What-If Scenarios):")
    if explanation['counterfactuals']['risk_reduction_scenarios']:
        print(f"   Risk Reduction:")
        for scenario in explanation['counterfactuals']['risk_reduction_scenarios']:
            print(f"   - {scenario}")
    if explanation['counterfactuals']['risk_escalation_scenarios']:
        print(f"   Risk Escalation:")
        for scenario in explanation['counterfactuals']['risk_escalation_scenarios']:
            print(f"   - {scenario}")
    
    # Assertions
    assert 'decision_summary' in explanation, "Missing decision_summary"
    assert 'status' in explanation['decision_summary'], "Missing status in decision_summary"
    assert 'message' in explanation['decision_summary'], "Missing message in decision_summary"
    assert len(explanation['signal_contributions']) >= 3, "Expected at least 3 signal contributions"
    assert 'previous_risk_score' in explanation['decision_delta'], "Missing previous_risk_score"
    assert 'counterfactuals' in explanation, "Missing counterfactuals"
    assert explanation['alert_level'] == 'orange', "Expected orange alert"
    assert explanation['risk_score'] == 67.5, "Risk score should match input"
    assert explanation['confidence'] in ['high', 'medium', 'low'], "Invalid confidence level"
    
    print("\n✅ TEST PASSED\n")
    return True


# ============================================================================
# TEST 2: Scenario 5 - Catastrophic Collapse (Red Alert)
# ============================================================================

def test_scenario_5_catastrophic():
    """Test explanation for catastrophic multi-signal decline"""
    print("\n" + "="*80)
    print("TEST 2: Feature #3 - Catastrophic Collapse Explanation (Gold-Standard)")
    print("="*80)
    
    # Mock Feature #2 output
    feature2_output = {
        "trend_id": "trend_xyz_789",
        "trend_name": "#DanceChallenge 2026",
        "decline_risk_score": 89.3,
        "alert_level": "red",
        "lifecycle_stage": 2,
        "stage_name": "Viral",
        "confidence": "high",
        "data_quality": "complete",
        "signal_breakdown": {
            "engagement_drop": 95,
            "velocity_decline": 88,
            "creator_decline": 76,
            "quality_decline": 82
        },
        "historical_risk_scores": [
            {"date": "2026-02-05", "risk": 35.0},
            {"date": "2026-02-06", "risk": 62.1},
            {"date": "2026-02-07", "risk": 89.3}
        ],
        "data_completeness": {
            "available_days": 7,
            "expected_days": 7
        }
    }
    
    analysis_date = "2026-02-07T16:45:00Z"
    
    explanation = generate_explanation(feature2_output, analysis_date)
    
    print(f"\n📋 TREND: {explanation['trend_name']} (ID: {explanation['trend_id']})")
    print(f"📅 ANALYSIS DATE: {explanation['analysis_date']}")
    print(f"📊 RISK SCORE: {explanation['risk_score']}/100 [{explanation['alert_level'].upper()}]")
    print(f"🎬 LIFECYCLE STAGE: {explanation['stage_name']}")
    print(f"🎯 CONFIDENCE: {explanation['confidence'].upper()}")
    
    print(f"\n📌 DECISION SUMMARY:")
    print(f"   Status: {explanation['decision_summary']['status']}")
    print(f"   Message: {explanation['decision_summary']['message']}")
    
    print(f"\n📊 SIGNAL CONTRIBUTIONS (Top 3):")
    for contrib in explanation['signal_contributions']:
        print(f"   - {contrib['signal']}: {contrib['signal_score']}/100")
        print(f"     Impact: {contrib['impact_on_risk']} points")
    
    # Assertions
    assert 'decision_summary' in explanation, "Missing decision_summary"
    assert explanation['decision_summary']['status'] == 'critical', "Should indicate critical status"
    assert len(explanation['signal_contributions']) >= 3, "Expected at least 3 signal contributions"
    assert explanation['alert_level'] == 'red', "Expected red alert"
    assert explanation['risk_score'] == 89.3, "Risk score should match input"
    assert explanation['confidence'] in ['high', 'medium', 'low'], "Invalid confidence level"
    
    print("\n✅ TEST PASSED\n")
    return True


# ============================================================================
# TEST 3: Healthy Viral Growth (Green Alert)
# ============================================================================

def test_scenario_1_healthy_viral():
    """Test explanation for healthy viral trend"""
    print("\n" + "="*80)
    print("TEST 3: Feature #3 - Healthy Viral Growth Explanation (Gold-Standard)")
    print("="*80)
    
    # Mock Feature #2 output
    feature2_output = {
        "trend_id": "trend_healthy_001",
        "trend_name": "#ViralDance Trend",
        "decline_risk_score": 18.5,
        "alert_level": "green",
        "lifecycle_stage": 2,
        "stage_name": "Viral",
        "confidence": "high",
        "data_quality": "complete",
        "signal_breakdown": {
            "engagement_drop": 5,
            "velocity_decline": 8,
            "creator_decline": 12,
            "quality_decline": 15
        },
        "historical_risk_scores": [
            {"date": "2026-02-05", "risk": 15.0},
            {"date": "2026-02-06", "risk": 17.2},
            {"date": "2026-02-07", "risk": 18.5}
        ],
        "data_completeness": {
            "available_days": 7,
            "expected_days": 7
        }
    }
    
    analysis_date = "2026-02-07T10:15:00Z"
    
    explanation = generate_explanation(feature2_output, analysis_date)
    
    print(f"\n📋 TREND: {explanation['trend_name']} (ID: {explanation['trend_id']})")
    print(f"📅 ANALYSIS DATE: {explanation['analysis_date']}")
    print(f"📊 RISK SCORE: {explanation['risk_score']}/100 [{explanation['alert_level'].upper()}]")
    print(f"🎬 LIFECYCLE STAGE: {explanation['stage_name']}")
    print(f"🎯 CONFIDENCE: {explanation['confidence'].upper()}")
    
    print(f"\n📌 DECISION SUMMARY:")
    print(f"   Status: {explanation['decision_summary']['status']}")
    print(f"   Message: {explanation['decision_summary']['message']}")
    
    print(f"\n📊 SIGNAL CONTRIBUTIONS (Top 3):")
    for contrib in explanation['signal_contributions']:
        print(f"   - {contrib['signal']}: {contrib['signal_score']}/100")
    
    # Assertions
    assert 'decision_summary' in explanation, "Missing decision_summary"
    assert explanation['decision_summary']['status'] == 'healthy', "Should indicate healthy status"
    assert len(explanation['signal_contributions']) >= 3, "Expected at least 3 signal contributions"
    assert explanation['alert_level'] == 'green', "Expected green alert"
    assert explanation['risk_score'] == 18.5, "Risk score should match input"
    assert explanation['confidence'] in ['high', 'medium', 'low'], "Invalid confidence level"
    
    print("\n✅ TEST PASSED\n")
    return True


# ============================================================================
# TEST 4: Batch Explanations
# ============================================================================

def test_batch_explanations():
    """Test generating explanations for multiple trends"""
    print("\n" + "="*80)
    print("TEST 4: Feature #3 - Batch Explanations (Gold-Standard)")
    print("="*80)
    
    # Mock multiple Feature #2 outputs
    feature2_outputs = [
        {
            "trend_id": "trend_001",
            "trend_name": "Trend A",
            "decline_risk_score": 45.2,
            "alert_level": "yellow",
            "lifecycle_stage": 3,
            "stage_name": "Plateau",
            "confidence": "high",
            "data_quality": "complete",
            "signal_breakdown": {
                "engagement_drop": 35,
                "velocity_decline": 42,
                "creator_decline": 28,
                "quality_decline": 20
            },
            "historical_risk_scores": [
                {"date": "2026-02-05", "risk": 30.0},
                {"date": "2026-02-06", "risk": 38.1},
            ],
            "data_completeness": {"available_days": 6, "expected_days": 7}
        },
        {
            "trend_id": "trend_002",
            "trend_name": "Trend B",
            "decline_risk_score": 75.8,
            "alert_level": "orange",
            "lifecycle_stage": 3,
            "stage_name": "Plateau",
            "confidence": "high",
            "data_quality": "complete",
            "signal_breakdown": {
                "engagement_drop": 68,
                "velocity_decline": 72,
                "creator_decline": 65,
                "quality_decline": 58
            },
            "historical_risk_scores": [
                {"date": "2026-02-05", "risk": 45.0},
                {"date": "2026-02-06", "risk": 60.2},
            ],
            "data_completeness": {"available_days": 7, "expected_days": 7}
        },
        {
            "trend_id": "trend_003",
            "trend_name": "Trend C",
            "decline_risk_score": 12.3,
            "alert_level": "green",
            "lifecycle_stage": 2,
            "stage_name": "Viral",
            "confidence": "high",
            "data_quality": "complete",
            "signal_breakdown": {
                "engagement_drop": 8,
                "velocity_decline": 10,
                "creator_decline": 6,
                "quality_decline": 5
            },
            "historical_risk_scores": [
                {"date": "2026-02-05", "risk": 10.0},
                {"date": "2026-02-06", "risk": 11.5},
            ],
            "data_completeness": {"available_days": 7, "expected_days": 7}
        }
    ]
    
    analysis_date = "2026-02-07T12:00:00Z"
    
    explanations = explain_multiple_trends(feature2_outputs, analysis_date)
    
    print(f"\n📊 Generated explanations for {len(explanations)} trends:")
    
    for idx, explanation in enumerate(explanations, 1):
        print(f"\n--- TREND {idx}: {explanation['trend_name']} ---")
        print(f"Risk: {explanation['risk_score']}/100 [{explanation['alert_level'].upper()}]")
        print(f"Decision Status: {explanation['decision_summary']['status']}")
        print(f"Top Signals: {', '.join([c['signal'] for c in explanation['signal_contributions'][:2]])}")
    
    # Assertions
    assert len(explanations) == 3, "Expected 3 explanations"
    assert all('decision_summary' in e for e in explanations), "All should have decision_summary"
    assert all('signal_contributions' in e for e in explanations), "All should have signal_contributions"
    assert explanations[0]['alert_level'] == 'yellow', "Trend 1 should be yellow"
    assert explanations[1]['alert_level'] == 'orange', "Trend 2 should be orange"
    assert explanations[2]['alert_level'] == 'green', "Trend 3 should be green"
    
    print("\n✅ TEST PASSED\n")
    return True


# ============================================================================
# TEST 5: Lifecycle-Stage Aware Context
# ============================================================================

def test_lifecycle_context():
    """Test that explanations vary based on lifecycle stage"""
    print("\n" + "="*80)
    print("TEST 5: Feature #3 - Lifecycle-Stage Context Awareness (Gold-Standard)")
    print("="*80)
    
    # Same signal breakdown, different lifecycle stages
    same_signals = {
        "engagement_drop": 45,
        "velocity_decline": 42,
        "creator_decline": 40,
        "quality_decline": 38
    }
    
    historical = [
        {"date": "2026-02-05", "risk": 38.0},
        {"date": "2026-02-06", "risk": 39.8},
    ]
    
    data_completeness = {
        "available_days": 7,
        "expected_days": 7
    }
    
    stages = [
        (1, "Emerging"),
        (2, "Viral"),
        (3, "Plateau"),
        (4, "Decline"),
        (5, "Dead")
    ]
    
    print(f"\n📋 Same Signal Breakdown (45/42/40/38) across different lifecycle stages:")
    
    explanations_by_stage = {}
    for stage_id, stage_name in stages:
        feature2_output = {
            "trend_id": f"trend_stage_{stage_id}",
            "trend_name": f"Test Trend - {stage_name}",
            "decline_risk_score": 41.2,
            "alert_level": "yellow",
            "lifecycle_stage": stage_id,
            "stage_name": stage_name,
            "confidence": "high",
            "data_quality": "complete",
            "signal_breakdown": same_signals,
            "historical_risk_scores": historical,
            "data_completeness": data_completeness
        }
        
        explanation = generate_explanation(feature2_output, "2026-02-07T12:00:00Z")
        explanations_by_stage[stage_id] = explanation
        
        print(f"\n🎬 Stage {stage_id} ({stage_name}):")
        print(f"   Decision Status: {explanation['decision_summary']['status']}")
        print(f"   Message: {explanation['decision_summary']['message'][:70]}...")
        print(f"   Confidence: {explanation['confidence'].upper()}")
    
    # Assertions
    for stage_id, explanation in explanations_by_stage.items():
        assert 'decision_summary' in explanation, f"Missing decision_summary for stage {stage_id}"
        assert 'signal_contributions' in explanation, f"Missing signal_contributions for stage {stage_id}"
        assert 'counterfactuals' in explanation, f"Missing counterfactuals for stage {stage_id}"
        assert explanation['confidence'] in ['high', 'medium', 'low'], f"Invalid confidence for stage {stage_id}"
    
    # Verify lifecycle awareness by checking decision messages vary
    messages = [e['decision_summary']['message'] for e in explanations_by_stage.values()]
    unique_messages = len(set(messages))
    assert unique_messages >= 2, "Explanations should vary by lifecycle stage"
    
    print("\n✅ Context awareness verified - explanations vary by lifecycle stage\n")
    return True


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all Explainable AI tests"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + " FEATURE #3: EXPLAINABLE AI ENGINE (GOLD-STANDARD) ".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    try:
        test_scenario_2_sharp_collapse()
        test_scenario_5_catastrophic()
        test_scenario_1_healthy_viral()
        test_batch_explanations()
        test_lifecycle_context()
        
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " ALL FEATURE #3 GOLD-STANDARD TESTS PASSED ".center(78) + "█")
        print("█" + " "*78 + "█")
        print("█"*80 + "\n")
        
        return True
    
    except AssertionError as e:
        print(f"\n\n[FAILED] TEST ASSERTION ERROR: {e}\n")
        return False
    except Exception as e:
        print(f"\n\n[ERROR] UNEXPECTED EXCEPTION: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
