"""
Explainable AI Engine - Feature #3
Generates structured decision justification for decline risk outputs
"""

import logging
from typing import List, Dict, Optional
from templates import STAGE_CONTEXT, RISK_INTERPRETATION, SIGNAL_IMPORTANCE

logger = logging.getLogger(__name__)

# ============================================================================
# MAIN EXPLANATION FUNCTION
# ============================================================================

def generate_explanation(
    feature2_output: Dict,
    analysis_date: str
) -> Dict:
    """
    Generate structured decision explainability object.
    
    Args:
        feature2_output: Complete output from Feature #2 (Early Decline Detection)
            Must include:
            - trend_id, trend_name
            - decline_risk_score, alert_level
            - signal_breakdown
            - lifecycle_stage, stage_name
            - confirmation, data_quality
            - historical_risk_scores (optional, list of {date, risk})
            - data_completeness (optional, {available_days, expected_days})
        
        analysis_date: ISO format date string
    
    Returns:
        Gold-standard explainability object
    """
    try:
        trend_id = feature2_output.get("trend_id", "unknown")
        trend_name = feature2_output.get("trend_name", "")
        risk_score = feature2_output.get("decline_risk_score", 0)
        alert_level = feature2_output.get("alert_level", "unknown")
        lifecycle_stage = feature2_output.get("lifecycle_stage", 3)
        stage_name = feature2_output.get("stage_name", "Unknown")
        signal_breakdown = feature2_output.get("signal_breakdown", {})
        historical_scores = feature2_output.get("historical_risk_scores", [])
        data_completeness = feature2_output.get("data_completeness", {})
        
        logger.info(f"Generating explanation for {trend_id} - Risk: {risk_score} ({alert_level})")
        
        # 1. Rank signals by impact
        ranked_signals = rank_signals_by_impact(signal_breakdown)
        
        # 2. Generate signal contributions
        signal_contributions = generate_signal_contributions(
            ranked_signals,
            signal_breakdown,
            lifecycle_stage,
            risk_score
        )
        
        # 3. Generate decision summary
        decision_summary = generate_decision_summary(risk_score, alert_level, lifecycle_stage)
        
        # 4. Generate temporal explanation (why now)
        decision_delta = generate_decision_delta(risk_score, historical_scores)
        
        # 5. Generate counterfactuals
        counterfactuals = generate_counterfactuals(
            risk_score,
            alert_level,
            ranked_signals,
            signal_breakdown
        )
        
        # 6. Calculate confidence
        confidence = calculate_confidence(
            risk_score,
            ranked_signals,
            historical_scores,
            data_completeness
        )
        
        logger.info(f"Explanation complete - Confidence: {confidence}")
        
        return {
            "trend_id": trend_id,
            "trend_name": trend_name,
            "analysis_date": analysis_date,
            "risk_score": risk_score,
            "alert_level": alert_level,
            "confidence": confidence,
            "lifecycle_stage": lifecycle_stage,
            "stage_name": stage_name,
            "decision_summary": decision_summary,
            "signal_contributions": signal_contributions,
            "decision_delta": decision_delta,
            "counterfactuals": counterfactuals
        }
    
    except Exception as e:
        logger.error(f"Explanation generation failed: {e}", exc_info=True)
        return {
            "trend_id": feature2_output.get("trend_id", "unknown"),
            "trend_name": feature2_output.get("trend_name", ""),
            "analysis_date": analysis_date,
            "risk_score": 0,
            "alert_level": "unknown",
            "confidence": "low",
            "lifecycle_stage": 3,
            "stage_name": "Unknown",
            "decision_summary": {
                "status": "error",
                "message": f"Unable to generate explanation: {str(e)}"
            },
            "signal_contributions": [],
            "decision_delta": {},
            "counterfactuals": {"risk_reduction_scenarios": [], "risk_escalation_scenarios": []}
        }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def rank_signals_by_impact(signal_breakdown: Dict) -> List[tuple]:
    """Rank signals by weighted impact"""
    signals_with_weight = []
    
    for signal_name, score in signal_breakdown.items():
        weight = SIGNAL_IMPORTANCE.get(signal_name, 0.5)
        impact = score * weight
        signals_with_weight.append((signal_name, score, impact))
    
    ranked = sorted(signals_with_weight, key=lambda x: x[2], reverse=True)
    return [(signal, score) for signal, score, _ in ranked]


def get_stage_context(lifecycle_stage: int) -> Dict:
    """Get context for lifecycle stage"""
    return STAGE_CONTEXT.get(lifecycle_stage, STAGE_CONTEXT[3])


# ============================================================================
# 1. SIGNAL CONTRIBUTIONS
# ============================================================================

