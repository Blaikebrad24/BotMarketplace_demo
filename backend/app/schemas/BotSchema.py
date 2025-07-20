# File: app/schemas/bot.py
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.base import TimestampSchema

class BotBase(BaseModel):
    """
    Base bot schema with common fields.
    """
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    detailed_description: Optional[str] = None
    price: Decimal = Field(..., ge=0, decimal_places=2)  # ge = greater or equal to 0
    difficulty_level: str = Field(default="beginner")
    python_version: str = Field(default="3.9+")

class BotCreate(BotBase):
    """
    Schema for creating a new bot.
    """
    category_ids: List[str] = Field(..., description="List of category IDs")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "File Organizer Pro",
                "description": "Automatically organize files by type and date",
                "detailed_description": "A powerful file organization bot...",
                "price": 9.99,
                "difficulty_level": "beginner",
                "python_version": "3.9+",
                "category_ids": ["cat1-uuid", "cat2-uuid"]
            }
        }
    )

class BotUpdate(BaseModel):
    """
    Schema for updating bot information.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    detailed_description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    is_active: Optional[bool] = None
    category_ids: Optional[List[str]] = None

class BotResponse(BotBase, TimestampSchema):
    """
    Schema for bot data in API responses.
    """
    is_free: bool
    execution_time_estimate: Optional[int]
    docker_image: Optional[str]
    github_repo_url: Optional[str]
    demo_video_url: Optional[str]
    thumbnail_url: Optional[str]
    is_active: bool
    download_count: int
    rating_average: Decimal
    rating_count: int
    
    # Nested schemas for related data
    categories: List["CategoryResponse"] = []
    
    model_config = ConfigDict(from_attributes=True)

# Category schemas (simplified)
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon_url: Optional[str] = None

class CategoryResponse(CategoryBase, TimestampSchema):
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

# Update BotResponse to resolve forward reference
BotResponse.model_rebuild()