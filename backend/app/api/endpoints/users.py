# File: app/api/endpoints/users.py
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps.database import get_db
from app.api.deps.auth import get_current_active_user
from app.crud.user import user as user_crud
from app.models.UserModel import UserModel
from app.schemas.UserSchema import UserResponse, UserUpdate

"""
User management endpoints.
"""

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: UserModel = Depends(get_current_active_user),) -> Any:
    """
        Get current user information.
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            Current user data
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(*,db: Session = Depends(get_db),user_in: UserUpdate,current_user: UserModel = Depends(get_current_active_user),) -> Any:
    """
        Update current user information.
        
        Args:
            db: Database session
            user_in: User update data
            current_user: Current authenticated user
            
        Returns:
            Updated user data
    """
    user = user_crud.update(db, db_obj=current_user, obj_in=user_in)
    return user