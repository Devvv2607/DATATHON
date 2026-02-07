"""
Mock data generator for testing without database
"""

from datetime import datetime, timedelta
from models import DailyMetric, LifecycleInfo, DeclineSignalRequest

def generate_declining_trend() -> DeclineSignalRequest:
    """Generate mock declining trend (test data)"""
    metrics = []
    base_date = datetime.utcnow() - timedelta(days=7)
    
    for i in range(7):
        date = base_date + timedelta(days=i)
        # Sharp decline after day 3
        if i < 3:
            multiplier = 1.0 + (i * 0.05)
        else:
            multiplier = 1.15 * (1.0 - (i - 3) * 0.15)
        
        metric = DailyMetric(
            date=date.strftime("%Y-%m-%d"),
            total_engagement=int(5000 * multiplier),
            views=int(50000 * multiplier),
            posts_count=int(100 * multiplier),
            creators_count=int(50 * multiplier * 0.9),
            avg_creator_followers=10000 * multiplier * 0.95,
            avg_comments_per_post=max(5, 15 - i),
            avg_engagement_per_post=max(10, 50 - i * 2)
        )
        metrics.append(metric)
    
    return DeclineSignalRequest(
        trend_id="test_declining",
        trend_name="Test Declining Trend",
        lifecycle_info=LifecycleInfo(
            trend_id="test_declining",
            trend_name="Test Declining Trend",
            lifecycle_stage=2,
            stage_name="Viral Explosion",
            days_in_stage=5,
            confidence=0.85
        ),
        daily_metrics=metrics
    )

def generate_healthy_trend() -> DeclineSignalRequest:
    """Generate mock healthy trend (baseline)"""
    metrics = []
    base_date = datetime.utcnow() - timedelta(days=7)
    
    for i in range(7):
        date = base_date + timedelta(days=i)
        multiplier = 1.0 + (i * 0.08)  # Steady growth
        
        metric = DailyMetric(
            date=date.strftime("%Y-%m-%d"),
            total_engagement=int(5000 * multiplier),
            views=int(50000 * multiplier * 1.1),
            posts_count=int(100 * multiplier),
            creators_count=int(50 * multiplier),
            avg_creator_followers=10000 * multiplier * 0.98,
            avg_comments_per_post=15,
            avg_engagement_per_post=50 + (i * 0.5)
        )
        metrics.append(metric)
    
    return DeclineSignalRequest(
        trend_id="test_healthy",
        trend_name="Test Healthy Trend",
        lifecycle_info=LifecycleInfo(
            trend_id="test_healthy",
            trend_name="Test Healthy Trend",
            lifecycle_stage=2,
            stage_name="Viral Explosion",
            days_in_stage=3,
            confidence=0.90
        ),
        daily_metrics=metrics
    )

def generate_no_feature1_trend() -> DeclineSignalRequest:
    """Generate trend WITHOUT lifecycle info (Feature #1 down)"""
    metrics = []
    base_date = datetime.utcnow() - timedelta(days=3)
    
    for i in range(3):
        date = base_date + timedelta(days=i)
        metric = DailyMetric(
            date=date.strftime("%Y-%m-%d"),
            total_engagement=5000 - (i * 500),
            views=50000 - (i * 5000),
            posts_count=100,
            creators_count=50 - i,
            avg_creator_followers=10000,
            avg_comments_per_post=15 - i,
            avg_engagement_per_post=50
        )
        metrics.append(metric)
    
    return DeclineSignalRequest(
        trend_id="test_fallback",
        trend_name="Test Fallback (No Feature #1)",
        lifecycle_info=None,  # Feature #1 API failed!
        daily_metrics=metrics
    )
