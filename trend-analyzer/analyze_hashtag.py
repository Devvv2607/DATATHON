#!/usr/bin/env python3
"""
Simple Twitter Hashtag Analyzer
Input any hashtag and get instant DeepSeek AI analysis
"""

import os
import sys
from datetime import datetime
import logging

from twitter_api import TwitterAPIClient
from explanation_engine import TrendAnalysisExplainer
from config import Config

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def generate_sample_tweets(hashtag: str, count: int = 10):
    """Generate sample tweets if API fails."""
    return [
        {
            "text": f"Just learned about #{hashtag}! This trend is absolutely amazing and getting everyone talking right now.",
            "likes": 245,
            "retweets": 87,
            "replies": 34,
            "id": f"sample_1"
        },
        {
            "text": f"#{hashtag} is trending! Everyone's sharing their thoughts and reactions. The engagement is incredible!",
            "likes": 512,
            "retweets": 203,
            "replies": 89,
            "id": f"sample_2"
        },
        {
            "text": f"Can't stop scrolling through #{hashtag}. The creativity and responses from the community are fire 🔥",
            "likes": 678,
            "retweets": 234,
            "replies": 145,
            "id": f"sample_3"
        },
        {
            "text": f"#{hashtag} just broke my timeline. Never seen this much engagement before!",
            "likes": 1203,
            "retweets": 456,
            "replies": 234,
            "id": f"sample_4"
        },
        {
            "text": f"The #{hashtag} trend explains so much. Finally people are talking about this!",
            "likes": 889,
            "retweets": 321,
            "replies": 156,
            "id": f"sample_5"
        },
        {
            "text": f"#{hashtag} is everything right now. Check the replies, people have THOUGHTS 👀",
            "likes": 745,
            "retweets": 289,
            "replies": 178,
            "id": f"sample_6"
        },
        {
            "text": f"When #{hashtag} started trending, everyone had the same reaction. Absolutely viral.",
            "likes": 567,
            "retweets": 198,
            "replies": 98,
            "id": f"sample_7"
        },
        {
            "text": f"#{hashtag} is proof that social media still has the power to unite people. Incredible to see!",
            "likes": 834,
            "retweets": 312,
            "replies": 167,
            "id": f"sample_8"
        },
        {
            "text": f"The insights in #{hashtag} are blowing my mind. This conversation needs to happen more often.",
            "likes": 421,
            "retweets": 156,
            "replies": 87,
            "id": f"sample_9"
        },
        {
            "text": f"#{hashtag} trending means we all woke up and chose to talk about something important today.",
            "likes": 923,
            "retweets": 345,
            "replies": 201,
            "id": f"sample_10"
        },
    ]


def analyze_hashtag(hashtag: str):
    """Analyze a hashtag with real data or sample data."""
    
    # Clean hashtag
    if hashtag.startswith("#"):
        hashtag = hashtag[1:]
    
    print(f"\n{'='*80}")
    print(f"🔍 ANALYZING: #{hashtag}")
    print(f"{'='*80}\n")
    
    # Step 1: Fetch tweets
    print("📥 Fetching tweets from Twitter API...")
    twitter_client = TwitterAPIClient(Config.TWITTER_API_KEY)
    search_result = twitter_client.search_tweets(hashtag, max_results=100)
    
    # Handle response
    tweets_data = search_result.get("data", []) if isinstance(search_result, dict) else []
    
    if not tweets_data:
        print("   ⚠️  API unavailable or no tweets found. Using sample data for analysis...\n")
        tweets_data = generate_sample_tweets(hashtag)
    else:
        print(f"   ✅ Found {len(tweets_data)} real tweets\n")
    
    # Step 2: Process tweets
    print("📊 Processing tweet data...")
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
            })
    
    # Calculate metrics
    total_likes = sum(t.get('likes', 0) for t in processed_tweets)
    total_retweets = sum(t.get('retweets', 0) for t in processed_tweets)
    total_replies = sum(t.get('replies', 0) for t in processed_tweets)
    total_engagement = total_likes + total_retweets + total_replies
    
    print(f"   ✅ Processed {len(processed_tweets)} tweets\n")
    
    # Step 3: Show basic metrics
    print("📈 BASIC METRICS:")
    print(f"   Total Likes:      {total_likes:>10,}")
    print(f"   Total Retweets:   {total_retweets:>10,}")
    print(f"   Total Replies:    {total_replies:>10,}")
    print(f"   Total Engagement: {total_engagement:>10,}")
    print()
    
    # Step 4: Get AI Analysis
    print("🤖 Generating DeepSeek AI Analysis...")
    print("   Please wait...\n")
    
    try:
        explainer = TrendAnalysisExplainer(api_key=Config.FEATHERLESS_API_KEY)
        
        # Format tweet samples
        tweets_sample = "\n".join([
            f"   • {t.get('text', '')[:150]}... (❤️ {t.get('likes', 0)})"
            for t in processed_tweets[:5]
        ])
        
        # Create analysis input
        analysis_input = {
            "trend_name": hashtag,
            "engagement_metrics": {
                "total_likes": total_likes,
                "total_retweets": total_retweets,
                "total_replies": total_replies,
                "avg_engagement": total_engagement / len(processed_tweets) if processed_tweets else 0
            },
            "sample_tweets": tweets_sample,
            "total_tweets_analyzed": len(tweets_data)
        }
        
        # Get analysis
        ai_analysis = explainer.explain_trend(analysis_input)
        
        # Display results
        print(f"{'='*80}")
        print(f"✅ DEEPSEEK AI ANALYSIS FOR #{hashtag}")
        print(f"{'='*80}\n")
        
        if ai_analysis:
            full_analysis = ai_analysis.get('full_analysis', '')
            if full_analysis:
                print(full_analysis)
            else:
                print("Analysis completed but no detailed output.")
        
        # Show sample tweets
        print(f"\n{'='*80}")
        print(f"📝 SAMPLE TWEETS")
        print(f"{'='*80}\n")
        
        for i, tweet in enumerate(processed_tweets[:5], 1):
            print(f"{i}. {tweet.get('text', '')}")
            print(f"   ❤️  {tweet.get('likes', 0):>6} | 🔄 {tweet.get('retweets', 0):>6} | 💬 {tweet.get('replies', 0):>6}\n")
        
    except Exception as e:
        print(f"❌ Error getting AI analysis: {str(e)}")
        print(f"\nTroubleshooting:")
        print(f"   • Check your DeepSeek API key in config.py")
        print(f"   • Check your internet connection")
        print(f"   • The API might be temporarily unavailable")


def main():
    """Main function."""
    print("\n" + "="*80)
    print(" "*15 + "🚀 TWITTER HASHTAG ANALYZER WITH DEEPSEEK AI 🚀")
    print("="*80)
    print("\nAnalyze any hashtag or trend and get instant AI-powered insights!\n")
    
    while True:
        hashtag = input("Enter hashtag to analyze (or 'exit' to quit): ").strip()
        
        if hashtag.lower() == 'exit':
            print("\n👋 Thank you for using the analyzer!")
            break
        
        if not hashtag:
            print("❌ Please enter a valid hashtag\n")
            continue
        
        analyze_hashtag(hashtag)
        
        print("\n" + "-"*80 + "\n")


if __name__ == "__main__":
    main()
