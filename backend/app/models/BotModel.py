
# File: app/models/bot.py
from sqlalchemy import Column, String, Text, DECIMAL, Boolean, Integer
from sqlalchemy.orm import relationship
from app.models.BaseModel import BaseModel

class BotModel(BaseModel):
    """
    Bot model representing automation bots in our marketplace.
    
    New SQLAlchemy concepts:
    - DECIMAL: For precise decimal numbers (like money)
    - Integer: For whole numbers
    - Secondary tables: For many-to-many relationships
    """
    
    # Basic bot information
    name = Column(String(255), nullable=False, index=True,comment="Bot name")
    
    description = Column(Text,comment="Short description of what the bot does")
    
    detailed_description = Column(Text,comment="Long description with features and usage instructions" )
    
    # Pricing information
    price = Column(DECIMAL(10, 2), nullable=False)  # 10 digits total, 2 after decimal pointnullable=False,index=True,comment="Bot price in USD (e.g., 9.99)")
    
    is_free = Column(Boolean, default=False,comment="Whether the bot is free")
    
    # Technical information
    difficulty_level = Column(String(50), default="beginner",comment="Difficulty level: beginner, intermediate, advanced")
    
    python_version = Column(String(20), default="3.9+",comment="Required Python version")
    
    execution_time_estimate = Column(Integer,comment="Estimated execution time in seconds")
    
    # Technical details
    docker_image = Column(String(255),comment="Docker image name for this bot")
    
    github_repo_url = Column(String(255),comment="GitHub repository URL")
    
    # Media
    demo_video_url = Column(String(255),comment="URL to demo video" )
    
    thumbnail_url = Column(String(255),comment="URL to bot thumbnail image")
    
    # Status and metrics
    is_active = Column(Boolean, default=True,comment="Whether the bot is available for purchase")
    
    download_count = Column(Integer, default=0,comment="Number of times the bot has been downloaded" )
    
    rating_average = Column(DECIMAL(3, 2), default=0.00,comment="Average rating (0.00 to 5.00)")
    
    rating_count = Column(Integer, default=0,comment="Number of ratings received")
    
    # Relationships
    categories = relationship("CategoryModel",secondary="bot_categories",back_populates="bots")
    
    order_items = relationship( "OrderItemModel", back_populates="bot")
    
    executions = relationship("BotExecutionModel",  back_populates="bot" )
    
    reviews = relationship("BotReviewModel", back_populates="bot",cascade="all, delete-orphan")
    
    user_access = relationship("UserBotAccessModel", back_populates="bot")
    
    def __repr__(self):
        return f"<Bot(name='{self.name}', price={self.price})>"