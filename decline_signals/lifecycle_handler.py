"""
Lifecycle Stage Handler - Feature #1 Integration Point

IMPORTANT: This is a temporary placeholder for Feature #1 (Lifecycle Detection).
Your friend will replace this with actual lifecycle detection logic.

Until Feature #1 is ready, this provides safe fallbacks so the decline detection
engine works independently.
"""

import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

def resolve_lifecycle_stage(
    lifecycle_info: Optional[Dict] = None
) -> Tuple[int, str, str]:
    """
    Resolve lifecycle stage from Feature #1 input.
    
    PLACEHOLDER: When Feature #1 is ready, this function will receive real
    lifecycle detection data in the format below. For now, it provides safe defaults.
    
    Args:
        lifecycle_info: Dict from Feature #1 with keys:
            - lifecycle_stage: int (1=Emergence, 2=Viral, 3=Plateau, 4=Decline, 5=Death)
            - stage_name: str (e.g., "Viral Explosion")
            - days_in_stage: int (how many days in current stage)
            - confidence: float (0.0-1.0, how confident is detection)
    
    Returns:
        (stage: int, stage_name: str, data_quality: "complete" | "degraded")
    
    Note:
        - When lifecycle_info is None: Uses PLATEAU (stage 3) as safe default
        - data_quality = "complete" when Feature #1 provides data
        - data_quality = "degraded" when falling back to defaults
    """
    
    # Feature #1 unavailable - use safe fallback
    if lifecycle_info is None:
        logger.warning(
            "Feature #1 (Lifecycle Detection) unavailable. "
            "Using PLATEAU stage fallback (medium sensitivity). "
            "Data quality marked as 'degraded'."
        )
        return 3, "Plateau", "degraded"
    
    # Extract and validate stage number
    try:
        stage = int(lifecycle_info.get("lifecycle_stage", 3))
    except (TypeError, ValueError):
        logger.error(
            f"Invalid lifecycle_stage from Feature #1: "
            f"{lifecycle_info.get('lifecycle_stage')}. Falling back to PLATEAU."
        )
        return 3, "Plateau", "degraded"
    
    # Ensure stage is in valid range
    if stage < 1 or stage > 5:
        logger.warning(
            f"Feature #1 returned stage {stage} (out of range [1-5]). "
            f"Using PLATEAU fallback."
        )
        return 3, "Plateau", "degraded"
    
    # Get human-readable stage name
    stage_name = lifecycle_info.get("stage_name", f"Stage {stage}")
    
    # Feature #1 provided valid data
    logger.info(f"Using lifecycle from Feature #1: Stage {stage} ({stage_name})")
    return stage, stage_name, "complete"
