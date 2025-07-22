# File: app/api/deps/auth.py
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud.user import user as user_crud
from app.models.UserModel import UserModel
from app.api.deps.database import get_db

"""
Authentication dependencies for FastAPI.

These functions are used as dependencies in API endpoints that require authentication.
"""

# Security scheme for JWT tokens
security = HTTPBearer()

def get_current_user(db: Session = Depends(get_db),credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserModel:
    """
        Get the current authenticated user from JWT token.
        
        Args:
            db: Database session
            credentials: JWT token from Authorization header
            
        Returns:
            Current user model
            
        Raises:
            HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(
            credentials.credentials, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # Get user ID from token
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = user_crud.get(db, id=user_id)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user: UserModel = Depends(get_current_user),) -> UserModel:
    """
        Get current user and ensure they are active.
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            Active user model
            
        Raises:
            HTTPException: If user is inactive
    """
    if not user_crud.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    return current_user

