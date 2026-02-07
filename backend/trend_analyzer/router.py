"""
FastAPI Router for Trend Analyzer
Twitter/X trend decline analysis with AI-powered explanations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from .trend_analyzer import TrendAnalyzer
from .explanation_engine import TrendAnalysisExplainer
from .schemas import TrendMetricsInput, TrendAnalysisOutput
from .sample_data import load_sample_data

router = APIRouter(prefix="/api/trend-analyzer", tags=["Trend Analyzer"])
logger = logging.getLogger(__name__)

# Initialize analyzer and explainer
analyzer = TrendAnalyzer()
explainer = TrendAnalysisExplainer()


class AnalyzeRequest(BaseModel):
    """Request model for trend analysis"""
    trend_name: str
    metrics: Optional[Dict[str, Any]] = None
    use_sample: bool = False
    sample_type: str = "declining"  # declining, growing, collapsed


class AnalyzeWithExplanationRequest(BaseModel):
    """Request model with AI explanations"""
    trend_name: str
    metrics: Optional[Dict[str, Any]] = None
    use_sample: bool = False
    sample_type: str = "declining"
    include_strategy: bool = True


@router.post("/analyze")
async def analyze_trend(request: AnalyzeRequest):
    """
    Analyze Twitter/X trend for decline signals
    
    Returns 8 decline cause types with confidence scores:
    - Engagement Decay
    - Content Saturation
    - Creator Disengagement
    - Influencer Dropoff
    - Posting Frequency Collapse
    - Algorithmic Visibility
    - Audience Fatigue
    - Competing Trend
    """
    try:
        # Get metrics (sample or provided)
        if request.use_sample or request.metrics is None:
            logger.info(f"Using sample data: {request.sample_type}")
            metrics_data = load_sample_data(request.sample_type)
        else:
            metrics_data = request.metrics
        
        # Add trend name
        metrics_data["trend_name"] = request.trend_name
        
        # Analyze
        result = analyzer.analyze(metrics_data)
        
        return {
            "success": True,
            "trend_name": request.trend_name,
            "analysis": result
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-with-ai")
async def analyze_with_ai_explanation(request: AnalyzeWithExplanationRequest):
    """
    Analyze trend with AI-powered explanations
    
    Uses Featherless AI (DeepSeek V3) to generate:
    - Natural language explanations for each decline cause
    - Recovery/exit strategy recommendations
    - Executive summary
    """
    try:
        # Get metrics
        if request.use_sample or request.metrics is None:
            logger.info(f"Using sample data: {request.sample_type}")
            metrics_data = load_sample_data(request.sample_type)
        else:
            metrics_data = request.metrics
        
        metrics_data["trend_name"] = request.trend_name
        
        # Analyze
        analysis_result = analyzer.analyze(metrics_data)
        
        # Generate AI explanations
        logger.info("Generating AI explanations...")
        explained_causes = explainer.explain_decline_causes(
            analysis_result,
            metrics_data
        )
        
        # Generate strategy if requested
        strategy = None
        if request.include_strategy:
            logger.info("Generating strategy...")
            strategy = explainer.generate_strategy(
                analysis_result,
                metrics_data
            )
        
        return {
            "success": True,
            "trend_name": request.trend_name,
            "analysis": analysis_result,
            "ai_explanations": explained_causes,
            "strategy": strategy
        }
        
    except Exception as e:
        logger.error(f"AI analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sample-analysis")
async def get_sample_analysis(sample_type: str = "declining"):
    """
    Get analysis of sample data
    
    Available types: declining, growing, collapsed
    """
    try:
        metrics_data = load_sample_data(sample_type)
        metrics_data["trend_name"] = f"Sample {sample_type.title()} Trend"
        
        result = analyzer.analyze(metrics_data)
        
        return {
            "success": True,
            "sample_type": sample_type,
            "analysis": result
        }
        
    except Exception as e:
        logger.error(f"Sample analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check for Trend Analyzer service"""
    return {
        "status": "healthy",
        "service": "Trend Analyzer",
        "features": {
            "decline_detectors": 8,
            "ai_powered": True,
            "platforms": ["Twitter/X", "Reddit (fallback)"]
        }
    }
