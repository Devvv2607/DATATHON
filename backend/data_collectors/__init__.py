"""
Data Collectors Module
Integrates external data sources (Reddit, Twitter, Google Trends)
"""

from .reddit_collector import router as reddit_router

__all__ = ["reddit_router"]
