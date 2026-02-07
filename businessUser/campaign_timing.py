"""
Feature 7: Campaign Timing Recommendation
Tells when and how to run campaigns - with Grok API for hashtag generation
"""

import logging
import os
from datetime import datetime, timedelta
from .visualization_generators import generate_timeline_visualization

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

logger = logging.getLogger(__name__)


def generate_hashtags_and_timing(stage: int, topic: str = "trending") -> dict:
    """
    Use Grok API to generate relevant hashtags and optimal posting times.
    
    Args:
        stage: Lifecycle stage (1-5)
        topic: Content topic/keyword
    
    Returns:
        {
            "hashtags": [...],
            "optimal_posting_times": {...},
            "posting_frequency": str
        }
    """
    try:
        if not Anthropic:
            logger.warning("Anthropic client not available, using fallback hashtags")
            return generate_fallback_hashtags(stage, topic)
        
        api_key = os.getenv("GROK_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            logger.warning("No API key found in .env, using fallback hashtags")
            return generate_fallback_hashtags(stage, topic)
        
        client = Anthropic(api_key=api_key)
        
        stage_names = {1: "Emerging", 2: "Viral", 3: "Plateau", 4: "Declining", 5: "Dead"}
        stage_name = stage_names.get(stage, "Unknown")
        
        prompt = f"""Generate exactly 8 relevant hashtags for a {stage_name} {topic} content.
        
Return ONLY a JSON object with this exact structure:
{{
  "hashtags": ["#hashtag1", "#hashtag2", ..., "#hashtag8"],
  "primary_hashtag": "#main_hashtag",
  "trending_related": ["#trending1", "#trending2"],
  "niche_specific": ["#niche1", "#niche2"]
}}

Make hashtags relevant to {stage_name} stage content about {topic}."""
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Parse JSON from response
        import json
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            hashtag_data = json.loads(json_match.group())
        else:
            hashtag_data = generate_fallback_hashtags(stage, topic)
        
        # Determine posting times based on stage
        posting_times = get_optimal_posting_times(stage)
        
        return {
            "hashtags": hashtag_data.get("hashtags", []),
            "primary_hashtag": hashtag_data.get("primary_hashtag", ""),
            "trending_related": hashtag_data.get("trending_related", []),
            "niche_specific": hashtag_data.get("niche_specific", []),
            "optimal_posting_times": posting_times,
            "posting_frequency": get_posting_frequency(stage)
        }
    
    except Exception as e:
        logger.error(f"Error generating hashtags via Grok: {e}")
        return generate_fallback_hashtags(stage, topic)


def generate_fallback_hashtags(stage: int, topic: str) -> dict:
    """
    Generate hashtags without API when Grok is unavailable.
    """
    hashtag_map = {
        1: {  # Emerging
            "hashtags": ["#emerging", "#newtrend", "#discovery", "#trending", "#watchthis", "#innovative", "#fresh", "#upandcoming"],
            "primary_hashtag": "#newtrend",
            "trending_related": ["#trending", "#viral"],
            "niche_specific": ["#discovery", "#innovative"]
        },
        2: {  # Viral
            "hashtags": ["#viral", "#trending", "#foryou", "#fyp", "#fy", "#popular", "#hot", "#mustwatch"],
            "primary_hashtag": "#viral",
            "trending_related": ["#trending", "#foryou"],
            "niche_specific": ["#popular", "#hot"]
        },
        3: {  # Plateau
            "hashtags": ["#established", "#community", "#fans", "#engaged", "#loyal", "#classic", "#favorite", "#ongoing"],
            "primary_hashtag": "#community",
            "trending_related": ["#established", "#engaged"],
            "niche_specific": ["#loyal", "#favorite"]
        },
        4: {  # Declining
            "hashtags": ["#classic", "#throwback", "#nostalgic", "#appreciation", "#legacy", "#original", "#timeless", "#remembering"],
            "primary_hashtag": "#throwback",
            "trending_related": ["#nostalgia", "#classic"],
            "niche_specific": ["#legacy", "#remembering"]
        },
        5: {  # Dead
            "hashtags": ["#archive", "#history", "#legacy", "#throwback", "#classic", "#dated", "#retro", "#memories"],
            "primary_hashtag": "#legacy",
            "trending_related": ["#archive", "#history"],
            "niche_specific": ["#retro", "#memories"]
        }
    }
    
    stage_hashtags = hashtag_map.get(stage, hashtag_map[3])
    stage_hashtags["optimal_posting_times"] = get_optimal_posting_times(stage)
    stage_hashtags["posting_frequency"] = get_posting_frequency(stage)
    
    return stage_hashtags


def get_optimal_posting_times(stage: int) -> dict:
    """
    Get optimal posting times based on lifecycle stage.
    
    Args:
        stage: Lifecycle stage (1-5)
    
    Returns:
        Dict with posting times and days
    """
    time_map = {
        1: {  # Emerging
            "times": ["08:00 AM", "02:00 PM", "07:00 PM"],
            "days": ["Tuesday", "Wednesday", "Thursday"],
            "frequency_per_day": 2,
            "rationale": "Test multiple times to find audience"
        },
        2: {  # Viral
            "times": ["07:00 AM", "12:00 PM", "06:00 PM", "09:00 PM"],
            "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "frequency_per_day": 3,
            "rationale": "Post frequently during peak viral window"
        },
        3: {  # Plateau
            "times": ["09:00 AM", "01:00 PM", "06:00 PM"],
            "days": ["Tuesday", "Wednesday", "Thursday", "Friday"],
            "frequency_per_day": 2,
            "rationale": "Maintain consistency with established audience"
        },
        4: {  # Declining
            "times": ["10:00 AM", "03:00 PM"],
            "days": ["Wednesday", "Thursday"],
            "frequency_per_day": 1,
            "rationale": "Lower frequency, focus on core audience"
        },
        5: {  # Dead
            "times": ["12:00 PM"],
            "days": ["Sunday"],
            "frequency_per_day": 0,
            "rationale": "Minimal posting - consider sunset or archive"
        }
    }
    
    return time_map.get(stage, time_map[3])


def get_posting_frequency(stage: int) -> str:
    """
    Get recommended posting frequency for stage.
    """
    freq_map = {
        1: "Every 12-24 hours (test discovery)",
        2: "3-4 times daily (capitalize on viral moment)",
        3: "2 times daily (maintain engagement)",
        4: "Once daily or every other day (preserve audience)",
        5: "Archive only (trend is dead)"
    }
    return freq_map.get(stage, "2 times daily")


def get_campaign_timing(
    lifecycle_stage: int,
    risk_score: float,
    roi_trend: str = "stable",
    content_topic: str = "trending"
) -> dict:
    """
    Recommend campaign timing, types, hashtags, and optimal posting times.
    
    Args:
        lifecycle_stage: 1-5
        risk_score: 0-100
        roi_trend: "up|stable|down"
        content_topic: Content topic for hashtag generation
    
    Returns:
        {
            "campaign_recommendation": {
                "recommended_window": str,
                "allowed_campaigns": [str],
                "avoid_campaigns": [str],
                "hashtags": {...},
                "posting_times": {...},
                "visualization": {...}
            }
        }
    """
    try:
        # Stage-based timing
        stage_windows = {
            1: "48-72 hours",    # Emerging
            2: "24-48 hours",    # Viral
            3: "24-48 hours",    # Plateau
            4: "12-24 hours",    # Decline
            5: "Not recommended" # Dead
        }
        
        recommended_window = stage_windows.get(lifecycle_stage, "24-48 hours")
        
        # Risk-based campaign selection
        if risk_score < 30:
            allowed = ["long_term_paid", "influencer_partnerships", "content_seeding"]
            avoid = ["flash_sales"]
        elif risk_score < 57:
            allowed = ["short_term_influencer", "content_seeding"]
            avoid = ["long_term_paid"]
        elif risk_score < 80:
            allowed = ["short_term_influencer"]
            avoid = ["long_term_paid", "content_seeding"]
        else:
            allowed = []
            avoid = ["all_campaigns"]
        
        # Generate hashtags and posting times using Grok API
        hashtag_data = generate_hashtags_and_timing(lifecycle_stage, content_topic)
        
        # Generate visualization
        viz = generate_timeline_visualization(allowed, lifecycle_stage)
        
        return {
            "campaign_recommendation": {
                "recommended_window": recommended_window,
                "allowed_campaigns": allowed,
                "avoid_campaigns": avoid,
                "hashtags": hashtag_data.get("hashtags", []),
                "primary_hashtag": hashtag_data.get("primary_hashtag", ""),
                "trending_hashtags": hashtag_data.get("trending_related", []),
                "niche_hashtags": hashtag_data.get("niche_specific", []),
                "optimal_posting_times": hashtag_data.get("optimal_posting_times", {}),
                "posting_frequency": hashtag_data.get("posting_frequency", ""),
                "visualization": viz
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error recommending campaign timing: {e}")
        return {
            "campaign_recommendation": {
                "recommended_window": "24-48 hours",
                "allowed_campaigns": [],
                "avoid_campaigns": [],
                "hashtags": [],
                "optimal_posting_times": {},
                "posting_frequency": ""
            }
        }
