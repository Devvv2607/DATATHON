"""
Social Media Trend Analysis Platform - FastAPI Backend
Main application entry point with CORS, routers, and middleware
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from trend_analysis.router import router as trend_router

# Initialize FastAPI app
app = FastAPI(
    title="Trend Decline Prediction API",
    description="ML-powered social media trend analysis and decline prediction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register feature routers
app.include_router(trend_router, prefix="/api/trends", tags=["Trends"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Trend Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "trends": "/api/trends",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check for monitoring"""
    return {
        "status": "healthy",
        "database": "connected",  # Placeholder for DB check
        "ml_models": "loaded",    # Placeholder for ML model status
        "cache": "active"         # Placeholder for cache status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
