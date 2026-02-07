"""Configuration management for Brand Trend Revenue Intelligence Agent"""
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # GROQ API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Trend Classification Thresholds (percentage per month)
    GROWTH_THRESHOLD = float(os.getenv("GROWTH_THRESHOLD", "5.0"))
    DECLINE_THRESHOLD = float(os.getenv("DECLINE_THRESHOLD", "-5.0"))
    
    # Trend Discovery Settings
    MIN_TRENDS_REQUIRED = int(os.getenv("MIN_TRENDS_REQUIRED", "3"))
    TREND_TIMEFRAME = os.getenv("TREND_TIMEFRAME", "today 3-m")
    
    # GROQ Model Settings
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
    GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
    GROQ_MAX_TOKENS = int(os.getenv("GROQ_MAX_TOKENS", "2000"))
    
    # Retry Settings
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAYS = [1, 2, 4, 8]  # Exponential backoff in seconds
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate required configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If required configuration is missing
        """
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is required. "
                "Please set it in .env file or environment variables."
            )
        
        if cls.GROWTH_THRESHOLD <= 0:
            raise ValueError("GROWTH_THRESHOLD must be positive")
        
        if cls.DECLINE_THRESHOLD >= 0:
            raise ValueError("DECLINE_THRESHOLD must be negative")
        
        if cls.MIN_TRENDS_REQUIRED < 1:
            raise ValueError("MIN_TRENDS_REQUIRED must be at least 1")
        
        return True
    
    @classmethod
    def get_summary(cls) -> str:
        """
        Get configuration summary.
        
        Returns:
            String with configuration details
        """
        return f"""
Configuration:
--------------
GROQ Model: {cls.GROQ_MODEL}
Growth Threshold: {cls.GROWTH_THRESHOLD}% per month
Decline Threshold: {cls.DECLINE_THRESHOLD}% per month
Min Trends Required: {cls.MIN_TRENDS_REQUIRED}
Trend Timeframe: {cls.TREND_TIMEFRAME}
Temperature: {cls.GROQ_TEMPERATURE}
Max Tokens: {cls.GROQ_MAX_TOKENS}
Max Retries: {cls.MAX_RETRIES}
"""


# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")
