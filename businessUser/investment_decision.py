"""
Feature 5: Risk × ROI Investment Decision
Combines risk and ROI into clear investment action
"""

import logging

logger = logging.getLogger(__name__)


def get_investment_decision(risk_score: float, net_roi: float) -> dict:
    """
    Determine investment action based on risk and ROI.
    
    Args:
        risk_score: 0-100
        net_roi: numeric profit/loss
    
    Returns:
        {
            "investment_decision": {
                "recommended_action": "scale|tactical_only|monitor|exit",
                "rationale": str,
                "quadrant": str,
                "risk_x": float,
                "opportunity_y": float
            }
        }
    """
    try:
        # Classify risk and ROI
        is_high_risk = risk_score >= 57
        is_profitable = net_roi > 0
        
        # Decision matrix
        if not is_high_risk and is_profitable:
            action = "scale"
            rationale = "Low risk, high ROI - scale investment."
            quadrant = "scale"
        elif is_high_risk and is_profitable:
            action = "tactical_only"
            rationale = "High risk but profitable - use short-term tactics only."
            quadrant = "tactical_only"
        elif not is_high_risk and not is_profitable:
            action = "monitor"
            rationale = "Low risk but unprofitable - continue monitoring."
            quadrant = "monitor"
        else:  # High risk, unprofitable
            action = "exit"
            rationale = "High risk and unprofitable - recommend exit."
            quadrant = "exit"
        
        return {
            "investment_decision": {
                "recommended_action": action,
                "rationale": rationale,
                "quadrant": quadrant,
                "risk_x": round(risk_score, 1),
                "opportunity_y": round(net_roi, 2)
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error determining investment decision: {e}")
        return {
            "investment_decision": {
                "recommended_action": "monitor",
                "rationale": "Unable to determine action"
            }
        }
