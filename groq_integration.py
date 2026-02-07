"""
Groq API Integration Module
Generates creative content ideas for comeback and growth modes
"""

import json
from typing import Dict, List, Any
from groq import Groq

class GroqContentGenerator:
    """Generate content ideas using Groq API"""
    
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def generate_comeback_content(
        self, 
        trend_name: str, 
        decline_drivers: List[str],
        related_topics: List[str]
    ) -> Dict[str, Any]:
        """
        Generate comeback mode content (alert_level: red/orange)
        """
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
- 3 realistic Instagram/TikTok reel ideas
- 3 engaging captions/hooks (mix English and Hinglish)
- 2 remix formats that change content structure
- Each should explain how it combats decline (fatigue, saturation, boredom)
- Avoid generic advice and offensive content
- Feel like real creator strategies

Return valid JSON only, no markdown code blocks.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.8,
        )
        
        try:
            content = response.choices[0].message.content
            # Clean up response
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response", "raw": response.choices[0].message.content}
    
    def generate_growth_content(
        self,
        trend_name: str,
        growth_opportunities: List[str],
        related_topics: List[str]
    ) -> Dict[str, Any]:
        """
        Generate growth mode content (alert_level: green/yellow)
        """
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
- Each should explain how it increases reach and engagement
- Avoid generic advice and offensive content
- Feel like real creator strategies

Return valid JSON only, no markdown code blocks.
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.8,
        )
        
        try:
            content = response.choices[0].message.content
            # Clean up response
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            if content.endswith("```"):
                content = content[:-3]
            
            return json.loads(content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response", "raw": response.choices[0].message.content}
