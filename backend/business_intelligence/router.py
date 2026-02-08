"""
Business Intelligence API Router
Protected endpoints for business user analytics with real trend data
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path to import businessUser modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from auth.dependencies import require_business_user
from businessUser import (
    roi_attribution,
    investment_decision,
    executive_takeaway,
    campaign_timing,
    alternative_trends,
    risk_reversal_engine
)
from .domains import get_domain_specific_content, BUSINESS_DOMAINS
from trend_analysis.service import TrendAnalysisService

router = APIRouter(prefix="/api/business", tags=["Business Intelligence"])
trend_service = TrendAnalysisService()

# In-memory storage for business data (in production, use MongoDB)
business_data_store = {}


@router.get("/domains")
async def get_business_domains(
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Get available business domains
    """
    return {
        "success": True,
        "domains": BUSINESS_DOMAINS
    }


@router.post("/user-data")
async def save_business_data(
    request: dict,
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Save business user's custom data for personalized insights
    """
    try:
        # Get user email as identifier (more reliable than _id)
        user_id = current_user.get("email") or current_user.get("_id") or current_user.get("id", "unknown")
        domain = request.get("domain", "technology")
        data = request.get("data", {})
        
        # Store data (in production, save to MongoDB)
        storage_key = f"{user_id}_{domain}"
        business_data_store[storage_key] = {
            "user_id": user_id,
            "domain": domain,
            "data": data,
            "updated_at": "2026-02-08"
        }
        
        return {
            "success": True,
            "message": "Business data saved successfully",
            "storage_key": storage_key,
            "user": current_user.get("full_name", "User")
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@router.get("/user-data")
async def get_business_data(
    domain: str = Query("technology", description="Business domain key"),
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Retrieve business user's saved data
    """
    try:
        user_id = current_user.get("email") or current_user.get("_id") or current_user.get("id", "unknown")
        key = f"{user_id}_{domain}"
        
        if key in business_data_store:
            return {
                "success": True,
                "data": business_data_store[key]["data"]
            }
        else:
            return {
                "success": False,
                "message": "No data found for this domain"
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.post("/roi-analysis")
async def analyze_roi(
    domain: str = Query("technology", description="Business domain key"),
    trend_id: str = Query("trend_1", description="Trend ID to analyze"),
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Analyze ROI for content performance using real trend data
    """
    try:
        # Get real trend data
        trends = trend_service.get_all_trends()
        trend_data = next((t for t in trends if t["id"] == trend_id), trends[0] if trends else {})
        
        # Get domain-specific content
        domain_content = get_domain_specific_content(domain, trend_data)
        
        # Check if user has saved business data
        user_id = current_user.get("email") or current_user.get("_id") or current_user.get("id", "unknown")
        user_data_key = f"{user_id}_{domain}"
        user_has_data = user_data_key in business_data_store
        
        if user_has_data:
            # Use user's actual data
            saved_data = business_data_store[user_data_key]["data"]
            # Adjust content items with user's actual metrics
            for item in domain_content["content_items"]:
                item["revenue"] = float(saved_data.get("monthly_revenue", 15000)) / len(domain_content["content_items"])
                item["cost"] = float(saved_data.get("monthly_costs", 3000)) / len(domain_content["content_items"])
        
        # Analyze ROI using businessUser module
        result = roi_attribution.analyze_roi(domain_content["content_items"])
        
        return {
            "success": True,
            "domain": domain_content["domain"],
            "trend_analyzed": trend_data.get("name", "AI Revolution"),
            "platforms": trend_data.get("platforms", ["Twitter", "Instagram"]),
            "data": result,
            "domain_categories": domain_content["categories"],
            "user": current_user["full_name"],
            "personalized": user_has_data,
            "data_source": "Your business data" if user_has_data else "Sample data (add your data in Business Data page)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/investment-decision")
async def get_investment_decision(
    domain: str = Query("technology", description="Business domain key"),
    trend_id: str = Query("trend_1", description="Trend ID to analyze"),
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Get investment recommendation based on Risk×ROI matrix for specific domain
    """
    try:
        # Get real trend data
        trends = trend_service.get_all_trends()
        trend_data = next((t for t in trends if t["id"] == trend_id), trends[0] if trends else {})
        
        # Calculate risk and ROI from real data
        health_score = trend_data.get("metrics", {}).get("health_score", 70)
        risk_score = 100 - health_score  # Inverse of health
        
        # Get domain content for ROI calculation
        domain_content = get_domain_specific_content(domain, trend_data)
        roi_result = roi_attribution.analyze_roi(domain_content["content_items"])
        net_roi = roi_result.get("summary", {}).get("net_profit", 0)
        
        # Get investment decision
        decision = investment_decision.get_investment_decision(risk_score, net_roi)
        
        return {
            "success": True,
            "domain": BUSINESS_DOMAINS[domain]["name"],
            "trend": trend_data.get("name", "AI Revolution"),
            "decision": decision,
            "risk_score": risk_score,
            "net_roi": net_roi,
            "health_score": health_score,
            "user": current_user["full_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/executive-summary")
async def get_executive_summary(
    domain: str = Query("technology", description="Business domain key"),
    trend_id: str = Query("trend_1", description="Trend ID"),
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Generate C-suite executive summary for domain performance
    """
    try:
        # Get trend data
        trends = trend_service.get_all_trends()
        trend_data = next((t for t in trends if t["id"] == trend_id), trends[0] if trends else {})
        
        # Calculate risk and ROI
        health_score = trend_data.get("metrics", {}).get("health_score", 70)
        risk_score = 100 - health_score
        
        # Get domain content for ROI
        domain_content = get_domain_specific_content(domain, trend_data)
        roi_result = roi_attribution.analyze_roi(domain_content["content_items"])
        
        roi_summary = {
            "net_roi": roi_result.get("summary", {}).get("net_profit", 0),
            "status": "profitable" if roi_result.get("summary", {}).get("net_profit", 0) > 0 else "loss"
        }
        
        # Generate executive takeaway
        summary = executive_takeaway.get_executive_takeaway(risk_score, "stable", roi_summary)
        
        return {
            "success": True,
            "domain": BUSINESS_DOMAINS[domain]["name"],
            "trend": trend_data.get("name"),
            "summary": summary,
            "user": current_user["full_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/campaign-timing")
async def get_campaign_timing(
    domain: str = Query("technology", description="Business domain key"),
    trend_id: str = Query("trend_1", description="Trend ID"),
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Get optimal posting times and hashtags for domain campaigns
    """
    try:
        # Get trend data
        trends = trend_service.get_all_trends()
        trend_data = next((t for t in trends if t["id"] == trend_id), trends[0] if trends else {})
        
        # Get domain-specific hashtags
        domain_data = BUSINESS_DOMAINS[domain]
        
        # Generate timing and hashtags
        timing = campaign_timing.generate_hashtags_and_timing(
            "growth",
            trend_data.get("name", "Technology Trends")
        )
        
        # Add domain-specific hashtags
        timing["recommended_hashtags"] = domain_data["trends"] + timing.get("recommended_hashtags", [])[:3]
        
        return {
            "success": True,
            "domain": domain_data["name"],
            "timing": timing,
            "trend": trend_data.get("name"),
            "user": current_user["full_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alternative-trends")
async def find_alternative_trends(
    domain: str = Query("technology", description="Business domain key"),
    trend_id: str = Query("trend_1", description="Current trend ID"),
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Find alternative trends for pivot opportunities in domain
    """
    try:
        # Get current trend data
        trends = trend_service.get_all_trends()
        current_trend = next((t for t in trends if t["id"] == trend_id), trends[0] if trends else {})
        
        # Get domain-specific keywords
        domain_data = BUSINESS_DOMAINS[domain]
        
        # Find alternatives using businessUser module
        alternatives = alternative_trends.get_alternative_trends(
            current_keyword=current_trend.get("name", "AI Revolution"),
            current_growth=current_trend.get("metrics", {}).get("engagement_rate", 5.0),
            related_queries=domain_data["categories"]
        )
        
        return {
            "success": True,
            "domain": domain_data["name"],
            "current_trend": current_trend.get("name"),
            "alternatives": alternatives,
            "user": current_user["full_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/risk-analysis")
async def analyze_risk_scenarios(
    domain: str = Query("technology", description="Business domain key"),
    trend_id: str = Query("trend_1", description="Trend ID"),
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Analyze what-if scenarios for domain investment decisions
    """
    try:
        # Get trend data
        trends = trend_service.get_all_trends()
        trend_data = next((t for t in trends if t["id"] == trend_id), trends[0] if trends else {})
        
        # Calculate risk score
        health_score = trend_data.get("metrics", {}).get("health_score", 70)
        risk_score = 100 - health_score
        
        # Build signal breakdown
        signal_breakdown = {
            "engagement_drop": max(0, 100 - trend_data.get("metrics", {}).get("engagement_rate", 5.0) * 10),
            "velocity_decline": max(0, 50 - trend_data.get("metrics", {}).get("viral_coefficient", 1.5) * 20),
            "creator_decline": 30,  # Default
            "quality_decline": 25   # Default
        }
        
        # Get decision levers
        scenarios = risk_reversal_engine.get_decision_levers(signal_breakdown, risk_score)
        
        return {
            "success": True,
            "domain": BUSINESS_DOMAINS[domain]["name"],
            "trend": trend_data.get("name"),
            "scenarios": scenarios,
            "current_risk": risk_score,
            "current_health": health_score,
            "user": current_user["full_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/what-if-simulator")
async def run_what_if_simulation(
    request: dict,
    domain: str = Query("technology", description="Business domain key"),
    trend_id: str = Query("trend_1", description="Trend ID to analyze"),
    include_executive_summary: bool = Query(True, description="Include detailed executive summary"),
    current_user: dict = Depends(require_business_user)
) -> Dict[str, Any]:
    """
    Run What-If scenario simulation for campaign planning
    
    Integrates with What-If Simulator to provide:
    - Range-based growth projections (engagement, reach, creator participation)
    - ROI probabilities with confidence intervals
    - Risk trajectory analysis
    - Strategic recommendations (scale/test_small/monitor/avoid)
    - Sensitivity analysis for key assumptions
    - Optional executive summary
    """
    try:
        # Import simulator modules
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))
        from what_if_simulator.simulator import WhatIfSimulator
        from what_if_simulator.types import (
            ScenarioInput, TrendContext, CampaignStrategy, 
            Assumptions, Constraints
        )
        from what_if_simulator.external_systems import (
            ExternalSystemsClient,
            MockTrendLifecycleEngine,
            MockEarlyDeclineDetection,
            MockROIAttribution
        )
        from dataclasses import asdict
        
        # Get real trend data
        trends = trend_service.get_all_trends()
        trend_data = next((t for t in trends if t["id"] == trend_id), trends[0] if trends else {})
        
        # Calculate metrics for simulator
        health_score = trend_data.get("metrics", {}).get("health_score", 70)
        risk_score = 100 - health_score
        
        # Map trend status to lifecycle stage
        lifecycle_map = {
            "emerging": "emerging",
            "growing": "growth",
            "peak": "peak",
            "declining": "decline",
            "dormant": "dormant"
        }
        trend_status = trend_data.get("status", "growing").lower()
        lifecycle_stage = lifecycle_map.get(trend_status, "growth")
        
        # Determine confidence level
        if health_score > 70:
            confidence = "high"
        elif health_score > 50:
            confidence = "medium"
        else:
            confidence = "low"
        
        # Build TrendContext
        trend_context = TrendContext(
            trend_id=trend_id,
            trend_name=trend_data.get("name", "Unknown Trend"),
            platform=trend_data.get("platforms", ["Twitter"])[0] if trend_data.get("platforms") else "Twitter",
            lifecycle_stage=lifecycle_stage,
            current_risk_score=risk_score,
            confidence=confidence
        )
        
        # Build CampaignStrategy from request
        campaign_strategy = CampaignStrategy(
            campaign_type=request.get("campaign_type", "mixed"),
            budget_range=request.get("budget_range", "medium"),
            campaign_duration_days=request.get("campaign_duration_days", 30),
            creator_tier=request.get("creator_tier", "mixed"),
            content_intensity=request.get("content_intensity", "medium")
        )
        
        # Build Assumptions from request
        assumptions = Assumptions(
            engagement_trend=request.get("engagement_trend", "neutral"),
            creator_participation=request.get("creator_participation", "stable"),
            market_noise=request.get("market_noise", "medium")
        )
        
        # Build Constraints from request
        constraints = Constraints(
            risk_tolerance=request.get("risk_tolerance", "medium"),
            max_budget_cap=request.get("max_budget_cap", 50000)
        )
        
        # Create ScenarioInput
        scenario = ScenarioInput(
            scenario_id=request.get("scenario_id", f"{trend_id}_{domain}_scenario"),
            trend_context=trend_context,
            campaign_strategy=campaign_strategy,
            assumptions=assumptions,
            constraints=constraints
        )
        
        # Initialize simulator with mock external systems
        external_systems = ExternalSystemsClient(
            trend_lifecycle_engine=MockTrendLifecycleEngine(),
            early_decline_detection=MockEarlyDeclineDetection(),
            roi_attribution=MockROIAttribution()
        )
        simulator = WhatIfSimulator(external_systems)
        
        # Run simulation
        simulation_result = simulator.simulate(scenario, include_executive_summary=include_executive_summary)
        
        # Check for validation errors
        if hasattr(simulation_result, 'error_code'):
            return {
                "success": False,
                "error_code": simulation_result.error_code,
                "error_message": simulation_result.error_message,
                "validation_failures": [
                    {
                        "field": failure.field,
                        "message": failure.message,
                        "guidance": failure.guidance
                    }
                    for failure in simulation_result.validation_failures
                ],
                "domain": BUSINESS_DOMAINS[domain]["name"],
                "trend": trend_data.get("name"),
                "user": current_user["full_name"]
            }
        
        # Convert dataclass to dict
        result_dict = asdict(simulation_result)
        
        return {
            "success": True,
            "domain": BUSINESS_DOMAINS[domain]["name"],
            "trend": trend_data.get("name"),
            "trend_id": trend_id,
            "simulation": result_dict,
            "user": current_user["full_name"],
            "timestamp": "2026-02-08"
        }
        
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "domain": BUSINESS_DOMAINS.get(domain, {}).get("name", domain),
            "user": current_user.get("full_name", "Unknown")
        }


