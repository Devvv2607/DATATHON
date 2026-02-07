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
    
    # === LIFECYCLE STAGE ADJUSTMENT ===
    # Viral/Emergence trends: Reduce sensitivity (they're supposed to be growing!)
    # Plateau/Decline/Death: Normal or increased sensitivity
    stage_multiplier = 1.0
    if lifecycle_stage in [1, 2]:  # Emergence or Viral
        stage_multiplier = 0.5  # Reduce decline scores by 50% for growing trends
        logger.info(f"📊 Lifecycle stage {lifecycle_stage}: Applying 0.5x multiplier (growing trend)")
    elif lifecycle_stage == 5:  # Death
        stage_multiplier = 1.3  # Increase sensitivity for dead trends
        logger.info(f"📊 Lifecycle stage {lifecycle_stage}: Applying 1.3x multiplier (dead trend)")
    
    # Weighted aggregation
    weighted_sum = 0.0
    for signal_name, weight in SIGNAL_WEIGHTS.items():
        score = signal_scores.get(signal_name, 0.0)
        weighted_sum += score * weight
    
    # Apply stage multiplier
    decline_risk_score = weighted_sum * stage_multiplier
    decline_risk_score = min(max(decline_risk_score, 0.0), 100.0)
    
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
