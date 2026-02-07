"""
Pydantic Models for Comeback AI API
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


# ============================================================================
# INPUT MODELS
# ============================================================================

class ComebackRequest(BaseModel):
    """Request to generate comeback content for a trend"""
    trend_name: str = Field(..., description="Name of the trend to analyze")
    
    # Optional: If not provided, will fetch from lifecycle + decline signals APIs
    alert_level: Optional[str] = Field(None, description="red, orange, yellow, green")
    lifecycle_stage: Optional[int] = Field(None, description="1-5")
    decline_risk_score: Optional[float] = Field(None, description="0-100")


# ============================================================================
# OUTPUT MODELS
# ============================================================================

class ReelIdea(BaseModel):
    """Single reel/video content idea"""
    id: int
    title: str
    description: str
    hook: str
    why_it_works: str


class Caption(BaseModel):
    """Social media caption/hook"""
    id: int
    caption: str
    language: str  # "english" or "Hinglish"


class RemixFormat(BaseModel):
    """Content format remix idea"""
    id: int
    format: str
    structure: str
    example: str


class ContentIdeas(BaseModel):
    """Generated content ideas"""
    reels: List[ReelIdea] = Field(..., description="3 reel/video ideas")
    captions: List[Caption] = Field(..., description="3 caption/hook ideas")
    remixes: List[RemixFormat] = Field(..., description="2 remix format ideas")


class ComebackResponse(BaseModel):
    """Complete comeback content generation response"""
    trend_name: str
    alert_level: str  # "red", "orange", "yellow", "green"
    mode: str  # "COMEBACK MODE" or "GROWTH MODE"
    decline_risk_score: float
    lifecycle_stage: int
    stage_name: str
    
    # Strategy context
    decline_drivers: Optional[List[str]] = None  # For COMEBACK mode
    growth_opportunities: Optional[List[str]] = None  # For GROWTH mode
    content_strategy: str
    
    # Generated content
    content: ContentIdeas
    
    # Metadata
    generated_at: str
    confidence: str


class ComebackHealthResponse(BaseModel):
    """Health check for comeback AI service"""
    status: str
    groq_api_configured: bool
    last_generation: Optional[str] = None
