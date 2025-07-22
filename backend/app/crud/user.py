# File: app/crud/user.py
from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.UserModel import UserModel
from app.schemas.UserSchema import UserCreate, UserUpdate
from app.utils.security import get_password_hash, verify_password

class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    """
    CRUD operations for User model with additional authentication methods.
    
    This extends the base CRUD class with user-specific operations like
    authentication and email lookups.
    """
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[UserModel]:
        """
        Get user by email address.
        
        Args:
            db: Database session
            email: User's email address
            
        Returns:
            User model or None if not found
        """
        return db.query(UserModel).filter(UserModel.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[UserModel]:
        """
        Get user by username.
        
        Args:
            db: Database session
            username: User's username
            
        Returns:
            User model or None if not found
        """
        return db.query(UserModel).filter(UserModel.username == username).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> UserModel:
        """
        Create a new user with hashed password.
        
        Args:
            db: Database session
            obj_in: User creation schema
            
        Returns:
            Created user model
        """
        # Hash the password before storing
        hashed_password = get_password_hash(obj_in.password)
        
        # Create user data dict
        db_obj = UserModel(
            email=obj_in.email,
            username=obj_in.username,
            password_hash=hashed_password,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj
    
    def authenticate(
        self, 
        db: Session, 
        *, 
        username: str, 
        password: str
    ) -> Optional[UserModel]:
        """
        Authenticate user with username/email and password.
        
        Args:
            db: Database session
            username: Username or email
            password: Plain text password
            
        Returns:
            User model if authentication successful, None otherwise
        """
        # Try to find user by username or email
        user = self.get_by_username(db, username=username)
        if not user:
            user = self.get_by_email(db, email=username)
        
        # Check if user exists and password is correct
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    def is_active(self, user: UserModel) -> bool:
        """
        Check if user account is active.
        
        Args:
            user: User model instance
            
        Returns:
            True if user is active, False otherwise
        """
        return user.is_active
    
    def is_verified(self, user: UserModel) -> bool:
        """
        Check if user email is verified.
        
        Args:
            user: User model instance
            
        Returns:
            True if user is verified, False otherwise
        """
        return user.is_verified

# Create instance to use in API endpoints
user = CRUDUser(UserModel)