"""Signal 2: Velocity Decline Detector"""

from typing import List, Tuple
from models import DailyMetric
import logging

logger = logging.getLogger(__name__)

def calculate_velocity_decline(
    daily_metrics: List[DailyMetric],
    sensitivity: str,
    thresholds: dict
) -> Tuple[float, str]:
    """
    Detect slowing growth (negative acceleration) = EARLIEST indicator.
    Also detect entering decline phase (transition from positive to negative growth).
    
    Returns: (risk_score: 0-100, explanation: str)
    """
    if len(daily_metrics) < 4:
        return 0.0, "Insufficient data"
    
    accel_threshold = thresholds[sensitivity]["accel_threshold"]
    max_score = thresholds[sensitivity]["max_score"]
    
    # Calculate growth rates
    growth_rates = []
    for i in range(1, len(daily_metrics)):
        prev = daily_metrics[i-1].total_engagement
        curr = daily_metrics[i].total_engagement
        if prev > 0:
            growth_rates.append((curr - prev) / prev)
        else:
            growth_rates.append(0.0)
    
    if len(growth_rates) < 2:
        return 0.0, "Insufficient growth data"
    
    # Calculate acceleration (recent period)
    period = min(3, len(growth_rates))
    recent_rates = growth_rates[-period:]
    
    accelerations = []
    for i in range(1, len(recent_rates)):
        accelerations.append(recent_rates[i] - recent_rates[i-1])
    
    avg_acceleration = sum(accelerations) / len(accelerations) if accelerations else 0.0
    current_growth = growth_rates[-1]
    
    risk_score = 0.0
    
    # CASE 1: Still growing (current_growth > 0)
    # Penalize if growth rate is slowing (negative acceleration)
    if current_growth > 0:
        if avg_acceleration < accel_threshold:
            # Growing but slowing significantly
            normalized = min(abs(avg_acceleration) / abs(accel_threshold), 2.0)
            risk_score = min(normalized * max_score, 100.0)
        else:
            # Growing but slowing less than threshold (low risk)
            risk_score = (abs(avg_acceleration) / abs(accel_threshold)) * max_score * 0.4
    
    # CASE 2: Entered decline phase (current_growth < 0)
    # Score based on magnitude of decline rate, not acceleration
    elif current_growth < 0:
        # Measure how steep the decline is
        # accel_threshold is negative (e.g., -0.08), so we compare absolute values
        decline_magnitude = abs(current_growth)
        threshold_magnitude = abs(accel_threshold)
        
        # If decline is steep, score it proportionally
        if decline_magnitude >= threshold_magnitude:
            # Decline is at or beyond threshold - high risk
            normalized = min(decline_magnitude / threshold_magnitude, 2.5)
            risk_score = min(normalized * max_score * 0.85, 100.0)
        else:
            # Mild decline - partial score
            risk_score = (decline_magnitude / threshold_magnitude) * max_score * 0.5
    
    else:
        # Zero growth - neutral
        risk_score = 0.0
    
    explanation = f"Acceleration: {avg_acceleration:.4f} (threshold: {accel_threshold})"
    logger.debug(f"Velocity Decline: {explanation} → Score: {risk_score:.1f}")
    
    return float(risk_score), explanation
