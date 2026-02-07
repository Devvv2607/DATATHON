"""
Test Suite for Explainable AI Engine (Feature #3)
Tests explanation generation for various risk scenarios
"""

import sys
import os
from datetime import datetime

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'decline_signals'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'decline_signals', 'explainable_ai'))

from explainable_ai.explainer import generate_explanation, explain_multiple_trends

# ============================================================================
# TEST SCENARIOS - Feature #2 Outputs
# ============================================================================

def test_scenario_1_healthy_green():
    """LOW RISK: Healthy viral trend - GREEN alert"""
    print("\n" + "="*80)
    print("TEST 1: Healthy Viral Trend - GREEN Alert")
    print("="*80)
    
    feature2_output = {
        "trend_id": "trend_001",
        "trend_name": "#VocalChallenge",
        "lifecycle_stage": 2,
        "stage_name": "Viral",
        "decline_risk_score": 22.5,
        "alert_level": "green",
        "confidence": "high",
        "data_quality": "complete",
        "signal_breakdown": {
            "engagement_drop": 15,
            "velocity_decline": 18,
            "creator_decline": 12,
            "quality_decline": 8
        },
        "time_to_die": None
    }
    
    explanation = generate_explanation(feature2_output, datetime.now().isoformat())
    
    print(f"\n📌 Trend: {explanation['trend_name']} ({explanation['trend_id']})")
    print(f"📊 Risk Score: {explanation['risk_score']:.1f} ({explanation['alert_level'].upper()})")
    print(f"🎭 Lifecycle Stage: {explanation['stage_name']}")
    
    print(f"\n💡 EXPLANATIONS:")
    for i, stmt in enumerate(explanation['explanations'], 1):
        print(f"   {i}. {stmt}")
    
    assert explanation['alert_level'] == "green", "Expected GREEN alert"
    assert len(explanation['explanations']) >= 2, "Expected at least 2 statements"
    print(f"\n✅ TEST PASSED\n")
    return True


def test_scenario_2_yellow_warning():
    """MODERATE RISK: Early warning signs - YELLOW alert"""
    print("\n" + "="*80)
    print("TEST 2: Early Warning - YELLOW Alert")
    print("="*80)
    
    feature2_output = {
        "trend_id": "trend_002",
        "trend_name": "#DanceChallenge",
        "lifecycle_stage": 2,
        "stage_name": "Viral",
        "decline_risk_score": 44.2,
        "alert_level": "yellow",
        "confidence": "high",
        "data_quality": "complete",
        "signal_breakdown": {
            "engagement_drop": 52,
            "velocity_decline": 38,
            "creator_decline": 28,
            "quality_decline": 22
        },
        "time_to_die": None
    }
    
    explanation = generate_explanation(feature2_output, datetime.now().isoformat())
    
    print(f"\n📌 Trend: {explanation['trend_name']} ({explanation['trend_id']})")
    print(f"📊 Risk Score: {explanation['risk_score']:.1f} ({explanation['alert_level'].upper()})")
    print(f"🎭 Lifecycle Stage: {explanation['stage_name']}")
    
    print(f"\n💡 EXPLANATIONS:")
    for i, stmt in enumerate(explanation['explanations'], 1):
        print(f"   {i}. {stmt}")
    
    assert explanation['alert_level'] == "yellow", "Expected YELLOW alert"
    assert len(explanation['explanations']) >= 2, "Expected at least 2 statements"
    print(f"\n✅ TEST PASSED\n")
    return True


def test_scenario_3_orange_risk():
    """HIGH RISK: Multiple signals firing - ORANGE alert"""
    print("\n" + "="*80)
    print("TEST 3: High Risk - ORANGE Alert")
    print("="*80)
    
    feature2_output = {
        "trend_id": "trend_003",
        "trend_name": "#SoundTrend",
        "lifecycle_stage": 2,
        "stage_name": "Viral",
        "decline_risk_score": 67.8,
        "alert_level": "orange",
        "confidence": "high",
        "data_quality": "complete",
        "signal_breakdown": {
            "engagement_drop": 72,
            "velocity_decline": 65,
            "creator_decline": 58,
            "quality_decline": 45
        },
        "time_to_die": 7
    }
    
    explanation = generate_explanation(feature2_output, datetime.now().isoformat())
    
    print(f"\n📌 Trend: {explanation['trend_name']} ({explanation['trend_id']})")
    print(f"📊 Risk Score: {explanation['risk_score']:.1f} ({explanation['alert_level'].upper()})")
    print(f"🎭 Lifecycle Stage: {explanation['stage_name']}")
    print(f"⏰ Time to Die: {feature2_output['time_to_die']} days" if feature2_output['time_to_die'] else "⏰ Time to Die: Unknown")
    
    print(f"\n💡 EXPLANATIONS:")
    for i, stmt in enumerate(explanation['explanations'], 1):
        print(f"   {i}. {stmt}")
    
    assert explanation['alert_level'] == "orange", "Expected ORANGE alert"
    assert len(explanation['explanations']) >= 2, "Expected at least 2 statements"
    assert "PRIMARY DRIVER" in explanation['explanations'][1], "Expected primary driver statement"
    print(f"\n✅ TEST PASSED\n")
    return True


