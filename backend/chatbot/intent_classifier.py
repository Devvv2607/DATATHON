"""
Intent Classification using Groq LLM
Classifies user questions into actionable intents
"""

import os
from groq import Groq
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    logger.warning("GROQ_API_KEY not found. Intent classification will fail.")

groq_client = Groq(api_key=groq_api_key) if groq_api_key else None


INTENT_CLASSIFICATION_PROMPT = """You are an intent classifier for a trend analysis chatbot. Classify the user's question into ONE of these intents:

INTENTS:
1. why_declining - User asks why a trend is declining/losing popularity
   Examples: "Why is fidget spinner declining?", "What's causing the drop in engagement?"

2. why_alert - User asks why they received a specific alert level (RED/ORANGE/YELLOW/GREEN)
   Examples: "Why is this ORANGE?", "Explain the red alert", "Why did I get this alert level?"

3. what_to_do - User asks for content strategy/what to create/how to respond
   Examples: "What should I do?", "Give me comeback ideas", "How can I revive this?"

4. show_data - User wants to see raw metrics/data/charts
   Examples: "Show me the data", "What are the numbers?", "Display engagement metrics"

5. compare_trends - User wants to compare multiple trends
   Examples: "Compare fidget spinner vs cricket", "Which is doing better?"

6. general - General questions about trends, greetings, or unclear intent
   Examples: "Hello", "How does this work?", "Tell me about trends"

Respond with ONLY the intent name (lowercase, underscore-separated). No explanation."""


def classify_intent(message: str, conversation_history: Optional[list] = None) -> Dict[str, any]:
    """
    Classify user message intent using Groq LLM
    
    Returns:
        {
            "intent": str,
            "confidence": float,
            "entities": dict (trend names, alert levels mentioned)
        }
    """
    if not groq_client:
        logger.error("Groq client not initialized")
        return {
            "intent": "general",
            "confidence": 0.5,
            "entities": {}
        }
    
    try:
        # Build context from conversation history
        context = ""
        if conversation_history:
            recent = conversation_history[-3:]  # Last 3 messages
            context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent])
            context = f"\n\nCONVERSATION CONTEXT:\n{context}\n"
        
        # Call Groq API
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": INTENT_CLASSIFICATION_PROMPT},
                {"role": "user", "content": f"{context}\nCURRENT QUESTION: {message}"}
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        intent = response.choices[0].message.content.strip().lower()
        
        # Extract entities (trend names, alert levels)
        entities = extract_entities(message)
        
        logger.info(f"Classified intent: {intent}, entities: {entities}")
        
        return {
            "intent": intent,
            "confidence": 0.9,  # High confidence with LLM
            "entities": entities
        }
        
    except Exception as e:
        logger.error(f"Intent classification failed: {str(e)}")
        return {
            "intent": "general",
            "confidence": 0.3,
            "entities": {}
        }


def extract_entities(message: str) -> Dict[str, any]:
    """
    Extract entities from message (trend names, alert levels, etc.)
    """
    entities = {}
    
    message_lower = message.lower()
    
    # Extract alert levels
    alert_keywords = {
        "red": "red",
        "orange": "orange",
        "yellow": "yellow",
        "green": "green"
    }
    for keyword, level in alert_keywords.items():
        if keyword in message_lower:
            entities["alert_level"] = level
            break
    
    # Extract trend name (simple heuristic - words after "about", "for", or between quotes)
    if '"' in message:
        # Extract quoted text
        import re
        quoted = re.findall(r'"([^"]*)"', message)
        if quoted:
            entities["trend_name"] = quoted[0]
    elif " about " in message_lower:
        parts = message_lower.split(" about ")
        if len(parts) > 1:
            # Take next few words after "about"
            trend_words = parts[1].split()[:4]
            entities["trend_name"] = " ".join(trend_words).strip("?.,!")
    elif " for " in message_lower:
        parts = message_lower.split(" for ")
        if len(parts) > 1:
            trend_words = parts[1].split()[:4]
            entities["trend_name"] = " ".join(trend_words).strip("?.,!")
    
    return entities
