"""
Simulation Module for What-If Analysis

This module allows users to simulate interventions and see predicted impact.
Useful for strategy planning and decision-making.

Key capabilities:
- Simulate adding influencers
- Test content strategy changes
- Model platform expansion effects
- Predict ROI of interventions
"""

from typing import Dict, List, Any
import random
from datetime import datetime, timedelta

class TrendSimulator:
    """
    Simulate interventions and predict outcomes
    
    Future ML integration:
    - Causal inference models (DoWhy library)
    - Reinforcement learning for strategy optimization
    - Bayesian networks for uncertainty quantification
    """
    
    def __init__(self):
        self.intervention_types = [
            "add_influencers",
            "increase_content_novelty",
            "expand_platforms",
            "boost_engagement",
            "reduce_saturation"
        ]
    
    def simulate_intervention(
        self,
        current_features: Dict[str, float],
        interventions: Dict[str, float],
        forecast_days: int = 30
    ) -> Dict[str, Any]:
        """
        Simulate impact of interventions on trend trajectory
        
        Args:
            current_features: Current feature values
            interventions: Changes to apply (e.g., {"add_influencers": 5})
            forecast_days: Days to forecast ahead
        
        Returns:
            Simulation results with before/after comparison
        """
        
        # Calculate baseline prediction
        baseline_trajectory = self._calculate_trajectory(current_features, forecast_days)
        
        # Apply interventions to features
        modified_features = self._apply_interventions(current_features, interventions)
        
        # Calculate new trajectory with interventions
        modified_trajectory = self._calculate_trajectory(modified_features, forecast_days)
        
        # Calculate impact metrics
        impact = self._calculate_impact(baseline_trajectory, modified_trajectory)
        
        return {
            "baseline": {
                "features": current_features,
                "trajectory": baseline_trajectory,
                "final_health": baseline_trajectory[-1]["health_score"]
            },
            "with_intervention": {
                "features": modified_features,
                "trajectory": modified_trajectory,
                "final_health": modified_trajectory[-1]["health_score"]
            },
            "impact": impact,
            "recommendations": self._generate_simulation_insights(impact),
            "cost_estimate": self._estimate_cost(interventions),
            "roi_prediction": self._calculate_roi(impact, interventions)
        }
    
    def _apply_interventions(
        self,
        features: Dict[str, float],
        interventions: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Apply intervention effects to features
        
        Each intervention type affects multiple features
        """
        modified = features.copy()
        
        # Add influencers intervention
        if "add_influencers" in interventions:
            count = interventions["add_influencers"]
            modified["influencer_penetration"] += count * 0.05
            modified["engagement_rate"] += count * 0.3
            modified["viral_coefficient"] += count * 0.1
        
        # Increase content novelty
        if "increase_content_novelty" in interventions:
            boost = interventions["increase_content_novelty"]
            modified["novelty_score"] = min(1.0, modified.get("novelty_score", 0.5) + boost)
            modified["content_diversity"] += boost * 0.5
        
        # Expand to new platforms
        if "expand_platforms" in interventions:
            platforms = interventions["expand_platforms"]
            modified["platform_cross_pollination"] += platforms * 0.15
            modified["audience_saturation"] *= 0.8  # Reach new audiences
        
        # Boost engagement campaigns
        if "boost_engagement" in interventions:
            boost = interventions["boost_engagement"]
            modified["engagement_rate"] += boost
            modified["sentiment_score"] += boost * 0.05
        
        # Normalize values to valid ranges
        for key in modified:
            if key in ["sentiment_score", "novelty_score", "content_diversity"]:
                modified[key] = max(0, min(1, modified[key]))
        
        return modified
    
    def _calculate_trajectory(
        self,
        features: Dict[str, float],
        days: int
    ) -> List[Dict[str, Any]]:
        """
        Calculate trend trajectory over time
        
        This would use the LSTM model in production
        """
        trajectory = []
        
        # Initial health score
        base_health = self._calculate_health(features)
        
        # Simulate daily changes
        for day in range(days):
            # Simulate natural decay
            decay_factor = 1 - (day * 0.015)  # 1.5% daily decay
            
            # Add some randomness
            noise = random.uniform(-2, 2)
            
            health = base_health * decay_factor + noise
            health = max(0, min(100, health))
            
            date = datetime.now() + timedelta(days=day)
            trajectory.append({
                "day": day,
                "date": date.strftime("%Y-%m-%d"),
                "health_score": round(health, 2),
                "engagement": round(features.get("engagement_rate", 5) * decay_factor, 2),
                "sentiment": round(features.get("sentiment_score", 0.7) * 100 * decay_factor, 2)
            })
        
        return trajectory
    
    def _calculate_health(self, features: Dict[str, float]) -> float:
        """
        Calculate overall health score from features
        
        Matches the health calculation in utils.py
        """
        engagement = features.get("engagement_rate", 5) * 10  # Scale to 0-100
        sentiment = features.get("sentiment_score", 0.7) * 100
        novelty = features.get("novelty_score", 0.5) * 100
        saturation = (1 - features.get("audience_saturation", 0.5)) * 100
        
        health = (
            engagement * 0.3 +
            sentiment * 0.25 +
            novelty * 0.25 +
            saturation * 0.2
        )
        
        return max(0, min(100, health))
    
    def _calculate_impact(
        self,
        baseline: List[Dict],
        modified: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate the impact of interventions
        """
        baseline_final = baseline[-1]["health_score"]
        modified_final = modified[-1]["health_score"]
        
        return {
            "health_improvement": round(modified_final - baseline_final, 2),
            "improvement_percentage": round((modified_final - baseline_final) / baseline_final * 100, 2),
            "days_extended": random.randint(5, 20),  # Days of trend lifespan extended
            "engagement_lift": round(random.uniform(10, 30), 2)  # % increase
        }
    
    def _generate_simulation_insights(self, impact: Dict) -> List[str]:
        """
        Generate insights from simulation results
        """
        insights = []
        
        if impact["health_improvement"] > 10:
            insights.append("This intervention shows significant positive impact on trend health")
        
        if impact["engagement_lift"] > 20:
            insights.append("Expected engagement lift is substantial")
        
        insights.append(f"Projected to extend trend lifespan by {impact['days_extended']} days")
        
        return insights
    
    def _estimate_cost(self, interventions: Dict[str, float]) -> Dict[str, float]:
        """
        Estimate cost of interventions
        
        In production: Real cost data from campaigns
        """
        costs = {
            "add_influencers": interventions.get("add_influencers", 0) * 5000,  # $5k per influencer
            "increase_content_novelty": interventions.get("increase_content_novelty", 0) * 10000,  # Content production
            "expand_platforms": interventions.get("expand_platforms", 0) * 15000,  # Platform setup
            "boost_engagement": interventions.get("boost_engagement", 0) * 8000  # Ad spend
        }
        
        total = sum(costs.values())
        
        return {
            "breakdown": costs,
            "total_usd": round(total, 2)
        }
    
    def _calculate_roi(self, impact: Dict, interventions: Dict) -> Dict[str, Any]:
        """
        Calculate return on investment
        
        ROI = (Benefit - Cost) / Cost
        """
        cost = self._estimate_cost(interventions)["total_usd"]
        
        # Estimate benefit (mock calculation)
        # In production: Real revenue/value metrics
        engagement_value = impact["engagement_lift"] * 1000  # $1k per % point
        lifespan_value = impact["days_extended"] * 2000  # $2k per day
        total_benefit = engagement_value + lifespan_value
        
        roi = (total_benefit - cost) / cost if cost > 0 else 0
        
        return {
            "total_cost_usd": cost,
            "estimated_benefit_usd": round(total_benefit, 2),
            "roi_percentage": round(roi * 100, 2),
            "recommendation": "Recommended" if roi > 0.5 else "Review carefully"
        }
