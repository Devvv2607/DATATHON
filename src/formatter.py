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
    """Formats analysis results as structured JSON"""
    
    def format_response(
        self,
        classification: TrendClassification,
        recommendations: Union[GrowthRecommendations, DeclineAnalysis, None],
        trend_data: TrendData
    ) -> str:
        """
        Format complete analysis as JSON.
        
        Args:
            classification: Trend classification
            recommendations: Growth recommendations or decline analysis
            trend_data: Original trend data
            
        Returns:
            Pretty-printed JSON string
        """
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
