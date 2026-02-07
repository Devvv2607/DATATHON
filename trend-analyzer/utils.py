"""
Utility functions for the Trend Analyzer.
Includes metric calculations, confidence scoring, and recommendation logic.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
import json


@dataclass
class MetricThresholds:
    """Defines thresholds for detecting decline."""
    engagement_decay_threshold: float = -0.10  # -10% weekly
    content_saturation_unique_ratio: float = 0.30  # <30% unique = saturation
    creator_disengagement_threshold: float = -0.25  # -25% posting
    influencer_dropoff_threshold: float = -0.20  # -20% top accounts
    posting_volume_collapse_threshold: float = 0.50  # <50% of previous
    audience_upvote_ratio_threshold: float = 0.50  # <50% upvotes = bad
    competing_trend_share_threshold: float = 0.30  # <30% of category = loss


def calculate_engagement_decay_score(
    x_velocity: float = None,
    reddit_comment_change: float = None,
    tiktok_engagement_change: float = None
) -> float:
    """
    Calculate engagement decay score (0-1).
    
    Args:
        x_velocity: X engagement weekly velocity
        reddit_comment_change: Reddit comment % change
        tiktok_engagement_change: TikTok engagement % change
    
    Returns:
        Composite score (0-1) indicating engagement decay severity
    """
    scores = []
    
    if x_velocity is not None and x_velocity < -0.1:
        scores.append(min(1.0, abs(x_velocity) * 2))
    
    if reddit_comment_change is not None and reddit_comment_change < -0.15:
        scores.append(min(1.0, abs(reddit_comment_change) * 1.5))
    
    if tiktok_engagement_change is not None and tiktok_engagement_change < -0.15:
        scores.append(min(1.0, abs(tiktok_engagement_change) * 1.5))
    
    if not scores:
        return 0.0
    
    return sum(scores) / len(scores)


def calculate_content_saturation_score(
    x_unique_ratio: float = None,
    reddit_variance: float = None,
    tiktok_reuse_rate: float = None
) -> float:
    """Calculate content saturation score (0-1)."""
    scores = []
    
    if x_unique_ratio is not None and x_unique_ratio < 0.3:
        scores.append(1.0 - x_unique_ratio)
    
    if reddit_variance is not None and reddit_variance < 0.4:
        scores.append(0.8 - reddit_variance)
    
    if tiktok_reuse_rate is not None and tiktok_reuse_rate > 0.6:
        scores.append(tiktok_reuse_rate)
    
    if not scores:
        return 0.0
    
    return min(1.0, sum(scores) / len(scores))


def calculate_creator_disengagement_score(
    x_posting_change: float = None,
    reddit_posting_change: float = None,
    tiktok_video_change: float = None
) -> float:
    """Calculate creator disengagement score (0-1)."""
    scores = []
    
    if x_posting_change is not None and x_posting_change < -0.3:
        scores.append(min(1.0, abs(x_posting_change)))
    
    if reddit_posting_change is not None and reddit_posting_change < -0.25:
        scores.append(min(1.0, abs(reddit_posting_change)))
    
    if tiktok_video_change is not None and tiktok_video_change < -0.35:
        scores.append(min(1.0, abs(tiktok_video_change)))
    
    if not scores:
        return 0.0
    
    return min(1.0, sum(scores) / len(scores))


def calculate_posting_volume_collapse_score(
    x_volume_change: float = None,
    reddit_volume_change: float = None,
    tiktok_volume_change: float = None
) -> float:
    """Calculate posting volume collapse score (0-1)."""
    scores = []
    
    if x_volume_change is not None:
        curr_ratio = x_volume_change if x_volume_change > 0 else 0.1
        if curr_ratio < 0.5:
            scores.append(1.0 - curr_ratio)
    
    if reddit_volume_change is not None:
        curr_ratio = reddit_volume_change if reddit_volume_change > 0 else 0.1
        if curr_ratio < 0.45:
            scores.append(1.0 - curr_ratio)
    
    if tiktok_volume_change is not None:
        curr_ratio = tiktok_volume_change if tiktok_volume_change > 0 else 0.1
        if curr_ratio < 0.4:
            scores.append(1.0 - curr_ratio)
    
    if not scores:
        return 0.0
    
    return min(1.0, sum(scores) / len(scores))


def normalize_confidence(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Normalize a value to 0-1 range."""
    if max_val == min_val:
        return 0.5
    return min(1.0, max(0.0, (value - min_val) / (max_val - min_val)))


