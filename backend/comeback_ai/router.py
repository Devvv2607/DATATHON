"""
FastAPI Router for Comeback AI - Creative Content Generation
Generates strategic social media content based on trend lifecycle and decline signals
"""

from fastapi import APIRouter, HTTPException
import logging
from typing import Optional

from comeback_ai.schema import (
    ComebackRequest,
    ComebackResponse,
    ComebackHealthResponse
)
from comeback_ai.service import ComebackAIService

router = APIRouter(prefix="/api/comeback", tags=["Comeback AI"])
logger = logging.getLogger(__name__)

# Initialize service
try:
    service = ComebackAIService()
except Exception as e:
    service = None
    logger.error(f"❌ ComebackAIService unavailable: {e}")


@router.post("/generate", response_model=ComebackResponse)
async def generate_comeback_content(request: ComebackRequest):
    """
    Generate strategic comeback/growth content for a trend
    
    **Automatic Mode** (Recommended):
    ```json
    {
        "trend_name": "fidget spinner"
    }
    ```
    → System will automatically fetch lifecycle + decline signals and generate content
    
    **Manual Mode** (If you already have the data):
    ```json
    {
        "trend_name": "fidget spinner",
        "alert_level": "red",
        "lifecycle_stage": 5,
        "decline_risk_score": 85.0
    }
    ```
    
    **Response**:
    - `mode`: "COMEBACK MODE" (red/orange) or "GROWTH MODE" (green/yellow)
    - `content.reels`: 3 video/reel ideas with hooks and strategy
    - `content.captions`: 3 social media captions (English + Hinglish)
    - `content.remixes`: 2 content format remix ideas
    - `decline_drivers` or `growth_opportunities`: Strategic context
    
    **Content Strategy**:
    - **COMEBACK MODE**: Revive declining trends with fresh angles
    - **GROWTH MODE**: Accelerate rising trends with reach expansion
    """
    
    try:
        if service is None:
            raise HTTPException(
                status_code=503,
                detail="Comeback AI not configured. Please set GROQ_API_KEY in backend/.env",
            )
        logger.info(f"\n{'='*80}")
        logger.info(f"📥 Received request: {request.trend_name}")
        logger.info(f"{'='*80}")
        
        response = await service.generate_comeback_content(request)
        
        logger.info(f"✅ Successfully generated content for: {request.trend_name}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Content generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate content: {str(e)}"
        )


@router.get("/health", response_model=ComebackHealthResponse)
async def health_check():
    """
    Check if Comeback AI service is operational
    """
    
    try:
        # Check if Groq API is configured
        groq_configured = service is not None and service.groq_generator is not None
        
        return ComebackHealthResponse(
            status="healthy" if groq_configured else "unhealthy",
            groq_api_configured=groq_configured,
            last_generation=None
        )
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return ComebackHealthResponse(
            status="unhealthy",
            groq_api_configured=False,
            last_generation=None
        )


@router.post("/quick-test")
async def quick_test(trend_name: str = "AI memes"):
    """
    Quick test endpoint to verify Comeback AI is working
    
    Usage: POST /api/comeback/quick-test?trend_name=fidget%20spinner
    """
    
    try:
        if service is None:
            raise HTTPException(
                status_code=503,
                detail="Comeback AI not configured. Please set GROQ_API_KEY in backend/.env",
            )
        request = ComebackRequest(trend_name=trend_name)
        response = await service.generate_comeback_content(request)
        
        return {
            "status": "success",
            "trend_name": response.trend_name,
            "mode": response.mode,
            "alert_level": response.alert_level,
            "reels_count": len(response.content.reels),
            "captions_count": len(response.content.captions),
            "remixes_count": len(response.content.remixes),
            "sample_reel": response.content.reels[0].dict() if response.content.reels else None
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
