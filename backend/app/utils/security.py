# File: app/utils/security.py
from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

"""
Security utilities for password hashing and JWT tokens.

Libraries used:
- passlib: For password hashing (bcrypt algorithm)
- python-jose: For JWT token creation and verification
"""

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    
    """
        Create a JWT access token.
        
        Args:
            subject: Usually the user ID or username
            expires_delta: How long the token should be valid
            
        Returns:
            Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Create the JWT payload
    to_encode = {"exp": expire, "sub": str(subject)}
    
    # Encode the token
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    """
        Verify a password against its hash.
        
        Args:
            plain_password: The plain text password
            hashed_password: The stored password hash
            
        Returns:
            True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
    """
    return pwd_context.hash(password)