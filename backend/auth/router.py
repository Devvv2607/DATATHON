"""
Authentication Router
Endpoints for signup, login, and user management
"""

from fastapi import APIRouter, HTTPException, status, Depends
from .models import (
    UserSignupRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
    UserType
)
from .password_handler import hash_password, verify_password
from .jwt_handler import create_access_token
from .database import get_auth_db, AuthDatabase
from .dependencies import get_current_user
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: UserSignupRequest):
    """
    Register a new user
    
    - **email**: User email (must be unique)
    - **password**: Password (min 8 characters)
    - **full_name**: User's full name
    - **user_type**: "general" or "business"
    - **company_name**: Company name (required for business users)
    """
    try:
        db = get_auth_db()
        
        # Validate business user requirements
        if request.user_type == UserType.BUSINESS and not request.company_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company name is required for business users"
            )
        
        # Check if email already exists
        existing_user = await db.get_user_by_email(request.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        password_hash = hash_password(request.password)
        
        # Create user document
        user_data = {
            "email": request.email.lower(),
            "password_hash": password_hash,
            "full_name": request.full_name,
            "user_type": request.user_type.value,
            "company_name": request.company_name
        }
        
        # Insert user
        user_id = await db.create_user(user_data)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create user"
            )
        
        # Generate JWT token
        token_data = {
            "sub": user_id,
            "email": request.email,
            "user_type": request.user_type.value,
            "full_name": request.full_name,
            "company_name": request.company_name
        }
        access_token = create_access_token(token_data)
        
        # Prepare user response
        user_response = UserResponse(
            id=user_id,
            email=request.email,
            full_name=request.full_name,
            user_type=request.user_type,
            company_name=request.company_name,
            created_at=datetime.utcnow()
        )
        
        logger.info(f"✅ New user registered: {request.email} ({request.user_type.value})")
        
        return TokenResponse(
            access_token=access_token,
            user=user_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest):
    """
    Login with email and password
    
    - **email**: User email
    - **password**: User password
    """
    try:
        db = get_auth_db()
        
        # Get user by email
        user = await db.get_user_by_email(request.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(request.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Update last login
        await db.update_last_login(user["id"])
        
        # Generate JWT token
        token_data = {
            "sub": user["id"],
            "email": user["email"],
            "user_type": user["user_type"],
            "full_name": user["full_name"],
            "company_name": user.get("company_name")
        }
        access_token = create_access_token(token_data)
        
        # Prepare user response
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            user_type=UserType(user["user_type"]),
            company_name=user.get("company_name"),
            created_at=user["created_at"]
        )
        
        logger.info(f"✅ User logged in: {request.email}")
        
        return TokenResponse(
            access_token=access_token,
            user=user_response
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information
    Requires valid JWT token in Authorization header
    """
    try:
        db = get_auth_db()
        
        # Fetch fresh user data from database
        user = await db.get_user_by_id(current_user["id"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            user_type=UserType(user["user_type"]),
            company_name=user.get("company_name"),
            created_at=user["created_at"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user information"
        )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout current user
    Note: JWT tokens are stateless, so logout is handled client-side by removing the token
    This endpoint is for logging purposes
    """
    logger.info(f"✅ User logged out: {current_user['email']}")
    return {"message": "Logged out successfully"}
