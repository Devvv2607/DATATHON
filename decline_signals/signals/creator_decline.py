"""Signal 3: Creator Activity Decline"""

from typing import List, Tuple
from models import DailyMetric
import logging

logger = logging.getLogger(__name__)

def calculate_creator_decline(
    daily_metrics: List[DailyMetric],
    sensitivity: str,
    thresholds: dict
) -> Tuple[float, str]:
    """
    Detect creators abandoning the trend (leading indicator).
    
    Creators are first movers - they leave before audiences notice.
    
    Returns: (risk_score: 0-100, explanation: str)
    """
    if len(daily_metrics) < 3:
        return 0.0, "Insufficient data"
    
    creator_drop_threshold = thresholds[sensitivity]["creator_drop_percent"]
    avg_follower_weight = thresholds[sensitivity]["avg_follower_weight"]
    max_score = thresholds[sensitivity]["max_score"]
    
    # Baseline (first days)
    baseline_period = min(3, len(daily_metrics) - 2)
    baseline_creators = sum(m.creators_count for m in daily_metrics[:baseline_period]) / baseline_period
    baseline_followers = sum(m.avg_creator_followers for m in daily_metrics[:baseline_period]) / baseline_period
    
    # Current (last days)
    current_period = min(3, len(daily_metrics) - 1)
    current_creators = sum(m.creators_count for m in daily_metrics[-current_period:]) / current_period
    current_followers = sum(m.avg_creator_followers for m in daily_metrics[-current_period:]) / current_period
    
    # Calculate % changes
    creator_decline_pct = ((baseline_creators - current_creators) / baseline_creators * 100) if baseline_creators > 0 else 0
    follower_decline_pct = ((baseline_followers - current_followers) / baseline_followers * 100) if baseline_followers > 0 else 0
    
    # Score
    risk_score = 0.0
    
    if creator_decline_pct <= 0:
        creator_score = 0.0
    elif creator_decline_pct < creator_drop_threshold:
        creator_score = (creator_decline_pct / creator_drop_threshold) * max_score * 0.5
    else:
        normalized = min(creator_decline_pct / creator_drop_threshold, 2.0)
        creator_score = min(normalized * max_score, 100.0)
    
    if follower_decline_pct <= 0:
        follower_score = 0.0
    else:
        follower_score = (follower_decline_pct / 50) * max_score * avg_follower_weight
    
    # Both declining = serious concern
    if creator_decline_pct > 0 and follower_decline_pct > 0:
        risk_score = 0.7 * creator_score + 0.3 * follower_score
    else:
        risk_score = max(creator_score, follower_score)
    
    risk_score = min(risk_score, 100.0)
    explanation = f"Creators: {creator_decline_pct:.1f}%, Followers: {follower_decline_pct:.1f}%"
    logger.debug(f"Creator Decline: {explanation} → Score: {risk_score:.1f}")
    
    return float(risk_score), explanation
