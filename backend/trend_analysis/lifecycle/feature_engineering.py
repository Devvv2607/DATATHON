"""
Feature Engineering: Extract signals from Google Trends, Twitter, Reddit APIs
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import statistics

# Google Trends
from pytrends.request import TrendReq

# Twitter/X API
try:
    import tweepy
except ImportError:
    tweepy = None

# Reddit API
try:
    import praw
except ImportError:
    praw = None

from .schemas import GoogleTrendsSignals, TwitterSignals, RedditSignals, AggregatedSignals
from .utils import (
    calculate_slope, calculate_rolling_mean, calculate_velocity,
    calculate_growth_rate, calculate_momentum, detect_decay_signal,
    calculate_engagement_saturation, get_date_range, safe_divide
)

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Extract and compute features from multiple platforms
    """
    
    def __init__(self):
        self.google_client = None
        self.twitter_client = None
        self.reddit_client = None
        self._init_clients()
    
    def _init_clients(self):
        """Initialize API clients"""
        # Google Trends (no auth required)
        try:
            self.google_client = TrendReq(hl='en-US', tz=360)
            logger.info("✅ Google Trends client initialized")
        except Exception as e:
            logger.error(f"❌ Google Trends init failed: {e}")
        
        # Twitter/X API (requires keys)
        if tweepy:
            try:
                bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
                if bearer_token:
                    self.twitter_client = tweepy.Client(bearer_token=bearer_token)
                    logger.info("✅ Twitter API client initialized")
                else:
                    logger.warning("⚠️ TWITTER_BEARER_TOKEN not set")
            except Exception as e:
                logger.error(f"❌ Twitter API init failed: {e}")
        
        # Reddit API (requires credentials)
        if praw:
            try:
                client_id = os.getenv("REDDIT_CLIENT_ID")
                client_secret = os.getenv("REDDIT_CLIENT_SECRET")
                user_agent = os.getenv("REDDIT_USER_AGENT", "TrendAnalysis/1.0")
                
                if client_id and client_secret:
                    # Use read-only mode to avoid async issues
                    self.reddit_client = praw.Reddit(
                        client_id=client_id,
                        client_secret=client_secret,
                        user_agent=user_agent,
                        check_for_async=False  # Disable async warning
                    )
                    logger.info("✅ Reddit API client initialized (sync mode)")
                else:
                    logger.warning("⚠️ Reddit credentials not set")
            except Exception as e:
                logger.error(f"❌ Reddit API init failed: {e}")
    
    async def extract_google_signals(self, trend_name: str) -> GoogleTrendsSignals:
        """
        Extract Google Trends signals
        """
        try:
            if not self.google_client:
                raise ValueError("Google Trends client not initialized")
            
            # Build payload
            self.google_client.build_payload([trend_name], timeframe='today 3-m')
            
            # Get interest over time
            interest_df = self.google_client.interest_over_time()
            
            if interest_df.empty or trend_name not in interest_df.columns:
                logger.warning(f"No Google Trends data for '{trend_name}'")
                return self._default_google_signals()
            
            values = interest_df[trend_name].tolist()
            
            # Calculate features
            interest_score = values[-1] if values else 0.0
            interest_slope = calculate_slope(values)
            rolling_mean_interest = calculate_rolling_mean(values, window=7)
            
            return GoogleTrendsSignals(
                interest_score=float(interest_score),
                interest_slope=float(interest_slope),
                rolling_mean_interest=float(rolling_mean_interest),
                raw_data={
                    "values": values[-30:],  # Last 30 days
                    "query_date": datetime.now().isoformat()
                }
            )
        
        except Exception as e:
            logger.error(f"Google Trends extraction failed: {e}")
            return self._default_google_signals()
    
    async def extract_twitter_signals(self, trend_name: str) -> TwitterSignals:
        """
        Extract Twitter/X signals
        """
        try:
            if not self.twitter_client:
                raise ValueError("Twitter client not initialized")
            
            # Search recent tweets (last 7 days)
            start_time = datetime.now() - timedelta(days=7)
            
            tweets = self.twitter_client.search_recent_tweets(
                query=trend_name,
                max_results=100,
                start_time=start_time,
                tweet_fields=['public_metrics', 'created_at']
            )
            
            if not tweets.data:
                logger.warning(f"No Twitter data for '{trend_name}'")
                return self._default_twitter_signals()
            
            # Aggregate metrics
            total_likes = 0
            total_retweets = 0
            total_replies = 0
            post_volume = len(tweets.data)
            
            daily_volumes = {}
            for tweet in tweets.data:
                metrics = tweet.public_metrics
                total_likes += metrics.get('like_count', 0)
                total_retweets += metrics.get('retweet_count', 0)
                total_replies += metrics.get('reply_count', 0)
                
                # Track daily volume
                date_key = tweet.created_at.date().isoformat()
                daily_volumes[date_key] = daily_volumes.get(date_key, 0) + 1
            
            # Calculate engagement rate
            total_engagement = total_likes + total_retweets + total_replies
            engagement_rate = safe_divide(total_engagement, post_volume)
            
            # Calculate velocity
            volume_values = list(daily_volumes.values())
            velocity = calculate_momentum(volume_values) if len(volume_values) > 1 else 0.0
            
            return TwitterSignals(
                post_volume=post_volume,
                engagement_rate=float(engagement_rate),
                velocity=float(velocity),
                raw_data={
                    "total_likes": total_likes,
                    "total_retweets": total_retweets,
                    "total_replies": total_replies,
                    "daily_volumes": daily_volumes
                }
            )
        
        except Exception as e:
            logger.error(f"Twitter extraction failed: {e}")
            return self._default_twitter_signals()
    
    async def extract_reddit_signals(self, trend_name: str) -> RedditSignals:
        """
        Extract Reddit signals using integrated collector
        """
        logger.info(f"🔍 Extracting Reddit signals for '{trend_name}'...")
        
        try:
            if not self.reddit_client:
                logger.warning("❌ Reddit client not initialized")
                raise ValueError("Reddit client not initialized")
            
            # Use the same logic as reddit_collector but for lifecycle analysis
            from datetime import timedelta
            import re
            
            # Nostalgia detection keywords
            NOSTALGIA_KEYWORDS = [
                "remember", "throwback", "nostalgia", "back in", "used to", 
                "miss", "childhood", "old days", "tbt", "fbf", "flashback",
                "was popular", "died", "dead trend", "anyone remember", 
                "brings back", "good old", "rip", "miss when", "back when",
                "the days when", "vintage", "retro", "classic", "og"
            ]
            
            # Search Reddit for recent posts (last 7 days for velocity)
            all_posts = list(self.reddit_client.subreddit("all").search(
                trend_name, 
                time_filter='week', 
                limit=100
            ))
            
            if not all_posts:
                logger.warning(f"No Reddit data for '{trend_name}'")
                return self._default_reddit_signals()
            
            # Filter out nostalgia posts
            active_posts = []
            nostalgia_posts = []
            current_year = datetime.now().year
            
            for post in all_posts:
                title_lower = post.title.lower()
                
                # Check for nostalgia keywords
                has_nostalgia_keyword = any(keyword in title_lower for keyword in NOSTALGIA_KEYWORDS)
                
                # Check for old year mentions (2017-2022 are clearly old)
                old_years = [str(year) for year in range(2015, current_year - 2)]  # Years older than 2 years ago
                references_old_year = any(year in title_lower for year in old_years)
                
                # Check for phrases like "back in" + recent year (e.g., "back in 2023")
                has_past_reference = bool(re.search(r'(back in|remember.*20\d{2}|was.*20\d{2})', title_lower))
                
                if has_nostalgia_keyword or references_old_year or has_past_reference:
                    nostalgia_posts.append(post)
                else:
                    active_posts.append(post)
            
            # Use active posts (filter out nostalgia)
            posts = active_posts
            
            logger.info(f"📊 Reddit filtering: {len(all_posts)} total → {len(posts)} active, {len(nostalgia_posts)} nostalgia filtered")
            
            if not posts:
                logger.warning(f"All Reddit posts are nostalgia/throwback content for '{trend_name}'")
                return self._default_reddit_signals()
            
            # Aggregate metrics
            post_count = len(posts)
            total_comments = sum(post.num_comments for post in posts)
            total_score = sum(post.score for post in posts)
            
            # Track daily activity for growth calculation
            daily_posts = {}
            daily_comments = {}
            daily_scores = {}
            
            for post in posts:
                created = datetime.fromtimestamp(post.created_utc)
                date_key = created.date().isoformat()
                
                daily_posts[date_key] = daily_posts.get(date_key, 0) + 1
                daily_comments[date_key] = daily_comments.get(date_key, 0) + post.num_comments
                daily_scores[date_key] = daily_scores.get(date_key, 0) + post.score
            
            # Calculate discussion growth rate
            post_values = list(daily_posts.values())
            comment_values = list(daily_comments.values())
            
            post_growth = calculate_growth_rate(post_values) if len(post_values) > 1 else 0.0
            comment_growth = calculate_growth_rate(comment_values) if len(comment_values) > 1 else 0.0
            discussion_growth_rate = (post_growth + comment_growth) / 2
            
            logger.info(f"✅ Reddit: {post_count} posts, {total_comments} comments, growth: {discussion_growth_rate:.1f}%")
            
            return RedditSignals(
                post_count=post_count,
                comment_count=total_comments,
                discussion_growth_rate=float(discussion_growth_rate),
                raw_data={
                    "daily_posts": daily_posts,
                    "daily_comments": daily_comments,
                    "daily_scores": daily_scores,
                    "avg_score": float(total_score / post_count) if post_count > 0 else 0.0,
                    "total_score": total_score
                }
            )
        
        except Exception as e:
            logger.error(f"Reddit extraction failed: {e}")
            return self._default_reddit_signals()
    
    def compute_aggregated_signals(
        self,
        google: GoogleTrendsSignals,
        twitter: TwitterSignals,
        reddit: RedditSignals
    ) -> AggregatedSignals:
        """
        Compute cross-platform aggregated signals
        """
        # Extract recent values for momentum calculation
        google_values = google.raw_data.get("values", [0])
        
        # Growth rate (weighted average across platforms)
        google_growth = google.interest_slope * 10  # Scale slope to percentage
        twitter_growth = twitter.velocity
        reddit_growth = reddit.discussion_growth_rate
        
        growth_rate = (google_growth * 0.4 + twitter_growth * 0.3 + reddit_growth * 0.3)
        
        # Momentum (rolling average of growth)
        momentum = calculate_momentum([
            google.interest_score,
            twitter.engagement_rate,
            float(reddit.post_count)
        ])
        
        # Decay signal
        decay_signal = detect_decay_signal(google_values)
        
        # Engagement saturation
        peak_engagement = max(google_values) if google_values else 1.0
        current_engagement = google.interest_score
        engagement_saturation = calculate_engagement_saturation(
            current_engagement, 
            peak_engagement
        )
        
        return AggregatedSignals(
            growth_rate=float(growth_rate),
            momentum=float(momentum),
            decay_signal=float(decay_signal),
            engagement_saturation=float(engagement_saturation)
        )
    
    # === Default/Fallback Signals ===
    
    def _default_google_signals(self) -> GoogleTrendsSignals:
        return GoogleTrendsSignals(
            interest_score=0.0,
            interest_slope=0.0,
            rolling_mean_interest=0.0,
            raw_data={}
        )
    
    def _default_twitter_signals(self) -> TwitterSignals:
        return TwitterSignals(
            post_volume=0,
            engagement_rate=0.0,
            velocity=0.0,
            raw_data={}
        )
    
    def _default_reddit_signals(self) -> RedditSignals:
        return RedditSignals(
            post_count=0,
            comment_count=0,
            discussion_growth_rate=0.0,
            raw_data={}
        )
