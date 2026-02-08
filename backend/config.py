"""
Configuration settings for the application
Uses environment variables with fallback defaults
"""

import json

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Settings
    # Keep as string to avoid pydantic-settings attempting JSON parsing before validation.
    # Accepts either:
    # - comma-separated string: "http://a,http://b"
    # - JSON array string:      "[\"http://a\",\"http://b\"]"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"

    def allowed_origins_list(self) -> List[str]:
        raw = (self.ALLOWED_ORIGINS or "").strip()
        if not raw:
            return []
        if raw.startswith("["):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return [str(x).strip() for x in parsed if str(x).strip()]
            except Exception:
                return []
        return [part.strip() for part in raw.split(",") if part.strip()]
    
    # Database (for future implementation)
    DATABASE_URL: str = "sqlite:///./trends.db"
    
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "trend_analysis"
    
    # Google Gemini AI API
    GOOGLE_GEMINI_API_KEY: str = ""
    
    # Twitter/X API
    TWITTER_BEARER_TOKEN: str = ""
    
    # Reddit API
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_USERNAME: str = ""
    REDDIT_PASSWORD: str = ""
    REDDIT_USER_AGENT: str = "TrendLens/1.0"
    
    # ML Model Settings
    MODEL_PATH: str = "./models/"
    FEATURE_CACHE_TTL: int = 3600  # 1 hour
    PREDICTION_THRESHOLD: float = 0.65  # Decline probability threshold
    
    # External API Keys (mock for now)
    TWITTER_API_KEY: str = "mock_twitter_key"
    REDDIT_API_KEY: str = "mock_reddit_key"
    INSTAGRAM_API_KEY: str = "mock_instagram_key"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'allow'

# Create global settings instance
settings = Settings()
