"""Signal 1: Engagement Drop Detector"""

from typing import List, Tuple
from models import DailyMetric
import logging

logger = logging.getLogger(__name__)

def calculate_engagement_drop(
    daily_metrics: List[DailyMetric],
    sensitivity: str,
    thresholds: dict
) -> Tuple[float, str]:
    """
    Detect sudden/sustained drops in engagement volume.
    
    Returns: (risk_score: 0-100, explanation: str)
    """
    if len(daily_metrics) < 2:
        return 0.0, "Insufficient data"
    
    drop_percent_threshold = thresholds[sensitivity]["drop_percent"]
    period_days = min(thresholds[sensitivity]["period_days"], len(daily_metrics) - 1)
    max_score = thresholds[sensitivity]["max_score"]
    
    # Baseline: first few days
    baseline_period = min(3, len(daily_metrics) - period_days)
    baseline = sum(m.total_engagement for m in daily_metrics[:baseline_period]) / baseline_period if baseline_period > 0 else daily_metrics[0].total_engagement
    
    # Current: last few days
    current = sum(m.total_engagement for m in daily_metrics[-period_days:]) / period_days
    
    # Calculate % drop
    percent_drop = ((baseline - current) / baseline * 100) if baseline > 0 else 0
    
    if percent_drop <= 0:
        risk_score = 0.0
    elif percent_drop < drop_percent_threshold:
        risk_score = (percent_drop / drop_percent_threshold) * max_score * 0.5
    else:
        normalized = min(percent_drop / drop_percent_threshold, 2.0)
        risk_score = min(normalized * max_score, 100.0)
    
    explanation = f"Drop: {percent_drop:.1f}% (threshold: {drop_percent_threshold}%)"
    logger.debug(f"Engagement Drop: {explanation} → Score: {risk_score:.1f}")
    
    return float(risk_score), explanation
