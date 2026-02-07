"""
Configuration module for Twitter API credentials and settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Twitter API Configuration
    TWITTER_API_KEY = os.getenv(
        "TWITTER_API_KEY",
        "67d16668demsh8563ec142db49dap16b0c2jsnf8fe97893ba1"  # Your RapidAPI key
    )
    TWITTER_API_HOST = os.getenv(
        "TWITTER_API_HOST",
        "twitter-api45.p.rapidapi.com"
    )
    
    # Featherless AI Configuration (for AI explanations)
    FEATHERLESS_API_KEY = os.getenv(
        "FEATHERLESS_API_KEY",
        "rc_16258f4d33f9df27a5a977ef7010dee1344c6fb68e073e5e749f83c20c780b6c"  # Your Featherless AI key
    )
    FEATHERLESS_API_URL = os.getenv(
        "FEATHERLESS_API_URL",
        "https://api.featherless.ai/v1"
    )
    FEATHERLESS_MODEL = os.getenv(
        "FEATHERLESS_MODEL",
        "deepseek-ai/DeepSeek-V3-0324"
    )
    
    # Trend Analyzer Configuration
    MIN_CONFIDENCE_THRESHOLD = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", "0.3"))
    
    # Data Collection
    DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "US")
    MAX_TRENDS_TO_FETCH = int(os.getenv("MAX_TRENDS_TO_FETCH", "50"))
    TWEETS_PER_HASHTAG = int(os.getenv("TWEETS_PER_HASHTAG", "100"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Database (if needed)
    DATABASE_URL = os.getenv("DATABASE_URL", None)
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.TWITTER_API_KEY:
            raise ValueError("TWITTER_API_KEY not configured")
        print("✅ Configuration validated")
        return True


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    LOG_LEVEL = "WARNING"


class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = True
    TESTING = True
    LOG_LEVEL = "DEBUG"


def get_config(env: Optional[str] = None) -> Config:
    """
    Get configuration based on environment.
    
    Args:
        env: Environment name (development, production, testing)
    
    Returns:
        Configuration object
    """
    if env is None:
        env = os.getenv("ENVIRONMENT", "development")
    
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    config_class = configs.get(env.lower(), DevelopmentConfig)
    return config_class()


# Default configuration
DEFAULT_CONFIG = get_config()
