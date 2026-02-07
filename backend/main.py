"""
Social Media Trend Analysis Platform - FastAPI Backend
Main application entry point with CORS, routers, and middleware
"""

from dotenv import load_dotenv
load_dotenv()  # Load .env before importing config

import logging

# Configure logging to show INFO level messages
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     %(message)s'
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from trend_analysis.router import router as trend_router
from trend_analysis.lifecycle.controller import router as lifecycle_router
from data_collectors.reddit_collector import router as reddit_router
from decline_signals.router import router as decline_signals_router
from comeback_ai.router import router as comeback_router
from trend_analyzer.router import router as trend_analyzer_router
from explainable_ai.router import router as explainable_ai_router
from chatbot.router import router as chatbot_router

# Initialize FastAPI app
app = FastAPI(
    title="Trend Decline Prediction API",
    description="ML-powered social media trend analysis and decline prediction with lifecycle detection",
    version="2.0.0",
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
app.include_router(lifecycle_router, tags=["Trend Lifecycle"])
app.include_router(reddit_router, tags=["Data Collection"])
app.include_router(decline_signals_router, prefix="/api/decline-signals", tags=["Early Decline Detection"])
app.include_router(comeback_router, tags=["Comeback AI - Content Generation"])
app.include_router(trend_analyzer_router, tags=["Trend Analyzer - Twitter/X Analysis"])
app.include_router(explainable_ai_router, tags=["Explainable AI - Decision Transparency"])
app.include_router(chatbot_router, tags=["Chatbot - Unified Interface"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Trend Analysis API",
        "version": "2.0.0",
        "endpoints": {
            "trends": "/api/trends",
            "lifecycle": "/api/trend/lifecycle",
            "decline_signals": "/api/decline-signals/analyze",
            "comeback_ai": "/api/comeback/generate",
            "trend_analyzer": "/api/trend-analyzer/analyze",
            "explainable_ai": "/api/explainable-ai/explain",
            "chatbot": "/api/chat/message",
            "reddit_data": "/api/data/reddit/search",
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
