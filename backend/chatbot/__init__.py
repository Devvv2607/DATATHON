"""
Chatbot Module
Unified interface for Trend Analyzer + Explainable AI + Comeback AI
"""

from .intent_classifier import classify_intent
from .service import ChatbotService
from .schema import ChatMessage, ChatResponse

__all__ = [
    "classify_intent",
    "ChatbotService",
    "ChatMessage",
    "ChatResponse"
]
