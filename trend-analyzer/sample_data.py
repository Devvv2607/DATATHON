"""
Sample data and utility functions for Twitter/X Trend Analyzer.
"""

import json
from pathlib import Path
from typing import Dict, Any


# Sample input data for testing - DECLINING TREND
SAMPLE_TREND_DATA = {
    "trend_name": "#TechTok",
    "x": {
        "tweet_volume": {"current": 45000, "previous_period": 52000},
        "weekly_engagement_velocity": -0.15,
        "unique_content_ratio": 0.22,
        "posts_per_day": {"current": 2800, "previous_period": 3200},
        "reach_per_tweet": {"current": 850, "previous_period": 1100},
        "impression_velocity": -0.18,
        "top_accounts_participation": {"current": 42, "previous_period": 55},
        "top_influencer_engagement": {"current": 12500, "previous_period": 18000},
        "sentiment_score": {"current": -0.08, "previous_period": 0.15},
        "days_since_peak": 28
    }
}

# Alternative sample: A trend showing growth
SAMPLE_TREND_GROWING = {
    "trend_name": "#AIRevolution",
    "x": {
        "tweet_volume": {"current": 125000, "previous_period": 95000},
        "weekly_engagement_velocity": 0.32,
        "unique_content_ratio": 0.65,
        "posts_per_day": {"current": 8900, "previous_period": 7200},
        "reach_per_tweet": {"current": 2200, "previous_period": 1800},
        "impression_velocity": 0.28,
        "top_accounts_participation": {"current": 128, "previous_period": 95},
        "top_influencer_engagement": {"current": 55000, "previous_period": 38000},
        "sentiment_score": {"current": 0.68, "previous_period": 0.52},
        "days_since_peak": 3
    }
}

# Alternative sample: Completely collapsed trend
SAMPLE_TREND_COLLAPSED = {
    "trend_name": "#OldMemeFormat",
    "x": {
        "tweet_volume": {"current": 2100, "previous_period": 18500},
        "weekly_engagement_velocity": -0.62,
        "unique_content_ratio": 0.08,
        "posts_per_day": {"current": 150, "previous_period": 1050},
        "reach_per_tweet": {"current": 120, "previous_period": 950},
        "impression_velocity": -0.58,
        "top_accounts_participation": {"current": 3, "previous_period": 38},
        "top_influencer_engagement": {"current": 250, "previous_period": 15000},
        "sentiment_score": {"current": -0.45, "previous_period": 0.22},
        "days_since_peak": 95
    }
}


def load_sample_data(sample_type: str = "declining") -> Dict[str, Any]:
    """Load sample X/Twitter trend data for testing."""
    samples = {
        "declining": SAMPLE_TREND_DATA,
        "growing": SAMPLE_TREND_GROWING,
        "collapsed": SAMPLE_TREND_COLLAPSED,
    }
    return samples.get(sample_type, SAMPLE_TREND_DATA)


def save_json_to_file(data: Dict[str, Any], filepath: str) -> None:
    """Save data as JSON to file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_json_from_file(filepath: str) -> Dict[str, Any]:
    """Load JSON data from file."""
    with open(filepath, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    # Save sample data to files
    save_json_to_file(SAMPLE_TREND_DATA, "sample_data_declining.json")
    save_json_to_file(SAMPLE_TREND_GROWING, "sample_data_growing.json")
    save_json_to_file(SAMPLE_TREND_COLLAPSED, "sample_data_collapsed.json")
    print("Sample data files created successfully.")
