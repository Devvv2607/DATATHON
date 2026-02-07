"""
Feature 10: Executive Summary / One-Liner Takeaway
For C-suite consumption: one paragraph decision recommendation
"""

import logging

logger = logging.getLogger(__name__)


def get_executive_takeaway(risk_score: float, risk_trend: str, roi_summary: dict) -> dict:
    """
    Generate one-paragraph decision recommendation for leadership.
    
    Args:
        risk_score: 0-100 risk level
        risk_trend: "rising" | "stable" | "falling"
        roi_summary: {
            "net_roi": float (revenue - cost),
            "status": "profitable" | "breakeven" | "loss"
        }
    
    Returns:
        {
            "executive_summary": str,
            "recommendation": str
        }
    """
    try:
        # Decision framework
        if risk_score < 30:
            if roi_summary.get("status") == "profitable":
                rec = "Scale now: Low risk, profitability confirmed. Increase investment and frequency."
                summary = f"Green light to expand. Audience is healthy ({int(risk_score)} risk), ROI is positive. Recommend increasing content cadence and budget."
            else:
                rec = "Maintain: Low risk but ROI needs improvement. Monitor and optimize content."
                summary = f"Stable opportunity. Risk is low ({int(risk_score)}), but profitability needs work. Test new content types before scaling."
        
        elif risk_score < 57:
            if roi_summary.get("status") == "profitable":
                rec = "Tactical expansion: Moderate risk, but proven ROI. Proceed with caution on new initiatives."
                summary = f"Yellow light for growth. Audience shows caution signals ({int(risk_score)} risk), but revenue supports continued investment. Limit new campaigns to short-term windows only."
            else:
                rec = "Monitor closely: Moderate risk and uncertain ROI. Don't increase spend."
                summary = f"Proceed cautiously. Risk is rising ({int(risk_score)}), and ROI is questionable. Hold campaign expansion, focus on retention and quality."
        
        elif risk_score < 80:
            rec = "Active intervention: High risk. Prepare exit strategy or turnaround plan."
            summary = f"Red flag detected. Audience is declining ({int(risk_score)} risk) and ROI is at risk. Reallocate budget to safer channels; prepare to discontinue if trend continues."
        
        else:
            rec = "Exit: Critical risk. Discontinue or restructure immediately."
            summary = f"Critical status. Audience collapse imminent ({int(risk_score)} risk). Recommend immediate pivot or shutdown. Reallocate resources to healthier properties."
        
        # Adjust for trend
        if risk_trend == "falling":
            summary += " Recovery signs detected—stabilization possible within 7 days if intervention engaged."
        elif risk_trend == "rising":
            summary += " Situation deteriorating—accelerated action required."
        
        return {
            "executive_summary": summary,
            "recommendation": rec
        }
    
    except Exception as e:
        logger.error(f"✗ Error generating executive takeaway: {e}")
        return {
            "executive_summary": "Unable to generate summary.",
            "recommendation": "Require data review."
        }
