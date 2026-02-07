"""
Reddit Data Collector
Integrated version of the standalone Reddit scraper for trend analysis
"""

import praw
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter()

# Reddit API Credentials
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "TrendLens/1.0")

# Configuration
DEFAULT_DAYS_BACK = 30
DEFAULT_POST_LIMIT = 100
TOP_COMMENTS_LIMIT = 50


# === Pydantic Models ===

class RedditSearchRequest(BaseModel):
    """Request model for Reddit data collection"""
    keyword: str = Field(..., min_length=1, max_length=200)
    days_back: int = Field(default=30, ge=1, le=90)
    post_limit: int = Field(default=100, ge=10, le=500)
    fetch_comments: bool = Field(default=True)
    subreddits: Optional[List[str]] = Field(default=None)


class RedditPostSummary(BaseModel):
    """Summary of collected Reddit data"""
    total_posts: int
    total_comments: int
    date_range: str
    top_subreddits: List[Dict[str, Any]]
    avg_score: float
    avg_comments_per_post: float


class RedditCollectionResponse(BaseModel):
    """Response model for Reddit data collection"""
    success: bool
    keyword: str
    summary: RedditPostSummary
    posts: List[Dict[str, Any]]


# === Helper Functions ===

def create_reddit_instance():
    """Create and return a Reddit instance using PRAW"""
    try:
        return praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD,
            user_agent=REDDIT_USER_AGENT
        )
    except Exception as e:
        logger.error(f"Failed to create Reddit instance: {e}")
        raise HTTPException(status_code=500, detail="Reddit API authentication failed")


def get_cutoff_timestamp(days_back: int) -> float:
    """Calculate the UTC timestamp for the cutoff date"""
    cutoff_date = datetime.utcnow() - timedelta(days=days_back)
    return cutoff_date.timestamp()


def extract_post_data(post) -> Dict[str, Any]:
    """Extract relevant data from a Reddit post"""
    created_dt = datetime.utcfromtimestamp(post.created_utc)
    
    return {
        "post_id": post.id,
        "title": post.title,
        "selftext": post.selftext[:500] if post.selftext else "",  # Truncate for response size
        "subreddit": post.subreddit.display_name,
        "author": str(post.author) if post.author else "[deleted]",
        "created_utc": post.created_utc,
        "created_datetime": created_dt.isoformat(),
        "created_date": created_dt.strftime("%Y-%m-%d"),
        "score": post.score,
        "upvote_ratio": post.upvote_ratio,
        "num_comments": post.num_comments,
        "url": post.url,
        "permalink": f"https://reddit.com{post.permalink}",
        "comments": []
    }


def extract_comment_data(comment) -> Dict[str, Any]:
    """Extract relevant data from a Reddit comment"""
    created_dt = datetime.utcfromtimestamp(comment.created_utc)
    
    return {
        "comment_id": comment.id,
        "author": str(comment.author) if comment.author else "[deleted]",
        "body": comment.body[:300] if comment.body else "",  # Truncate
        "score": comment.score,
        "created_utc": comment.created_utc,
        "created_datetime": created_dt.isoformat(),
    }


def get_top_comments(post, limit: int = 50) -> List[Dict[str, Any]]:
    """Get top comments from a post"""
    comments = []
    
    try:
        post.comments.replace_more(limit=0)
        all_comments = post.comments.list()
        sorted_comments = sorted(all_comments, key=lambda x: x.score, reverse=True)[:limit]
        
        for comment in sorted_comments:
            try:
                comments.append(extract_comment_data(comment))
            except Exception:
                continue
    except Exception as e:
        logger.warning(f"Could not fetch comments: {e}")
    
    return comments


