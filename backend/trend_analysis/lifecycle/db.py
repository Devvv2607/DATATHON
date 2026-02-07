"""
MongoDB Connection and Operations for Trend Lifecycle
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo import ASCENDING, DESCENDING
import logging

logger = logging.getLogger(__name__)


class LifecycleDB:
    """MongoDB operations for trend lifecycle tracking"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self.collection: Optional[AsyncIOMotorCollection] = None
        self._initialized = False
    
    async def connect(self):
        """Initialize MongoDB connection"""
        if self._initialized:
            return
        
        try:
            mongo_uri = os.getenv(
                "MONGODB_URI", 
                "mongodb://localhost:27017"
            )
            db_name = os.getenv("MONGODB_DB_NAME", "trend_analysis")
            
            self.client = AsyncIOMotorClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=10
            )
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info("✅ MongoDB connected successfully")
            
            self.db = self.client[db_name]
            self.collection = self.db["trend_lifecycle"]
            
            # Create indexes
            await self._create_indexes()
            
            self._initialized = True
            
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            # Fallback: app will work without MongoDB (in-memory only)
            self._initialized = False
    
    async def _create_indexes(self):
        """Create required indexes for performance"""
        try:
            await self.collection.create_index(
                [("trend_name", ASCENDING)],
                unique=True
            )
            await self.collection.create_index(
                [("lifecycle_stage", ASCENDING)]
            )
            await self.collection.create_index(
                [("last_updated", DESCENDING)]
            )
            logger.info("✅ MongoDB indexes created")
        except Exception as e:
            logger.warning(f"Index creation failed: {e}")
    
    async def upsert_lifecycle(self, data: Dict[str, Any]) -> str:
        """
        Upsert lifecycle data with automatic days_in_stage calculation
        Returns: trend_id
        """
        if not self._initialized or self.collection is None:
            logger.warning("MongoDB not available, returning mock trend_id")
            return data.get("trend_id", "mock_trend_id")
        
        trend_name = data["trend_name"]
        new_stage = data["lifecycle_stage"]
        
        # Check existing document
        existing = await self.collection.find_one({"trend_name": trend_name})
        
        if existing:
            trend_id = existing["trend_id"]
            old_stage = existing.get("lifecycle_stage")
            
            # Calculate days_in_stage
            if old_stage == new_stage:
                # Same stage - increment days
                data["days_in_stage"] = existing.get("days_in_stage", 0) + 1
            else:
                # Stage changed - reset counter
                data["days_in_stage"] = 0
            
            # Preserve created_at
            data["created_at"] = existing.get("created_at", datetime.utcnow())
        else:
            # New trend
            trend_id = data["trend_id"]
            data["days_in_stage"] = 0
            data["created_at"] = datetime.utcnow()
        
        data["trend_id"] = trend_id
        data["last_updated"] = datetime.utcnow()
        
        # Upsert
        await self.collection.update_one(
            {"trend_name": trend_name},
            {"$set": data},
            upsert=True
        )
        
        logger.info(f"✅ Upserted lifecycle for '{trend_name}' (Stage: {new_stage})")
        return trend_id
    
    async def get_by_name(self, trend_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve lifecycle data by trend name"""
        if not self._initialized or self.collection is None:
            return None
        
        return await self.collection.find_one({"trend_name": trend_name})
    
    async def get_by_id(self, trend_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve lifecycle data by trend_id"""
        if not self._initialized or self.collection is None:
            return None
        
        return await self.collection.find_one({"trend_id": trend_id})
    
    async def get_by_stage(self, stage: int, limit: int = 50) -> list:
        """Get all trends in a specific lifecycle stage"""
        if not self._initialized or self.collection is None:
            return []
        
        cursor = self.collection.find(
            {"lifecycle_stage": stage}
        ).sort("last_updated", DESCENDING).limit(limit)
        
        return await cursor.to_list(length=limit)
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Singleton instance
lifecycle_db = LifecycleDB()
