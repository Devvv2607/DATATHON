"""
FastAPI Router for Explainable AI
Decision justification for decline risk alerts
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import logging
from datetime import datetime

from .explainer import generate_explanation

router = APIRouter(prefix="/api/explainable-ai", tags=["Explainable AI"])
logger = logging.getLogger(__name__)


class ExplainRequest(BaseModel):
    """Request model for generating explanations"""
    trend_id: str
    trend_name: str
    decline_risk_score: float
    alert_level: str
    lifecycle_stage: int
    stage_name: str
    confidence: str
    data_quality: str
    signal_breakdown: Dict[str, float]
    historical_risk_scores: Optional[List[Dict[str, Any]]] = None
    data_completeness: Optional[Dict[str, int]] = None
    analysis_date: Optional[str] = None


class ExplainResponse(BaseModel):
    """Response model with explanation"""
    success: bool
    explanation: Dict[str, Any]


@router.post("/explain", response_model=ExplainResponse)
async def explain_decline_risk(request: ExplainRequest):
    """
    Generate explanation for decline risk alert
    
    Takes Feature #2 (Decline Signals) output and generates:
    - Signal contributions ranked by impact
    - Decision summary (why this alert level)
    - Temporal explanation (why now)
    - Counterfactuals (what would change the alert)
    - Confidence scoring
    
    This is lifecycle-stage aware (different sensitivity per stage)
    """
    try:
        # Convert request to Feature #2 output format
        feature2_output = {
            "trend_id": request.trend_id,
            "trend_name": request.trend_name,
            "decline_risk_score": request.decline_risk_score,
            "alert_level": request.alert_level,
            "lifecycle_stage": request.lifecycle_stage,
            "stage_name": request.stage_name,
            "confidence": request.confidence,
            "data_quality": request.data_quality,
            "signal_breakdown": request.signal_breakdown,
            "historical_risk_scores": request.historical_risk_scores or [],
            "data_completeness": request.data_completeness or {
                "available_days": 7,
                "expected_days": 7
            }
        }
        
        # Use provided date or current datetime
        analysis_date = request.analysis_date or datetime.now().isoformat()
        
        # Generate explanation
        logger.info(f"Generating explanation for {request.trend_name}")
        explanation = generate_explanation(feature2_output, analysis_date)
        
        return {
            "success": True,
            "explanation": explanation
        }
        
    except Exception as e:
        logger.error(f"Explanation generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain-from-decline-signals")
async def explain_from_decline_signals(
    trend_name: str,
    decline_signals_response: Dict[str, Any]
):
    """
    Generate explanation directly from Decline Signals API response
    
    Convenience endpoint that accepts the full response from
    /api/decline-signals/analyze
    """
    try:
        # Extract relevant fields
        feature2_output = {
            "trend_id": decline_signals_response.get("trend_id", "unknown"),
            "trend_name": trend_name,
            "decline_risk_score": decline_signals_response.get("decline_risk_score", 0),
            "alert_level": decline_signals_response.get("alert_level", "green"),
            "lifecycle_stage": decline_signals_response.get("lifecycle", {}).get("stage", 3),
            "stage_name": decline_signals_response.get("lifecycle", {}).get("stage_name", "Unknown"),
            "confidence": decline_signals_response.get("confidence", "medium"),
            "data_quality": "complete",
            "signal_breakdown": decline_signals_response.get("signal_breakdown", {}),
            "historical_risk_scores": [],
            "data_completeness": {
                "available_days": 7,
                "expected_days": 7
            }
        }
        
        analysis_date = datetime.now().isoformat()
        
        # Generate explanation
        explanation = generate_explanation(feature2_output, analysis_date)
        
        return {
            "success": True,
            "explanation": explanation
        }
        
    except Exception as e:
        logger.error(f"Explanation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check for Explainable AI service"""
    return {
        "status": "healthy",
        "service": "Explainable AI",
        "features": {
            "explanation_type": "rule-based",
            "lifecycle_aware": True,
            "counterfactuals": True
        }
    }
