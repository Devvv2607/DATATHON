"""Utility functions for the simulator."""

import uuid
from datetime import datetime
from typing import Tuple
from .types import RangeValue


def generate_scenario_id() -> str:
    """Generate a unique scenario ID."""
    return str(uuid.uuid4())


def get_current_timestamp() -> datetime:
    """Get current timestamp."""
    return datetime.utcnow()


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(max_val, value))


def normalize_to_range(value: float, min_val: float = 0, max_val: float = 100) -> float:
    """Normalize a value to a specific range."""
    return clamp(value, min_val, max_val)


def widen_range(range_value: RangeValue, factor: float) -> RangeValue:
    """
    Widen a range by a factor.
    
    Args:
        range_value: The range to widen
        factor: Widening factor (1.0 = no change, 1.5 = 50% wider)
        
    Returns:
        Widened range
    """
    if factor <= 1.0:
        return range_value
    
    mid = (range_value.min + range_value.max) / 2
    half_width = (range_value.max - range_value.min) / 2
    new_half_width = half_width * factor
    
    return RangeValue(
        min=mid - new_half_width,
        max=mid + new_half_width,
    )


def apply_multiplier_to_range(
    range_value: RangeValue,
    multiplier_min: float,
    multiplier_max: float,
) -> RangeValue:
    """
    Apply multiplier range to a value range.
    
    Args:
        range_value: The range to multiply
        multiplier_min: Minimum multiplier
        multiplier_max: Maximum multiplier
        
    Returns:
        Multiplied range
    """
    return RangeValue(
        min=range_value.min * multiplier_min,
        max=range_value.max * multiplier_max,
    )


def calculate_probability_from_range(
    range_value: RangeValue,
    threshold: float = 0,
    above_threshold: bool = True,
) -> float:
    """
    Calculate probability that a range value meets a threshold.
    
    Args:
        range_value: The range to evaluate
        threshold: The threshold value
        above_threshold: If True, calculate P(value >= threshold), else P(value < threshold)
        
    Returns:
        Probability as percentage (0-100)
    """
    if above_threshold:
        if range_value.min >= threshold:
            return 100.0
        elif range_value.max < threshold:
            return 0.0
        else:
            # Linear interpolation
            return ((range_value.max - threshold) / (range_value.max - range_value.min)) * 100
    else:
        if range_value.max < threshold:
            return 100.0
        elif range_value.min >= threshold:
            return 0.0
        else:
            # Linear interpolation
            return ((threshold - range_value.min) / (range_value.max - range_value.min)) * 100


def get_range_width(range_value: RangeValue) -> float:
    """Get the width of a range."""
    return range_value.max - range_value.min


def get_range_midpoint(range_value: RangeValue) -> float:
    """Get the midpoint of a range."""
    return (range_value.min + range_value.max) / 2
