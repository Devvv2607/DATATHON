"""
Chatbot Service
Orchestrates Trend Analyzer + Explainable AI + Comeback AI
"""

import os
import logging
import requests
from typing import Dict, Any, List, Optional
from groq import Groq

logger = logging.getLogger(__name__)

# Initialize Groq for response formatting
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key) if groq_api_key else None


class ChatbotService:
    """Orchestrates all trend intelligence features"""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.lifecycle_api = f"{self.base_url}/api/trend/lifecycle"
        self.decline_signals_api = f"{self.base_url}/api/decline-signals/analyze"
        self.trend_analyzer_api = f"{self.base_url}/api/trend-analyzer"
        self.explainable_ai_api = f"{self.base_url}/api/explainable-ai"
        self.comeback_ai_api = f"{self.base_url}/api/comeback/generate"

    def apply_document_context(
        self,
        *,
        result: Dict[str, Any],
        user_message: str,
        intent: str,
        trend_name: Optional[str],
        document_filename: str,
        document_text: str,
    ) -> Dict[str, Any]:
        if not document_text.strip():
            return result

        trimmed_doc = document_text.strip()
        if len(trimmed_doc) > 12000:
            trimmed_doc = trimmed_doc[:12000]

        if not groq_client:
            augmented = result.copy()
            augmented["message"] = (
                f"{result.get('message', '')}\n\n"
                f"📎 Document context attached: {document_filename}. "
                "(Groq is not configured, so I'm not able to fully incorporate the document into the answer.)"
            ).strip()
            return augmented

        try:
            system = (
                "You are a trend intelligence assistant. "
                "The user may attach a document (PDF/DOCX/TXT) as extra context. "
                "Treat it as a business document, not as the abbreviation 'PDF' for other meanings. "
                "Use the provided document context only if it is relevant. "
                "If the document is not relevant, say so briefly. "
                "Do not hallucinate details that are not present in the document or in the structured data. "
                "Keep the tone concise and actionable."
            )

            prompt = (
                f"USER QUESTION:\n{user_message}\n\n"
                f"INTENT: {intent}\n"
                f"TREND (if any): {trend_name or 'N/A'}\n\n"
                f"CURRENT DRAFT ANSWER:\n{result.get('message', '')}\n\n"
                "STRUCTURED DATA (JSON):\n"
                f"{result.get('structured_data', [])}\n\n"
                f"DOCUMENT CONTEXT ({document_filename}) [may be partial]:\n{trimmed_doc}\n\n"
                "TASK:\n"
                "Rewrite the answer so it incorporates any relevant document facts/constraints, "
                "and improve explainability. If the document conflicts with the draft answer, "
                "call out the conflict and prefer the document."
            )

            resp = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=450,
            )

            augmented = result.copy()
            augmented["message"] = (resp.choices[0].message.content or "").strip()
            return augmented
        except Exception as e:
            logger.error(f"Failed to apply document context: {str(e)}")
            return result
    
    async def handle_why_declining(self, trend_name: str) -> Dict[str, Any]:
        """
        Handle "Why is this trend declining?" questions
        Uses: Trend Analyzer + Explainable AI
        """
        try:
            # Step 1: Get lifecycle data
            lifecycle_response = requests.post(
                self.lifecycle_api,
                json={"trend_name": trend_name}
            )
            lifecycle_data = lifecycle_response.json()
            
            # Step 2: Get decline signals
            decline_response = requests.post(
                self.decline_signals_api,
                json={
                    "trend_name": trend_name,
                    "lifecycle_stage": lifecycle_data.get("lifecycle_stage", 3),
                    "stage_name": lifecycle_data.get("stage_name", "Plateau")
                }
            )
            decline_data = decline_response.json()
            
            # Step 3: Analyze with Trend Analyzer (use sample for now, will integrate Twitter/Reddit later)
            analyzer_response = requests.post(
                f"{self.trend_analyzer_api}/analyze-with-ai",
                json={
                    "trend_name": trend_name,
                    "use_sample": True,
                    "sample_type": "declining",
                    "include_strategy": True
                }
            )
            analyzer_data = analyzer_response.json()
            
            # Step 4: Get explanation from Explainable AI
            explainer_response = requests.post(
                f"{self.explainable_ai_api}/explain-from-decline-signals",
                json={
                    "trend_name": trend_name,
                    "decline_signals_response": decline_data
                }
            )
            explainer_data = explainer_response.json()
            
            # Step 5: Format response conversationally using Groq
            formatted_message = self._format_decline_response(
                trend_name,
                analyzer_data,
                explainer_data,
                decline_data
            )
            
            return {
                "message": formatted_message,
                "structured_data": [
                    {
                        "type": "analysis",
                        "data": analyzer_data.get("analysis", {})
                    },
                    {
                        "type": "explanation",
                        "data": explainer_data.get("explanation", {})
                    },
                    {
                        "type": "decline_signals",
                        "data": decline_data
                    }
                ],
                "suggested_followups": [
                    "What should I do about this?",
                    "Show me the raw data",
                    "Why did I get this alert level?"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error handling why_declining: {str(e)}")
            return {
                "message": f"I encountered an error analyzing {trend_name}. Error: {str(e)}",
                "structured_data": [],
                "suggested_followups": []
            }
    
    async def handle_what_to_do(self, trend_name: str) -> Dict[str, Any]:
        """
        Handle "What should I do?" questions
        Uses: Comeback AI
        """
        try:
            # Call Comeback AI
            response = requests.post(
                self.comeback_ai_api,
                json={"trend_name": trend_name}
            )
            comeback_data = response.json()
            
            # Format response
            formatted_message = self._format_comeback_response(
                trend_name,
                comeback_data
            )
            
            return {
                "message": formatted_message,
                "structured_data": [
                    {
                        "type": "content",
                        "data": comeback_data
                    }
                ],
                "suggested_followups": [
                    "Why is this trend declining?",
                    "Show me more reel ideas",
                    "Explain the alert level"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error handling what_to_do: {str(e)}")
            return {
                "message": f"I couldn't generate content strategies. Error: {str(e)}",
                "structured_data": [],
                "suggested_followups": []
            }
    
    async def handle_why_alert(self, trend_name: str) -> Dict[str, Any]:
        """
        Handle "Why this alert level?" questions
        Uses: Explainable AI
        """
        try:
            # Get decline signals
            lifecycle_response = requests.post(
                self.lifecycle_api,
                json={"trend_name": trend_name}
            )
            lifecycle_data = lifecycle_response.json()
            
            decline_response = requests.post(
                self.decline_signals_api,
                json={
                    "trend_name": trend_name,
                    "lifecycle_stage": lifecycle_data.get("lifecycle_stage", 3),
                    "stage_name": lifecycle_data.get("stage_name", "Plateau")
                }
            )
            decline_data = decline_response.json()
            
            # Get explanation
            explainer_response = requests.post(
                f"{self.explainable_ai_api}/explain-from-decline-signals",
                json={
                    "trend_name": trend_name,
                    "decline_signals_response": decline_data
                }
            )
            explainer_data = explainer_response.json()
            
            # Format response
            formatted_message = self._format_alert_explanation(
                trend_name,
                explainer_data,
                decline_data
            )
            
            return {
                "message": formatted_message,
                "structured_data": [
                    {
                        "type": "explanation",
                        "data": explainer_data.get("explanation", {})
                    },
                    {
                        "type": "decline_signals",
                        "data": decline_data
                    }
                ],
                "suggested_followups": [
                    "What should I do about this?",
                    "Show me detailed analysis",
                    "What if engagement increased?"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error handling why_alert: {str(e)}")
            return {
                "message": f"I couldn't explain the alert. Error: {str(e)}",
                "structured_data": [],
                "suggested_followups": []
            }
    
    async def handle_show_data(self, trend_name: str) -> Dict[str, Any]:
        """
        Handle "Show me data" requests
        Uses: Lifecycle + Decline Signals APIs
        """
        try:
            # Get all data
            lifecycle_response = requests.post(
                self.lifecycle_api,
                json={"trend_name": trend_name}
            )
            lifecycle_data = lifecycle_response.json()
            
            decline_response = requests.post(
                self.decline_signals_api,
                json={
                    "trend_name": trend_name,
                    "lifecycle_stage": lifecycle_data.get("lifecycle_stage", 3),
                    "stage_name": lifecycle_data.get("stage_name", "Plateau")
                }
            )
            decline_data = decline_response.json()
            
            message = f"📊 **Data for {trend_name}**\n\n"
            message += f"**Lifecycle:** Stage {lifecycle_data.get('lifecycle_stage')} - {lifecycle_data.get('stage_name')}\n"
            message += f"**Risk Score:** {decline_data.get('decline_risk_score', 0)}/100\n"
            message += f"**Alert Level:** {decline_data.get('alert_level', 'unknown').upper()}\n\n"
            message += "See detailed metrics in the structured data below."
            
            return {
                "message": message,
                "structured_data": [
                    {
                        "type": "chart",
                        "data": {
                            "lifecycle": lifecycle_data,
                            "decline_signals": decline_data
                        }
                    }
                ],
                "suggested_followups": [
                    "Why is this declining?",
                    "What should I do?",
                    "Explain the alert"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error handling show_data: {str(e)}")
            return {
                "message": f"Couldn't fetch data. Error: {str(e)}",
                "structured_data": [],
                "suggested_followups": []
            }
    
    async def handle_general(self, message: str) -> Dict[str, Any]:
        """
        Handle general questions using Groq
        """
        if not groq_client:
            return {
                "message": "I'm a trend analysis assistant. Ask me about trend declines, content strategies, or alert explanations!",
                "structured_data": [],
                "suggested_followups": [
                    "Why is fidget spinner declining?",
                    "What should I do about this trend?",
                    "Explain the alert level"
                ]
            }
        
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful trend analysis assistant. Keep responses brief and friendly."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return {
                "message": response.choices[0].message.content,
                "structured_data": [],
                "suggested_followups": [
                    "Analyze a trend",
                    "Show me examples",
                    "How does this work?"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in general handler: {str(e)}")
            return {
                "message": "Hello! I'm your trend intelligence assistant. Ask me about why trends decline, what content to create, or explanations for alerts.",
                "structured_data": [],
                "suggested_followups": []
            }
    
    def _format_decline_response(
        self,
        trend_name: str,
        analyzer_data: Dict,
        explainer_data: Dict,
        decline_data: Dict
    ) -> str:
        """Format decline analysis into conversational response"""
        try:
            analysis = analyzer_data.get("analysis", {})
            causes = analysis.get("root_causes", [])
            
            # Get top 3 causes
            top_causes = sorted(causes, key=lambda x: x.get("confidence", 0), reverse=True)[:3]
            
            message = f"📉 **{trend_name}** is showing decline signals. Here's why:\n\n"
            
            for i, cause in enumerate(top_causes, 1):
                cause_type = cause.get("cause_type", "Unknown")
                confidence = int(cause.get("confidence", 0) * 100)
                message += f"**{i}. {cause_type}** ({confidence}% confidence)\n"
            
            # Add alert level context
            alert = decline_data.get("alert_level", "unknown").upper()
            risk = decline_data.get("decline_risk_score", 0)
            message += f"\n🚨 **Alert:** {alert} (Risk {risk}/100)\n"
            
            # Add strategy if available
            strategy = analyzer_data.get("strategy")
            if strategy:
                message += f"\n💡 **Recommended Action:** {strategy[:200]}..."
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting decline response: {str(e)}")
            return f"I found decline signals for {trend_name}. Check the structured data for details."
    
    def _format_comeback_response(self, trend_name: str, comeback_data: Dict) -> str:
        """Format comeback content into conversational response"""
        try:
            mode = comeback_data.get("mode", "COMEBACK")
            reels = comeback_data.get("reels", [])
            
            message = f"🎬 **{mode} Strategy for {trend_name}**\n\n"
            message += f"I've generated {len(reels)} reel ideas:\n\n"
            
            for i, reel in enumerate(reels[:3], 1):
                hook = reel.get("hook", "")[:60]
                message += f"**{i}. {hook}...**\n"
            
            message += "\nCheck the structured data below for full reel scripts, captions, and strategic reasoning!"
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting comeback response: {str(e)}")
            return f"I've generated content strategies for {trend_name}. See details below."
    
    def _format_alert_explanation(
        self,
        trend_name: str,
        explainer_data: Dict,
        decline_data: Dict
    ) -> str:
        """Format alert explanation into conversational response"""
        try:
            explanation = explainer_data.get("explanation", {})
            decision = explanation.get("decision_summary", {})
            
            alert = decline_data.get("alert_level", "unknown").upper()
            risk = decline_data.get("decline_risk_score", 0)
            
            message = f"🎯 **Why {alert} Alert for {trend_name}?**\n\n"
            message += f"**Risk Score:** {risk}/100\n"
            message += f"**Status:** {decision.get('status', 'unknown').title()}\n\n"
            message += f"{decision.get('message', 'Analysis complete.')}\n\n"
            
            # Add top signals
            signals = explanation.get("signal_contributions", [])[:3]
            if signals:
                message += "**Top Contributing Signals:**\n"
                for sig in signals:
                    sig_name = sig.get("signal", "").replace("_", " ").title()
                    impact = sig.get("impact_on_risk", 0)
                    message += f"- {sig_name}: +{impact} points\n"
            
            return message
            
        except Exception as e:
            logger.error(f"Error formatting alert explanation: {str(e)}")
            return f"The {decline_data.get('alert_level', 'unknown')} alert is based on current decline signals. See details below."
