"""Aggregation Engine - Combines signals into final score"""

from typing import Dict, Tuple
from decline_signals.config import SIGNAL_WEIGHTS, get_alert_level
import logging

logger = logging.getLogger(__name__)

def aggregate_signals(
    signal_scores: Dict[str, float],
    lifecycle_stage: int,
    data_quality: str = "complete"
) -> Tuple[float, str, str]:
    """
    Combine 4 signals into single Decline Risk Score (0-100).
    
    Returns: (risk_score, alert_level, confidence)
    """
    
    # Weighted aggregation
    weighted_sum = 0.0
    for signal_name, weight in SIGNAL_WEIGHTS.items():
        score = signal_scores.get(signal_name, 0.0)
        weighted_sum += score * weight
    
    decline_risk_score = min(max(weighted_sum, 0.0), 100.0)
    
    # Confidence based on data quality
    if data_quality == "degraded":
        confidence = "low"
    elif lifecycle_stage == 5:  # Death stage
        confidence = "medium"
    else:
        confidence = "high"
    
    alert_level = get_alert_level(decline_risk_score)
    
    logger.info(
        f"Aggregation: {signal_scores} → Score: {decline_risk_score:.1f} ({alert_level})"
    )
    
    return decline_risk_score, alert_level, confidence
