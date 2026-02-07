"""Signal 4: Quality Decline Detector"""

from typing import List, Tuple
from decline_signals.models import DailyMetric
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# SIGNAL 4: QUALITY DECLINE DETECTOR
# ============================================================================

def calculate_quality_decline(
    daily_metrics: List[DailyMetric],
    sensitivity: str,
    thresholds: dict
) -> Tuple[float, str]:
    """
    Detect content becoming spammy/low-effort (engagement per post & ratio).
    
    Returns: (risk_score: 0-100, explanation: str)
    """
    if len(daily_metrics) < 3:
        return 0.0, "Insufficient data"
    
    epp_drop_threshold = thresholds[sensitivity]["engagement_per_post_drop"]
    ratio_threshold = thresholds[sensitivity]["engagement_ratio_threshold"]
    max_score = thresholds[sensitivity]["max_score"]
    
    # Baseline (first days)
    baseline_period = min(3, len(daily_metrics) - 2)
    baseline_metrics = daily_metrics[:baseline_period]
    
    baseline_epp = sum(m.avg_engagement_per_post for m in baseline_metrics if m.posts_count > 0) / len([m for m in baseline_metrics if m.posts_count > 0]) if any(m.posts_count > 0 for m in baseline_metrics) else 1
    
    baseline_ev_ratios = [m.total_engagement / m.views for m in baseline_metrics if m.views > 0]
    baseline_ev_ratio = sum(baseline_ev_ratios) / len(baseline_ev_ratios) if baseline_ev_ratios else 0.05
    
    # Current (last days)
    current_period = min(3, len(daily_metrics) - 1)
    current_metrics = daily_metrics[-current_period:]
    
    current_epp = sum(m.avg_engagement_per_post for m in current_metrics if m.posts_count > 0) / len([m for m in current_metrics if m.posts_count > 0]) if any(m.posts_count > 0 for m in current_metrics) else 1
    
    current_ev_ratios = [m.total_engagement / m.views for m in current_metrics if m.views > 0]
    current_ev_ratio = sum(current_ev_ratios) / len(current_ev_ratios) if current_ev_ratios else 0.05
    
    # Calculate % changes
    epp_decline_pct = ((baseline_epp - current_epp) / baseline_epp * 100) if baseline_epp > 0 else 0
    ratio_decline_pct = ((baseline_ev_ratio - current_ev_ratio) / baseline_ev_ratio * 100) if baseline_ev_ratio > 0 else 0
    
    # Score
    if epp_decline_pct <= 0:
        epp_score = 0.0
    elif epp_decline_pct < epp_drop_threshold:
        epp_score = (epp_decline_pct / epp_drop_threshold) * max_score * 0.5
    else:
        normalized = min(epp_decline_pct / epp_drop_threshold, 2.0)
        epp_score = min(normalized * max_score, 100.0)
    
    if ratio_decline_pct <= 0:
        ratio_score = 0.0
    else:
        if current_ev_ratio < ratio_threshold:
            ratio_score = min((ratio_threshold - current_ev_ratio) / ratio_threshold * max_score, 100.0)
        else:
            ratio_score = (ratio_decline_pct / 20) * max_score * 0.3
    
    # Both declining = quality issue
    if epp_decline_pct > 0 and ratio_decline_pct > 0:
        risk_score = 0.6 * epp_score + 0.4 * ratio_score
    else:
        risk_score = max(epp_score, ratio_score)
    
    risk_score = min(risk_score, 100.0)
    explanation = f"EPP: {epp_decline_pct:.1f}%, Ratio: {ratio_decline_pct:.1f}%"
    logger.debug(f"Quality Decline: {explanation} → Score: {risk_score:.1f}")
    
    return float(risk_score), explanation
