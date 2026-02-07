"""
API Controller for Trend Lifecycle Detection
FastAPI endpoints for lifecycle analysis
"""

import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from .schemas import TrendLifecycleRequest, TrendLifecycleResponse
from .service import lifecycle_service
from .db import lifecycle_db

logger = logging.getLogger(__name__)

router = APIRouter()


@router.on_event("startup")
async def startup():
    """Initialize MongoDB connection on startup"""
    await lifecycle_db.connect()


@router.post(
    "/api/trend/lifecycle",
    response_model=TrendLifecycleResponse,
    status_code=status.HTTP_200_OK,
    summary="Detect Trend Lifecycle Stage",
    description="""
    Detect which lifecycle stage a social media trend is currently in.
    
    **Pipeline:**
    1. Extract signals from Google Trends, Twitter, Reddit
    2. Classify stage using rule-based model
    3. Validate with Google Gemini AI
    4. Store in MongoDB
    
    **Returns:** Strict JSON contract with trend lifecycle data
    """,
    tags=["Trend Lifecycle"]
)
async def detect_lifecycle(request: TrendLifecycleRequest):
    """
    Main endpoint for lifecycle detection
    
    **Example Request:**
    ```json
    {
      "trend_name": "Grimace Shake"
    }
    ```
    
    **Example Response:**
    ```json
    {
      "trend_id": "507f1f77bcf86cd799439011",
      "trend_name": "Grimace Shake",
      "lifecycle_stage": 2,
      "stage_name": "Viral Explosion",
      "days_in_stage": 5,
      "confidence": 0.85
    }
    ```
    """
    try:
        logger.info(f"🔍 Lifecycle detection request: {request.trend_name}")
        
        result = await lifecycle_service.detect_lifecycle(request.trend_name)
        
        logger.info(f"✅ Lifecycle detection successful: {result.stage_name}")
        
        return result
    
    except Exception as e:
        logger.error(f"❌ Lifecycle detection failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lifecycle detection failed: {str(e)}"
        )


@router.get(
    "/api/trend/lifecycle/{trend_name}",
    summary="Get Lifecycle Data by Trend Name",
    description="Retrieve stored lifecycle data for a specific trend",
    tags=["Trend Lifecycle"]
)
async def get_lifecycle(trend_name: str):
    """
    Get lifecycle data by trend name
    """
    try:
        result = await lifecycle_service.get_lifecycle_by_name(trend_name)
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get lifecycle failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/api/trend/lifecycle/stage/{stage}",
    summary="Get Trends by Lifecycle Stage",
    description="Get all trends currently in a specific lifecycle stage (1-5)",
    tags=["Trend Lifecycle"]
)
async def get_trends_by_stage(stage: int, limit: int = 50):
    """
    Get all trends in a specific stage
    
    **Stages:**
    - 1: Emergence
    - 2: Viral Explosion
    - 3: Plateau
    - 4: Decline
    - 5: Death
    """
    if not 1 <= stage <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stage must be between 1 and 5"
        )
    
    try:
        trends = await lifecycle_service.get_trends_by_stage(stage, limit)
        return JSONResponse(content={"stage": stage, "trends": trends, "count": len(trends)})
    
    except Exception as e:
        logger.error(f"Get trends by stage failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get(
    "/api/trend/lifecycle/health",
    summary="Health Check",
    description="Check if the lifecycle service is operational",
    tags=["Trend Lifecycle"]
)
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Trend Lifecycle Detection",
        "mongodb_connected": lifecycle_db._initialized
    }
