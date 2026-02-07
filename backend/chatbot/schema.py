"""
Pydantic schemas for Chatbot API
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Single chat message"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None


class ChatRequest(BaseModel):
    """Request to chat endpoint"""
    message: str
    trend_name: Optional[str] = None
    conversation_history: Optional[List[ChatMessage]] = []


class StructuredData(BaseModel):
    """Structured data to display alongside text response"""
    type: str  # "analysis", "explanation", "content", "chart"
    data: Dict[str, Any]


class ChatResponse(BaseModel):
    """Response from chat endpoint"""
    success: bool
    message: str
    intent: str
    structured_data: Optional[List[StructuredData]] = []
    suggested_followups: Optional[List[str]] = []
