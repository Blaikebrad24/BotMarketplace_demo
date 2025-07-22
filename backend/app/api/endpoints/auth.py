# File: app/api/endpoints/auth.py
from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps.database import get_db
from app.crud.user import user as user_crud
from app.schemas.UserSchema import UserCreate, UserResponse, Token
from app.utils.security import create_access_token
from app.core.config import settings

"""
Authentication endpoints for user registration and login.
"""

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(*,db: Session = Depends(get_db),user_in: UserCreate,) -> Any:
    
    """
        Register a new user.
        
        Args:
            db: Database session
            user_in: User registration data
            
        Returns:
            Created user data
            
        Raises:
            HTTPException: If user already exists
    """
    # Check if user already exists
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    user = user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # Create new user
    user = user_crud.create(db, obj_in=user_in)
    return user

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    
    """
        Login and get access token.
        
        Args:
            db: Database session
            form_data: Login form data (username and password)
            
        Returns:
            Access token and token type
            
        Raises:
            HTTPException: If credentials are incorrect
    """
    #Authenticate user
    user = user_crud.authenticate(db, username=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }