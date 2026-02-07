"""
Groq API Client for Content Generation
Generates creative comeback and growth content using Groq's LLM
"""

import json
import os
import logging
from typing import Dict, List, Any
from groq import Groq

logger = logging.getLogger(__name__)


class GroqContentGenerator:
    """Generate content ideas using Groq API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-versatile"
        logger.info(f"✅ Groq client initialized with model: {self.model}")
    
    def generate_comeback_content(
        self, 
        trend_name: str, 
        decline_drivers: List[str],
        related_topics: List[str]
    ) -> Dict[str, Any]:
        """
        Generate COMEBACK MODE content (alert_level: red/orange)
        For declining or saturated trends
        """
        logger.info(f"🎨 Generating COMEBACK content for: {trend_name}")
        
        prompt = f"""
You are a Senior Growth Marketer + Creator Strategist + Meme Culture Analyst.

Trend: {trend_name}
Decline Drivers: {', '.join(decline_drivers)}
Related Topics: {', '.join(related_topics)}

Generate COMEBACK MODE content in JSON format. Return exactly:
{{
    "reels": [
        {{"id": 1, "title": "...", "description": "...", "hook": "...", "why_it_works": "..."}}
    ],
    "captions": [
        {{"id": 1, "caption": "...", "language": "english"}}
    ],
    "remixes": [
        {{"id": 1, "format": "...", "structure": "...", "example": "..."}}
    ]
}}

Requirements:
- 3 realistic Instagram/TikTok reel ideas that combat the decline
- 3 engaging captions/hooks (mix English and Hinglish)
- 2 remix formats that change content structure
- Each should explain how it combats the specific decline drivers
- Focus on: reducing fatigue, breaking saturation, re-engaging audience
- Avoid generic advice and offensive content
- Feel like real creator strategies

