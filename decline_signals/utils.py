"""Utility Functions"""

from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def setup_logging(level: str = "INFO"):
    """Configure logging"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def get_iso_timestamp() -> str:
    """Get current timestamp in ISO format with Z"""
    return datetime.utcnow().isoformat() + "Z"
