"""
FastAPI REST service for Twitter/X Trend Analyzer.
Provides HTTP endpoints for Twitter trend analysis.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from trend_analyzer import TrendAnalyzer
from schemas import TrendMetricsInput, TrendAnalysisOutput, ErrorResponse
from sample_data import load_sample_data
from explanation_engine import TrendAnalysisExplainer


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="Twitter Trend Intelligence Engine",
    description="Twitter/X trend decline analysis with causal explanation",
    version="2.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = TrendAnalyzer(min_confidence_threshold=0.3)

# Initialize explanation engine
try:
    explainer = TrendAnalysisExplainer()
    explanation_available = True
except Exception as e:
    logger.warning(f"Explanation engine not available: {str(e)}")
    explainer = None
    explanation_available = False


@app.get("/", tags=["Info"])
def root():
    """Root endpoint - API information."""
    return {
        "name": "Twitter Trend Intelligence Engine",
        "version": "2.0.0",
        "description": "Analyzes X/Twitter trends to detect decline causes",
        "endpoints": {
            "POST /analyze": "Analyze a Twitter trend from provided metrics",
            "GET /health": "Health check",
            "GET /sample-analysis": "Run analysis on sample data",
        }
    }


@app.get("/health", tags=["Info"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "Trend Intelligence Engine"
    }


@app.post("/analyze", response_model=TrendAnalysisOutput, tags=["Analysis"])
def analyze_trend(metrics: TrendMetricsInput) -> dict:
    """
    Analyze a Twitter/X trend for decline causes.
    
    **Request Body:**
    - `trend_name` (string): Name of the trend, hashtag, or topic
    - `x` (object, required): X/Twitter platform metrics
    
    **Response:**
    Returns structured JSON with:
    - `trend_status`: GROWING, STABLE, DECLINING, or COLLAPSED
    - `decline_probability`: 0-1 confidence of decline
    - `severity_level`: STABLE, WARNING, CRITICAL, or COLLAPSED
    - `root_causes`: List of detected causes with confidence scores
    - `cross_platform_summary`: Health metrics for X
    - `recommended_actions`: Recovery or exit strategies
    - `confidence_in_analysis`: 0-1 confidence in analysis quality
    """
    try:
        logger.info(f"Analyzing trend: {metrics.trend_name}")
        
        if not metrics.x:
            raise ValueError("X/Twitter metrics are required for analysis")
        
        # Convert Pydantic model to dict
        metrics_dict = metrics.model_dump(exclude_none=True)
        
        # Run analysis
        result = analyzer.analyze(metrics_dict)
        
        logger.info(f"Analysis complete for {metrics.trend_name}: {result['trend_status']}")
        
        return result
    
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing trend: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error during analysis: {str(e)}"
        )


@app.get("/sample-analysis", response_model=TrendAnalysisOutput, tags=["Demo"])
def run_sample_analysis(
    sample_type: str = Query(
        "declining",
        description="Type of sample: 'declining', 'growing', or 'collapsed'"
    )
) -> dict:
    """
    Run analysis on pre-loaded sample data.
    
    **Query Parameters:**
    - `sample_type`: "declining", "growing", or "collapsed"
    
    **Returns:**
    Same as /analyze endpoint. Useful for testing the engine.
    """
    try:
        if sample_type not in ["declining", "growing", "collapsed"]:
            raise ValueError(f"Invalid sample_type: {sample_type}. Must be 'declining', 'growing', or 'collapsed'")
        
        sample_data = load_sample_data(sample_type)
        logger.info(f"Running sample analysis: {sample_type}")
        
        result = analyzer.analyze(sample_data)
        
        return result
    
    except Exception as e:
        logger.error(f"Error in sample analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error during sample analysis: {str(e)}"
        )


@app.post("/batch-analyze", tags=["Analysis"])
def batch_analyze_trends(trends: list[TrendMetricsInput]) -> dict:
    """
    Analyze multiple trends in one request.
    
    **Request Body:**
    Array of trend metric objects (same format as /analyze)
    
    **Returns:**
    Array of analysis results with metadata
    """
    try:
        if len(trends) > 100:
            raise ValueError("Maximum 100 trends per batch request")
        
        results = []
        errors = []
        
        for i, trend in enumerate(trends):
            try:
                metrics_dict = trend.model_dump(exclude_none=True)
                result = analyzer.analyze(metrics_dict)
                results.append(result)
            except Exception as e:
                errors.append({
                    "index": i,
                    "trend_name": trend.trend_name,
                    "error": str(e)
                })
        
        return {
            "total_requested": len(trends),
            "successful_analyses": len(results),
            "failed_analyses": len(errors),
            "results": results,
            "errors": errors,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Error in batch processing: {str(e)}"
        )


@app.get("/sample-metrics-schema", tags=["Documentation"])
def get_sample_schema():
    """
    Get a sample JSON schema for metrics input.
    Useful for API integration testing.
    """
    return {
        "description": "Sample metrics structure for trend analysis",
        "example": {
            "trend_name": "#TechTok",
            "x": {
                "tweet_volume": {"current": 45000, "previous_period": 52000},
                "weekly_engagement_velocity": -0.15,
                "unique_content_ratio": 0.25,
            }
        },
        "schema_notes": {
            "trend_name": "Required string identifier",
            "x": "Required: X/Twitter metrics",
            "note": "All X metrics optional but more data = higher confidence"
        }
    }


@app.post("/explain", tags=["AI Analysis"])
def explain_trend_decline(metrics: TrendMetricsInput) -> dict:
    """
    Get AI-powered explanations for why a trend is declining.
    Uses Featherless AI (DeepSeek) to generate detailed insights.
    
    **Request Body:**
    - Same as `/analyze` endpoint
    
    **Response:**
    Returns detailed explanations for each detected decline cause
    """
    if not explanation_available:
        raise HTTPException(
            status_code=503,
            detail="AI explanation service not available. Please configure Featherless AI API key."
        )
    
    try:
        logger.info(f"Generating explanations for: {metrics.trend_name}")
        
        # First, run the analysis
        metrics_dict = metrics.model_dump(exclude_none=True)
        analysis_result = analyzer.analyze(metrics_dict)
        
        # Then get AI explanations
        explanations = explainer.explain_decline_causes(analysis_result)
        
        return {
            "trend_name": metrics.trend_name,
            "analysis": analysis_result,
            "ai_explanations": explanations,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error generating explanations: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/strategy", tags=["AI Analysis"])
def generate_recovery_strategy(metrics: TrendMetricsInput) -> dict:
    """
    Generate an AI-powered recovery or exit strategy for a declining trend.
    Uses Featherless AI to create actionable recommendations.
    
    **Request Body:**
    - Same as `/analyze` endpoint
    
    **Response:**
    Detailed strategic recommendation with tactics and timeline
    """
    if not explanation_available:
        raise HTTPException(
            status_code=503,
            detail="AI strategy service not available. Please configure Featherless AI API key."
        )
    
    try:
        logger.info(f"Generating strategy for: {metrics.trend_name}")
        
        # Run analysis
        metrics_dict = metrics.model_dump(exclude_none=True)
        analysis_result = analyzer.analyze(metrics_dict)
        
        # Generate strategy
        strategy = explainer.generate_strategy(analysis_result)
        
        return {
            "trend_name": metrics.trend_name,
            "trend_status": analysis_result["trend_status"],
            "severity": analysis_result["severity_level"],
            "ai_strategy": strategy,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error generating strategy: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/full-report", tags=["AI Analysis"])
def generate_full_report(metrics: TrendMetricsInput) -> dict:
    """
    Generate a comprehensive AI-powered report combining analysis and insights.
    Includes explanations, strategy, executive summary, and competitive analysis.
    
    **Request Body:**
    - Same as `/analyze` endpoint
    
    **Response:**
    Complete report with multiple analytical sections
    """
    if not explanation_available:
        raise HTTPException(
            status_code=503,
            detail="AI report service not available. Please configure Featherless AI API key."
        )
    
    try:
        logger.info(f"Generating full report for: {metrics.trend_name}")
        
        # Run analysis
        metrics_dict = metrics.model_dump(exclude_none=True)
        analysis_result = analyzer.analyze(metrics_dict)
        
        # Generate full report
        report = explainer.generate_full_report(analysis_result)
        
        return report
    
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/executive-summary", tags=["AI Analysis"])
def generate_executive_summary(metrics: TrendMetricsInput) -> dict:
    """
    Generate a C-level executive summary suitable for board presentations.
    
    **Request Body:**
    - Same as `/analyze` endpoint
    
    **Response:**
    Business-focused summary for executives
    """
    if not explanation_available:
        raise HTTPException(
            status_code=503,
            detail="AI summary service not available."
        )
    
    try:
        logger.info(f"Generating executive summary for: {metrics.trend_name}")
        
        metrics_dict = metrics.model_dump(exclude_none=True)
        analysis_result = analyzer.analyze(metrics_dict)
        
        summary = explainer.generate_executive_summary(analysis_result)
        
        return {
            "trend_name": metrics.trend_name,
            "status": analysis_result["trend_status"],
            "severity": analysis_result["severity_level"],
            "executive_summary": summary,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api-docs-markdown", tags=["Documentation"])
def get_api_docs():
    """Get API documentation in Markdown format."""
    return {
        "api_name": "Twitter Trend Intelligence Engine with AI Explanations",
        "version": "2.0.0",
        "documentation": """
# Twitter Trend Analyzer API Documentation

## Overview
Analyzes X/Twitter trends to detect decline causes with AI-powered explanations.

## Core Endpoints

### POST /analyze
Analyze a single trend for decline causes.

**Returns:** Structured analysis with confidence scores and decline causes

### GET /sample-analysis?sample_type=declining|growing|collapsed
Run analysis on pre-loaded sample data. Great for testing.

### POST /batch-analyze
Analyze up to 100 trends in a single request.

## AI-Powered Endpoints

### POST /explain
Get detailed AI explanations for detected decline causes (2-3 sentences per cause).

### POST /strategy
Generate actionable recovery or exit strategy (3-4 paragraphs).

### POST /executive-summary
Generate C-level executive summary suitable for board presentations.

### POST /full-report
Comprehensive report combining analysis, explanations, strategy, and competitive insights.

## Decline Cause Types (Detected Automatically)
- Engagement Decay
- Content Saturation
- Creator Disengagement
- Influencer Activity Collapse
- Posting Frequency Collapse
- Algorithmic Visibility Reduction
- Audience Fatigue
- Temporal Relevance Loss

## Status Codes
- 200: Success
- 400: Bad request
- 503: AI service unavailable
- 500: Server error
"""
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