Return valid JSON only, no markdown code blocks.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.8,
            )
            
            content = self._clean_json_response(response.choices[0].message.content)
            parsed = json.loads(content)
            logger.info(f"✅ Generated {len(parsed.get('reels', []))} reels, {len(parsed.get('captions', []))} captions")
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed: {e}")
            return self._fallback_comeback_content(trend_name)
        except Exception as e:
            logger.error(f"❌ Groq API error: {e}")
            return self._fallback_comeback_content(trend_name)
    
    def generate_growth_content(
        self,
        trend_name: str,
        growth_opportunities: List[str],
        related_topics: List[str]
    ) -> Dict[str, Any]:
        """
        Generate GROWTH MODE content (alert_level: green/yellow)
        For rising or emerging trends
        """
        logger.info(f"🚀 Generating GROWTH content for: {trend_name}")
        
        prompt = f"""
You are a Senior Growth Marketer + Creator Strategist + Meme Culture Analyst.

Trend: {trend_name}
Growth Opportunities: {', '.join(growth_opportunities)}
Related Topics: {', '.join(related_topics)}

Generate GROWTH MODE content in JSON format. Return exactly:
{{
    "reels": [
        {{"id": 1, "title": "...", "description": "...", "hook": "...", "why_it_works": "..."}}
    ],
    "captions": [
        {{"id": 1, "caption": "...", "language": "english"}}
    ],
    "remixes": [
        {{"id": 1, "format": "...", "structure": "...", "example": "..."}}
    ]
}}

Requirements:
- 3 creative Instagram/TikTok reel ideas to accelerate growth
- 3 engaging captions/hooks (mix English and Hinglish)
- 2 remix formats for scaling content
- Each should explain how it captures the growth opportunities
- Focus on: reach expansion, virality, cross-platform scaling
- Avoid generic advice and offensive content
- Feel like real creator strategies

Return valid JSON only, no markdown code blocks.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.8,
            )
            
            content = self._clean_json_response(response.choices[0].message.content)
            parsed = json.loads(content)
            logger.info(f"✅ Generated {len(parsed.get('reels', []))} reels, {len(parsed.get('captions', []))} captions")
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON parsing failed: {e}")
            return self._fallback_growth_content(trend_name)
        except Exception as e:
            logger.error(f"❌ Groq API error: {e}")
            return self._fallback_growth_content(trend_name)
    
    def _clean_json_response(self, content: str) -> str:
        """Remove markdown code blocks from Groq response"""
        content = content.strip()
        
        # Remove markdown code blocks
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        if content.endswith("```"):
            content = content[:-3]
        
        return content.strip()
    
    def _fallback_comeback_content(self, trend_name: str) -> Dict[str, Any]:
        """Fallback content if Groq API fails"""
        logger.warning(f"⚠️ Using fallback comeback content for: {trend_name}")
        return {
            "reels": [
                {
                    "id": 1,
                    "title": f"{trend_name} Reimagined",
                    "description": "Create a fresh take on the trend with unexpected twists",
                    "hook": "You've never seen it like this before",
                    "why_it_works": "Breaks audience fatigue with novelty"
                },
                {
                    "id": 2,
                    "title": f"Behind the {trend_name}",
                    "description": "Show the making-of process and creator journey",
                    "hook": "The truth behind the trend",
                    "why_it_works": "Adds authenticity and human connection"
                },
                {
                    "id": 3,
                    "title": f"{trend_name} Challenge 2.0",
                    "description": "Remix the original with new rules or format",
                    "hook": "Think you mastered it? Try this version",
                    "why_it_works": "Re-engages existing audience with fresh challenge"
                }
            ],
            "captions": [
                {"id": 1, "caption": f"Time to revive {trend_name} 🔥", "language": "english"},
                {"id": 2, "caption": f"{trend_name} comeback kar raha hai! 🚀", "language": "Hinglish"},
                {"id": 3, "caption": "Same trend, completely different vibe", "language": "english"}
            ],
            "remixes": [
                {
                    "id": 1,
                    "format": "Before & After",
                    "structure": "Show the trend then vs now with upgrades",
                    "example": "Original dance vs elevated choreography"
                },
                {
                    "id": 2,
                    "format": "Mashup Edition",
                    "structure": "Combine with another trending topic",
                    "example": f"{trend_name} meets current viral meme"
                }
            ]
        }
    
    def _fallback_growth_content(self, trend_name: str) -> Dict[str, Any]:
        """Fallback content if Groq API fails"""
        logger.warning(f"⚠️ Using fallback growth content for: {trend_name}")
        return {
            "reels": [
                {
                    "id": 1,
                    "title": f"{trend_name} Explainer",
                    "description": "Break down why this trend is blowing up",
                    "hook": "Everyone's talking about it, here's why",
                    "why_it_works": "Captures curious audiences seeking context"
                },
                {
                    "id": 2,
                    "title": f"Join the {trend_name} Movement",
                    "description": "Participatory content encouraging user submissions",
                    "hook": "Your turn to try this viral trend",
                    "why_it_works": "Increases reach through UGC amplification"
                },
                {
                    "id": 3,
                    "title": f"{trend_name} Pro Tips",
                    "description": "Advanced tips for mastering the trend",
                    "hook": "Level up your game with these secrets",
                    "why_it_works": "Provides value to engaged audience"
                }
            ],
            "captions": [
                {"id": 1, "caption": f"{trend_name} is taking over! 🌊", "language": "english"},
                {"id": 2, "caption": f"Abhi nahi kiya toh kab karoge? {trend_name} 🔥", "language": "Hinglish"},
                {"id": 3, "caption": "Don't miss out on this wave", "language": "english"}
            ],
            "remixes": [
                {
                    "id": 1,
                    "format": "Reaction Series",
                    "structure": "React to others doing the trend",
                    "example": "Duet/stitch with top creators"
                },
                {
                    "id": 2,
                    "format": "Tutorial Breakdown",
                    "structure": "Step-by-step guide with personality",
                    "example": "How to nail the trend in 60 seconds"
                }
            ]
        }
