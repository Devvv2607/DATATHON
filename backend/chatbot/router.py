"""
FastAPI Router for Chatbot
Unified conversational interface for trend intelligence
"""

from fastapi import APIRouter, HTTPException
import logging

from .schema import ChatRequest, ChatResponse, StructuredData
from .intent_classifier import classify_intent
from .service import ChatbotService
from document_context.store import get_document_context_store

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])
logger = logging.getLogger(__name__)

# Initialize service
chatbot_service = ChatbotService()


@router.post("/message", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - handles all conversational queries
    
    Supports intents:
    - why_declining: "Why is this trend declining?"
    - why_alert: "Why did I get this alert level?"
    - what_to_do: "What should I do?" / "Give me comeback ideas"
    - show_data: "Show me the metrics"
    - general: General questions and greetings
    """
    try:
        # Classify intent
        intent_result = classify_intent(
            request.message,
            conversation_history=request.conversation_history
        )
        
        intent = intent_result["intent"]
        entities = intent_result.get("entities", {})
        
        # Extract trend name (from request or entities)
        trend_name = request.trend_name or entities.get("trend_name")
        
        logger.info(f"Intent: {intent}, Trend: {trend_name}")
        
        # Route to appropriate handler
        if intent == "why_declining":
            if not trend_name:
                return ChatResponse(
                    success=False,
                    message="Please specify which trend you'd like to analyze. Example: 'Why is fidget spinner declining?'",
                    intent=intent,
                    suggested_followups=["Try: Why is [trend name] declining?"]
                )
            
            result = await chatbot_service.handle_why_declining(trend_name)
            
        elif intent == "what_to_do":
            if not trend_name:
                return ChatResponse(
                    success=False,
                    message="Please specify which trend you want strategies for. Example: 'What should I do about fidget spinner?'",
                    intent=intent,
                    suggested_followups=["Try: What should I do about [trend name]?"]
                )
            
            result = await chatbot_service.handle_what_to_do(trend_name)
            
        elif intent == "why_alert":
            if not trend_name:
                return ChatResponse(
                    success=False,
                    message="Please specify which trend's alert you want explained. Example: 'Why is fidget spinner ORANGE?'",
                    intent=intent,
                    suggested_followups=["Try: Why is [trend name] [color]?"]
                )
            
            result = await chatbot_service.handle_why_alert(trend_name)
            
        elif intent == "show_data":
            if not trend_name:
                return ChatResponse(
                    success=False,
                    message="Please specify which trend's data you want to see. Example: 'Show me data for fidget spinner'",
                    intent=intent,
                    suggested_followups=["Try: Show data for [trend name]"]
                )
            
            result = await chatbot_service.handle_show_data(trend_name)
            
        elif intent == "general":
            result = await chatbot_service.handle_general(request.message)
            
        else:
            result = {
                "message": "I'm not sure how to help with that. Try asking about trend analysis, content strategies, or alert explanations.",
                "structured_data": [],
                "suggested_followups": [
                    "Why is fidget spinner declining?",
                    "What should I do about cricket match?",
                    "Explain the alert level"
                ]
            }
        
        if request.context_id:
            stored = get_document_context_store().get(request.context_id)
            if not stored:
                return ChatResponse(
                    success=False,
                    message="The uploaded PDF context expired or was not found. Please upload the PDF again.",
                    intent=intent,
                    structured_data=result.get("structured_data", []),
                    suggested_followups=result.get("suggested_followups", []),
                )

            result = chatbot_service.apply_document_context(
                result=result,
                user_message=request.message,
                intent=intent,
                trend_name=trend_name,
                document_filename=stored.filename,
                document_text=stored.text,
            )

        return ChatResponse(
            success=True,
            message=result["message"],
            intent=intent,
            structured_data=result.get("structured_data", []),
            suggested_followups=result.get("suggested_followups", [])
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check for Chatbot service"""
    return {
        "status": "healthy",
        "service": "Chatbot",
        "features": {
            "intent_classification": True,
            "orchestrates": [
                "Trend Analyzer",
                "Explainable AI",
                "Comeback AI"
            ]
        }
    }
