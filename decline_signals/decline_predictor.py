"""
Time-to-Decline Prediction Module
Estimates when a trend will reach critical decline thresholds
Based on velocity trends and burn rate calculations
"""

import logging
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import statistics

from models import DailyMetric

logger = logging.getLogger(__name__)

# ============================================================================
# CRITICAL THRESHOLDS (per alert level)
# ============================================================================

CRITICAL_THRESHOLDS = {
    "green": 30,      # Risk score below 30
    "yellow": 57,     # Risk score 30-57
    "orange": 80,     # Risk score 57-80
    "red": 100        # Risk score 80+
}

# ============================================================================
# BURN RATE CALCULATION
# ============================================================================

def calculate_engagement_burn_rate(daily_metrics: List[DailyMetric]) -> Dict:
    """
    Calculate daily engagement loss rate (burn rate)
    
    Returns:
    {
        "daily_loss_abs": float,      # avg engagement loss per day
        "daily_loss_pct": float,      # avg % loss per day
        "trend": "stable|declining|accelerating",
        "confidence": float           # 0-1 based on consistency
    }
    """
    if len(daily_metrics) < 2:
        logger.warning("⚠ Not enough data for burn rate calculation (need ≥2 days)")
        return {
            "daily_loss_abs": 0.0,
            "daily_loss_pct": 0.0,
            "trend": "unknown",
            "confidence": 0.0
        }
    
    try:
        engagement_values = [m.total_engagement for m in daily_metrics]
        
        # Calculate daily changes
        daily_changes = []
        daily_pct_changes = []
        
        for i in range(1, len(engagement_values)):
            prev_eng = engagement_values[i-1]
            curr_eng = engagement_values[i]
            change = curr_eng - prev_eng
            daily_changes.append(change)
            
            if prev_eng > 0:
                pct_change = (change / prev_eng) * 100
                daily_pct_changes.append(pct_change)
        
        if not daily_changes:
            return {
                "daily_loss_abs": 0.0,
                "daily_loss_pct": 0.0,
                "trend": "unknown",
                "confidence": 0.0
            }
        
        # Average losses (negative = decline)
        avg_abs_loss = statistics.mean(daily_changes)
        avg_pct_loss = statistics.mean(daily_pct_changes) if daily_pct_changes else 0.0
        
        # Trend direction
        if avg_abs_loss > 5:  # Small positive buffer for noise
            trend = "growing"
        elif avg_abs_loss < -5:
            trend = "declining"
        else:
            trend = "stable"
        
        # Consistency (lower variance = higher confidence)
        if len(daily_changes) > 1:
            stdev = statistics.stdev(daily_changes)
            consistency = max(0.0, 1.0 - (stdev / (abs(avg_abs_loss) + 1)))
        else:
            consistency = 0.5
        
        logger.debug(f"✓ Burn rate: {avg_abs_loss:.1f} eng/day ({avg_pct_loss:.2f}%), trend: {trend}")
        
        return {
            "daily_loss_abs": avg_abs_loss,
            "daily_loss_pct": avg_pct_loss,
            "trend": trend,
            "confidence": max(0.0, min(consistency, 1.0))
        }
    
    except Exception as e:
        logger.error(f"✗ Burn rate calculation failed: {e}")
        return {
            "daily_loss_abs": 0.0,
            "daily_loss_pct": 0.0,
            "trend": "unknown",
            "confidence": 0.0
        }


# ============================================================================
# TRAJECTORY PROJECTION
# ============================================================================

