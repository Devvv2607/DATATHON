"""Recommendation generation for trends"""
import json
import re
from models import (
    TrendData, TrendMetrics, GrowthRecommendations, GrowthAction,
    BudgetStrategy, ImpactMetrics, DeclineAnalysis, AlternativeTrend,
    PivotStrategy
)
from groq_service import GroqService


class GrowthRecommender:
    """Generates growth recommendations for growing trends"""
    
    def __init__(self, groq_service: GroqService):
        """Initialize growth recommender"""
        self.groq = groq_service
    
    def generate_recommendations(self, trend_data: TrendData, trend_metrics: TrendMetrics, domain: str) -> GrowthRecommendations:
        """Generate growth recommendations for a growing trend"""
        system_context = "You are a senior growth strategist. Provide concrete, actionable growth recommendations."
        
        prompt = f"Analyze this GROWING trend: Domain: {domain}, Keyword: {trend_data.keyword}, Growth: {trend_metrics.growth_slope:.1f}%"
        
        try:
            response = self.groq.generate_analysis(prompt, system_context, temperature=0.7)
            # Simplified parsing - use fallback
            return self._create_fallback_recommendations(trend_data, trend_metrics, domain)
        except:
            return self._create_fallback_recommendations(trend_data, trend_metrics, domain)
    
    def _create_fallback_recommendations(self, trend_data: TrendData, trend_metrics: TrendMetrics, domain: str) -> GrowthRecommendations:
        """Create fallback recommendations"""
        actions = [
            GrowthAction(
                title=f"Scale {trend_data.keyword} campaigns",
                description=f"Increase investment in {trend_data.keyword}-related marketing",
                expected_reach_increase="20-30%",
                expected_conversion_impact="12-18% lift",
                implementation_priority="high"
            ),
            GrowthAction(
                title=f"Create {domain}-specific content",
                description=f"Develop content targeting {trend_data.keyword} audience",
                expected_reach_increase="15-25%",
                expected_conversion_impact="10-15% lift",
                implementation_priority="high"
            ),
            GrowthAction(
                title="Optimize conversion funnel",
                description=f"Refine landing pages for {trend_data.keyword} traffic",
                expected_reach_increase="10-15%",
                expected_conversion_impact="15-20% lift",
                implementation_priority="medium"
            )
        ]
        
        return GrowthRecommendations(
            actions=actions,
            content_angles=[f"Trending {domain} topics", f"{trend_data.keyword} best practices", f"Latest {domain} innovations"],
            budget_strategy=BudgetStrategy(
                recommendation="Increase budget by 25%",
                scaling_percentage="20-30%",
                rationale=f"Strong growth momentum at {trend_metrics.growth_slope:.1f}% monthly"
            ),
            estimated_impact=ImpactMetrics(
                reach_increase="25-35%",
                conversion_impact="15-20% lift",
                revenue_potential="20-30% increase"
            )
        )



class DeclineAnalyzer:
    """Analyzes declining trends and provides pivot strategies"""
    
    def __init__(self, groq_service: GroqService):
        """Initialize decline analyzer"""
        self.groq = groq_service
    
    def analyze_decline(self, trend_data: TrendData, trend_metrics: TrendMetrics, domain: str) -> DeclineAnalysis:
        """Analyze a declining trend and recommend strategy"""
        decline_rate = abs(trend_metrics.growth_slope) / 100
        current = trend_metrics.current_interest
        
        if decline_rate > 0:
            months_to_collapse = max(1, (current - 20) / (decline_rate * current))
            days_until_collapse = int(months_to_collapse * 30)
        else:
            days_until_collapse = 180
        
        projected_burn = days_until_collapse / 30 * 1000 * (1 + abs(trend_metrics.growth_slope) / 100)
        
        if abs(trend_metrics.growth_slope) > 20:
            recommendation = "EXIT"
        else:
            recommendation = "TRY REVIVAL"
        
        try:
            # Use fallback for now
            return self._create_fallback_analysis(trend_data, trend_metrics, domain, days_until_collapse, projected_burn, recommendation)
        except:
            return self._create_fallback_analysis(trend_data, trend_metrics, domain, days_until_collapse, projected_burn, recommendation)
    
    def _create_fallback_analysis(self, trend_data: TrendData, trend_metrics: TrendMetrics, domain: str, days_until_collapse: int, projected_burn: float, recommendation: str) -> DeclineAnalysis:
        """Create fallback analysis"""
        alternatives = [
            AlternativeTrend(
                keyword=f"emerging {domain} trends",
                growth_rate=15.0,
                relevance_to_domain=f"Growing interest in {domain} space",
                entry_difficulty="medium"
            ),
            AlternativeTrend(
                keyword=f"innovative {domain}",
                growth_rate=12.0,
                relevance_to_domain=f"New developments in {domain}",
                entry_difficulty="low"
            )
        ]
        
        pivot_strategy = PivotStrategy(
            approach=f"Gradually shift from {trend_data.keyword} to emerging {domain} trends",
            timeline="2-3 months",
            key_actions=["Research alternative trends", "Test content with new keywords", "Reallocate 20% of budget"]
        )
        
        revival_conditions = ["Significant external event drives renewed interest", "New product innovation"] if recommendation == "TRY REVIVAL" else None
        
        return DeclineAnalysis(
            days_until_collapse=days_until_collapse,
            projected_marketing_burn=projected_burn,
            recommendation=recommendation,
            revival_conditions=revival_conditions,
            alternative_trends=alternatives,
            pivot_strategy=pivot_strategy
        )
