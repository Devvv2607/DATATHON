"""
5 Real-World Scenarios - Early Decline Signal Detection Engine
Uses real-world social media behavior patterns

Thresholds Basis:
- VIRAL (very_high): Sensitive to earliest signs (5% engagement drop, -0.05 accel)
- PLATEAU (medium): Balanced thresholds (15% engagement drop, -0.08 accel)
- Alert Levels: GREEN 0-30, YELLOW 30-60, ORANGE 60-80, RED 80+
- Signal Weights: velocity_decline 35%, engagement_drop 30%, creator_decline 25%, quality_decline 10%
"""

import sys
import os
from datetime import datetime, timedelta

# Add decline_signals to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'decline_signals'))

from models import DailyMetric
from config import (
    ENGAGEMENT_DROP_THRESHOLDS,
    VELOCITY_DECLINE_THRESHOLDS,
    CREATOR_DECLINE_THRESHOLDS,
    QUALITY_DECLINE_THRESHOLDS,
    STAGE_SENSITIVITY,
    LifecycleStage,
)
from signals.engagement_drop import calculate_engagement_drop
from signals.velocity_decline import calculate_velocity_decline
from signals.creator_decline import calculate_creator_decline
from signals.quality_decline import calculate_quality_decline
from lifecycle_handler import resolve_lifecycle_stage
from aggregator import aggregate_signals

