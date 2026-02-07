"""
PyTrends + Groq Integration Module
Fetches trending data via PyTrends and enhances with Groq AI analysis
"""

import json
from typing import List, Dict, Any
from pytrends.request import TrendReq
from groq import Groq

class TrendsAnalyzer:
    """Fetch and analyze Google Trends data, enhanced with Groq API"""
    
    def __init__(self, groq_api_key: str = None):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        self.groq_client = Groq(api_key=groq_api_key) if groq_api_key else None
        self.model = "llama-3.3-70b-versatile"
    
    def get_trending_hashtags(self, keyword: str) -> List[str]:
        """
        Fetch related queries and convert to hashtags
        """
        try:
            self.pytrends.build_payload([keyword], timeframe='now 7-d')
            
            # Get related rising queries
            related_queries = self.pytrends.related_queries()
            
            hashtags = []
            
            if related_queries and keyword in related_queries:
                rising = related_queries[keyword].get('rising', [])
                top = related_queries[keyword].get('top', [])
                
                # Convert to hashtags
                if rising is not None and len(rising) > 0:
                    rising_hashtags = [f"#{q.replace(' ', '')}" for q in rising['query'].head(5).tolist()]
                    hashtags.extend(rising_hashtags)
                
                if top is not None and len(top) > 0:
                    top_hashtags = [f"#{q.replace(' ', '')}" for q in top['query'].head(5).tolist()]
                    hashtags.extend(top_hashtags)
            
            return hashtags[:10]  # Return top 10
        
        except Exception as e:
            return [f"#{keyword}"]
    
    def get_related_topics(self, keyword: str) -> List[str]:
        """
        Get related topics from Google Trends
        """
        try:
            self.pytrends.build_payload([keyword], timeframe='now 7-d')
            
            related_topics = self.pytrends.related_topics()
            
            topics = []
            if related_topics and keyword in related_topics:
                rising = related_topics[keyword].get('rising', [])
                top = related_topics[keyword].get('top', [])
                
                if rising is not None and len(rising) > 0:
                    rising_topics = rising['title'].head(3).tolist()
                    topics.extend(rising_topics)
                
                if top is not None and len(top) > 0:
                    top_topics = top['title'].head(3).tolist()
                    topics.extend(top_topics)
            
            return list(set(topics))
        
        except Exception as e:
            return [keyword]
    
    def analyze_trend(self, keyword: str) -> Dict[str, Any]:
        """
        Complete trend analysis with Groq enhancement
        """
        hashtags = self.get_trending_hashtags(keyword)
        topics = self.get_related_topics(keyword)
        
        raw_analysis = {
            "keyword": keyword,
            "hashtags": hashtags,
            "related_topics": topics,
        }
        
        # Enhance with Groq AI analysis
        if self.groq_client:
            enhanced = self._groq_enhance_trends(keyword, hashtags, topics)
            raw_analysis.update(enhanced)
        
        return raw_analysis
    
    def _groq_enhance_trends(self, keyword: str, hashtags: List[str], topics: List[str]) -> Dict[str, Any]:
        """
        Use Groq API to analyze and enhance trends data
        """
        prompt = f"""
Analyze this trending topic and provide strategic insights:

KEYWORD: {keyword}
TRENDING HASHTAGS: {', '.join(hashtags)}
RELATED TOPICS: {', '.join(topics)}

Provide analysis in JSON format with:
{{
    "trend_momentum": "rising|stable|declining",
    "audience_sentiment": "positive|mixed|negative",
    "best_content_angle": "brief description",
    "potential_creator_niches": ["niche1", "niche2", "niche3"],
    "recommended_posting_time": "description",
    "virality_potential": "high|medium|low",
    "growth_forecast": "brief forecast for next 7-30 days"
}}

Be concise and actionable.
"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7,
            )
            
            content = response.choices[0].message.content.strip()
            
            # Clean JSON
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            if content.endswith("```"):
                content = content[:-3]
            
            groq_insights = json.loads(content)
            return {"groq_insights": groq_insights}
        
        except Exception as e:
            return {"groq_insights": {"error": f"Analysis failed: {str(e)}"}}
    
    def generate_hashtags_with_groq(self, keyword: str) -> Dict[str, Any]:
        """
        Generate intelligent hashtags using Groq based on trends
        """
        hashtags = self.get_trending_hashtags(keyword)
        
        if not self.groq_client:
            return {"hashtags": hashtags, "hashtag_categories": {}}
        
        prompt = f"""
Categorize and enhance these trending hashtags for {keyword}:

HASHTAGS: {', '.join(hashtags)}

Return JSON with:
{{
    "viral_hashtags": ["hashtag1", "hashtag2"],
    "niche_hashtags": ["hashtag1", "hashtag2"],
    "reach_hashtags": ["hashtag1", "hashtag2"],
    "hashtag_strategy": "brief strategy"
}}
"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7,
            )
            
            content = response.choices[0].message.content.strip()
            
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            if content.endswith("```"):
                content = content[:-3]
            
            categorized = json.loads(content)
            return {
                "hashtags": hashtags,
                "categorized_hashtags": categorized
            }
        
        except Exception as e:
            return {"hashtags": hashtags, "error": str(e)}
