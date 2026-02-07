"""
Utility Functions for Trend Lifecycle Detection
"""

import logging
from datetime import datetime, timedelta
from typing import List, Tuple
import statistics

logger = logging.getLogger(__name__)


def calculate_slope(values: List[float]) -> float:
    """
    Calculate linear regression slope
    Returns: slope coefficient
    """
    if len(values) < 2:
        return 0.0
    
    n = len(values)
    x = list(range(n))
    
    x_mean = statistics.mean(x)
    y_mean = statistics.mean(values)
    
    numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def calculate_rolling_mean(values: List[float], window: int = 7) -> float:
    """
    Calculate rolling mean for recent window
    """
    if not values:
        return 0.0
    
    recent_values = values[-window:]
    return statistics.mean(recent_values) if recent_values else 0.0


def calculate_velocity(current: float, previous: float) -> float:
    """
    Calculate day-over-day velocity (percentage change)
    """
    if previous == 0:
        return 0.0 if current == 0 else 100.0
    
    return ((current - previous) / previous) * 100


def calculate_growth_rate(values: List[float], window: int = 7) -> float:
    """
    Calculate growth rate over recent window
    """
    if len(values) < 2:
        return 0.0
    
    recent = values[-window:]
    if len(recent) < 2:
        return 0.0
    
    start_val = recent[0]
    end_val = recent[-1]
    
    if start_val == 0:
        return 0.0 if end_val == 0 else 100.0
    
    return ((end_val - start_val) / start_val) * 100


def calculate_momentum(values: List[float], window: int = 3) -> float:
    """
    Calculate momentum as rolling average of recent growth rates
    """
    if len(values) < window + 1:
        return 0.0
    
    growth_rates = []
    for i in range(len(values) - window, len(values)):
        if i > 0:
            rate = calculate_velocity(values[i], values[i-1])
            growth_rates.append(rate)
    
    return statistics.mean(growth_rates) if growth_rates else 0.0


def detect_decay_signal(values: List[float], threshold: int = 5) -> float:
    """
    Detect sustained negative momentum
    Returns: decay signal strength (0-1)
    """
    if len(values) < threshold:
        return 0.0
    
    recent = values[-threshold:]
    negative_count = sum(1 for i in range(1, len(recent)) 
                        if recent[i] < recent[i-1])
    
    decay_ratio = negative_count / (len(recent) - 1)
    return decay_ratio


def calculate_engagement_saturation(
    current_engagement: float, 
    peak_engagement: float
) -> float:
    """
    Calculate how saturated engagement is relative to peak
    Returns: saturation level (0-1)
    """
    if peak_engagement == 0:
        return 0.0
    
    return min(current_engagement / peak_engagement, 1.0)


def normalize_confidence(base_confidence: float, signal_strength: float) -> float:
    """
    Normalize confidence score based on signal strength
    """
    adjusted = base_confidence * signal_strength
    return max(0.0, min(1.0, adjusted))


def get_date_range(days: int = 30) -> Tuple[datetime, datetime]:
    """
    Get date range for API queries
    Returns: (start_date, end_date)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division with default fallback"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError, ZeroDivisionError):
        return default


def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp value between min and max"""
    return max(min_val, min(max_val, value))
