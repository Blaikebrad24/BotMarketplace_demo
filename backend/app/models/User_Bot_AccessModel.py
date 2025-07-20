# File: app/models/user_bot_access.py
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from app.models.BaseModel import BaseModel

class UserBotAccessModel(BaseModel):
    """
    User bot access model for tracking which users can access which bots.
    
    This is useful for:
    - Subscription-based access
    - Time-limited trials
    - Gift access
    - Refund handling
    """
    
    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        comment="User with access"
    )
    
    bot_id = Column(
        UUID(as_uuid=True),
        ForeignKey('bots.id', ondelete='CASCADE'),
        nullable=False,
        comment="Bot being accessed"
    )
    
    # Access details
    access_type = Column(
        String(50),
        default="purchased",
        comment="Type of access: purchased, trial, subscription, gift"
    )
    
    granted_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="When access was granted"
    )
    
    expires_at = Column(
        DateTime(timezone=True),
        comment="When access expires (NULL for permanent)"
    )
    
    is_active = Column(
        Boolean,
        default=True,
        comment="Whether access is currently active"
    )
    
    # Relationships 
    user = relationship(
        "UserModel",
        back_populates="bot_access",
        
    )
    
    bot = relationship(
        "BotModel",
        back_populates="user_access",
       
    )
    
    # Table constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'bot_id', name='unique_user_bot_access'),
    )
    
    def __repr__(self):
        return f"<UserBotAccess(user_id='{self.user_id}', bot_id='{self.bot_id}', type='{self.access_type}')>"