# File: app/schemas/user.py
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.schemas.base import TimestampSchema

"""
User Schemas for different use cases:

1. UserCreate: Data needed to create a new user
2. UserUpdate: Data that can be updated
3. UserResponse: Data returned in API responses
4. UserLogin: Data for authentication
"""

class UserBase(BaseModel):
    """
    Base user schema with common fields.
    """
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Pydantic Validation Features:
    - EmailStr: Validates email format
    - Field: Adds validation rules and documentation
    - min_length/max_length: String length validation
    """
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=100,
        description="Password (8-100 characters)"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "password": "securepassword123"
            }
        }
    )

class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    All fields are optional for partial updates.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class UserResponse(UserBase, TimestampSchema):
    """
    Schema for user data in API responses.
    
    Notice: No password field! Never return passwords.
    """
    is_active: bool
    is_verified: bool
    subscription_tier: str
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "user@example.com",
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "is_active": True,
                "is_verified": True,
                "subscription_tier": "free",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }
    )

class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="User password")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "john_doe",
                "password": "securepassword123"
            }
        }
    )

class Token(BaseModel):
    """
    Schema for authentication tokens.
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: int