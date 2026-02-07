"""
AI-Powered Trend Analysis Explanation Module
Uses Featherless AI (DeepSeek) to generate detailed explanations and recommendations.
"""

from openai import OpenAI
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TrendAnalysisExplainer:
    """
    Uses LLM to provide detailed explanations for trend analysis results.
    Integrates with Featherless AI (DeepSeek model).
    """
    
    def __init__(
        self,
        api_key: str = "rc_16258f4d33f9df27a5a977ef7010dee1344c6fb68e073e5e749f83c20c780b6c",
        base_url: str = "https://api.featherless.ai/v1",
        model: str = "deepseek-ai/DeepSeek-V3-0324"
    ):
        """
        Initialize the explanation engine.
        
        Args:
            api_key: Featherless AI API key
            base_url: API base URL
            model: Model to use (default: DeepSeek V3)
        """
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        logger.info(f"TrendAnalysisExplainer initialized with {model}")
    
    def explain_decline_causes(self, analysis_result: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate detailed explanations for each decline cause.
        
        Args:
            analysis_result: Complete trend analysis result
        
        Returns:
            Dictionary mapping cause types to detailed explanations
        """
        try:
            trend_name = analysis_result.get("trend_name", "Unknown")
            root_causes = analysis_result.get("root_causes", [])
            
            if not root_causes:
                return {"summary": f"Trend '{trend_name}' shows no significant decline causes."}
            
            explanations = {}
            
            for cause in root_causes[:5]:  # Explain top 5 causes
                cause_type = cause.get("cause_type", "Unknown")
                confidence = cause.get("confidence", 0)
                evidence = cause.get("evidence", [])
                
                prompt = f"""
You are a social media strategist analyzing Twitter trend decline. Provide a concise but insightful 
explanation (2-3 sentences) for why this trend is experiencing this specific decline cause.

Trend: {trend_name}
Cause: {cause_type}
Confidence: {confidence:.0%}
Evidence:
{json.dumps(evidence, indent=2)}

Explain in business language what this means and why it matters for content creators/marketers.
"""
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=300,
                    temperature=0.7,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert social media strategist and data analyst. Provide clear, actionable insights."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                
                explanation = response.choices[0].message.content
                explanations[cause_type] = explanation
                logger.debug(f"Generated explanation for {cause_type}")
            
            return explanations
        
        except Exception as e:
            logger.error(f"Error generating cause explanations: {str(e)}")
            return {"error": f"Failed to generate explanations: {str(e)}"}
    
    def generate_strategy(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a recovery or exit strategy based on analysis.
        
        Args:
            analysis_result: Complete trend analysis result
        
        Returns:
            Detailed strategy recommendation
        """
        try:
            trend_name = analysis_result.get("trend_name", "Unknown")
            trend_status = analysis_result.get("trend_status", "UNKNOWN")
            severity = analysis_result.get("severity_level", "UNKNOWN")
            decline_prob = analysis_result.get("decline_probability", 0)
            root_causes = analysis_result.get("root_causes", [])
            
            causes_summary = "\n".join([
                f"- {c['cause_type']} ({c['confidence']:.0%} confidence)"
                for c in root_causes[:3]
            ])
            
            prompt = f"""
You are a senior social media strategist helping content creators and brands navigate Twitter trends.

Analyze this trend situation and provide a strategic recommendation:

**Trend:** {trend_name}
**Status:** {trend_status}
**Severity:** {severity}
**Decline Probability:** {decline_prob:.0%}

**Top Decline Causes:**
{causes_summary}

Provide a 3-4 paragraph strategic recommendation that includes:
1. Whether to continue, pivot, or exit the trend
2. Specific tactical actions they can take immediately
3. Timeline and expected outcomes
4. Risk assessment and alternatives

Be direct and actionable. Use business language, not technical jargon.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=800,
                temperature=0.7,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a strategic advisor for social media marketing. Provide clear, data-driven recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            strategy = response.choices[0].message.content
            logger.info(f"Generated strategy for {trend_name}")
            return strategy
        
        except Exception as e:
            logger.error(f"Error generating strategy: {str(e)}")
            return f"Failed to generate strategy: {str(e)}"
    
    def generate_executive_summary(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a C-level executive summary of the analysis.
        
        Args:
            analysis_result: Complete trend analysis result
        
        Returns:
            Executive summary in business language
        """
        try:
            trend_name = analysis_result.get("trend_name", "Unknown")
            trend_status = analysis_result.get("trend_status", "UNKNOWN")
            severity = analysis_result.get("severity_level", "UNKNOWN")
            decline_prob = analysis_result.get("decline_probability", 0)
            confidence = analysis_result.get("confidence_in_analysis", 0)
            
            platform_summary = json.dumps(
                analysis_result.get("cross_platform_summary", {}),
                indent=2
            )
            
            prompt = f"""
Create a concise executive summary (2-3 paragraphs) of this Twitter trend analysis for a CMO or CEO.

**Trend:** {trend_name}
**Current Status:** {trend_status}
**Severity Level:** {severity}
**Risk of Decline:** {decline_prob:.0%}
**Analysis Confidence:** {confidence:.0%}

**Platform Metrics:**
{platform_summary}

The summary should:
- Open with a clear recommendation (continue/pivot/exit)
- Explain the business impact in plain English
- Highlight key risks and opportunities
- Be suitable for a board presentation

Keep it professional but accessible to non-technical executives.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=600,
                temperature=0.6,
                messages=[
                    {
                        "role": "system",
                        "content": "You are writing an executive summary for C-level business leaders. Be concise, clear, and action-oriented."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            summary = response.choices[0].message.content
            logger.info(f"Generated executive summary for {trend_name}")
            return summary
        
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            return f"Failed to generate summary: {str(e)}"
    
    def analyze_competitor_activity(self, analysis_result: Dict[str, Any]) -> str:
        """
        Analyze what competitors might be doing with this trend.
        
        Args:
            analysis_result: Complete trend analysis result
        
        Returns:
            Competitive analysis insights
        """
        try:
            trend_name = analysis_result.get("trend_name", "Unknown")
            root_causes = analysis_result.get("root_causes", [])
            
            causes_text = "\n".join([
                f"- {c['cause_type']}: {c['business_explanation']}"
                for c in root_causes[:3]
            ])
            
            prompt = f"""
Provide competitive analysis insights for brands trying to capitalize on this Twitter trend.

**Trend:** {trend_name}
**Decline Factors:**
{causes_text}

Based on these decline factors, analyze:
1. How competitors might be approaching this trend differently
2. What competitive advantages exist in the current landscape
3. Untapped opportunities that competitors haven't noticed
4. First-mover advantage potential if the trend reverses

Be specific and actionable. Assume the reader is a marketing strategist at a major brand.
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a competitive analyst for social media marketing. Provide strategic insights on how brands can gain advantage."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            analysis = response.choices[0].message.content
            logger.info(f"Generated competitive analysis for {trend_name}")
            return analysis
        
        except Exception as e:
            logger.error(f"Error generating competitive analysis: {str(e)}")
            return f"Failed to generate analysis: {str(e)}"
    
    def generate_full_report(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete AI-powered report combining all analyses.
        
        Args:
            analysis_result: Complete trend analysis result
        
        Returns:
            Comprehensive report with multiple sections
        """
        logger.info(f"Generating full report for {analysis_result.get('trend_name')}")
        
        report = {
            "trend_name": analysis_result.get("trend_name"),
            "generated_at": datetime.utcnow().isoformat(),
            "original_analysis": analysis_result,
            "detailed_explanations": self.explain_decline_causes(analysis_result),
            "strategic_recommendation": self.generate_strategy(analysis_result),
            "executive_summary": self.generate_executive_summary(analysis_result),
            "competitive_insights": self.analyze_competitor_activity(analysis_result)
        }
        
        return report
    
    def explain_trend(self, trend_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Provide comprehensive analysis for a trending hashtag/meme.
        
        Args:
            trend_data: Dictionary containing trend analysis data
                       (hashtag, engagement_metrics, tweets, etc.)
        
        Returns:
            Dictionary with AI-powered analysis categories
        """
        try:
            hashtag = trend_data.get("trend_name", "Unknown")
            engagement = trend_data.get("engagement_metrics", {})
            tweets_sample = trend_data.get("sample_tweets", "")
            total_tweets = trend_data.get("total_tweets_analyzed", 0)
            
            # Build the analysis prompt
            analysis_prompt = f"""
Analyze this trending topic on Twitter/X and provide actionable insights:

**Trend:** #{hashtag}
**Total Tweets Analyzed:** {total_tweets}
**Engagement Metrics:**
- Total Likes: {engagement.get('total_likes', 0):,}
- Total Retweets: {engagement.get('total_retweets', 0):,}
- Total Replies: {engagement.get('total_replies', 0):,}
- Average Engagement per Tweet: {engagement.get('avg_engagement', 0):.2f}

**Sample Tweets:**
{tweets_sample}

Please provide a comprehensive analysis covering:
1. **Trend Overview**: What is this trend about and why is it trending?
2. **Engagement Analysis**: Is this trend gaining or losing momentum?
3. **Audience Sentiment**: What's the general sentiment of the audience?
4. **Content Themes**: What are the main topics/themes within this trend?
5. **Strategic Recommendations**: What should marketers/content creators do?
6. **Potential Risks**: Any negative aspects or misinformation to watch?
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert social media analyst and strategist with deep knowledge of 
Twitter/X trends, viral content, audience behavior, and digital marketing. Provide data-driven, actionable insights 
that help content creators and marketers understand and capitalize on trending topics."""
                    },
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ]
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse the response into structured categories
            results = {
                "full_analysis": analysis_text,
                "timestamp": datetime.now().isoformat()
            }
            
            # Try to extract individual sections
            sections = [
                "Trend Overview",
                "Engagement Analysis",
                "Audience Sentiment",
                "Content Themes",
                "Strategic Recommendations",
                "Potential Risks"
            ]
            
            for section in sections:
                if section in analysis_text:
                    start = analysis_text.find(section)
                    end = analysis_text.find("\n", start + 100)
                    if end == -1:
                        end = len(analysis_text)
                    results[section.lower().replace(" ", "_")] = analysis_text[start:end].strip()
            
            logger.info(f"Generated analysis for #{hashtag}")
            return results
            
        except Exception as e:
            logger.error(f"Error explaining trend: {str(e)}")
            return {
                "error": str(e),
                "full_analysis": f"Could not analyze trend: {str(e)}"
            }


