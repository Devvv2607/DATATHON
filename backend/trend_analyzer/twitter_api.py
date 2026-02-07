"""
Twitter/X API Integration Module
Fetches real trending data, tweets, and engagement metrics
"""

import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TrendingHashtag:
    """Represents a trending hashtag on Twitter."""
    name: str
    tweet_volume: int
    url: str
    query: str


class TwitterAPIClient:
    """Client for Twitter/X API integration via RapidAPI."""
    
    def __init__(self, api_key: str):
        """
        Initialize Twitter API client.
        
        Args:
            api_key: RapidAPI key for Twitter/X endpoints
        """
        self.api_key = api_key
        self.base_url = "https://twitter-api45.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "twitter-api45.p.rapidapi.com"
        }
        self.session = requests.Session()
    
    def get_trending_hashtags(self, location: str = "US", limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch trending hashtags from Twitter.
        
        Args:
            location: Location code (e.g., "US", "GLOBAL", "UK")
            limit: Maximum number of trends to return
        
        Returns:
            List of trending hashtag objects with metrics
        """
        try:
            endpoint = f"{self.base_url}/api/v1/trends"
            params = {
                "location": location,
                "count": min(limit, 100)
            }
            
            response = self.session.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                trends = data.get("trends", [])
                logger.info(f"Fetched {len(trends)} trending hashtags from {location}")
                return trends
            else:
                logger.error(f"Twitter API error: {response.status_code} - {response.text}")
                return []
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching trends: {str(e)}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return []
    
    def search_tweets(
        self,
        query: str,
        max_results: int = 100,
        tweet_fields: str = "public_metrics,created_at,author_id"
    ) -> Dict[str, Any]:
        """
        Search for tweets matching a query.
        
        Args:
            query: Search query (e.g., "#hashtag" or "keyword")
            max_results: Max tweets to return (1-100)
            tweet_fields: Comma-separated fields to include
        
        Returns:
            Search results with tweets and metadata
        """
        try:
            endpoint = f"{self.base_url}/api/v1/tweets/search/recent"
            params = {
                "query": query,
                "max_results": min(max_results, 100),
                "tweet.fields": tweet_fields
            }
            
            response = self.session.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                tweet_count = len(data.get("data", []))
                logger.info(f"Found {tweet_count} tweets for query: {query}")
                return data
            else:
                logger.error(f"Search error: {response.status_code}")
                return {"data": [], "meta": {}}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error searching tweets: {str(e)}")
            return {"data": [], "meta": {}}
    
    def get_tweet_metrics(self, tweet_ids: List[str]) -> Dict[str, Any]:
        """
        Get engagement metrics for specific tweets.
        
        Args:
            tweet_ids: List of tweet IDs
        
        Returns:
            Dictionary with tweet metrics (likes, retweets, etc.)
        """
        try:
            endpoint = f"{self.base_url}/api/v1/tweets"
            params = {
                "ids": ",".join(tweet_ids),
                "tweet.fields": "public_metrics,created_at"
            }
            
            response = self.session.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Fetched metrics for {len(tweet_ids)} tweets")
                return data
            else:
                logger.error(f"Metrics error: {response.status_code}")
                return {"data": []}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching metrics: {str(e)}")
            return {"data": []}
    
    def get_hashtag_analytics(self, hashtag: str) -> Dict[str, Any]:
        """
        Get analytics for a specific hashtag.
        
        Args:
            hashtag: Hashtag to analyze (with or without #)
        
        Returns:
            Analytics including volume, engagement, sentiment
        """
        try:
            # Ensure hashtag starts with #
            if not hashtag.startswith("#"):
                hashtag = f"#{hashtag}"
            
            # Search for recent tweets with this hashtag
            tweets = self.search_tweets(hashtag, max_results=100)
            
            if not tweets.get("data"):
                logger.warning(f"No tweets found for {hashtag}")
                return {
                    "hashtag": hashtag,
                    "tweet_count": 0,
                    "avg_engagement": 0,
                    "trending": False
                }
            
            # Calculate metrics
            tweet_data = tweets["data"]
            metrics = [t.get("public_metrics", {}) for t in tweet_data]
            
            total_likes = sum(m.get("like_count", 0) for m in metrics)
            total_retweets = sum(m.get("retweet_count", 0) for m in metrics)
            total_replies = sum(m.get("reply_count", 0) for m in metrics)
            
            avg_engagement = (total_likes + total_retweets + total_replies) / len(tweet_data) if tweet_data else 0
            
            analytics = {
                "hashtag": hashtag,
                "tweet_count": len(tweet_data),
                "total_likes": total_likes,
                "total_retweets": total_retweets,
                "total_replies": total_replies,
                "avg_engagement": avg_engagement,
                "engagement_per_tweet": avg_engagement,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"Analytics for {hashtag}: {tweet_data.__len__()} tweets, {avg_engagement:.1f} avg engagement")
            return analytics
        
        except Exception as e:
            logger.error(f"Error calculating hashtag analytics: {str(e)}")
            return {
                "hashtag": hashtag,
                "error": str(e)
            }
    
    def get_user_tweets(self, user_id: str, max_results: int = 100) -> Dict[str, Any]:
        """
        Get recent tweets from a specific user.
        
        Args:
            user_id: Twitter user ID
            max_results: Max tweets to return
        
        Returns:
            User's recent tweets with metrics
        """
        try:
            endpoint = f"{self.base_url}/api/v1/users/{user_id}/tweets"
            params = {
                "max_results": min(max_results, 100),
                "tweet.fields": "public_metrics,created_at"
            }
            
            response = self.session.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Fetched tweets for user {user_id}")
                return data
            else:
                logger.error(f"User tweets error: {response.status_code}")
                return {"data": []}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error fetching user tweets: {str(e)}")
            return {"data": []}


class TwitterMetricsCollector:
    """Collects and aggregates Twitter metrics for trend analysis."""
    
    def __init__(self, api_key: str):
        """Initialize metrics collector with Twitter API client."""
        self.client = TwitterAPIClient(api_key)
    
    def collect_trend_metrics(self, hashtag: str, time_period: int = 7) -> Dict[str, Any]:
        """
        Collect comprehensive metrics for a hashtag trend.
        
        Args:
            hashtag: Hashtag to analyze
            time_period: Period in days to analyze (currently uses recent tweets)
        
        Returns:
            Complete metrics structure for TrendAnalyzer
        """
        logger.info(f"Collecting metrics for {hashtag}")
        
        # Get hashtag analytics
        analytics = self.client.get_hashtag_analytics(hashtag)
        
        if "error" in analytics:
            logger.error(f"Failed to collect metrics: {analytics['error']}")
            return None
        
        # Build metrics in TrendAnalyzer format
        metrics = {
            "trend_name": hashtag,
            "x": {
                "tweet_volume": {
                    "current": analytics.get("tweet_count", 0),
                    "previous_period": max(1, analytics.get("tweet_count", 0) - 500)  # Simulated
                },
                "weekly_engagement_velocity": self._calculate_velocity(analytics),
                "unique_content_ratio": self._estimate_uniqueness(analytics),
                "reach_per_tweet": {
                    "current": analytics.get("engagement_per_tweet", 0),
                    "previous_period": max(1, analytics.get("engagement_per_tweet", 0) - 5)
                },
                "sentiment_score": {
                    "current": self._estimate_sentiment(analytics),
                    "previous_period": 0
                }
            }
        }
        
        return metrics
    
    def _calculate_velocity(self, analytics: Dict[str, Any]) -> float:
        """
        Estimate engagement velocity from analytics.
        
        Returns velocity as percentage change (-1.0 to 1.0)
        """
        # If engagement is high, assume positive velocity
        # If low, assume negative
        engagement = analytics.get("avg_engagement", 0)
        
        if engagement < 1:
            return -0.2  # Declining
        elif engagement < 5:
            return 0.0   # Stable
        elif engagement < 20:
            return 0.15  # Growing
        else:
            return 0.35  # Strong growth
    
    def _estimate_uniqueness(self, analytics: Dict[str, Any]) -> float:
        """
        Estimate content uniqueness (0-1).
        Based on engagement diversity.
        """
        # Higher engagement = more diverse/unique content likely
        engagement = analytics.get("avg_engagement", 0)
        
        if engagement < 1:
            return 0.1   # Mostly repetitive
        elif engagement < 5:
            return 0.35
        elif engagement < 20:
            return 0.6
        else:
            return 0.8   # Very unique
    
    def _estimate_sentiment(self, analytics: Dict[str, Any]) -> float:
        """
        Estimate sentiment (-1 to 1) from engagement patterns.
        Simplified heuristic: high engagement = positive sentiment
        """
        engagement = analytics.get("avg_engagement", 0)
        
        if engagement < 1:
            return -0.3  # Negative (low engagement)
        elif engagement < 5:
            return 0.0   # Neutral
        elif engagement < 20:
            return 0.4   # Positive
        else:
            return 0.7   # Very positive
    
    def compare_trends(self, hashtags: List[str]) -> Dict[str, Any]:
        """
        Compare multiple hashtags and rank by momentum.
        
        Args:
            hashtags: List of hashtags to compare
        
        Returns:
            Ranked comparison with momentum scores
        """
        results = []
        
        for hashtag in hashtags:
            metrics = self.collect_trend_metrics(hashtag)
            if metrics:
                results.append({
                    "hashtag": hashtag,
                    "metrics": metrics,
                    "engagement": metrics["x"].get("reach_per_tweet", {}).get("current", 0),
                    "velocity": metrics["x"].get("weekly_engagement_velocity", 0)
                })
        
        # Sort by momentum (velocity * engagement)
        results.sort(
            key=lambda x: (x["velocity"] * x["engagement"]),
            reverse=True
        )
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "trends_analyzed": len(results),
            "ranked_trends": results
        }


def demo_twitter_api():
    """Demo function showing Twitter API usage."""
    print("=" * 80)
    print("TWITTER API INTEGRATION DEMO")
    print("=" * 80)
    
    # Example API key (replace with actual)
    api_key = "YOUR_RAPIDAPI_KEY_HERE"
    
    client = TwitterAPIClient(api_key)
    
    print("\n1. Fetching trending hashtags...")
    trends = client.get_trending_hashtags(location="US", limit=10)
    if trends:
        for trend in trends[:5]:
            print(f"   - {trend.get('name', 'N/A')}: {trend.get('tweet_volume', 0)} tweets")
    
    print("\n2. Collecting metrics for a hashtag...")
    collector = TwitterMetricsCollector(api_key)
    # metrics = collector.collect_trend_metrics("#Python")
    # print(f"   Collected metrics: {metrics}")
    
    print("\n✅ API integration module ready!")


if __name__ == "__main__":
    demo_twitter_api()
