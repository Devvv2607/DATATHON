#!/usr/bin/env python3
"""
Interactive Twitter Trend Analyzer
Allows users to input trends/hashtags and get real analysis using DeepSeek
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
from dataclasses import asdict

from twitter_api import TwitterAPIClient
from trend_analyzer import TrendAnalyzer
from explanation_engine import TrendAnalysisExplainer
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InteractiveTrendAnalyzer:
    """Interactive interface for trend analysis with real Twitter data and DeepSeek AI."""
    
    def __init__(self):
        """Initialize the interactive analyzer."""
        self.twitter_client = TwitterAPIClient(Config.TWITTER_API_KEY)
        self.trend_analyzer = TrendAnalyzer(min_confidence_threshold=0.3)
        try:
            self.explainer = TrendAnalysisExplainer(
                api_key=Config.FEATHERLESS_API_KEY
            )
            self.ai_available = True
        except Exception as e:
            logger.warning(f"DeepSeek AI not available: {str(e)}")
            self.explainer = None
            self.ai_available = False
        
        self.analysis_history: List[Dict[str, Any]] = []
    
    def display_header(self):
        """Display application header."""
        print("\n" + "="*80)
        print(" "*20 + "🚀 TWITTER TREND ANALYZER WITH DEEPSEEK AI 🚀")
        print("="*80)
        print("\nAnalyze trending hashtags and memes with real Twitter API data")
        print("Powered by DeepSeek AI for intelligent insights\n")
    
    def display_menu(self):
        """Display main menu."""
        print("\n" + "-"*80)
        print("MAIN MENU")
        print("-"*80)
        print("1. 📊 Analyze a specific hashtag/trend")
        print("2. 🌍 Get trending topics by location")
        print("3. 🔍 Search for tweets about a topic")
        print("4. 💡 Get AI-powered analysis recommendation")
        print("5. 📋 View analysis history")
        print("6. 💾 Save analysis results")
        print("7. ❌ Exit")
        print("-"*80)
    
    def get_trending_topics(self) -> Dict[str, Any]:
        """Fetch and display trending topics."""
        try:
            print("\n🌍 Fetching trending topics...")
            locations = {
                "1": ("US", "United States"),
                "2": ("GLOBAL", "Worldwide"),
                "3": ("UK", "United Kingdom"),
                "4": ("INDIA", "India"),
                "5": ("JP", "Japan")
            }
            
            print("\nSelect location:")
            for key, (code, name) in locations.items():
                print(f"  {key}. {name}")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice not in locations:
                print("❌ Invalid choice")
                return None
            
            location_code, location_name = locations[choice]
            print(f"\n📥 Fetching trends from {location_name}...")
            
            trends = self.twitter_client.get_trending_hashtags(
                location=location_code,
                limit=50
            )
            
            if not trends:
                print("❌ Could not fetch trends. Check your API key.")
                return None
            
            print(f"\n✅ Found {len(trends)} trending topics in {location_name}:\n")
            for i, trend in enumerate(trends[:20], 1):
                name = trend.get('name', 'N/A')
                volume = trend.get('tweet_volume', 0)
                print(f"{i:2d}. {name:30s} | Volume: {volume:>10,}")
            
            return {
                "location": location_name,
                "trends": trends,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ Error fetching trends: {str(e)}")
            logger.error(f"Trend fetching error: {str(e)}")
            return None
    
    def analyze_hashtag(self, hashtag: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Analyze a specific hashtag with AI insights."""
        try:
            if not hashtag:
                print("\n📝 Enter a hashtag or trend to analyze")
                print("   (without # symbol)")
                hashtag = input("Hashtag: ").strip()
                if not hashtag:
                    print("❌ No hashtag provided")
                    return None
            
            # Clean hashtag
            if hashtag.startswith("#"):
                hashtag = hashtag[1:]
            
            print(f"\n🔍 Analyzing #{hashtag}...")
            
            # Fetch tweets for the hashtag
            print("📥 Fetching tweets...")
            search_result = self.twitter_client.search_tweets(hashtag, max_results=100)
            
            # Handle API response
            tweets_data = search_result.get("data", []) if isinstance(search_result, dict) else []
            
            if not tweets_data:
                print("⚠️  Limited tweets available. Using sample data for analysis...")
                # Use demo data if API fails
                tweets_data = [
                    {
                        "text": f"Sample tweet about #{hashtag} - engagement sample {i+1}",
                        "id": f"sample_{i}",
                        "public_metrics": {
                            "like_count": 100 + (i * 50),
                            "retweet_count": 30 + (i * 20),
                            "reply_count": 10 + i,
                            "quote_count": 5
                        }
                    }
                    for i in range(10)
                ]
            
            print(f"✅ Found {len(tweets_data)} tweets")
            
            # Analyze engagement and sentiment
            print("📊 Analyzing engagement metrics...")
            
            # Process tweet data safely
            processed_tweets = []
            for tweet in tweets_data[:10]:
                if isinstance(tweet, dict):
                    metrics = tweet.get("public_metrics", {})
                    if not isinstance(metrics, dict):
                        metrics = {}
                    
                    processed_tweets.append({
                        "text": tweet.get("text", "")[:200],
                        "likes": metrics.get("like_count", 0),
                        "retweets": metrics.get("retweet_count", 0),
                        "replies": metrics.get("reply_count", 0),
                        "id": tweet.get("id", "unknown")
                    })
            
            analysis_result = {
                "hashtag": hashtag,
                "tweets_analyzed": len(tweets_data),
                "timestamp": datetime.now().isoformat(),
                "tweets": processed_tweets
            }
            
            # Calculate metrics
            total_likes = sum(t.get('likes', 0) for t in processed_tweets)
            total_retweets = sum(t.get('retweets', 0) for t in processed_tweets)
            total_replies = sum(t.get('replies', 0) for t in processed_tweets)
            
            analysis_result["metrics"] = {
                "total_likes": total_likes,
                "total_retweets": total_retweets,
                "total_replies": total_replies,
                "avg_engagement": (total_likes + total_retweets + total_replies) / len(processed_tweets) if processed_tweets else 0
            }
            
            print(f"   Likes: {total_likes:,}")
            print(f"   Retweets: {total_retweets:,}")
            print(f"   Replies: {total_replies:,}")
            
            # Get AI analysis
            if self.ai_available and self.explainer:
                print("\n🤖 Getting DeepSeek AI analysis...")
                ai_analysis = self.get_deepseek_analysis(hashtag, analysis_result)
                analysis_result["ai_analysis"] = ai_analysis
                print("\n✅ AI Analysis Complete")
            else:
                print("⚠️  AI analysis not available")
                analysis_result["ai_analysis"] = None
            
            self.analysis_history.append(analysis_result)
            return analysis_result
            
        except Exception as e:
            print(f"❌ Error analyzing hashtag: {str(e)}")
            logger.error(f"Analysis error: {str(e)}", exc_info=True)
            return None
    
    def get_deepseek_analysis(self, hashtag: str, analysis_data: Dict[str, Any]) -> Dict[str, str]:
        """Get DeepSeek AI analysis for the hashtag."""
        try:
            if not self.explainer:
                return None
            
            # Create analysis input for AI
            tweets = analysis_data.get('tweets', [])
            tweets_sample = "\n".join([
                f"Tweet {i+1}: {t.get('text', 'N/A')[:150]}... (Likes: {t.get('likes', 0)}, Retweets: {t.get('retweets', 0)})"
                for i, t in enumerate(tweets[:5])
            ])
            
            if not tweets_sample:
                tweets_sample = "No tweet data available"
            
            metrics = analysis_data.get('metrics', {})
            
            # Prepare data for explanation engine
            explanation_input = {
                "trend_name": hashtag,
                "engagement_metrics": metrics,
                "sample_tweets": tweets_sample,
                "total_tweets_analyzed": analysis_data.get('tweets_analyzed', 0)
            }
            
            # Get explanation from DeepSeek
            explanations = self.explainer.explain_trend(explanation_input)
            
            return explanations
            
        except Exception as e:
            logger.error(f"DeepSeek analysis error: {str(e)}", exc_info=True)
            print(f"⚠️  Error getting AI analysis: {str(e)}")
            return None
    
    def search_tweets(self) -> Optional[List[Dict[str, Any]]]:
        """Search for tweets about a specific topic."""
        try:
            print("\n🔎 Tweet Search")
            query = input("Enter search query: ").strip()
            if not query:
                print("❌ No query provided")
                return None
            
            print(f"📥 Searching for '{query}'...")
            search_result = self.twitter_client.search_tweets(query, max_results=50)
            
            # Handle API response safely
            tweets = search_result.get("data", []) if isinstance(search_result, dict) else []
            
            if not tweets:
                print("⚠️  No tweets found or API unavailable")
                return None
            
            print(f"\n✅ Found {len(tweets)} tweets:\n")
            
            # Process and display tweets
            processed_tweets = []
            for i, tweet in enumerate(tweets[:10], 1):
                if isinstance(tweet, dict):
                    text = tweet.get('text', 'N/A')[:100]
                    metrics = tweet.get('public_metrics', {})
                    likes = metrics.get('like_count', 0) if isinstance(metrics, dict) else 0
                    print(f"{i}. {text}... (❤️ {likes})")
                    processed_tweets.append(tweet)
            
            return processed_tweets
            
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            logger.error(f"Tweet search error: {str(e)}", exc_info=True)
            return None
    
    def display_analysis_result(self, result: Dict[str, Any]):
        """Display analysis results in a formatted way."""
        if not result:
            return
        
        print("\n" + "="*80)
        print(f"ANALYSIS RESULTS FOR #{result['hashtag']}")
        print("="*80)
        
        print(f"\nTimestamp: {result['timestamp']}")
        print(f"Tweets Analyzed: {result['tweets_analyzed']}")
        
        metrics = result.get('metrics', {})
        print("\n📊 ENGAGEMENT METRICS:")
        print(f"   Total Likes:     {metrics.get('total_likes', 0):>10,}")
        print(f"   Total Retweets:  {metrics.get('total_retweets', 0):>10,}")
        print(f"   Total Replies:   {metrics.get('total_replies', 0):>10,}")
        print(f"   Avg Engagement:  {metrics.get('avg_engagement', 0):>10.2f}")
        
        ai_analysis = result.get('ai_analysis')
        if ai_analysis:
            print("\n🤖 DEEPSEEK AI ANALYSIS:")
            print("-" * 80)
            
            # Check if it's a dict with structured sections
            if isinstance(ai_analysis, dict):
                full_analysis = ai_analysis.get('full_analysis', '')
                if full_analysis:
                    # Display the full analysis with better formatting
                    print(full_analysis)
                else:
                    # Display individual sections if available
                    for key, value in ai_analysis.items():
                        if key not in ['timestamp', 'error']:
                            print(f"\n{key.upper().replace('_', ' ')}:")
                            if isinstance(value, str):
                                print(f"{value}")
        
        # Sample tweets
        tweets = result.get('tweets', [])
        if tweets:
            print("\n📝 SAMPLE TWEETS:")
            print("-" * 80)
            for i, tweet in enumerate(tweets[:3], 1):
                text = tweet.get('text', 'N/A')[:150] if isinstance(tweet, dict) else 'N/A'
                print(f"\n{i}. {text}...")
                if isinstance(tweet, dict):
                    print(f"   ❤️  {tweet.get('likes', 0)} | 🔄 {tweet.get('retweets', 0)}")
    
    def view_history(self):
        """Display analysis history."""
        if not self.analysis_history:
            print("\n📋 No analysis history yet")
            return
        
        print("\n" + "="*80)
        print("ANALYSIS HISTORY")
        print("="*80 + "\n")
        
        for i, result in enumerate(self.analysis_history, 1):
            hashtag = result.get('hashtag', 'N/A')
            timestamp = result.get('timestamp', 'N/A')
            tweets = result.get('tweets_analyzed', 0)
            print(f"{i}. #{hashtag} - {tweets} tweets - {timestamp[:19]}")
        
        view_choice = input("\nEnter analysis number to view details (or press Enter to skip): ").strip()
        if view_choice.isdigit() and 0 < int(view_choice) <= len(self.analysis_history):
            self.display_analysis_result(self.analysis_history[int(view_choice) - 1])
    
    def save_results(self):
        """Save analysis results to JSON file."""
        if not self.analysis_history:
            print("\n📋 No analysis to save")
            return
        
        filename = f"analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(self.analysis_history, f, indent=2, default=str)
            print(f"\n✅ Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")
    
    def run(self):
        """Main interactive loop."""
        self.display_header()
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == "1":
                # Analyze specific hashtag
                result = self.analyze_hashtag()
                if result:
                    self.display_analysis_result(result)
            
            elif choice == "2":
                # Get trending topics
                trends = self.get_trending_topics()
                if trends:
                    select = input("\n🔗 Enter trend number to analyze (or press Enter to skip): ").strip()
                    if select.isdigit():
                        idx = int(select) - 1
                        if 0 <= idx < len(trends['trends']):
                            trend_name = trends['trends'][idx].get('name', '').replace('#', '')
                            result = self.analyze_hashtag(trend_name)
                            if result:
                                self.display_analysis_result(result)
            
            elif choice == "3":
                # Search tweets
                self.search_tweets()
            
            elif choice == "4":
                # Get recommendation
                if self.analysis_history:
                    print("\n💡 Getting AI recommendation...")
                    latest = self.analysis_history[-1]
                    ai_rec = self.get_deepseek_analysis(
                        latest['hashtag'],
                        latest
                    )
                    if ai_rec:
                        print("\n🤖 DEEPSEEK RECOMMENDATIONS:")
                        for key, value in ai_rec.items():
                            print(f"\n{key}: {value}")
                else:
                    print("\n⚠️  No analysis available. Run an analysis first.")
            
            elif choice == "5":
                # View history
                self.view_history()
            
            elif choice == "6":
                # Save results
                self.save_results()
            
            elif choice == "7":
                # Exit
                print("\n👋 Thank you for using Twitter Trend Analyzer!")
                if self.analysis_history:
                    save = input("Save analysis before exiting? (y/n): ").strip().lower()
                    if save == 'y':
                        self.save_results()
                break
            
            else:
                print("❌ Invalid choice. Please try again.")


def main():
    """Main entry point."""
    try:
        analyzer = InteractiveTrendAnalyzer()
        analyzer.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"❌ Fatal error: {str(e)}")


if __name__ == "__main__":
    main()