def calculate_weighted_average(
    values: List[float], weights: List[float] = None
) -> float:
    """Calculate weighted average of values."""
    if not values:
        return 0.0
    
    if weights is None:
        weights = [1.0] * len(values)
    
    if len(values) != len(weights):
        raise ValueError("Values and weights must have same length")
    
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0
    
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    return weighted_sum / total_weight


def detect_platform_health(metrics: Dict[str, Any]) -> Dict[str, str]:
    """
    Determine health status for each platform.
    
    Returns:
        Dictionary mapping platform names to health status (Declining|Stable|Growing)
    """
    health = {}
    
    # X/Twitter health
    if "x" in metrics and metrics["x"]:
        velocity = metrics["x"].get("weekly_engagement_velocity", 0)
        if velocity < -0.1:
            health["X"] = "Declining"
        elif velocity > 0.05:
            health["X"] = "Growing"
        else:
            health["X"] = "Stable"
    
    # Reddit health
    if "reddit" in metrics and metrics["reddit"]:
        growth = metrics["reddit"].get("subscriber_growth_rate", 0)
        if growth < 0.01:
            health["Reddit"] = "Declining"
        elif growth > 0.05:
            health["Reddit"] = "Growing"
        else:
            health["Reddit"] = "Stable"
    
    # TikTok health
    if "tiktok" in metrics and metrics["tiktok"]:
        views_decline = metrics["tiktok"].get("hashtag_views_decline", 0)
        if views_decline < -0.1:
            health["TikTok"] = "Declining"
        elif views_decline > 0.1:
            health["TikTok"] = "Growing"
        else:
            health["TikTok"] = "Stable"
    
    # Google Trends health
    if "google_trends" in metrics and metrics["google_trends"]:
        slope = metrics["google_trends"].get("search_interest_slope", 0)
        if slope < -0.1:
            health["Google_Trends"] = "Declining"
        elif slope > 0.1:
            health["Google_Trends"] = "Growing"
        else:
            health["Google_Trends"] = "Stable"
    
    return health


