#!/usr/bin/env python3
"""
Quick Twitter Trend Analyzer - Direct hashtag analysis with DeepSeek AI
Simply input a hashtag and get immediate AI-powered analysis
"""

import sys
import logging
from datetime import datetime
from twitter_api import TwitterAPIClient
from explanation_engine import TrendAnalysisExplainer
from config import Config

logging.basicConfig(
    level=logging.WARNING,  # Reduce noise
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_sample_tweets(hashtag, count=10):
    """Create sample tweet data when API is unavailable."""
    return [
        {
            "text": f"Sample tweet about #{hashtag} - Check out this trending topic! This is sample {i+1}",
            "id": f"sample_{i}",
            "public_metrics": {
                "like_count": 100 + (i * 50),
                "retweet_count": 30 + (i * 20),
                "reply_count": 10 + i,
            }
        }
        for i in range(count)
    ]


def process_tweets(tweets_data):
    """Process tweet data and extract metrics."""
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
    
    return processed_tweets


def analyze_hashtag_now(hashtag: str):
    """
    Quick analysis of any hashtag with immediate DeepSeek results.
    """
    
    # Clean hashtag
    if hashtag.startswith("#"):
        hashtag = hashtag[1:]
    
    print(f"\n{'='*80}")
    print(f"🔍 ANALYZING HASHTAG: #{hashtag}")
    print(f"{'='*80}\n")
    
    # Initialize API clients
    print("📥 Fetching tweets from Twitter API...")
    twitter_client = TwitterAPIClient(Config.TWITTER_API_KEY)
    search_result = twitter_client.search_tweets(hashtag, max_results=100)
    tweets_data = search_result.get("data", []) if isinstance(search_result, dict) else []
    
    if not tweets_data:
        print("⚠️  No tweets found via API. Using sample data for analysis...\n")
        tweets_data = create_sample_tweets(hashtag, 10)
    else:
        print(f"✅ Found {len(tweets_data)} tweets via API\n")
    
    # Process tweet data
    print("📊 Processing tweet metrics...")
    processed_tweets = process_tweets(tweets_data)
    
    # Calculate metrics
    total_likes = sum(t.get('likes', 0) for t in processed_tweets)
    total_retweets = sum(t.get('retweets', 0) for t in processed_tweets)
    total_replies = sum(t.get('replies', 0) for t in processed_tweets)
    avg_engagement = (total_likes + total_retweets + total_replies) / len(processed_tweets) if processed_tweets else 0
    
    print(f"   ✅ Tweets analyzed: {len(processed_tweets)}")
    print(f"   Total Likes: {total_likes:,}")
    print(f"   Total Retweets: {total_retweets:,}")
    print(f"   Total Replies: {total_replies:,}")
    print(f"   Avg Engagement: {avg_engagement:.2f}\n")
    
    # Prepare sample tweets text
    tweets_sample = "\n".join([
        f"Tweet {i+1}: {t.get('text', '')[:150]}... (Likes: {t.get('likes', 0)}, Retweets: {t.get('retweets', 0)})"
        for i, t in enumerate(processed_tweets[:5])
    ])
    
    # Get DeepSeek AI Analysis
    print("🤖 Requesting DeepSeek AI Analysis...")
    print("   (This may take a moment...)\n")
    
    try:
        explainer = TrendAnalysisExplainer(api_key=Config.FEATHERLESS_API_KEY)
        
        trend_data = {
            "trend_name": hashtag,
            "engagement_metrics": {
                "total_likes": total_likes,
                "total_retweets": total_retweets,
                "total_replies": total_replies,
                "avg_engagement": avg_engagement
            },
            "sample_tweets": tweets_sample,
            "total_tweets_analyzed": len(tweets_data)
        }
        
        analysis = explainer.explain_trend(trend_data)
        
        # Display the full analysis
        print("="*80)
        print(f"✅ AI ANALYSIS FOR #{hashtag}")
        print("="*80)
        
        if isinstance(analysis, dict):
            full_analysis = analysis.get('full_analysis', '')
            if full_analysis:
                print("\n" + full_analysis)
            else:
                print("\nNo analysis available")
        else:
            print(str(analysis))
        
        print("\n" + "="*80)
        print(f"Analysis completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"❌ Error getting AI analysis: {str(e)}")
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        print("   Make sure your DeepSeek API key is valid in config.py")
        print("   Current key (first 20 chars): " + Config.FEATHERLESS_API_KEY[:20] + "...\n")


def main():
    """Main entry point."""
    print("\n" + "="*80)
    print("🚀 TWITTER TREND ANALYZER WITH DEEPSEEK AI 🚀")
    print("="*80)
    print("\nAnalyze any Twitter hashtag with AI-powered insights\n")
    
    while True:
        try:
            hashtag = input("Enter a hashtag to analyze (or 'quit' to exit): ").strip()
            
            if hashtag.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for using Twitter Trend Analyzer!\n")
                break
            
            if not hashtag:
                print("❌ Please enter a valid hashtag\n")
                continue
            
            analyze_hashtag_now(hashtag)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            logger.error(f"Fatal error: {str(e)}", exc_info=True)
            print()


if __name__ == "__main__":
    main()
