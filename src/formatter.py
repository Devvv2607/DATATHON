"""JSON response formatting"""
import json
from datetime import datetime
from typing import Union
from dataclasses import asdict
from models import (
    TrendClassification, GrowthRecommendations, DeclineAnalysis,
    TrendData, ErrorResponse
)


class ResponseFormatter:
    """Formats analysis results as structured JSON or tables"""
    
    def __init__(self, output_format: str = "table"):
        """
        Initialize formatter.
        
        Args:
            output_format: "json" or "table" (default: table)
        """
        self.output_format = output_format
    
    def format_response(
        self,
        classification: TrendClassification,
        recommendations: Union[GrowthRecommendations, DeclineAnalysis, None],
        trend_data: TrendData
    ) -> str:
        """
        Format complete analysis as JSON or table.
        
        Args:
            classification: Trend classification
            recommendations: Growth recommendations or decline analysis
            trend_data: Original trend data
            
        Returns:
            Formatted string (JSON or table)
        """
        if self.output_format == "table":
            return self._format_as_table(classification, recommendations, trend_data)
        else:
            return self._format_as_json(classification, recommendations, trend_data)
    
    def _format_as_table(
        self,
        classification: TrendClassification,
        recommendations: Union[GrowthRecommendations, DeclineAnalysis, None],
        trend_data: TrendData
    ) -> str:
        """Format analysis as readable tables"""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append("BRAND TREND REVENUE INTELLIGENCE ANALYSIS")
        output.append("=" * 80)
        output.append(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        output.append("")
        
        # Trend Overview
        output.append("📊 TREND OVERVIEW")
        output.append("-" * 80)
        output.append(f"{'Domain:':<25} {trend_data.domain}")
        output.append(f"{'Keyword:':<25} {trend_data.keyword}")
        output.append(f"{'Classification:':<25} {classification.category.upper()}")
        output.append(f"{'Confidence:':<25} {classification.confidence:.1%}")
        output.append(f"{'Growth Rate:':<25} {classification.growth_rate:+.2f}% monthly")
        output.append(f"{'Current Interest:':<25} {trend_data.current_interest}/100")
        output.append(f"{'Peak Interest:':<25} {trend_data.peak_interest}/100")
        output.append("")
        output.append(f"{'Reasoning:':<25} {classification.reasoning}")
        output.append("")
        
        # Related Queries
        if trend_data.related_queries:
            output.append("🔍 RELATED QUERIES")
            output.append("-" * 80)
            for i, query in enumerate(trend_data.related_queries[:5], 1):
                output.append(f"  {i}. {query}")
            output.append("")
        
        # Recommendations based on type
        if isinstance(recommendations, GrowthRecommendations):
            output.extend(self._format_growth_recommendations(recommendations))
        elif isinstance(recommendations, DeclineAnalysis):
            output.extend(self._format_decline_analysis(recommendations))
        else:
            output.append("📋 RECOMMENDATION")
            output.append("-" * 80)
            output.append("Trend is STABLE. Monitor for changes and maintain current strategy.")
            output.append("")
        
        output.append("=" * 80)
        return "\n".join(output)
    
    def _format_growth_recommendations(self, recommendations: GrowthRecommendations) -> list:
        """Format growth recommendations as tables"""
        output = []
        
        output.append("💡 GROWTH RECOMMENDATIONS")
        output.append("=" * 80)
        output.append("")
        
        # Actions Table
        output.append("🎯 RECOMMENDED ACTIONS")
        output.append("-" * 80)
        output.append(f"{'#':<3} {'Action':<35} {'Priority':<10} {'Reach':<12} {'Conversion'}")
        output.append("-" * 80)
        for i, action in enumerate(recommendations.actions, 1):
            output.append(f"{i:<3} {action.title[:34]:<35} {action.implementation_priority.upper():<10} {action.expected_reach_increase:<12} {action.expected_conversion_impact}")
        output.append("")
        
        # Action Details
        output.append("📝 ACTION DETAILS")
        output.append("-" * 80)
        for i, action in enumerate(recommendations.actions, 1):
            output.append(f"{i}. {action.title}")
            output.append(f"   {action.description}")
            output.append("")
        
        # Budget Strategy
        output.append("💰 BUDGET STRATEGY")
        output.append("-" * 80)
        output.append(f"{'Recommendation:':<25} {recommendations.budget_strategy.recommendation}")
        output.append(f"{'Scaling Percentage:':<25} {recommendations.budget_strategy.scaling_percentage}")
        output.append(f"{'Rationale:':<25} {recommendations.budget_strategy.rationale}")
        output.append("")
        
        # Content Angles
        output.append("📝 CONTENT ANGLES")
        output.append("-" * 80)
        for i, angle in enumerate(recommendations.content_angles, 1):
            output.append(f"  {i}. {angle}")
        output.append("")
        
        # Estimated Impact
        output.append("📈 ESTIMATED IMPACT")
        output.append("-" * 80)
        output.append(f"{'Reach Increase:':<25} {recommendations.estimated_impact.reach_increase}")
        output.append(f"{'Conversion Impact:':<25} {recommendations.estimated_impact.conversion_impact}")
        output.append(f"{'Revenue Potential:':<25} {recommendations.estimated_impact.revenue_potential}")
        output.append("")
        
        return output
    
    def _format_decline_analysis(self, analysis: DeclineAnalysis) -> list:
        """Format decline analysis as tables"""
        output = []
        
        output.append("⚠️  DECLINE ANALYSIS & PIVOT STRATEGY")
        output.append("=" * 80)
        output.append("")
        
        # Risk Assessment
        output.append("🚨 RISK ASSESSMENT")
        output.append("-" * 80)
        output.append(f"{'Days Until Collapse:':<30} {analysis.days_until_collapse} days (~{analysis.days_until_collapse//30} months)")
        output.append(f"{'Projected Marketing Burn:':<30} ${analysis.projected_marketing_burn:,.2f}")
        output.append(f"{'Recommendation:':<30} {analysis.recommendation}")
        output.append("")
        
        # Revival Conditions (if applicable)
        if analysis.revival_conditions:
            output.append("🔧 REVIVAL CONDITIONS (If Attempting Revival)")
            output.append("-" * 80)
            for i, condition in enumerate(analysis.revival_conditions, 1):
                output.append(f"  {i}. {condition}")
            output.append("")
        
        # Alternative Trends
        output.append("🔄 ALTERNATIVE TRENDS TO PIVOT TOWARD")
        output.append("-" * 80)
        output.append(f"{'#':<3} {'Keyword':<30} {'Growth':<12} {'Difficulty':<12} {'Relevance'}")
        output.append("-" * 80)
        for i, alt in enumerate(analysis.alternative_trends, 1):
            output.append(f"{i:<3} {alt.keyword[:29]:<30} {alt.growth_rate:+.1f}%{'':<7} {alt.entry_difficulty.upper():<12} {alt.relevance_to_domain[:30]}")
        output.append("")
        
        # Pivot Strategy
        output.append("🎯 PIVOT STRATEGY")
        output.append("-" * 80)
        output.append(f"{'Approach:':<15} {analysis.pivot_strategy.approach}")
        output.append(f"{'Timeline:':<15} {analysis.pivot_strategy.timeline}")
        output.append("")
        output.append("Key Actions:")
        for i, action in enumerate(analysis.pivot_strategy.key_actions, 1):
            output.append(f"  {i}. {action}")
        output.append("")
        
        return output
    
    def _format_as_json(
        self,
        classification: TrendClassification,
        recommendations: Union[GrowthRecommendations, DeclineAnalysis, None],
        trend_data: TrendData
    ) -> str:
        """Format analysis as JSON (original format)"""
        try:
            # Build response structure
            response = {
                "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
                "domain": trend_data.domain,
                "trend_classification": {
                    "category": classification.category,
                    "confidence": classification.confidence,
                    "growth_rate": classification.growth_rate,
                    "reasoning": classification.reasoning
                },
                "trend_data": {
                    "keyword": trend_data.keyword,
                    "current_interest": trend_data.current_interest,
                    "peak_interest": trend_data.peak_interest,
                    "related_queries": trend_data.related_queries
                }
            }
            
            # Add recommendations based on type
            if isinstance(recommendations, GrowthRecommendations):
                response["recommendations"] = {
                    "type": "growth",
                    "actions": [
                        {
                            "title": action.title,
                            "description": action.description,
                            "expected_reach_increase": action.expected_reach_increase,
                            "expected_conversion_impact": action.expected_conversion_impact,
                            "implementation_priority": action.implementation_priority
                        }
                        for action in recommendations.actions
                    ],
                    "content_angles": recommendations.content_angles,
                    "budget_strategy": {
                        "recommendation": recommendations.budget_strategy.recommendation,
                        "scaling_percentage": recommendations.budget_strategy.scaling_percentage,
                        "rationale": recommendations.budget_strategy.rationale
                    },
                    "estimated_impact": {
                        "reach_increase": recommendations.estimated_impact.reach_increase,
                        "conversion_impact": recommendations.estimated_impact.conversion_impact,
                        "revenue_potential": recommendations.estimated_impact.revenue_potential
                    }
                }
            elif isinstance(recommendations, DeclineAnalysis):
                response["recommendations"] = {
                    "type": "decline",
                    "days_until_collapse": recommendations.days_until_collapse,
                    "projected_marketing_burn": recommendations.projected_marketing_burn,
                    "recommendation": recommendations.recommendation,
                    "alternative_trends": [
                        {
                            "keyword": alt.keyword,
                            "growth_rate": alt.growth_rate,
                            "relevance_to_domain": alt.relevance_to_domain,
                            "entry_difficulty": alt.entry_difficulty
                        }
                        for alt in recommendations.alternative_trends
                    ],
                    "pivot_strategy": {
                        "approach": recommendations.pivot_strategy.approach,
                        "timeline": recommendations.pivot_strategy.timeline,
                        "key_actions": recommendations.pivot_strategy.key_actions
                    }
                }
                
                if recommendations.revival_conditions:
                    response["recommendations"]["revival_conditions"] = recommendations.revival_conditions
            else:
                # Stable trend - minimal recommendations
                response["recommendations"] = {
                    "type": "stable",
                    "message": "Trend is stable. Monitor for changes and maintain current strategy."
                }
            
            # Validate JSON structure
            json_str = json.dumps(response, indent=2, ensure_ascii=False)
            
            # Verify it's valid by parsing it back
            json.loads(json_str)
            
            return json_str
            
        except Exception as e:
            # If formatting fails, return error response
            error = ErrorResponse(
                error_type="formatting_error",
                message=f"Failed to format response: {str(e)}",
                retry_possible=False
            )
            return json.dumps(asdict(error), indent=2)
    
    def format_error(self, error: ErrorResponse) -> str:
        """
        Format error as JSON.
        
        Args:
            error: ErrorResponse object
            
        Returns:
            JSON string
        """
        try:
            return json.dumps(asdict(error), indent=2, ensure_ascii=False)
        except:
            # Fallback error format
            return json.dumps({
                "status": "error",
                "message": "An error occurred",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }, indent=2)
