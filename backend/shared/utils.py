"""
Shared utilities for common operations across modules
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

def generate_mock_hashtag(prefix: str = "#") -> str:
    """Generate realistic-looking hashtags"""
    topics = [
        "AI", "Crypto", "Metaverse", "Sustainability", "Gaming", 
        "Fashion", "Fitness", "TechTrends", "NFT", "WebDev",
        "DataScience", "CloudComputing", "Blockchain", "IoT"
    ]
    return f"{prefix}{random.choice(topics)}{random.randint(2024, 2026)}"

def generate_time_series(days: int = 30, volatility: float = 0.2) -> List[Dict[str, Any]]:
    """
    Generate realistic time series data for trends
    
    Args:
        days: Number of days to generate
        volatility: How much the values fluctuate (0-1)
    
    Returns:
        List of {date, value} dictionaries
    """
    base_date = datetime.now() - timedelta(days=days)
    data = []
    
    # Simulate lifecycle: growth -> peak -> decline
    peak_day = days // 2
    
    for i in range(days):
        date = base_date + timedelta(days=i)
        
        # Lifecycle curve
        if i < peak_day:
            # Growth phase
            value = 20 + (80 / peak_day) * i
        else:
            # Decline phase
            value = 100 - (70 / (days - peak_day)) * (i - peak_day)
        
        # Add volatility
        noise = random.uniform(-volatility * 20, volatility * 20)
        value = max(0, min(100, value + noise))
        
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": round(value, 2)
        })
    
    return data

def calculate_velocity(data: List[float]) -> float:
    """
    Calculate trend velocity (rate of change)
    
    Args:
        data: List of numeric values over time
    
    Returns:
        Velocity score (-100 to 100)
    """
    if len(data) < 2:
        return 0.0
    
    # Simple linear regression slope
    n = len(data)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(data) / n
    
    numerator = sum((x[i] - x_mean) * (data[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    slope = numerator / denominator if denominator != 0 else 0
    
    # Normalize to -100 to 100 scale
    return max(-100, min(100, slope * 10))

def calculate_health_score(
    engagement: float,
    sentiment: float,
    velocity: float,
    novelty: float
) -> float:
    """
    Calculate overall trend health score
    
    Args:
        engagement: Engagement rate (0-100)
        sentiment: Sentiment score (0-100)
        velocity: Growth velocity (-100 to 100)
        novelty: Content novelty (0-100)
    
    Returns:
        Health score (0-100)
    """
    # Weighted average
    weights = {
        "engagement": 0.35,
        "sentiment": 0.25,
        "velocity": 0.25,
        "novelty": 0.15
    }
    
    # Normalize velocity to 0-100
    normalized_velocity = (velocity + 100) / 2
    
    score = (
        engagement * weights["engagement"] +
        sentiment * weights["sentiment"] +
        normalized_velocity * weights["velocity"] +
        novelty * weights["novelty"]
    )
    
    return round(max(0, min(100, score)), 2)

def format_large_number(num: int) -> str:
    """Format large numbers with K/M/B suffixes"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)
