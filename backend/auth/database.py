"""
Authentication Database Layer
MongoDB operations for user management
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional, Dict, Any
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class AuthDatabase:
    """User database operations"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.users = db["users"]
    
    async def create_indexes(self):
        """Create necessary indexes"""
        try:
            # Unique index on email
            await self.users.create_index("email", unique=True)
            logger.info("✅ Auth database indexes created")
        except Exception as e:
            logger.error(f"❌ Error creating auth indexes: {e}")
    
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a new user
        
        Args:
            user_data: User data including email, password_hash, etc.
        
        Returns:
            User ID if successful, None otherwise
        """
        try:
            user_data["created_at"] = datetime.utcnow()
            user_data["last_login"] = None
            
            result = await self.users.insert_one(user_data)
            logger.info(f"✅ User created: {user_data['email']}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"❌ Error creating user: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email
        
        Args:
            email: User email
        
        Returns:
            User document or None
        """
        try:
            user = await self.users.find_one({"email": email.lower()})
            if user:
                user["id"] = str(user.pop("_id"))
            return user
        except Exception as e:
            logger.error(f"❌ Error fetching user by email: {e}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        
        Args:
            user_id: User ID string
        
        Returns:
            User document or None
        """
        try:
            from bson import ObjectId
            user = await self.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user.pop("_id"))
            return user
        except Exception as e:
            logger.error(f"❌ Error fetching user by ID: {e}")
            return None
    
    async def update_last_login(self, user_id: str) -> bool:
        """
        Update user's last login timestamp
        
        Args:
            user_id: User ID
        
        Returns:
            True if successful
        """
        try:
            from bson import ObjectId
            await self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"last_login": datetime.utcnow()}}
            )
            return True
        except Exception as e:
            logger.error(f"❌ Error updating last login: {e}")
            return False
    
    async def email_exists(self, email: str) -> bool:
        """
        Check if email already exists
        
        Args:
            email: Email to check
        
        Returns:
            True if email exists
        """
        user = await self.get_user_by_email(email)
        return user is not None


# Global auth database instance (will be initialized in main.py)
auth_db: Optional[AuthDatabase] = None


def get_auth_db() -> AuthDatabase:
    """Get auth database instance"""
    if auth_db is None:
        raise RuntimeError("Auth database not initialized")
    return auth_db
