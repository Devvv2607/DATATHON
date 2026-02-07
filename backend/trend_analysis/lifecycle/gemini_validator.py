"""
Google Gemini AI Validator
Validates lifecycle stage classification and assigns confidence score
"""

import os
import logging
from typing import Tuple, Optional

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from .schemas import LifecycleStage, STAGE_NAMES, AggregatedSignals, GoogleTrendsSignals, TwitterSignals, RedditSignals

logger = logging.getLogger(__name__)


class GeminiValidator:
    """
    Uses Google Gemini AI to validate lifecycle classification
    and catch edge cases (revivals, false drops)
    """
    
    def __init__(self):
        self.model = None
        self._init_gemini()
    
    def _init_gemini(self):
        """Initialize Gemini API"""
        if not genai:
            logger.warning("⚠️ google-generativeai not installed")
            return
        
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not api_key:
            logger.warning("⚠️ GOOGLE_GEMINI_API_KEY not set")
            return
        
        try:
            genai.configure(api_key=api_key)
            # Use gemini-2.0-flash (latest stable model with generateContent)
            self.model = genai.GenerativeModel('models/gemini-2.0-flash')
            logger.info("✅ Gemini AI validator initialized (gemini-2.0-flash)")
        except Exception as e:
            logger.error(f"❌ Gemini init failed: {e}")
    
    async def validate_stage(
        self,
        trend_name: str,
        detected_stage: LifecycleStage,
        google: GoogleTrendsSignals,
        twitter: TwitterSignals,
        reddit: RedditSignals,
        aggregated: AggregatedSignals
    ) -> Tuple[bool, float, str]:
        """
        Validate the detected lifecycle stage using Gemini AI
        
        Returns:
            (is_valid, confidence_adjustment, reasoning)
        """
        if not self.model:
            logger.info("Gemini not available, using rule-based confidence")
            return True, 1.0, "Rule-based classification (Gemini unavailable)"
        
        try:
            # Build validation prompt
            prompt = self._build_validation_prompt(
                trend_name, detected_stage, google, twitter, reddit, aggregated
            )
            
            # Call Gemini
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                return True, 1.0, "Gemini response empty"
            
            # Parse response
            result = self._parse_gemini_response(response.text)
            
            logger.info(f"🤖 Gemini validation: {result['reasoning']}")
            
            return result['is_valid'], result['confidence_adjustment'], result['reasoning']
        
        except Exception as e:
            logger.error(f"Gemini validation failed: {e}")
            return True, 1.0, f"Validation error: {str(e)}"
    
    def _build_validation_prompt(
        self,
        trend_name: str,
        detected_stage: LifecycleStage,
        google: GoogleTrendsSignals,
        twitter: TwitterSignals,
        reddit: RedditSignals,
        aggregated: AggregatedSignals
    ) -> str:
        """
        Build validation prompt for Gemini
        """
        stage_name = STAGE_NAMES[detected_stage]
        
        prompt = f"""You are a social media trend analyst. Validate if the lifecycle stage classification is correct.

**Trend Name:** {trend_name}

**Detected Stage:** {stage_name} (Stage {detected_stage})

**Signals:**
- Google Trends Interest Score: {google.interest_score:.1f}/100
- Google Interest Slope: {google.interest_slope:.3f}
- Twitter Post Volume: {twitter.post_volume}
- Twitter Engagement Rate: {twitter.engagement_rate:.2f}
- Twitter Velocity: {twitter.velocity:.2f}%
- Reddit Post Count: {reddit.post_count}
- Reddit Discussion Growth: {reddit.discussion_growth_rate:.2f}%
- Aggregated Growth Rate: {aggregated.growth_rate:.2f}%
- Momentum: {aggregated.momentum:.2f}
- Decay Signal: {aggregated.decay_signal:.2f}
- Engagement Saturation: {aggregated.engagement_saturation:.2f}

**Lifecycle Stages:**
1. Emergence - Early growth, low-to-moderate activity
2. Viral Explosion - Rapid growth, high momentum
3. Plateau - Stable, high engagement, flat growth
4. Decline - Negative growth, sustained decay
5. Death - Near-zero activity

**Task:**
1. Validate if the detected stage is reasonable given the signals
2. Check for edge cases: revivals (sudden spike after decline), false drops (temporary dip), seasonal patterns
3. Provide a confidence adjustment multiplier (0.5 to 1.2)

**Response Format (JSON only):**
{{
  "is_valid": true/false,
  "confidence_adjustment": 0.8-1.2,
  "reasoning": "Brief explanation"
}}

Keep reasoning under 50 words. Focus on validation, not re-classification.
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> dict:
        """
        Parse Gemini's JSON response
        """
        import json
        import re
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    'is_valid': result.get('is_valid', True),
                    'confidence_adjustment': float(result.get('confidence_adjustment', 1.0)),
                    'reasoning': result.get('reasoning', 'Valid classification')
                }
        except Exception as e:
            logger.warning(f"Gemini response parsing failed: {e}")
        
        # Fallback
        return {
            'is_valid': True,
            'confidence_adjustment': 1.0,
            'reasoning': 'Could not parse Gemini response'
        }