def demo_explanation_engine():
    """Demo the explanation engine with sample data."""
    print("=" * 80)
    print("TREND ANALYSIS EXPLANATION ENGINE DEMO")
    print("=" * 80)
    
    # Sample analysis result
    sample_analysis = {
        "trend_name": "#TechTok",
        "trend_status": "DECLINING",
        "severity_level": "WARNING",
        "decline_probability": 0.72,
        "confidence_in_analysis": 0.65,
        "cross_platform_summary": {
            "X": {
                "tweet_volume": 45000,
                "engagement_velocity": -0.15,
                "health_status": "Declining"
            }
        },
        "root_causes": [
            {
                "cause_type": "Engagement Decay",
                "confidence": 0.85,
                "business_explanation": "Users are interacting less with content"
            },
            {
                "cause_type": "Content Saturation",
                "confidence": 0.72,
                "business_explanation": "Trend has become oversaturated with repetitive content"
            }
        ]
    }
    
    # Initialize explainer
    explainer = TrendAnalysisExplainer()
    
    print("\n1. Generating cause explanations...")
    explanations = explainer.explain_decline_causes(sample_analysis)
    for cause, explanation in explanations.items():
        print(f"\n   {cause}:")
        print(f"   {explanation[:200]}...")
    
    print("\n2. Generating strategic recommendation...")
    strategy = explainer.generate_strategy(sample_analysis)
    print(f"   {strategy[:300]}...")
    
    print("\n3. Creating executive summary...")
    summary = explainer.generate_executive_summary(sample_analysis)
    print(f"   {summary[:300]}...")
    
    print("\n✅ Explanation engine demo complete!")


if __name__ == "__main__":
    demo_explanation_engine()