def merge_trend_analyses(analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple trend analyses (e.g., same trend analyzed at different times).
    Useful for trend tracking over time.
    
    Args:
        analyses: List of analysis results from different time periods
    
    Returns:
        Merged analysis showing trend trajectory
    """
    if not analyses:
        return {}
    
    latest = analyses[-1]
    
    # Calculate momentum (is decline accelerating?)
    if len(analyses) >= 2:
        prev_decline = analyses[-2].get("decline_probability", 0.5)
        curr_decline = latest.get("decline_probability", 0.5)
        momentum = curr_decline - prev_decline
    else:
        momentum = 0.0
    
    # Identify emerging causes
    all_causes = {}
    for analysis in analyses:
        for cause in analysis.get("root_causes", []):
            cause_type = cause["cause_type"]
            if cause_type not in all_causes:
                all_causes[cause_type] = []
            all_causes[cause_type].append(cause["confidence"])
    
    emerging_causes = []
    for cause_type, confidences in all_causes.items():
        if len(confidences) > 1:
            trend_direction = confidences[-1] - confidences[0]
            if trend_direction > 0.2:  # Confidence increasing
                emerging_causes.append({
                    "cause_type": cause_type,
                    "trend_direction": "worsening",
                    "confidence_change": round(trend_direction, 3)
                })
    
    return {
        "total_analyses": len(analyses),
        "time_span_days": (len(analyses) - 1) * 7,  # Assuming weekly analysis
        "latest_analysis": latest,
        "momentum": round(momentum, 3),
        "momentum_direction": "accelerating_decline" if momentum > 0.1 else "stabilizing" if momentum < -0.1 else "neutral",
        "emerging_causes": emerging_causes,
    }


def generate_executive_summary(analysis: Dict[str, Any]) -> str:
    """Generate a plain-English executive summary of analysis."""
    trend_name = analysis.get("trend_name", "Unknown")
    status = analysis.get("trend_status", "UNKNOWN")
    decline_prob = analysis.get("decline_probability", 0)
    severity = analysis.get("severity_level", "UNKNOWN")
    causes = analysis.get("root_causes", [])
    
    summary = f"Trend: {trend_name}\n"
    summary += f"Status: {status} (Decline Probability: {decline_prob:.0%})\n"
    summary += f"Severity: {severity}\n\n"
    
    if causes:
        summary += "Root Causes (ranked by confidence):\n"
        for i, cause in enumerate(causes[:3], 1):
            summary += f"{i}. {cause['cause_type']} ({cause['confidence']:.0%} confidence)\n"
            summary += f"   {cause['business_explanation']}\n"
        summary += "\n"
    
    actions = analysis.get("recommended_actions", [])
    if actions:
        summary += "Recommended Actions:\n"
        for action in actions[:3]:
            summary += f"- [{action['priority']}] {action['description']}\n"
    
    return summary


def export_analysis_report(analysis: Dict[str, Any], format: str = "json") -> str:
    """
    Export analysis in different formats.
    
    Args:
        analysis: Analysis result dictionary
        format: "json", "csv", or "markdown"
    
    Returns:
        Formatted string representation
    """
    if format == "json":
        return json.dumps(analysis, indent=2)
    
    elif format == "markdown":
        md = f"# Trend Analysis: {analysis.get('trend_name', 'Unknown')}\n\n"
        md += f"**Analysis Time:** {analysis.get('analysis_timestamp', 'N/A')}\n\n"
        md += f"## Summary\n"
        md += f"- **Status:** {analysis.get('trend_status', 'N/A')}\n"
        md += f"- **Decline Probability:** {analysis.get('decline_probability', 0):.0%}\n"
        md += f"- **Severity:** {analysis.get('severity_level', 'N/A')}\n\n"
        
        md += f"## Root Causes\n"
        for cause in analysis.get("root_causes", []):
            md += f"### {cause['cause_type']}\n"
            md += f"- **Confidence:** {cause['confidence']:.0%}\n"
            md += f"- **Platforms:** {', '.join(cause['affected_platforms'])}\n"
            md += f"- **Explanation:** {cause['business_explanation']}\n"
            md += f"- **Evidence:**\n"
            for evidence in cause['evidence']:
                md += f"  - {evidence}\n"
            md += "\n"
        
        md += f"## Recommended Actions\n"
        for action in analysis.get("recommended_actions", []):
            md += f"### {action['description']}\n"
            md += f"- **Type:** {action['action_type']}\n"
            md += f"- **Priority:** {action['priority']}\n"
            md += f"- **Timeframe:** {action['timeframe']}\n"
            md += f"- **Expected Impact:** {action['expected_impact']}\n\n"
        
        return md
    
    elif format == "csv":
        csv = "Metric,Value\n"
        csv += f"Trend Name,{analysis.get('trend_name', '')}\n"
        csv += f"Status,{analysis.get('trend_status', '')}\n"
        csv += f"Decline Probability,{analysis.get('decline_probability', '')}\n"
        csv += f"Severity,{analysis.get('severity_level', '')}\n"
        csv += f"Analysis Confidence,{analysis.get('confidence_in_analysis', '')}\n"
        csv += f"Number of Root Causes,{len(analysis.get('root_causes', []))}\n"
        csv += f"Number of Recommendations,{len(analysis.get('recommended_actions', []))}\n"
        return csv
    
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'json', 'markdown', or 'csv'")


if __name__ == "__main__":
    # Example usage
    print("Utility functions loaded successfully.")
    print(f"Available functions:")
    print("- calculate_engagement_decay_score()")
    print("- calculate_content_saturation_score()")
    print("- calculate_creator_disengagement_score()")
    print("- calculate_posting_volume_collapse_score()")
    print("- detect_platform_health()")
    print("- merge_trend_analyses()")
    print("- generate_executive_summary()")
    print("- export_analysis_report()")
