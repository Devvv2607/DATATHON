"""
FastAPI Router for Trend Analysis Endpoints
All trend-related API endpoints with comprehensive documentation
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from trend_analysis.service import TrendAnalysisService
from trend_analysis.schema import (
    TrendOverview, TrendDetails, DeclinePrediction,
    ExplanationResponse, SimulationResponse, SimulationRequest,
    TrendsListResponse, PlatformType, TrendStatus
)

# Initialize router
router = APIRouter()

# Initialize service
service = TrendAnalysisService()

@router.get("/", response_model=TrendsListResponse)
async def get_trends(
    platforms: Optional[List[PlatformType]] = Query(None, description="Filter by platforms"),
    status: Optional[TrendStatus] = Query(None, description="Filter by trend status"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return")
):
    """
    Get list of trending topics with optional filters
    
    **Use cases:**
    - Dashboard overview of current trends
    - Filter by specific platforms
    - Focus on trends in certain lifecycle stages
    
    **Returns:** List of trends with key metrics
    """
    trends = service.get_all_trends(platforms=platforms, status=status, limit=limit)
    
    return TrendsListResponse(
        trends=trends,
        total=len(trends),
        page=1,
        page_size=limit
    )

@router.get("/{trend_id}", response_model=TrendDetails)
async def get_trend_detail(trend_id: str):
    """
    Get detailed information about a specific trend
    
    **Includes:**
    - Historical engagement and sentiment data
    - Top hashtags and influencers
    - Geographic distribution
    - Platform breakdown
    
    **Use cases:**
    - Deep dive into specific trend
    - Analyze historical performance
    - Identify key contributors
    """
    trend = service.get_trend_details(trend_id)
    
    if not trend:
        raise HTTPException(status_code=404, detail=f"Trend {trend_id} not found")
    
    return trend

@router.post("/predict/decline", response_model=DeclinePrediction)
async def predict_decline(trend_id: str = Query(..., description="Trend ID to analyze")):
    """
    Predict if and when a trend will decline
    
    **ML Model:** XGBoost classifier with 85%+ accuracy
    
    **Returns:**
    - Decline probability (0-1)
    - Estimated days until decline
    - Confidence level
    - Model version for tracking
    
    **Use cases:**
    - Risk assessment for marketing campaigns
    - Content strategy planning
    - Investment decisions
    """
    prediction = service.predict_decline(trend_id)
    
    if not prediction:
        raise HTTPException(status_code=404, detail=f"Trend {trend_id} not found")
    
    return prediction

@router.get("/explain/{trend_id}", response_model=ExplanationResponse)
async def explain_prediction(trend_id: str):
    """
    Get explainable AI insights for decline prediction
    
    **XAI Methods:**
    - SHAP values for feature attribution
    - Counterfactual scenarios
    - Natural language explanations
    
    **Returns:**
    - Why the trend is declining
    - Which factors are most impactful
    - What-if scenarios
    - Actionable recommendations
    
    **Use cases:**
    - Understand model decisions
    - Build trust in predictions
    - Identify intervention opportunities
    """
    explanation = service.explain_prediction(trend_id)
    
    if not explanation:
        raise HTTPException(status_code=404, detail=f"Trend {trend_id} not found")
    
    return explanation

@router.post("/simulate", response_model=SimulationResponse)
async def simulate_intervention(request: SimulationRequest):
    """
    Simulate what-if scenarios with interventions
    
    **Available interventions:**
    - `add_influencers`: Add N influencers (e.g., 5)
    - `increase_content_novelty`: Boost novelty by % (e.g., 0.2 for +20%)
    - `expand_platforms`: Launch on N new platforms
    - `boost_engagement`: Increase engagement campaigns
    
    **Example request:**
    ```json
    {
        "trend_id": "trend_1",
        "interventions": {
            "add_influencers": 5,
            "increase_content_novelty": 0.2
        },
        "forecast_days": 30
    }
    ```
    
    **Returns:**
    - Baseline vs intervention trajectory
    - Impact metrics (health improvement, engagement lift)
    - Cost estimates
    - ROI predictions
    
    **Use cases:**
    - Strategy planning
    - Budget allocation
    - A/B test planning
    """
    simulation = service.simulate_intervention(
        trend_id=request.trend_id,
        interventions=request.interventions,
        forecast_days=request.forecast_days
    )
    
    if not simulation:
        raise HTTPException(status_code=404, detail=f"Trend {request.trend_id} not found")
    
    return simulation

@router.get("/{trend_id}/trajectory")
async def get_trajectory(
    trend_id: str,
    days: int = Query(30, ge=7, le=90, description="Days to forecast")
):
    """
    Get predicted trend trajectory over time
    
    **Returns:** Daily predictions for:
    - Health score
    - Engagement rate
    - Sentiment
    - Confidence intervals
    
    **Use cases:**
    - Visualize trend lifecycle
    - Plan content calendar
    - Set alerts for decline
    """
    trajectory = service.get_trend_trajectory(trend_id, days)
    
    if not trajectory:
        raise HTTPException(status_code=404, detail=f"Trend {trend_id} not found")
    
    return {"trend_id": trend_id, "trajectory": trajectory, "forecast_days": days}

@router.get("/platform/{platform_name}")
async def get_platform_trends(
    platform_name: PlatformType,
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get top trends for a specific platform
    
    **Supported platforms:**
    - Twitter
    - Instagram
    - TikTok
    - Reddit
    - YouTube
    
    **Returns:** Platform-specific trending topics
    """
    trends = service.get_all_trends(platforms=[platform_name], limit=limit)
    
    return {
        "platform": platform_name,
        "trends": trends,
        "count": len(trends)
    }
