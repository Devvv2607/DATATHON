"""
Feature 8: Decline Window Estimator
Predict timeframe before critical action required
"""

import logging
from .visualization_generators import generate_countdown_visualization

logger = logging.getLogger(__name__)


def get_decline_window(risk_score: float, time_to_critical: int, projected_marketing_burn: float = None) -> dict:
    """
    Estimate days until critical action required (risk hits RED).
    
    Args:
        risk_score: Current risk 0-100
        time_to_critical: Days until RED (80+) from prediction engine
        projected_marketing_burn: Optional total projected burn before collapse ($)
    
    Returns:
        {
            "decline_window": {
                "days_remaining": int,
                "window_stage": "urgent" | "warning" | "stable",
                "action_deadline": str,
                "recommendation": str,
                "projected_marketing_burn": float,
                "projected_burn_per_day": float,
                "days_until_collapse": int,
                "collapse_confidence": float
            }
        }
    """
    try:
        # Estimate action window
        if risk_score >= 80:
            days_remaining = 0
            window_stage = "urgent"
            recommendation = "Immediate action required. Hours not days."
            collapse_confidence = 95.0
        elif time_to_critical is None or time_to_critical < 0:
            days_remaining = 7
            window_stage = "stable"
            recommendation = "No imminent decline. Monitor weekly."
            collapse_confidence = 10.0
        elif time_to_critical <= 1:
            days_remaining = 1
            window_stage = "urgent"
            recommendation = "Critical decision needed within 24 hours."
            collapse_confidence = 90.0
        elif time_to_critical <= 3:
            days_remaining = 3
            window_stage = "warning"
            recommendation = "Plan intervention within 48-72 hours."
            collapse_confidence = 75.0
        elif time_to_critical <= 7:
            days_remaining = time_to_critical
            window_stage = "warning"
            recommendation = f"Tactical action needed within {time_to_critical} days."
            collapse_confidence = 70.0
        else:
            days_remaining = 7
            window_stage = "stable"
            recommendation = "Trend stable. Resume normal monitoring cadence."
            collapse_confidence = 20.0
        
        # Calculate burn rate
        daily_burn = 0.0
        if projected_marketing_burn and days_remaining > 0:
            daily_burn = projected_marketing_burn / days_remaining if days_remaining > 0 else 0
        
        # Generate visualization
        viz = generate_countdown_visualization(days_remaining, window_stage)
        
        return {
            "decline_window": {
                "days_remaining": days_remaining,
                "window_stage": window_stage,
                "action_deadline": f"Next {days_remaining} days",
                "recommendation": recommendation,
                "projected_marketing_burn": round(projected_marketing_burn, 2) if projected_marketing_burn else None,
                "projected_burn_per_day": round(daily_burn, 2),
                "days_until_collapse": time_to_critical if time_to_critical else 999,
                "collapse_confidence": collapse_confidence,
                "visualization": viz
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error estimating decline window: {e}")
        return {
            "decline_window": {
                "days_remaining": 7,
                "window_stage": "stable",
                "action_deadline": "Next 7 days",
                "recommendation": "Unable to estimate. Resume standard monitoring."
            }
        }
