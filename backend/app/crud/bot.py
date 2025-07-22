# File: app/crud/bot.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.crud.base import CRUDBase
from app.models.BotModel import BotModel
from app.models.CategoryModel import CategoryModel
from app.schemas.BotSchema import BotCreate, BotUpdate

class CRUDBot(CRUDBase[BotModel, BotCreate, BotUpdate]):
    """
    CRUD operations for Bot model with marketplace-specific methods.
    """
    
    def get_active_bots(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[BotModel]:
        """
        Get active bots only.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of active bot models
        """
        return (
            db.query(BotModel)
            .filter(BotModel.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_category(self, db: Session, *, category_id: str,skip: int = 0, limit: int = 100) -> List[BotModel]:
        """
        Get bots by category.
        
        Args:
            db: Database session
            category_id: Category UUID
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of bot models in the category
        """
        return (
            db.query(BotModel)
            .join(BotModel.categories)
            .filter(
                and_(
                    CategoryModel.id == category_id,
                    BotModel.is_active == True
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_bots(self, db: Session,  *, query: str,skip: int = 0, limit: int = 100) -> List[BotModel]:
        """
        Search bots by name or description.
        
        Args:
            db: Database session
            query: Search query string
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of matching bot models
        """
        search_filter = or_(
            BotModel.name.ilike(f"%{query}%"),
            BotModel.description.ilike(f"%{query}%")
        )
        
        return (
            db.query(BotModel)
            .filter(
                and_(
                    search_filter,
                    BotModel.is_active == True
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_free_bots(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[BotModel]:
        """
        Get free bots only.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of free bot models
        """
        return (
            db.query(BotModel)
            .filter(
                and_(
                    BotModel.is_free == True,
                    BotModel.is_active == True
                )
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

# Create instance to use in API endpoints
bot = CRUDBot(BotModel)