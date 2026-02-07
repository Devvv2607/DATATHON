"""
Feature 11: Pivot Strategy Recommender
Suggests strategic actions for declining or underperforming trends
"""

import logging
from .visualization_generators import generate_pivot_roadmap

logger = logging.getLogger(__name__)


def get_pivot_strategy(classification: str, growth_rate: float, days_until_collapse: int, recommendation: str) -> dict:
    """
    Recommend strategic pivot actions based on trend health and urgency.
    
    Args:
        classification: Trend classification ("declining" | "emerging" | "plateau" | "critical")
        growth_rate: Daily growth rate (-100 to +100)
        days_until_collapse: Days before trend hits critical (0-180+)
        recommendation: Current recommendation ("TRY REVIVAL" | "PIVOT" | "MONITOR" | "EXIT")
    
    Returns:
        {
            "pivot_strategy": {
                "recommended_approach": str,
                "timeline_months": int,
                "key_actions": [str],
                "priority_level": "URGENT" | "HIGH" | "MEDIUM" | "LOW",
                "feasibility_score": float,
                "success_probability": float,
                "estimated_recovery_days": int,
                "resource_intensity": "LOW" | "MEDIUM" | "HIGH"
            }
        }
    """
    try:
        approach = "Monitor"
        timeline = 1
        actions = []
        priority = "MEDIUM"
        feasibility = 60.0
        success_prob = 50.0
        recovery_days = 30
        intensity = "MEDIUM"
        
        # Emergency dispatch logic
        if recommendation == "EXIT":
            approach = "Controlled Exit"
            timeline = 0
            actions = [
                "Wind down marketing spend over 7 days",
                "Capture remaining audience contacts for retargeting",
                "Document lessons learned for future content"
            ]
            priority = "URGENT"
            feasibility = 95.0
            success_prob = 100.0
            recovery_days = 0
            intensity = "LOW"
            
        elif days_until_collapse <= 2 and recommendation == "PIVOT":
            approach = "Immediate Pivot"
            timeline = 1
            actions = [
                "Test 3 alternative trends within 24 hours",
                "Shift 50% budget to highest-performing alternative",
                "Pause experiments on declining content",
                "Brief creative team on new direction"
            ]
            priority = "URGENT"
            feasibility = 70.0
            success_prob = 65.0
            recovery_days = 10
            intensity = "HIGH"
            
        elif days_until_collapse <= 7 and recommendation == "PIVOT":
            approach = "Accelerated Pivot"
            timeline = 2
            actions = [
                "Research and validate 5 alternative trends",
                "Create test content in top 2 alternatives",
                "Gradually shift audience to new content",
                "Build creator coalition around new trend",
                "Allocate 20-30% budget to alternatives"
            ]
            priority = "HIGH"
            feasibility = 80.0
            success_prob = 72.0
            recovery_days = 15
            intensity = "HIGH"
            
        elif recommendation == "TRY REVIVAL" and growth_rate > -30:
            approach = "Gradual Revival"
            timeline = 2
            actions = [
                "Identify what made earlier content successful",
                "Test refreshed content format in original niche",
                "Collaborate with high-performing creators",
                "Run targeted campaigns to early fans",
                "Monitor revival metrics daily"
            ]
            priority = "HIGH"
            feasibility = 75.0
            success_prob = 60.0
            recovery_days = 20
            intensity = "MEDIUM"
            
        elif recommendation == "TRY REVIVAL" and growth_rate <= -30:
            approach = "Strategic Pivot + Revival Testing"
            timeline = 3
            actions = [
                "Run parallel tests: revival vs pivot alternatives",
                "Allocate 70% to revival, 30% to alternatives",
                "Daily performance reporting and rebalancing",
                "Set clear success metrics (engagement ≥ 80% of peak)",
                "Decision point at day 10: continue or shift"
            ]
            priority = "HIGH"
            feasibility = 65.0
            success_prob = 55.0
            recovery_days = 25
            intensity = "HIGH"
            
        elif classification == "emerging" and growth_rate > 20:
            approach = "Aggressive Scale"
            timeline = 1
            actions = [
                "Increase marketing spend by 3-5x immediately",
                "Test variations on highest-performing format",
                "Expand creator pool 2x",
                "Daily optimization of ad spend",
                "Track growth rate and scale dynamically"
            ]
            priority = "HIGH"
            feasibility = 85.0
            success_prob = 80.0
            recovery_days = 0
            intensity = "HIGH"
            
        elif classification == "plateau" and growth_rate >= 0:
            approach = "Refresh + Audience Expansion"
            timeline = 2
            actions = [
                "Introduce new content variations within niche",
                "Target adjacent audience segments",
                "Partner with new creators in related spaces",
                "Refresh visuals and messaging quarterly",
                "Test new distribution channels"
            ]
            priority = "MEDIUM"
            feasibility = 80.0
            success_prob = 70.0
            recovery_days = 30
            intensity = "MEDIUM"
            
        else:
            approach = "Tactical Monitoring"
            timeline = 1
            actions = [
                "Daily metrics review (engagement, reach, velocity)",
                "Weekly creator performance assessment",
                "Monthly content format testing",
                "Maintain current spend with A/B testing"
            ]
            priority = "LOW"
            feasibility = 90.0
            success_prob = 75.0
            recovery_days = 0
            intensity = "LOW"
        
        # Generate visualization
        viz = generate_pivot_roadmap(actions, timeline, priority)
        
        return {
            "pivot_strategy": {
                "recommended_approach": approach,
                "timeline_months": timeline,
                "key_actions": actions,
                "priority_level": priority,
                "feasibility_score": feasibility,
                "success_probability": success_prob,
                "estimated_recovery_days": recovery_days,
                "resource_intensity": intensity,
                "visualization": viz
            }
        }
    
    except Exception as e:
        logger.error(f"✗ Error generating pivot strategy: {e}")
        return {
            "pivot_strategy": {
                "recommended_approach": "Monitor",
                "timeline_months": 1,
                "key_actions": [],
                "priority_level": "MEDIUM",
                "feasibility_score": 50.0,
                "success_probability": 50.0,
                "estimated_recovery_days": 0,
                "resource_intensity": "MEDIUM"
            }
        }
