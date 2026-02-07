"""
FastAPI Dependencies for Authentication
Dependency injection for protected routes
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .jwt_handler import decode_access_token
from .models import UserType
import logging

logger = logging.getLogger(__name__)

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Dependency to get current authenticated user from JWT token
    
    Args:
        credentials: Bearer token from Authorization header
    
    Returns:
        User data from token payload
    
    Raises:
        HTTPException 401: If token is invalid or expired
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user data from payload
    user_id = payload.get("sub")
    email = payload.get("email")
    user_type = payload.get("user_type")
    
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "id": user_id,
        "email": email,
        "user_type": user_type,
        "full_name": payload.get("full_name", ""),
        "company_name": payload.get("company_name")
    }


async def require_business_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependency to require business user access
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        User data if business user
    
    Raises:
        HTTPException 403: If user is not a business user
    """
    if current_user.get("user_type") != UserType.BUSINESS.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Business user access required. Please upgrade your account."
        )
    
    return current_user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[dict]:
    """
    Dependency to get user if authenticated, None otherwise
    Useful for endpoints that work with or without auth
    
    Args:
        credentials: Optional bearer token
    
    Returns:
        User data or None
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        return None
    
    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "user_type": payload.get("user_type"),
        "full_name": payload.get("full_name", ""),
        "company_name": payload.get("company_name")
    }
