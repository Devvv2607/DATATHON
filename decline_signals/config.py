"""
Configuration & Lifecycle-Aware Thresholds
All signal thresholds are lifecycle-aware and configurable
"""

from enum import Enum

class LifecycleStage(Enum):
    EMERGENCE = 1
    VIRAL = 2
    PLATEAU = 3
    DECLINE = 4
    DEATH = 5

# ============================================================================
# LIFECYCLE SENSITIVITY MAPPING
# ============================================================================
STAGE_SENSITIVITY = {
    LifecycleStage.EMERGENCE: "very_low",
    LifecycleStage.VIRAL: "very_high",
    LifecycleStage.PLATEAU: "medium",
    LifecycleStage.DECLINE: "low",
    LifecycleStage.DEATH: "minimal",
}

# ============================================================================
# SIGNAL 1: ENGAGEMENT DROP DETECTOR
# ============================================================================
ENGAGEMENT_DROP_THRESHOLDS = {
    "very_low": {"drop_percent": 40, "period_days": 5, "max_score": 20},
    "very_high": {"drop_percent": 10, "period_days": 3, "max_score": 100},
    "medium": {"drop_percent": 15, "period_days": 3, "max_score": 75},
    "low": {"drop_percent": 25, "period_days": 3, "max_score": 40},
    "minimal": {"drop_percent": 50, "period_days": 3, "max_score": 10},
}

# ============================================================================
# SIGNAL 2: VELOCITY DECLINE DETECTOR
# ============================================================================
VELOCITY_DECLINE_THRESHOLDS = {
    "very_low": {"accel_threshold": -0.15, "max_score": 15},
    "very_high": {"accel_threshold": -0.05, "max_score": 100},
    "medium": {"accel_threshold": -0.08, "max_score": 70},
    "low": {"accel_threshold": -0.20, "max_score": 30},
    "minimal": {"accel_threshold": -0.50, "max_score": 5},
}

# ============================================================================
# SIGNAL 3: CREATOR ACTIVITY DECLINE
# ============================================================================
CREATOR_DECLINE_THRESHOLDS = {
    "very_low": {"creator_drop_percent": 30, "avg_follower_weight": 0.3, "max_score": 20},
    "very_high": {"creator_drop_percent": 5, "avg_follower_weight": 0.5, "max_score": 100},
    "medium": {"creator_drop_percent": 10, "avg_follower_weight": 0.4, "max_score": 75},
    "low": {"creator_drop_percent": 20, "avg_follower_weight": 0.3, "max_score": 40},
    "minimal": {"creator_drop_percent": 50, "avg_follower_weight": 0.2, "max_score": 10},
}

# ============================================================================
# SIGNAL 4: QUALITY DECLINE DETECTOR
# ============================================================================
QUALITY_DECLINE_THRESHOLDS = {
    "very_low": {"engagement_per_post_drop": 30, "engagement_ratio_threshold": 0.02, "max_score": 15},
    "very_high": {"engagement_per_post_drop": 8, "engagement_ratio_threshold": 0.08, "max_score": 100},
    "medium": {"engagement_per_post_drop": 12, "engagement_ratio_threshold": 0.05, "max_score": 75},
    "low": {"engagement_per_post_drop": 20, "engagement_ratio_threshold": 0.03, "max_score": 40},
    "minimal": {"engagement_per_post_drop": 40, "engagement_ratio_threshold": 0.01, "max_score": 10},
}

# ============================================================================
# SIGNAL AGGREGATION WEIGHTS
# ============================================================================
SIGNAL_WEIGHTS = {
    "engagement_drop": 0.27,
    "velocity_decline": 0.28,  # Strong early indicator
    "creator_decline": 0.25,   # Leading indicator of abandonment
    "quality_decline": 0.20,   # Content quality is critical signal
}

# ============================================================================
# ALERT LEVEL MAPPING
# ============================================================================
ALERT_LEVELS = {
    (0, 30): "green",
    (30, 57): "yellow",
    (57, 80): "orange",
    (80, 101): "red",
}

def get_sensitivity_for_stage(stage: int) -> str:
    """Get sensitivity level for a lifecycle stage"""
    try:
        stage_enum = LifecycleStage(stage)
        return STAGE_SENSITIVITY[stage_enum]
    except ValueError:
        # Fallback to Plateau if invalid stage
        return STAGE_SENSITIVITY[LifecycleStage.PLATEAU]

def get_alert_level(risk_score: float) -> str:
    """Get alert level based on risk score"""
    for (min_score, max_score), level in ALERT_LEVELS.items():
        if min_score <= risk_score < max_score:
            return level
    return "red"