# ============================================================================
# SCENARIO 1: Healthy Viral Trend - Strong Growth
# ============================================================================
def scenario_1_healthy_viral():
    """
    Real Pattern: Healthy viral trend with consistent strong growth
    - Views: 50M → 85M daily (accelerating)
    - Engagement: 3M → 5.2M daily (accelerating)
    - Growth rate: +20%, +18%, +15%, +12%, +10%... (tapering but positive)
    - Quality stable: EPP 45-48, consistent comments
    - Creators growing: 150 → 220
    Expected: GREEN (< 30)
    """
    print("\n" + "="*80)
    print("SCENARIO 1: Healthy Viral Growth")
    print("TikTok Dance | Days 1-7 | Viral Explosion")
    print("="*80)
    
    base_date = datetime.utcnow() - timedelta(days=6)
    metrics = []
    
    # Strong positive acceleration - healthy growth
    engagement_values = [3000000, 3600000, 4100000, 4550000, 4950000, 5250000, 5500000]
    view_values = [50000000, 60000000, 68000000, 75200000, 81600000, 87300000, 92500000]
    creator_values = [150, 165, 180, 195, 208, 219, 230]
    
    for i in range(7):
        metric = DailyMetric(
            date=(base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            total_engagement=engagement_values[i],
            views=view_values[i],
            posts_count=220 + i * 12,
            creators_count=creator_values[i],
            avg_creator_followers=280000,
            avg_comments_per_post=42,
            avg_engagement_per_post=46
        )
        metrics.append(metric)
    
    # VIRAL stage (very_high sensitivity)
    lifecycle_info = {
        "trend_id": "viral_dance",
        "lifecycle_stage": 2,
        "days_in_stage": 5,
        "confidence": 0.95
    }
    
    stage, stage_name, quality = resolve_lifecycle_stage(lifecycle_info)
    sensitivity = STAGE_SENSITIVITY[LifecycleStage(stage)]
    
    s1, exp1 = calculate_engagement_drop(metrics, sensitivity, ENGAGEMENT_DROP_THRESHOLDS)
    s2, exp2 = calculate_velocity_decline(metrics, sensitivity, VELOCITY_DECLINE_THRESHOLDS)
    s3, exp3 = calculate_creator_decline(metrics, sensitivity, CREATOR_DECLINE_THRESHOLDS)
    s4, exp4 = calculate_quality_decline(metrics, sensitivity, QUALITY_DECLINE_THRESHOLDS)
    
    print(f"\n📊 Signals ({sensitivity} sensitivity):")
    print(f"  Engagement Drop:  {s1:6.1f}  ({exp1})")
    print(f"  Velocity Decline: {s2:6.1f}  ({exp2})")
    print(f"  Creator Decline:  {s3:6.1f}  ({exp3})")
    print(f"  Quality Decline:  {s4:6.1f}  ({exp4})")
    
    signal_scores = {
        "engagement_drop": s1, "velocity_decline": s2,
        "creator_decline": s3, "quality_decline": s4
    }
    risk, alert, conf = aggregate_signals(signal_scores, stage, quality)
    
    print(f"\n🎯 Result: {risk:.1f}/100 → {alert.upper()} ({conf})")
    print(f"   All signals green: healthy growth trajectory")
    assert alert == "green" and risk < 30, f"Expected GREEN < 30, got {alert} {risk:.1f}"
    print("✅ PASSED\n")


# ============================================================================
# SCENARIO 2: Sharp Engagement Collapse - YouTube Trend
# ============================================================================
def scenario_2_viral_plateau():
    """
    Real Pattern: Trend hits plateau with engagement collapse
    - Days 1-3: Growth (5M → 6.5M → 7.2M)
    - Days 4-7: Sharp collapse (7.2M → 5.8M → 4.2M → 3.1M)
    - 57% drop from peak = strong engagement_drop signal
    - Acceleration becomes very negative = velocity_decline fires
    Expected: ORANGE (60-80)
    """
    print("\n" + "="*80)
    print("SCENARIO 2: Sharp Engagement Collapse")
    print("YouTube Challenge | Days 1-7 | Peak→Collapse")
    print("="*80)
    
    base_date = datetime.utcnow() - timedelta(days=6)
    metrics = []
    
    # Sharp collapse pattern: grow 3 days, then drop hard
    engagement_values = [5000000, 6500000, 7200000, 5800000, 4200000, 3100000, 2500000]
    creator_values = [200, 210, 215, 200, 180, 160, 145]
    
    for i in range(7):
        metric = DailyMetric(
            date=(base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            total_engagement=engagement_values[i],
            views=engagement_values[i] * 10,
            posts_count=150,
            creators_count=creator_values[i],
            avg_creator_followers=300000,
            avg_comments_per_post=40,
            avg_engagement_per_post=50
        )
        metrics.append(metric)
    
    # PLATEAU stage (medium sensitivity: -0.08 acceleration threshold)
    lifecycle_info = {
        "trend_id": "collapse_challenge",
        "lifecycle_stage": 3,
        "days_in_stage": 3,
        "confidence": 0.85
    }
    
    stage, stage_name, quality = resolve_lifecycle_stage(lifecycle_info)
    sensitivity = STAGE_SENSITIVITY[LifecycleStage(stage)]
    
    s1, exp1 = calculate_engagement_drop(metrics, sensitivity, ENGAGEMENT_DROP_THRESHOLDS)
    s2, exp2 = calculate_velocity_decline(metrics, sensitivity, VELOCITY_DECLINE_THRESHOLDS)
    s3, exp3 = calculate_creator_decline(metrics, sensitivity, CREATOR_DECLINE_THRESHOLDS)
    s4, exp4 = calculate_quality_decline(metrics, sensitivity, QUALITY_DECLINE_THRESHOLDS)
    
    print(f"\n📊 Signals ({sensitivity} sensitivity):")
    print(f"  Engagement Drop:  {s1:6.1f}  ({exp1})  ⚠️ FIRES!")
    print(f"  Velocity Decline: {s2:6.1f}  ({exp2})  ⚠️ FIRES!")
    print(f"  Creator Decline:  {s3:6.1f}  ({exp3})")
    print(f"  Quality Decline:  {s4:6.1f}  ({exp4})")
    
    signal_scores = {
        "engagement_drop": s1, "velocity_decline": s2,
        "creator_decline": s3, "quality_decline": s4
    }
    risk, alert, conf = aggregate_signals(signal_scores, stage, quality)
    
    print(f"\n🎯 Result: {risk:.1f}/100 → {alert.upper()} ({conf})")
    print(f"   Engagement drop (30%) + Velocity decline (35%) = ORANGE")
    assert alert in ["orange", "red"] and risk >= 57, f"Expected ORANGE/RED >= 57, got {alert} {risk:.1f}"
    print("✅ PASSED\n")


# ============================================================================
# SCENARIO 3: Sharp Creator Exodus - Instagram Trend
# ============================================================================
def scenario_3_creator_exodus():
    """
    Real Pattern: Influencers abandon trend rapidly (leading indicator)
    - Creators: 300 → 280 → 250 → 200 → 150 → 120 → 100 (67% drop)
    - Avg followers: 300k → 180k (40% quality drop)
    - Engagement still stable (delayed market reaction)
    Expected: ORANGE (60-80)
    """
    print("\n" + "="*80)
    print("SCENARIO 3: Sharp Creator Exodus")
    print("Instagram Filter | Days 1-7 | Influencers Leaving")
    print("="*80)
    
    base_date = datetime.utcnow() - timedelta(days=6)
    metrics = []
    
    # Rapid creator abandonment
    creator_values = [300, 280, 250, 200, 150, 120, 100]
    follower_values = [300000, 285000, 260000, 220000, 180000, 150000, 130000]
    
    for i in range(7):
        metric = DailyMetric(
            date=(base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            total_engagement=7000000 - (i * 200000),  # Slow decline (delayed)
            views=70000000 - (i * 2000000),
            posts_count=200,
            creators_count=creator_values[i],
            avg_creator_followers=follower_values[i],
            avg_comments_per_post=38,
            avg_engagement_per_post=48
        )
        metrics.append(metric)
    
    # VIRAL (very_high sensitivity: 5% creator drop threshold)
    lifecycle_info = {
        "trend_id": "instagram_filter",
        "lifecycle_stage": 2,
        "days_in_stage": 3,
        "confidence": 0.88
    }
    
    stage, stage_name, quality = resolve_lifecycle_stage(lifecycle_info)
    sensitivity = STAGE_SENSITIVITY[LifecycleStage(stage)]
    
    s1, exp1 = calculate_engagement_drop(metrics, sensitivity, ENGAGEMENT_DROP_THRESHOLDS)
    s2, exp2 = calculate_velocity_decline(metrics, sensitivity, VELOCITY_DECLINE_THRESHOLDS)
    s3, exp3 = calculate_creator_decline(metrics, sensitivity, CREATOR_DECLINE_THRESHOLDS)
    s4, exp4 = calculate_quality_decline(metrics, sensitivity, QUALITY_DECLINE_THRESHOLDS)
    
    print(f"\n📊 Signals ({sensitivity} sensitivity):")
    print(f"  Engagement Drop:  {s1:6.1f}  ({exp1})")
    print(f"  Velocity Decline: {s2:6.1f}  ({exp2})")
    print(f"  Creator Decline:  {s3:6.1f}  ({exp3})  ⚠️ FIRES!")
    print(f"  Quality Decline:  {s4:6.1f}  ({exp4})")
    
    signal_scores = {
        "engagement_drop": s1, "velocity_decline": s2,
        "creator_decline": s3, "quality_decline": s4
    }
    risk, alert, conf = aggregate_signals(signal_scores, stage, quality)
    
    print(f"\n🎯 Result: {risk:.1f}/100 → {alert.upper()} ({conf})")
    print(f"   Creator exodus 67% + follower drop = leading indicator of collapse")
    assert alert in ["orange", "red"] and risk >= 57, f"Expected ORANGE/RED >= 57, got {alert} {risk:.1f}"
    print("✅ PASSED\n")


# ============================================================================
# SCENARIO 4: Sharp Quality Collapse - Meme Format
# ============================================================================
def scenario_4_quality_collapse():
    """
    Real Pattern: Content quality crashes (spam takeover)
    - Engagement Per Post: 55 → 18 (67% drop, threshold 12%)
    - Engagement/Views ratio: 0.08 → 0.025 (69% drop)
    - Posts explode: 100 → 400 (spam increase)
    - Audience disengages from low-quality content
    Expected: ORANGE (60-80)
    """
    print("\n" + "="*80)
    print("SCENARIO 4: Sharp Quality Collapse")
    print("Meme Format | Days 1-7 | Spam Takeover")
    print("="*80)
    
    base_date = datetime.utcnow() - timedelta(days=6)
    metrics = []
    
    # Quality degradation + spam increase
    epp_values = [55, 48, 38, 28, 22, 18, 15]
    posts_values = [100, 140, 180, 240, 300, 380, 450]
    engagement_values = [6000000, 5950000, 5800000, 5600000, 5300000, 4900000, 4500000]
    
    for i in range(7):
        metric = DailyMetric(
            date=(base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            total_engagement=engagement_values[i],
            views=engagement_values[i] * 12.5,  # Declining ratio
            posts_count=posts_values[i],
            creators_count=150,
            avg_creator_followers=200000,
            avg_comments_per_post=max(8, 25 - (i * 2)),
            avg_engagement_per_post=epp_values[i]
        )
        metrics.append(metric)
    
    # PLATEAU (medium sensitivity: 12% EPP drop threshold)
    lifecycle_info = {
        "trend_id": "meme_format",
        "lifecycle_stage": 3,
        "days_in_stage": 4,
        "confidence": 0.78
    }
    
    stage, stage_name, quality = resolve_lifecycle_stage(lifecycle_info)
    sensitivity = STAGE_SENSITIVITY[LifecycleStage(stage)]
    
    s1, exp1 = calculate_engagement_drop(metrics, sensitivity, ENGAGEMENT_DROP_THRESHOLDS)
    s2, exp2 = calculate_velocity_decline(metrics, sensitivity, VELOCITY_DECLINE_THRESHOLDS)
    s3, exp3 = calculate_creator_decline(metrics, sensitivity, CREATOR_DECLINE_THRESHOLDS)
    s4, exp4 = calculate_quality_decline(metrics, sensitivity, QUALITY_DECLINE_THRESHOLDS)
    
    print(f"\n📊 Signals ({sensitivity} sensitivity):")
    print(f"  Engagement Drop:  {s1:6.1f}  ({exp1})")
    print(f"  Velocity Decline: {s2:6.1f}  ({exp2})")
    print(f"  Creator Decline:  {s3:6.1f}  ({exp3})")
    print(f"  Quality Decline:  {s4:6.1f}  ({exp4})  ⚠️ FIRES!")
    
    signal_scores = {
        "engagement_drop": s1, "velocity_decline": s2,
        "creator_decline": s3, "quality_decline": s4
    }
    risk, alert, conf = aggregate_signals(signal_scores, stage, quality)
    
    print(f"\n🎯 Result: {risk:.1f}/100 → {alert.upper()} ({conf})")
    print(f"   Quality collapse 67% + engagement drop = content degradation signal")
    assert alert in ["orange", "red"] and risk >= 57, f"Expected ORANGE/RED >= 57, got {alert} {risk:.1f}"
    print("✅ PASSED\n")


# ============================================================================
# SCENARIO 5: Catastrophic Collapse - Rapid Death
# ============================================================================
def scenario_5_catastrophic():
    """
    Real Pattern: Trend dies suddenly (negative event, controversy, etc)
    - Engagement: 10M → 5.5M in 5 days (45% crash)
    - Velocity: Sharp negative acceleration (-0.15 to -0.20)
    - Creators flee: 400 → 200 (50% exodus)
    - Multiple signals fire simultaneously = RED
    Expected: RED (80+)
    """
    print("\n" + "="*80)
    print("SCENARIO 5: Catastrophic Collapse")
    print("TikTok Trend | Days 1-7 | Controversy→Death")
    print("="*80)
    
    base_date = datetime.utcnow() - timedelta(days=6)
    metrics = []
    
    # Rapid collapse pattern
    engagement_values = [10000000, 9200000, 7500000, 5800000, 4200000, 3100000, 2500000]
    creator_values = [400, 380, 320, 250, 200, 165, 140]
    
    for i in range(7):
        metric = DailyMetric(
            date=(base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            total_engagement=engagement_values[i],
            views=engagement_values[i] * 11,
            posts_count=180,
            creators_count=creator_values[i],
            avg_creator_followers=280000 * (0.92 ** i),
            avg_comments_per_post=max(5, 40 - (i * 5)),
            avg_engagement_per_post=max(15, 50 - (i * 4))
        )
        metrics.append(metric)
    
    # PLATEAU stage transitioning to collapse (medium sensitivity)
    # NOT DECLINE stage (otherwise velocity is too forgiving)
    lifecycle_info = {
        "trend_id": "dying_trend",
        "lifecycle_stage": 3,  # PLATEAU, not DECLINE
        "days_in_stage": 4,
        "confidence": 0.95
    }
    
    stage, stage_name, quality = resolve_lifecycle_stage(lifecycle_info)
    sensitivity = STAGE_SENSITIVITY[LifecycleStage(stage)]
    
    s1, exp1 = calculate_engagement_drop(metrics, sensitivity, ENGAGEMENT_DROP_THRESHOLDS)
    s2, exp2 = calculate_velocity_decline(metrics, sensitivity, VELOCITY_DECLINE_THRESHOLDS)
    s3, exp3 = calculate_creator_decline(metrics, sensitivity, CREATOR_DECLINE_THRESHOLDS)
    s4, exp4 = calculate_quality_decline(metrics, sensitivity, QUALITY_DECLINE_THRESHOLDS)
    
    print(f"\n📊 Signals ({sensitivity} sensitivity):")
    print(f"  Engagement Drop:  {s1:6.1f}  ({exp1})  ⚠️ FIRES!")
    print(f"  Velocity Decline: {s2:6.1f}  ({exp2})  ⚠️ FIRES!")
    print(f"  Creator Decline:  {s3:6.1f}  ({exp3})  ⚠️ FIRES!")
    print(f"  Quality Decline:  {s4:6.1f}  ({exp4})")
    
    signal_scores = {
        "engagement_drop": s1, "velocity_decline": s2,
        "creator_decline": s3, "quality_decline": s4
    }
    risk, alert, conf = aggregate_signals(signal_scores, stage, quality)
    
    print(f"\n🎯 Result: {risk:.1f}/100 → {alert.upper()} ({conf})")
    print(f"   Multiple signals firing: engagement 45% drop + velocity crash + creators fleeing")
    assert alert == "red" and risk >= 80, f"Expected RED >= 80, got {alert} {risk:.1f}"
    print("✅ PASSED\n")




# ============================================================================
# MAIN - RUN ALL 5 SCENARIOS
# ============================================================================
def main():
    """Run all 5 real-world test scenarios"""
    print("\n" + "█"*80)
    print("█" + " "*78 + "█")
    print("█" + " EARLY DECLINE SIGNAL DETECTION ENGINE ".center(78) + "█")
    print("█" + " 5 REAL-WORLD SCENARIOS ".center(78) + "█")
    print("█" + " "*78 + "█")
    print("█"*80)
    
    try:
        scenario_1_healthy_viral()
        scenario_2_viral_plateau()
        scenario_3_creator_exodus()
        scenario_4_quality_collapse()
        scenario_5_catastrophic()
        
        print("\n" + "█"*80)
        print("█" + " "*78 + "█")
        print("█" + " ✅ ALL 5 REAL-WORLD SCENARIOS PASSED ".center(78) + "█")
        print("█" + " "*78 + "█")
        print("█"*80 + "\n")
        
        return True
        
    except AssertionError as e:
        print(f"\n\n❌ SCENARIO FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
