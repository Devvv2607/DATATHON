"""
Feature 3: Engagement Health Snapshot
Translates technical signals into engagement health state
"""

import logging

logger = logging.getLogger(__name__)


def get_engagement_health(signal_breakdown: dict) -> dict:
    """
    Assess engagement health from signal scores.
    
    Args:
        signal_breakdown: {
            "engagement_drop": 0-100,
            "velocity_decline": 0-100,
            "creator_decline": 0-100,
            "quality_decline": 0-100
        }
    
    Returns:
        {
            "engagement_health": {
                "status": "healthy|weakening|declining",
                "explanation": str
            }
        }
    """
    try:
        eng_drop = signal_breakdown.get("engagement_drop", 0)
        vel_decline = signal_breakdown.get("velocity_decline", 0)
        creator_dec = signal_breakdown.get("creator_decline", 0)
        quality_dec = signal_breakdown.get("quality_decline", 0)
        
        signals = [eng_drop, vel_decline, creator_dec, quality_dec]
        high_signals = sum(1 for s in signals if s > 60)
        med_signals = sum(1 for s in signals if 40 <= s <= 60)
        
        # Status logic
        if high_signals >= 2:
            status = "declining"
            explanation = "Engagement and creator activity are falling simultaneously."
        elif high_signals == 1 and med_signals >= 1:
            status = "weakening"
            explanation = "Multiple engagement factors showing weakness."
        else:
            status = "healthy"
            explanation = "Engagement metrics remain stable."
        
        return {
            "engagement_health": {
                "status": status,
                "explanation": explanation
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error assessing engagement health: {e}")
        return {
            "engagement_health": {
                "status": "unknown",
                "explanation": "Unable to assess engagement health"
            }
        }
