"""
FastAPI Main Application
Early Decline Signal Detection Engine - Feature #2
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from datetime import datetime
from typing import Optional

from models import (
    DeclineSignalRequest,
    LifecycleInfo,
    DailyMetric,
    DeclineSignalResponse,
    SignalBreakdown,
    HealthCheckResponse
)
from database import init_database, get_database, close_database
from config import get_sensitivity_for_stage
from lifecycle_handler import resolve_lifecycle_stage, get_thresholds_for_stage
from signals.engagement_drop import calculate_engagement_drop
from signals.velocity_decline import calculate_velocity_decline
from signals.creator_decline import calculate_creator_decline
from signals.quality_decline import calculate_quality_decline
from aggregator import aggregate_signals
from decline_predictor import generate_decline_prediction
from utils import setup_logging, get_iso_timestamp

# Configure logging
setup_logging("INFO")
logger = logging.getLogger(__name__)

# Environment
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb+srv://user:pass@cluster.mongodb.net/datazen")
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "false").lower() == "true"

# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown"""
    logger.info("🚀 Starting Early Decline Signal Detection Engine (Feature #2)")
    
    if not USE_MOCK_DATA:
        try:
            await init_database(DATABASE_URL)
        except Exception as e:
            logger.error(f"✗ Database init failed: {e}")
    else:
        logger.info("ℹ  Mock mode - no database")
    
    yield
    
    if not USE_MOCK_DATA:
        await close_database()
    logger.info("👋 Shutdown complete")

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Early Decline Signal Detection Engine",
    description="Feature #2: Detects early warning signs of trend decline",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    db_connected = False
    
    try:
        if not USE_MOCK_DATA:
            try:
                db = await get_database()
                db_connected = await db.health_check()
                logger.debug("✓ Health check: Database connected")
            except Exception as db_error:
                logger.warning(f"⚠ Health check: Database connection failed: {db_error}")
                db_connected = False
        else:
            db_connected = True
            logger.debug("✓ Health check: Mock mode enabled")
        
        status_str = "healthy" if db_connected else "degraded"
        logger.info(f"Health check: {status_str}")
        
        return HealthCheckResponse(
            status=status_str,
            database_connected=db_connected,
            timestamp=get_iso_timestamp()
        )
    except Exception as e:
        logger.error(f"✗ Health check failed: {e}", exc_info=True)
        return HealthCheckResponse(
            status="error",
            database_connected=False,
            timestamp=get_iso_timestamp()
        )