def test_scenario_4_red_critical():
    """CRITICAL RISK: Severe decline - RED alert"""
    print("\n" + "="*80)
    print("TEST 4: Critical Risk - RED Alert")
    print("="*80)
    
    feature2_output = {
        "trend_id": "trend_004",
        "trend_name": "#ViralChallenge",
        "lifecycle_stage": 3,
        "stage_name": "Plateau",
        "decline_risk_score": 85.3,
        "alert_level": "red",
        "confidence": "high",
        "data_quality": "complete",
        "signal_breakdown": {
            "engagement_drop": 88,
            "velocity_decline": 82,
            "creator_decline": 76,
            "quality_decline": 68
        },
        "time_to_die": 3
    }
    
    explanation = generate_explanation(feature2_output, datetime.now().isoformat())
    
    print(f"\n📌 Trend: {explanation['trend_name']} ({explanation['trend_id']})")
    print(f"📊 Risk Score: {explanation['risk_score']:.1f} ({explanation['alert_level'].upper()})")
    print(f"🎭 Lifecycle Stage: {explanation['stage_name']}")
    print(f"⏰ Time to Die: {feature2_output['time_to_die']} days" if feature2_output['time_to_die'] else "⏰ Time to Die: Unknown")
    
    print(f"\n💡 EXPLANATIONS:")
    for i, stmt in enumerate(explanation['explanations'], 1):
        print(f"   {i}. {stmt}")
    
    assert explanation['alert_level'] == "red", "Expected RED alert"
    assert len(explanation['explanations']) >= 2, "Expected at least 2 statements"
    print(f"\n✅ TEST PASSED\n")
    return True


def test_scenario_5_declining_stage():
    """DECLINING STAGE: Different sensitivity context"""
    print("\n" + "="*80)
    print("TEST 5: Declining Stage - Forgiving Sensitivity")
    print("="*80)
    
    feature2_output = {
        "trend_id": "trend_005",
        "trend_name": "#OldTrend",
        "lifecycle_stage": 4,
        "stage_name": "Decline",
        "decline_risk_score": 52.1,
        "alert_level": "yellow",
        "confidence": "medium",
        "data_quality": "complete",
        "signal_breakdown": {
            "engagement_drop": 68,
            "velocity_decline": 55,
            "creator_decline": 42,
            "quality_decline": 35
        },
        "time_to_die": None
    }
    
    explanation = generate_explanation(feature2_output, datetime.now().isoformat())
    
    print(f"\n📌 Trend: {explanation['trend_name']} ({explanation['trend_id']})")
    print(f"📊 Risk Score: {explanation['risk_score']:.1f} ({explanation['alert_level'].upper()})")
    print(f"🎭 Lifecycle Stage: {explanation['stage_name']}")
    
    print(f"\n💡 EXPLANATIONS:")
    for i, stmt in enumerate(explanation['explanations'], 1):
        print(f"   {i}. {stmt}")
    
    # In Decline stage, same signals get different context (lower sensitivity)
    assert "Decline" in explanation['stage_name'], "Expected Decline stage"
    assert any("expected" in s.lower() for s in explanation['explanations']), "Expected normalized language for Decline stage"
    print(f"\n✅ TEST PASSED\n")
    return True


def test_batch_explanations():
    """Test batch explanation generation"""
    print("\n" + "="*80)
    print("TEST 6: Batch Explanation (Multiple Trends)")
    print("="*80)
    
    outputs = [
        {
            "trend_id": "trend_batch_1",
            "trend_name": "#Trend1",
            "lifecycle_stage": 2,
            "stage_name": "Viral",
            "decline_risk_score": 25.0,
            "alert_level": "green",
            "confidence": "high",
            "data_quality": "complete",
            "signal_breakdown": {"engagement_drop": 20, "velocity_decline": 15, "creator_decline": 10, "quality_decline": 8}
        },
        {
            "trend_id": "trend_batch_2",
            "trend_name": "#Trend2",
            "lifecycle_stage": 2,
            "stage_name": "Viral",
            "decline_risk_score": 70.0,
            "alert_level": "orange",
            "confidence": "high",
            "data_quality": "complete",
            "signal_breakdown": {"engagement_drop": 75, "velocity_decline": 68, "creator_decline": 60, "quality_decline": 50}
        }
    ]
    
    explanations = explain_multiple_trends(outputs, datetime.now().isoformat())
    
    print(f"\n📊 Generated explanations for {len(explanations)} trends:")
    for exp in explanations:
        print(f"\n   {exp['trend_name']} ({exp['trend_id']}): {exp['alert_level'].upper()}")
        for stmt in exp['explanations'][:2]:
            print(f"      - {stmt[:70]}...")
    
    assert len(explanations) == 2, "Expected 2 explanations"
    assert all('explanations' in e for e in explanations), "All should have explanations"
    print(f"\n✅ TEST PASSED\n")
    return True


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all explainable AI tests"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + " EXPLAINABLE AI / DECISION TRANSPARENCY ENGINE - FEATURE #3 ".center(78) + "█")
    print("█" + " Test Suite ".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    try:
        test_scenario_1_healthy_green()
        test_scenario_2_yellow_warning()
        test_scenario_3_orange_risk()
        test_scenario_4_red_critical()
        test_scenario_5_declining_stage()
        test_batch_explanations()
        
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " ✅ ALL EXPLAINABLE AI TESTS PASSED ".center(78) + "█")
        print("█" + " "*78 + "█")
        print("█"*80 + "\n")
        
        return True
    
    except AssertionError as e:
        print(f"\n\n❌ TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
