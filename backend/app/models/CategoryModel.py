

from sqlalchemy import Column, String, Boolean, Text
from sqlalchemy.orm import relationship 
from app.models.BaseModel import BaseModel 

class CategoryModel(BaseModel):
    
    """
    Category model for organzing bots. 
    New SqlAlchemy concepts
    1. Text: for longer text content (no length limit)
    2. ManyToMany relationship through association tables 
    """
    __tablename__ = "categories"
    name = Column(String(100), unique=True, nullable=False,index=True,comment="Category name (e.g., 'Productivity', 'File Management')")
   
    
    description = Column(Text,comment="Detailed description of the category")

    icon_url = Column(String(255),comment="URL to the category icon")

    is_active = Column(Boolean, default=True,comment="Whether the category is currently active")

    # Many-to-Many relationship with bots
    # A category can have many bots, and a bot can belong to many categories
    bots = relationship("BotModel",secondary="bot_categories", back_populates="categories")  # This is the junction tableback_populates="categories",comment="Bots in this category")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"