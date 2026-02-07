"""
Feature 1: Trend Business Context
Provides basic business framing for the trend
"""

import logging

logger = logging.getLogger(__name__)


def get_trend_context(trend_data: dict) -> dict:
    """
    Package trend metadata in business context.
    
    Args:
        trend_data: {
            "trend_id": str,
            "trend_name": str,
            "platform": str,
            "category": str,
            "lifecycle_stage": int (1-5),
            "stage_name": str,
            "last_updated": str
        }
    
    Returns:
        {
            "trend_context": {
                "trend_id": str,
                "trend_name": str,
                "platform": str,
                "category": str,
                "lifecycle_stage": str,
                "business_focus": str
            }
        }
    """
    try:
        stage_map = {
            1: "Emerging",
            2: "Viral",
            3: "Plateau",
            4: "Decline",
            5: "Dead"
        }
        
        lifecycle_stage = trend_data.get("lifecycle_stage", 3)
        
        return {
            "trend_context": {
                "trend_id": trend_data.get("trend_id", "unknown"),
                "trend_name": trend_data.get("trend_name", ""),
                "platform": trend_data.get("platform", "TikTok"),
                "category": trend_data.get("category", "General"),
                "lifecycle_stage": stage_map.get(lifecycle_stage, "Unknown"),
                "business_focus": "engagement_and_marketing",
                "last_updated": trend_data.get("last_updated", "")
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error getting trend context: {e}")
        return {
            "trend_context": {
                "trend_id": "unknown",
                "trend_name": "",
                "platform": "Unknown",
                "category": "Unknown",
                "lifecycle_stage": "Unknown",
                "business_focus": "engagement_and_marketing"
            }
        }