def search_reddit(
    reddit, 
    keyword: str, 
    cutoff_timestamp: float, 
    post_limit: int = 100,
    fetch_comments: bool = True,
    subreddits: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """Search Reddit for posts containing the keyword"""
    posts = []
    
    try:
        # Search scope
        if subreddits:
            subreddit_str = '+'.join(subreddits)
            search_sub = reddit.subreddit(subreddit_str)
            logger.info(f"Searching subreddits: {subreddit_str}")
        else:
            search_sub = reddit.subreddit('all')
            logger.info("Searching ALL of Reddit")
        
        # Search posts
        post_count = 0
        for post in search_sub.search(keyword, sort="new", time_filter="month", limit=post_limit):
            if post.created_utc >= cutoff_timestamp:
                post_count += 1
                logger.info(f"[{post_count}] r/{post.subreddit.display_name} | {post.title[:50]}...")
                
                post_data = extract_post_data(post)
                
                # Get comments if requested
                if fetch_comments and post.num_comments > 0:
                    post_data["comments"] = get_top_comments(post, TOP_COMMENTS_LIMIT)
                
                posts.append(post_data)
                
    except Exception as e:
        logger.error(f"Error searching Reddit: {e}")
        raise HTTPException(status_code=500, detail=f"Reddit search failed: {str(e)}")
    
    logger.info(f"Total posts collected: {len(posts)}")
    return posts


def calculate_summary(posts: List[Dict[str, Any]], days_back: int) -> RedditPostSummary:
    """Calculate summary statistics from collected posts"""
    if not posts:
        return RedditPostSummary(
            total_posts=0,
            total_comments=0,
            date_range=f"Last {days_back} days",
            top_subreddits=[],
            avg_score=0.0,
            avg_comments_per_post=0.0
        )
    
    total_comments = sum(post['num_comments'] for post in posts)
    total_score = sum(post['score'] for post in posts)
    
    # Count posts per subreddit
    subreddit_counts = {}
    for post in posts:
        sub = post['subreddit']
        subreddit_counts[sub] = subreddit_counts.get(sub, 0) + 1
    
    # Get top 5 subreddits
    top_subreddits = [
        {"name": sub, "post_count": count}
        for sub, count in sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    
    return RedditPostSummary(
        total_posts=len(posts),
        total_comments=total_comments,
        date_range=f"Last {days_back} days",
        top_subreddits=top_subreddits,
        avg_score=round(total_score / len(posts), 2),
        avg_comments_per_post=round(total_comments / len(posts), 2)
    )


# === API Endpoints ===

@router.post(
    "/api/data/reddit/search",
    response_model=RedditCollectionResponse,
    summary="Collect Reddit Data for Trend",
    description="Search Reddit for posts related to a trend keyword and collect engagement data",
    tags=["Data Collection"]
)
async def collect_reddit_data(request: RedditSearchRequest):
    """
    Collect Reddit data for trend analysis
    
    **Example Request:**
    ```json
    {
      "keyword": "Grimace Shake",
      "days_back": 30,
      "post_limit": 100,
      "fetch_comments": true
    }
    ```
    
    **Returns:**
    - Total posts and comments
    - Top subreddits
    - Engagement metrics
    - Full post data
    """
    logger.info(f"🔍 Reddit collection request: {request.keyword}")
    
    try:
        # Create Reddit client
        reddit = create_reddit_instance()
        
        # Calculate cutoff
        cutoff_timestamp = get_cutoff_timestamp(request.days_back)
        
        # Search Reddit
        posts = search_reddit(
            reddit,
            request.keyword,
            cutoff_timestamp,
            request.post_limit,
            request.fetch_comments,
            request.subreddits
        )
        
        # Calculate summary
        summary = calculate_summary(posts, request.days_back)
        
        logger.info(f"✅ Collected {len(posts)} posts from Reddit")
        
        return RedditCollectionResponse(
            success=True,
            keyword=request.keyword,
            summary=summary,
            posts=posts
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Reddit collection failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Reddit data collection failed: {str(e)}"
        )


@router.get(
    "/api/data/reddit/health",
    summary="Reddit API Health Check",
    description="Check if Reddit API is properly configured and accessible",
    tags=["Data Collection"]
)
async def reddit_health_check():
    """Check Reddit API connection"""
    try:
        reddit = create_reddit_instance()
        # Test by getting one post
        reddit.subreddit('test').hot(limit=1)
        
        return {
            "status": "healthy",
            "service": "Reddit API",
            "authenticated": True,
            "username": REDDIT_USERNAME
        }
    except Exception as e:
        logger.error(f"Reddit health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "Reddit API",
            "authenticated": False,
            "error": str(e)
        }
