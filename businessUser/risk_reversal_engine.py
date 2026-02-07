"""
Feature 9: What-If / Risk Reversal Engine
Shows what conditions would change the decision
"""

import logging

logger = logging.getLogger(__name__)


def get_decision_levers(signal_breakdown: dict, risk_score: float = None) -> dict:
    """
    Identify rule-based conditions that would reverse/escalate risk AND enable revival.
    
    Args:
        signal_breakdown: {
            "engagement_drop": 0-100,
            "velocity_decline": 0-100,
            "creator_decline": 0-100,
            "quality_decline": 0-100
        }
        risk_score: Current risk score 0-100 (optional, for revival feasibility)
    
    Returns:
        {
            "decision_levers": {
                "risk_reduction": [str],
                "risk_escalation": [str],
                "revival_conditions": [str],
                "revival_feasibility": "easy" | "moderate" | "difficult"
            }
        }
    """
    try:
        reduction_levers = []
        escalation_levers = []
        revival_conditions = []
        
        # Engagement drop analysis
        eng_score = signal_breakdown.get("engagement_drop", 0)
        if eng_score > 60:
            reduction_levers.append("Engagement +15% within 48h → downgrade risk by ~10 points")
            escalation_levers.append("Engagement −10% → escalate to Red alert")
            revival_conditions.append("Significant external event driving new engagement")
            revival_conditions.append("Viral moment or influencer amplification")
        elif eng_score > 40:
            reduction_levers.append("Engagement +10% within 48h → downgrade risk")
            revival_conditions.append("Sustained engagement improvement over 3+ days")
        
        # Velocity decline analysis
        vel_score = signal_breakdown.get("velocity_decline", 0)
        if vel_score > 60:
            reduction_levers.append("Growth momentum stabilizes for 2 days → risk reduces by ~8 points")
            escalation_levers.append("Growth turns more negative → Red alert likely")
            revival_conditions.append("Market trend reversal in favor of niche")
        
        # Creator decline analysis
        creator_score = signal_breakdown.get("creator_decline", 0)
        if creator_score > 50:
            reduction_levers.append("Creator participation stabilizes → risk reduces by ~6 points")
            revival_conditions.append("New creator surge or collaboration opportunity")
        
        # Quality decline analysis
        quality_score = signal_breakdown.get("quality_decline", 0)
        if quality_score > 50:
            reduction_levers.append("Content quality improves → risk reduces by ~5 points")
            revival_conditions.append("New innovative content format discovery")
        
        # Default conditions if nothing high
        if not reduction_levers:
            reduction_levers.append("Overall trend stabilization → risk lowers")
        if not escalation_levers:
            escalation_levers.append("Multi-signal deterioration → risk escalates")
        if not revival_conditions:
            revival_conditions.append("Industry shift toward this category")
            revival_conditions.append("New product innovation in space")
        
        # Determine revival feasibility
        revival_feasibility = "difficult"
        
        if risk_score is not None:
            if risk_score < 50:
                revival_feasibility = "easy"
            elif risk_score < 70:
                revival_feasibility = "moderate"
            else:
                revival_feasibility = "difficult"
        else:
            avg_signal = (eng_score + vel_score + creator_score + quality_score) / 4
            if avg_signal < 40:
                revival_feasibility = "easy"
            elif avg_signal < 70:
                revival_feasibility = "moderate"
            else:
                revival_feasibility = "difficult"
        
        return {
            "decision_levers": {
                "risk_reduction": reduction_levers[:3],
                "risk_escalation": escalation_levers[:2],
                "revival_conditions": revival_conditions[:3],
                "revival_feasibility": revival_feasibility
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error generating decision levers: {e}")
        return {
            "decision_levers": {
                "risk_reduction": [],
                "risk_escalation": [],
                "revival_conditions": [],
                "revival_feasibility": "unknown"
            }
        }
