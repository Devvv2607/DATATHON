"""
Feature 2: Executive Risk Decision Summary
Top-level business verdict for decision makers
"""

import logging

logger = logging.getLogger(__name__)


def get_risk_decision_summary(risk_data: dict) -> dict:
    """
    Convert numeric risk into business decision status.
    
    Args:
        risk_data: {
            "risk_score": 0-100,
            "alert_level": "green|yellow|orange|red",
            "confidence": "low|medium|high"
        }
    
    Returns:
        {
            "decision_summary": {
                "risk_score": float,
                "alert_level": str,
                "decision_status": str,
                "confidence": str,
                "message": str
            }
        }
    """
    try:
        risk_score = risk_data.get("risk_score", 0)
        alert_level = risk_data.get("alert_level", "green").lower()
        confidence = risk_data.get("confidence", "medium").lower()
        
        # Decision mapping
        decision_map = {
            "green": "safe",
            "yellow": "caution",
            "orange": "at_risk",
            "red": "exit"
        }
        
        message_map = {
            "green": "Trend is healthy. Safe to invest.",
            "yellow": "Early warning signs detected. Invest cautiously.",
            "orange": "Early decline signals detected. Invest cautiously.",
            "red": "Trend in critical decline. Recommend exit."
        }
        
        decision_status = decision_map.get(alert_level, "unknown")
        message = message_map.get(alert_level, "")
        
        return {
            "decision_summary": {
                "risk_score": risk_score,
                "alert_level": alert_level,
                "decision_status": decision_status,
                "confidence": confidence,
                "message": message
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error in risk decision summary: {e}")
        return {
            "decision_summary": {
                "risk_score": 0,
                "alert_level": "unknown",
                "decision_status": "unknown",
                "confidence": "low",
                "message": "Unable to determine decision status"
            }
        }