def generate_signal_contributions(
    ranked_signals: List[tuple],
    signal_breakdown: Dict,
    lifecycle_stage: int,
    total_risk: float
) -> List[Dict]:
    """
    Generate top 3 signal contributions with impact estimation.
    
    Impact calculation: (signal_score / 100) * signal_weight * 100
    This gives approximate contribution to final risk score.
    """
    contributions = []
    stage_context = get_stage_context(lifecycle_stage)
    
    # Process top 3 signals
    for idx, (signal_name, signal_score) in enumerate(ranked_signals[:3]):
        weight = SIGNAL_IMPORTANCE.get(signal_name, 0.5)
        
        # Estimate impact on risk (approximate)
        impact = round((signal_score / 100) * weight * 30, 0)  # Scaled contribution
        
        # Get explanation template
        template = stage_context["signal_templates"].get(
            signal_name,
            f"{signal_name} at {signal_score:.0f}"
        )
        
        # Generate reason
        if signal_name == "engagement_drop":
            pct_drop = int((signal_score / 100) * 50)
            reason = f"Engagement declined {pct_drop}% compared to the recent baseline, indicating weakening audience interest."
        elif signal_name == "velocity_decline":
            reason = "Growth acceleration turned negative over the last two days, suggesting loss of momentum."
        elif signal_name == "creator_decline":
            pct_drop = int((signal_score / 100) * 45)
            reason = f"Reduced participation from high-reach creators ({pct_drop}% decline) indicates early content abandonment."
        elif signal_name == "quality_decline":
            pct_drop = int((signal_score / 100) * 40)
            reason = f"Content quality declined {pct_drop}%, reducing user engagement per post."
        else:
            reason = template
        
        contributions.append({
            "signal": signal_name,
            "signal_score": round(signal_score, 1),
            "impact_on_risk": int(impact),
            "reason": reason
        })
    
    return contributions


# ============================================================================
# 2. DECISION SUMMARY
# ============================================================================

def generate_decision_summary(risk_score: float, alert_level: str, lifecycle_stage: int) -> Dict:
    """Generate decision status and message"""
    stage_name = STAGE_CONTEXT.get(lifecycle_stage, {}).get("stage_name", "Unknown")
    
    # Determine status
    if alert_level == "green":
        status = "healthy"
        message = f"No decline signals detected. Trend remains healthy during {stage_name} phase."
    elif alert_level == "yellow":
        status = "warning"
        message = f"Early warning signals detected. Close monitoring recommended during {stage_name} phase."
    elif alert_level == "orange":
        status = "at_risk"
        message = f"Early decline signals detected as the trend exits its {stage_name} phase."
    else:  # red
        status = "critical"
        message = f"Critical decline situation. Immediate investigation required. Trend in advanced {stage_name} phase contraction."
    
    return {
        "status": status,
        "message": message
    }


# ============================================================================
# 3. DECISION DELTA (Why Now?)
# ============================================================================

def generate_decision_delta(current_risk: float, historical_scores: List[Dict]) -> Dict:
    """
    Explain why risk changed now by comparing to previous day.
    """
    if not historical_scores or len(historical_scores) < 2:
        return {
            "previous_risk_score": None,
            "current_risk_score": current_risk,
            "primary_change": "Insufficient historical data to determine change trajectory."
        }
    
    # Get previous day score (last in list before current)
    previous_risk = round(historical_scores[-2]["risk"], 1) if len(historical_scores) >= 2 else None
    current_risk_rounded = round(current_risk, 1)
    
    if previous_risk is None:
        return {
            "previous_risk_score": None,
            "current_risk_score": current_risk_rounded,
            "primary_change": "Initial risk assessment."
        }
    
    risk_delta = current_risk_rounded - previous_risk
    
    if abs(risk_delta) < 5:
        primary_change = f"Minimal change in risk indicators ({risk_delta:+.1f} points)."
    elif risk_delta > 20:
        primary_change = f"Sharp escalation in decline signals. A sharp engagement drop combined with declining creator activity in the last 24 hours."
    elif risk_delta > 10:
        primary_change = f"Moderate increase ({risk_delta:+.1f} points). Multi-signal degradation observed over last 24-48 hours."
    elif risk_delta < -10:
        primary_change = f"Notable improvement ({risk_delta:+.1f} points). Key signals stabilizing."
    else:
        primary_change = f"Gradual change ({risk_delta:+.1f} points). Continued monitoring recommended."
    
    return {
        "previous_risk_score": previous_risk,
        "current_risk_score": current_risk_rounded,
        "primary_change": primary_change
    }


# ============================================================================
# 4. COUNTERFACTUALS (What-If)
# ============================================================================

