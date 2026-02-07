"""
Configuration settings for the application
Uses environment variables with fallback defaults
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000"
    ]
    
    # Database (for future implementation)
    DATABASE_URL: str = "sqlite:///./trends.db"
    
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
        case_sensitive = True

# Create global settings instance
settings = Settings()