@app.post("/api/trends/{trend_id}/decline-signals", response_model=DeclineSignalResponse)
async def detect_decline_signals(
    trend_id: str,
    request: DeclineSignalRequest
):
    """
    PRIMARY ENDPOINT: Detect early decline signals for a trend.
    
    Input:
    - trend_id (URL)
    - trend metrics + optional lifecycle info
    
    Output:
    - Decline risk score (0-100)
    - 4 signal breakdown
    - Alert level + confidence
    
    Note: If Feature #1 is down, fallback to stage 3 (Plateau) with data_quality="degraded"
    """
    
    try:
        logger.info(f"📊 Processing decline signals for: {request.trend_name} (id: {trend_id})")
        
        # Validate input
        if not request.daily_metrics or len(request.daily_metrics) < 2:
            logger.warning(f"✗ Invalid request for {trend_id}: insufficient metrics (provided: {len(request.daily_metrics) if request.daily_metrics else 0}, required: 2)")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Need at least 2 days of metrics"
            )
        
        # Convert metrics
        daily_metrics = [
            DailyMetric(**m.dict()) if isinstance(m, DailyMetric) else m 
            for m in request.daily_metrics
        ]
        
        # 1. Resolve lifecycle (with fallback)
        lifecycle_stage, stage_name, data_quality = resolve_lifecycle_stage(
            request.lifecycle_info.dict() if request.lifecycle_info else None
        )
        
        logger.info(f"   Stage: {stage_name} (data_quality: {data_quality})")
        
        # 2. Get thresholds for this stage
        thresholds = get_thresholds_for_stage(lifecycle_stage)
        sensitivity = get_sensitivity_for_stage(lifecycle_stage)
        
        # 3. Compute 4 signals
        signal_scores = {}
        
        try:
            score, _ = calculate_engagement_drop(daily_metrics, sensitivity, thresholds["engagement_drop"])
            signal_scores["engagement_drop"] = score
            logger.debug(f"   Signal 1 (Engagement): {score:.1f}")
        except Exception as e:
            logger.error(f"   Signal 1 failed: {e}")
            signal_scores["engagement_drop"] = 0.0
            data_quality = "degraded"
        
        try:
            score, _ = calculate_velocity_decline(daily_metrics, sensitivity, thresholds["velocity_decline"])
            signal_scores["velocity_decline"] = score
            logger.debug(f"   Signal 2 (Velocity): {score:.1f}")
        except Exception as e:
            logger.error(f"   Signal 2 failed: {e}")
            signal_scores["velocity_decline"] = 0.0
            data_quality = "degraded"
        
        try:
            score, _ = calculate_creator_decline(daily_metrics, sensitivity, thresholds["creator_decline"])
            signal_scores["creator_decline"] = score
            logger.debug(f"   Signal 3 (Creators): {score:.1f}")
        except Exception as e:
            logger.error(f"   Signal 3 failed: {e}")
            signal_scores["creator_decline"] = 0.0
            data_quality = "degraded"
        
        try:
            score, _ = calculate_quality_decline(daily_metrics, sensitivity, thresholds["quality_decline"])
            signal_scores["quality_decline"] = score
            logger.debug(f"   Signal 4 (Quality): {score:.1f}")
        except Exception as e:
            logger.error(f"   Signal 4 failed: {e}")
            signal_scores["quality_decline"] = 0.0
            data_quality = "degraded"
        
        # 4. Aggregate
        decline_risk_score, alert_level, confidence = aggregate_signals(
            signal_scores,
            lifecycle_stage,
            data_quality
        )
        
        # 4.5 Calculate time-to-decline (time_to_die)
        time_to_die = None
        try:
            predictions = generate_decline_prediction(
                daily_metrics,
                decline_risk_score,
                lifecycle_stage
            )
            time_to_die = predictions["time_to_critical"]["days_to_red"]
            if time_to_die:
                logger.debug(f"✓ Time to RED: {time_to_die} days")
        except Exception as e:
            logger.debug(f"⚠ Time-to-decline calculation skipped: {e}")
        
        # 5. Build response
        response = DeclineSignalResponse(
            trend_id=trend_id,
            decline_risk_score=round(decline_risk_score, 1),
            alert_level=alert_level,
            signal_breakdown=SignalBreakdown(
                engagement_drop=round(signal_scores["engagement_drop"], 1),
                velocity_decline=round(signal_scores["velocity_decline"], 1),
                creator_decline=round(signal_scores["creator_decline"], 1),
                quality_decline=round(signal_scores["quality_decline"], 1)
            ),
            timestamp=get_iso_timestamp(),
            confidence=confidence,
            data_quality=data_quality,
            time_to_die=time_to_die
        )
        
        # 6. Save to MongoDB (if not mock mode)
        if not USE_MOCK_DATA:
            try:
                db = await get_database()
                await db.save_decline_signal(
                    trend_id,
                    {
                        "timestamp": response.timestamp,
                        "decline_risk_score": response.decline_risk_score,
                        "alert_level": response.alert_level,
                        "signal_breakdown": response.signal_breakdown.dict(),
                        "confidence": response.confidence,
                        "data_quality": data_quality,
                        "lifecycle_stage": lifecycle_stage,
                        "trend_name": request.trend_name
                    }
                )
                logger.info("✓ Saved to MongoDB")
            except Exception as e:
                logger.warning(f"Failed to save: {e}")
        
        logger.info(f"✓ Complete: Risk {response.decline_risk_score}/100 ({alert_level.upper()}) for {trend_id}")
        return response
    
    except HTTPException as http_error:
        logger.warning(f"⚠ HTTP Error for {trend_id}: {http_error.detail}")
        raise
    except ValueError as ve:
        logger.error(f"✗ Value Error for {trend_id}: {ve}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid data: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"✗ Unexpected error for {trend_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during signal detection"
        )

@app.get("/api/trends/{trend_id}/decline-signals/history")
async def get_decline_history(trend_id: str, limit: int = 30):
    """Get signal history for a trend (last N records)"""
    try:
        logger.info(f"📜 Fetching history for trend: {trend_id} (limit: {limit})")
        
        if USE_MOCK_DATA:
            logger.debug(f"Mock mode: returning empty history for {trend_id}")
            return {"trend_id": trend_id, "history": [], "note": "mock mode"}
        
        db = await get_database()
        history = await db.get_decline_signals_history(trend_id, limit)
        logger.info(f"✓ Retrieved {len(history)} history records for {trend_id}")
        
        return {
            "trend_id": trend_id,
            "history": history,
            "count": len(history)
        }
    except ValueError as ve:
        logger.warning(f"⚠ Invalid input for history query (trend_id: {trend_id}): {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"✗ Failed to get history for {trend_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve history"
        )

@app.get("/api/trends/{trend_id}/decline-signals/latest")
async def get_latest_signal(trend_id: str):
    """Get most recent signal for a trend"""
    try:
        logger.info(f"🔔 Fetching latest signal for trend: {trend_id}")
        
        if USE_MOCK_DATA:
            logger.debug(f"Mock mode: latest signal not available")
            raise HTTPException(status_code=404, detail="No signals in mock mode")
        
        db = await get_database()
        history = await db.get_decline_signals_history(trend_id, limit=1)
        
        if not history:
            logger.warning(f"⚠ No signals found for trend: {trend_id}")
            raise HTTPException(status_code=404, detail="No signals found for this trend")
        
        logger.info(f"✓ Retrieved latest signal for {trend_id}")
        return {"trend_id": trend_id, "signal": history[0]}
    except HTTPException:
        raise
    except ValueError as ve:
        logger.warning(f"⚠ Invalid trend_id format: {trend_id}, error: {ve}")
        raise HTTPException(status_code=400, detail="Invalid trend ID")
    except Exception as e:
        logger.error(f"✗ Failed to get latest signal for {trend_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve latest signal"
        )

@app.get("/")
async def root():
    """API documentation"""
    try:
        logger.debug("📖 Serving API documentation")
        return {
            "service": "Early Decline Signal Detection Engine",
            "version": "1.0.0",
            "status": "operational",
            "endpoints": {
                "detect": "POST /api/trends/{trend_id}/decline-signals",
                "history": "GET /api/trends/{trend_id}/decline-signals/history",
                "latest": "GET /api/trends/{trend_id}/decline-signals/latest",
                "health": "GET /health",
                "docs": "GET /docs"
            }
        }
    except Exception as e:
        logger.error(f"✗ Error serving API documentation: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve API documentation"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