def project_engagement_trajectory(
    daily_metrics: List[DailyMetric],
    days_ahead: int = 7
) -> Dict:
    """
    Project engagement trajectory using linear regression
    
    Returns:
    {
        "current_engagement": float,
        "projected_engagement_days_7": float,
        "projected_engagement_days_14": float,
        "trend_slope": float,           # engagement change per day
        "projection_confidence": float  # 0-1
    }
    """
    if len(daily_metrics) < 2:
        logger.warning("⚠ Not enough data for trajectory projection")
        return {
            "current_engagement": float(daily_metrics[-1].total_engagement) if daily_metrics else 0.0,
            "projected_engagement_days_7": 0.0,
            "projected_engagement_days_14": 0.0,
            "trend_slope": 0.0,
            "projection_confidence": 0.0
        }
    
    try:
        engagement_values = [m.total_engagement for m in daily_metrics]
        current_eng = engagement_values[-1]
        
        # Linear regression: engagement ~ days
        n = len(engagement_values)
        x = list(range(n))  # days since first data point
        y = engagement_values
        
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)
        
        # Slope and intercept
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0.0
        else:
            slope = numerator / denominator
        
        intercept = y_mean - (slope * x_mean)
        
        # Project 7 and 14 days ahead
        proj_day_7 = intercept + (slope * (n + 7))
        proj_day_14 = intercept + (slope * (n + 14))
        
        # R-squared for confidence
        ss_res = sum((y[i] - (intercept + slope * x[i]))**2 for i in range(n))
        ss_tot = sum((y[i] - y_mean)**2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        confidence = max(0.0, min(r_squared, 1.0))
        
        logger.debug(f"✓ Trajectory: slope={slope:.1f} eng/day, R²={r_squared:.2f}")
        
        return {
            "current_engagement": current_eng,
            "projected_engagement_days_7": max(0.0, proj_day_7),
            "projected_engagement_days_14": max(0.0, proj_day_14),
            "trend_slope": slope,
            "projection_confidence": confidence
        }
    
    except Exception as e:
        logger.error(f"✗ Trajectory projection failed: {e}")
        return {
            "current_engagement": float(daily_metrics[-1].total_engagement) if daily_metrics else 0.0,
            "projected_engagement_days_7": 0.0,
            "projected_engagement_days_14": 0.0,
            "trend_slope": 0.0,
            "projection_confidence": 0.0
        }


# ============================================================================
# TIME-TO-CRITICAL ESTIMATION
# ============================================================================

def estimate_time_to_critical(
    daily_metrics: List[DailyMetric],
    current_risk_score: float,
    target_alert_level: str = "red"
) -> Dict:
    """
    Estimate how many days until trend reaches critical alert level
    
    Args:
        daily_metrics: Historical metric data
        current_risk_score: Current decline risk score (0-100)
        target_alert_level: "red" (80+), "orange" (57-80), or "yellow" (30-57)
    
    Returns:
    {
        "days_to_critical": int|None,    # None if already in target or growing
        "critical_threshold": float,      # Risk score threshold
        "days_to_orange": int|None,      # Days to ORANGE (57)
        "days_to_red": int|None,         # Days to RED (80)
        "estimated_date": str|None,      # ISO date when critical expected
        "confidence": float               # 0-1 prediction confidence
    }
    """
    if len(daily_metrics) < 2:
        logger.warning("⚠ Not enough data for time-to-critical estimation")
        return {
            "days_to_critical": None,
            "critical_threshold": CRITICAL_THRESHOLDS.get(target_alert_level, 80),
            "days_to_orange": None,
            "days_to_red": None,
            "estimated_date": None,
            "confidence": 0.0
        }
    
    try:
        burn_rate = calculate_engagement_burn_rate(daily_metrics)
        trajectory = project_engagement_trajectory(daily_metrics)
        
        # If growing or stable, no decline projected
        if burn_rate["trend"] in ["growing", "stable"]:
            logger.info("ℹ Trend is stable/growing - no decline time to calculate")
            return {
                "days_to_critical": None,
                "critical_threshold": CRITICAL_THRESHOLDS.get(target_alert_level, 80),
                "days_to_orange": None,
                "days_to_red": None,
                "estimated_date": None,
                "confidence": 0.0
            }
        
        current_eng = trajectory["current_engagement"]
        slope = trajectory["trend_slope"]
        
        # Estimate risk score trajectory
        # Rough model: risk_score increases by ~10 points per 10% engagement loss
        # (this should be calibrated with real data)
        
        if slope >= 0:  # Not declining
            return {
                "days_to_critical": None,
                "critical_threshold": CRITICAL_THRESHOLDS.get(target_alert_level, 80),
                "days_to_orange": None,
                "days_to_red": None,
                "estimated_date": None,
                "confidence": 0.0
            }
        
        # Days to engagement reaching critical level (e.g., 50% of current)
        critical_eng_loss_pct = 0.5  # 50% loss threshold
        critical_eng_value = current_eng * (1 - critical_eng_loss_pct)
        
        # days_to_critical = (current - critical) / loss_per_day
        loss_per_day = abs(slope)
        if loss_per_day > 0:
            eng_days_to_critical = (current_eng - critical_eng_value) / loss_per_day
        else:
            eng_days_to_critical = float('inf')
        
        # Map to risk score days (rough calibration)
        risk_score_days_to_target = max(1, int(eng_days_to_critical * 0.7))  # Adjusted ratio
        
        # Estimate all critical points
        days_to_orange = max(1, int(risk_score_days_to_target * 0.6)) if current_risk_score < 57 else 0
        days_to_red = max(1, int(risk_score_days_to_target)) if current_risk_score < 80 else 0
        days_to_critical = days_to_red if target_alert_level == "red" else days_to_orange
        
        # Estimated date
        if days_to_critical and days_to_critical > 0:
            last_date = datetime.fromisoformat(daily_metrics[-1].date.replace('Z', '+00:00'))
            estimated_critical_date = (last_date + timedelta(days=days_to_critical)).isoformat()
        else:
            estimated_critical_date = None
        
        # Confidence based on burn rate consistency and projection quality
        confidence = (burn_rate["confidence"] + trajectory["projection_confidence"]) / 2
        
        logger.info(f"✓ Time to critical: ~{days_to_critical} days (confidence: {confidence:.1%})")
        
        return {
            "days_to_critical": days_to_critical if days_to_critical > 0 else None,
            "critical_threshold": CRITICAL_THRESHOLDS.get(target_alert_level, 80),
            "days_to_orange": days_to_orange if days_to_orange > 0 else None,
            "days_to_red": days_to_red if days_to_red > 0 else None,
            "estimated_date": estimated_critical_date,
            "confidence": confidence
        }
    
    except Exception as e:
        logger.error(f"✗ Time-to-critical estimation failed: {e}")
        return {
            "days_to_critical": None,
            "critical_threshold": CRITICAL_THRESHOLDS.get(target_alert_level, 80),
            "days_to_orange": None,
            "days_to_red": None,
            "estimated_date": None,
            "confidence": 0.0
        }


# ============================================================================
# STAGE TRANSITION PREDICTION
# ============================================================================

def estimate_days_to_stage_transition(
    daily_metrics: List[DailyMetric],
    current_lifecycle_stage: int
) -> Dict:
    """
    Estimate how many days until transition to next lifecycle stage
    
    Returns:
    {
        "current_stage": int,
        "next_stage": int,
        "estimated_days": int|None,
        "transition_date": str|None,
        "confidence": float,
        "note": str
    }
    """
    if len(daily_metrics) < 2:
        return {
            "current_stage": current_lifecycle_stage,
            "next_stage": min(current_lifecycle_stage + 1, 5),
            "estimated_days": None,
            "transition_date": None,
            "confidence": 0.0,
            "note": "Insufficient data for transition prediction"
        }
    
    try:
        # Get trajectory and burn rate
        burn_rate = calculate_engagement_burn_rate(daily_metrics)
        trajectory = project_engagement_trajectory(daily_metrics)
        
        # Stage transitions are typically marked by:
        # Viral -> Peak: Peak engagement stabilizes
        # Peak -> Plateau: Engagement drops by 30-40%, velocity flattens
        # Plateau -> Decline: Sustained 20%+ week-over-week drop
        # Decline -> Dead: Engagement < 10% of peak
        
        if burn_rate["trend"] == "growing":
            est_days_to_transition = 14  # Growing phase usually lasts 1-2 weeks
        elif burn_rate["trend"] == "stable":
            est_days_to_transition = 21  # Stable phase typically lasts 2-3 weeks
        else:  # declining
            est_days_to_transition = 10  # Decline happens faster
        
        if trajectory["projection_confidence"] < 0.3:
            confidence = 0.2
        else:
            confidence = min((burn_rate["confidence"] + trajectory["projection_confidence"]) / 2, 0.8)
        
        # Calculate transition date
        last_date = datetime.fromisoformat(daily_metrics[-1].date.replace('Z', '+00:00'))
        transition_date = (last_date + timedelta(days=est_days_to_transition)).isoformat()
        
        next_stage = min(current_lifecycle_stage + 1, 5)
        
        logger.info(f"✓ Estimated stage transition: Stage {current_lifecycle_stage} -> {next_stage} in ~{est_days_to_transition} days")
        
        return {
            "current_stage": current_lifecycle_stage,
            "next_stage": next_stage,
            "estimated_days": est_days_to_transition,
            "transition_date": transition_date,
            "confidence": confidence,
            "note": f"Based on '{burn_rate['trend']}' trend"
        }
    
    except Exception as e:
        logger.error(f"✗ Stage transition estimation failed: {e}")
        return {
            "current_stage": current_lifecycle_stage,
            "next_stage": min(current_lifecycle_stage + 1, 5),
            "estimated_days": None,
            "transition_date": None,
            "confidence": 0.0,
            "note": f"Estimation error: {str(e)}"
        }


# ============================================================================
# MAIN PREDICTION FUNCTION
# ============================================================================

def generate_decline_prediction(
    daily_metrics: List[DailyMetric],
    current_risk_score: float,
    current_lifecycle_stage: int
) -> Dict:
    """
    Complete prediction package for decline risk
    
    Returns all predictions in a single structured response
    """
    try:
        burn_rate = calculate_engagement_burn_rate(daily_metrics)
        trajectory = project_engagement_trajectory(daily_metrics)
        time_to_critical = estimate_time_to_critical(daily_metrics, current_risk_score, "red")
        stage_transition = estimate_days_to_stage_transition(daily_metrics, current_lifecycle_stage)
        
        logger.info("✓ Decline prediction complete")
        
        return {
            "burn_rate": burn_rate,
            "trajectory": trajectory,
            "time_to_critical": time_to_critical,
            "stage_transition": stage_transition,
            "summary": {
                "at_risk": time_to_critical["days_to_red"] is not None and time_to_critical["days_to_red"] <= 14,
                "critical_date": time_to_critical["estimated_date"],
                "days_to_concern": time_to_critical["days_to_orange"],
                "overall_confidence": (
                    burn_rate["confidence"] +
                    trajectory["projection_confidence"] +
                    time_to_critical["confidence"] +
                    stage_transition["confidence"]
                ) / 4
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Decline prediction generation failed: {e}", exc_info=True)
        return {
            "burn_rate": {"daily_loss_abs": 0.0, "daily_loss_pct": 0.0, "trend": "unknown", "confidence": 0.0},
            "trajectory": {"current_engagement": 0.0, "projected_engagement_days_7": 0.0, "projected_engagement_days_14": 0.0, "trend_slope": 0.0, "projection_confidence": 0.0},
            "time_to_critical": {"days_to_critical": None, "critical_threshold": 80, "days_to_orange": None, "days_to_red": None, "estimated_date": None, "confidence": 0.0},
            "stage_transition": {"current_stage": current_lifecycle_stage, "next_stage": min(current_lifecycle_stage + 1, 5), "estimated_days": None, "transition_date": None, "confidence": 0.0, "note": f"Error: {str(e)}"},
            "summary": {"at_risk": False, "critical_date": None, "days_to_concern": None, "overall_confidence": 0.0}
        }
