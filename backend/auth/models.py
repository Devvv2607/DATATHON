"""
User Models for Authentication
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class UserType(str, Enum):
    GENERAL = "general"
    BUSINESS = "business"


class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=2)
    user_type: UserType = UserType.GENERAL
    company_name: Optional[str] = None  # Required for business users


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    user_type: UserType
    company_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class UserInDB(BaseModel):
    """User model as stored in MongoDB"""
    email: str
    password_hash: str
    full_name: str
    user_type: UserType
    company_name: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