def generate_counterfactuals(
    risk_score: float,
    alert_level: str,
    ranked_signals: List[tuple],
    signal_breakdown: Dict
) -> Dict:
    """
    Generate rule-based counterfactuals for risk reduction/escalation.
    """
    reduction_scenarios = []
    escalation_scenarios = []
    
    # Get primary signal
    primary_signal, primary_score = ranked_signals[0] if ranked_signals else (None, 0)
    
    # ===== RISK REDUCTION SCENARIOS =====
    if alert_level == "red":
        # Red → Orange
        reduction_scenarios.append(
            "If engagement rebounds by approximately 15% within the next 48 hours, the risk level would likely downgrade to Orange."
        )
        # Red → Orange via creator
        if signal_breakdown.get("creator_decline", 0) > 70:
            reduction_scenarios.append(
                "If creator participation stabilizes for two consecutive days, overall risk would decrease by approximately 12-15 points."
            )
    
    elif alert_level == "orange":
        # Orange → Yellow
        reduction_scenarios.append(
            "If engagement rebounds by approximately 15% within the next 48 hours, the risk level would likely downgrade to Yellow."
        )
        if signal_breakdown.get("velocity_decline", 0) > 60:
            reduction_scenarios.append(
                "If growth acceleration turns positive (even slightly), overall risk would decrease by 8-12 points."
            )
    
    elif alert_level == "yellow":
        # Yellow → Green
        reduction_scenarios.append(
            "Sustained engagement growth over the next 3 days would likely downgrade the alert to Green."
        )
    
    # ===== RISK ESCALATION SCENARIOS =====
    if alert_level == "green":
        escalation_scenarios.append(
            "A sharp engagement drop of 20% or more in the next day could escalate the alert to Yellow."
        )
    elif alert_level == "yellow":
        escalation_scenarios.append(
            "An additional engagement drop of 15% would likely escalate the alert to Orange."
        )
    elif alert_level == "orange":
        escalation_scenarios.append(
            "An additional engagement drop of 10% would likely escalate the alert to Red."
        )
    elif alert_level == "red":
        escalation_scenarios.append(
            "Further deterioration in engagement or creator participation could indicate trend irreversibility."
        )
    
    return {
        "risk_reduction_scenarios": reduction_scenarios,
        "risk_escalation_scenarios": escalation_scenarios
    }


# ============================================================================
# 5. CONFIDENCE ESTIMATION
# ============================================================================

def calculate_confidence(
    risk_score: float,
    ranked_signals: List[tuple],
    historical_scores: List[Dict],
    data_completeness: Dict
) -> str:
    """
    Calculate confidence based on:
    - Data completeness
    - Signal agreement
    - Historical stability
    """
    confidence_score = 0.0
    
    # 1. Data completeness (0-40 points)
    available_days = data_completeness.get("available_days", 0)
    expected_days = data_completeness.get("expected_days", 7)
    
    if available_days >= 6:
        confidence_score += 40
    elif available_days >= 4:
        confidence_score += 25
    elif available_days >= 2:
        confidence_score += 15
    
    # 2. Signal agreement (0-30 points)
    if len(ranked_signals) >= 2:
        top_signal_score = ranked_signals[0][1]
        second_signal_score = ranked_signals[1][1]
        
        # If all signals agreeing (within 20 points), confidence higher
        if abs(top_signal_score - second_signal_score) <= 20:
            confidence_score += 30
        elif abs(top_signal_score - second_signal_score) <= 35:
            confidence_score += 20
        else:
            confidence_score += 10
    
    # 3. Historical stability (0-30 points)
    if len(historical_scores) >= 2:
        recent_scores = [s["risk"] for s in historical_scores[-3:]]
        variance = max(recent_scores) - min(recent_scores) if len(recent_scores) > 1 else 0
        
        if variance <= 10:  # Stable
            confidence_score += 30
        elif variance <= 25:  # Moderately stable
            confidence_score += 18
        elif variance <= 40:  # Some volatility
            confidence_score += 8
    
    # Map score to confidence level
    if confidence_score >= 85:
        return "high"
    elif confidence_score >= 60:
        return "medium"
    else:
        return "low"


# ============================================================================
# BATCH EXPLANATION
# ============================================================================

def explain_multiple_trends(
    feature2_outputs: List[Dict],
    analysis_date: str
) -> List[Dict]:
    """Generate explanations for multiple trends"""
    explanations = []
    
    for output in feature2_outputs:
        explanation = generate_explanation(output, analysis_date)
        explanations.append(explanation)
    
    logger.info(f"Generated explanations for {len(explanations)} trends")
    return explanations
