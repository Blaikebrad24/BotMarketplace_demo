

from sqlalchemy import Column, String, Boolean 
from sqlalchemy.orm import relationship 
from app.models.BaseModel import BaseModel 

class UserModel(BaseModel):
    
    """
    User model representing the users of this application 
    
    SQLAlchemy Concepts: 
        - Column: Defines a database column 
        - String(length): variable length string with max length 
        - Boolean: True/False values 
        - Relationship: Defines relationships to other models 
        - index=True: creates database index for faster queries 
    """
    
    email = Column(String(length=255), unique=True, nullable=False, index=True, comment="User's email address")
    username = Column(String(length=50), unique=True, nullable=False, index=True, comment="Username for the user")
    password_hash = Column(String(length=255), nullable=False, comment="Hashed password for the user")
    first_name = Column(String(length=50), nullable=True, comment="User's first name")
    last_name = Column(String(length=50), nullable=True, comment="User's last name")
    
    # State variables 
    is_active = Column(Boolean, default=True, comment="Indicates if the user account is active")
    is_verified = Column(Boolean, default=False, comment="Indicates if the user's email is verified")
    subscription_tier = Column(String(50), default="free", comment="User's subscription level (free, premium, enterprise)")
    
    # relationships with other model entities 
    orders = relationship("OrderModel", back_populates="user", cascade="all, delete-orphan")
    bot_executions = relationship("BotExecutionModel", back_populates="user",cascade="all, delete-orphan")
    reviews = relationship("BotReviewModel", back_populates="user",cascade="all, delete-orphan")
    
    
    bot_access = relationship( "UserBotAccessModel", back_populates="user",cascade="all, delete-orphan")
    
    def __repr__(self):
        """
        String representation for debugging.
        When you print a UserModel, you'll see something readable.
        """
        return f"<User(username='{self.username}', email='{self.email}')>"