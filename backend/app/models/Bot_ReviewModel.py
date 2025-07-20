# File: app/models/bot_review.py
from sqlalchemy import Column, String, Text, Boolean, Integer, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from app.models.BaseModel import BaseModel

class BotReviewModel(BaseModel):
    """
    Bot review model for user ratings and reviews.
    
    New SQLAlchemy concepts:
    - CheckConstraint: Database-level validation
    - UniqueConstraint: Composite unique constraints
    """
    
    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        comment="User who wrote the review"
    )
    
    bot_id = Column(
        UUID(as_uuid=True),
        ForeignKey('bots.id', ondelete='CASCADE'),
        nullable=False,
        comment="Bot being reviewed"
    )
    
    # Review content
    rating = Column(
        Integer,
        CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating'),
        comment="Rating from 1 to 5 stars"
    )
    
    review_text = Column(
        Text,
        comment="Optional review text"
    )
    
    # Verification
    is_verified_purchase = Column(
        Boolean,
        default=False,
        comment="Whether this user actually purchased the bot"
    )
    
    # Relationships
    user = relationship(
        "UserModel",
        back_populates="reviews",
        
    )
    
    bot = relationship(
        "BotModel",
        back_populates="reviews",
        
    )
    
    # Table constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'bot_id', name='unique_user_bot_review'),
    )
    
    def __repr__(self):
        return f"<BotReview(bot_id='{self.bot_id}', rating={self.rating})>"