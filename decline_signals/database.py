"""MongoDB Atlas Data Access Layer"""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Dict, Any, List
import logging
import os

logger = logging.getLogger(__name__)

class MongoDBClient:
    """Simple async MongoDB client for reading/writing decline signals"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
    
    async def connect(self):
        """Connect to MongoDB Atlas"""
        try:
            self.client = AsyncIOMotorClient(self.database_url)
            await self.client.admin.command("ping")
            self.db = self.client["datazen"]
            logger.info("✓ Connected to MongoDB Atlas")
        except Exception as e:
            logger.error(f"✗ MongoDB connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Close connection"""
        if self.client:
            self.client.close()
            logger.info("✓ Disconnected from MongoDB")
    
    async def save_decline_signal(self, trend_id: str, signal_data: Dict[str, Any]) -> bool:
        """
        Save decline signal to trends document.
        
        Structure:
        {
            "trend_id": "12345",
            "trend_name": "Grimace Shake",
            "decline_signals": [
                {"timestamp": "2026-02-07T14:30:00Z", "decline_risk_score": 67.5, ...},
                ...
            ]
        }
        """
        try:
            trends_collection = self.db["trends"]
            
            # Ensure signal has timestamp
            if "timestamp" not in signal_data:
                from datetime import datetime
                signal_data["timestamp"] = datetime.utcnow().isoformat() + "Z"
            
            # Push signal to decline_signals array
            result = await trends_collection.update_one(
                {"trend_id": trend_id},
                {
                    "$push": {"decline_signals": signal_data},
                    "$set": {
                        "trend_name": signal_data.get("trend_name", ""),
                        "last_signal_time": signal_data.get("timestamp")
                    }
                },
                upsert=True
            )
            
            logger.info(f"✓ Saved decline signal for trend {trend_id}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to save signal: {e}")
            return False
    
    async def get_decline_signals_history(self, trend_id: str, limit: int = 30) -> List[Dict]:
        """Get signal history for a trend"""
        try:
            trends_collection = self.db["trends"]
            trend = await trends_collection.find_one(
                {"trend_id": trend_id},
                {"decline_signals": {"$slice": -limit}}
            )
            
            if trend and "decline_signals" in trend:
                return trend["decline_signals"]
            return []
        except Exception as e:
            logger.error(f"✗ Failed to get history: {e}")
            return []
    
    async def health_check(self) -> bool:
        """Check if database is connected"""
        try:
            if self.client:
                await self.client.admin.command("ping")
                return True
        except:
            pass
        return False

# Global instance
_db_client: Optional[MongoDBClient] = None

async def init_database(database_url: str) -> MongoDBClient:
    """Initialize database connection"""
    global _db_client
    _db_client = MongoDBClient(database_url)
    await _db_client.connect()
    return _db_client

async def get_database() -> MongoDBClient:
    """Get database instance"""
    global _db_client
    if _db_client is None:
        raise RuntimeError("Database not initialized")
    return _db_client

async def close_database():
    """Close database connection"""
    global _db_client
    if _db_client:
        await _db_client.disconnect()
