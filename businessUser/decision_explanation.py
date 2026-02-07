"""
Feature 6: Explainable Decision (Business-Friendly)
Explains why the system reached the decision
"""

import logging
from .visualization_generators import generate_signal_contribution_chart

logger = logging.getLogger(__name__)


def get_decision_explanation(
    signal_breakdown: dict,
    current_risk: float,
    previous_risk: float = None
) -> dict:
    """
    Explain the decision using top contributing signals.
    
    Args:
        signal_breakdown: {
            "engagement_drop": 0-100,
            "velocity_decline": 0-100,
            "creator_decline": 0-100,
            "quality_decline": 0-100
        }
        current_risk: Current risk score (0-100)
        previous_risk: Previous risk score (for comparison)
    
    Returns:
        {
            "decision_explanation": {
                "primary_driver": str,
                "secondary_drivers": [str],
                "why_now": str
            }
        }
    """
    try:
        # Rank signals by score
        signals_ranked = sorted(
            signal_breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        primary_driver = signals_ranked[0][0] if signals_ranked else "unknown"
        secondary_drivers = [s[0] for s in signals_ranked[1:3]] if len(signals_ranked) > 1 else []
        
        # Why now explanation
        if previous_risk is not None:
            risk_delta = current_risk - previous_risk
            if risk_delta > 10:
                why_now = f"Risk increased {risk_delta:.1f} points due to {primary_driver} deterioration in last 24h."
            elif risk_delta < -10:
                why_now = f"Risk decreased {abs(risk_delta):.1f} points due to signal improvement."
            else:
                why_now = "Risk shifted slightly due to multi-signal changes."
        else:
            why_now = f"Current risk driven primarily by {primary_driver}."
        
        # Generate visualization
        viz = generate_signal_contribution_chart(signal_breakdown, "Signal Breakdown")
        
        return {
            "decision_explanation": {
                "primary_driver": primary_driver,
                "secondary_drivers": secondary_drivers,
                "why_now": why_now,
                "visualization": viz
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error explaining decision: {e}")
        return {
            "decision_explanation": {
                "primary_driver": "unknown",
                "secondary_drivers": [],
                "why_now": "Unable to explain decision"
            }
        }
