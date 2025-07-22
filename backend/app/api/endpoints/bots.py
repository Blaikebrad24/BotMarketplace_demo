# File: app/api/endpoints/bots.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps.database import get_db
from app.crud.bot import bot as bot_crud
from app.schemas.BotSchema import BotResponse

"""
Bot marketplace endpoints.
"""

router = APIRouter()

@router.get("/", response_model=List[BotResponse])
def read_bots(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=100, description="Number of items to return"),
    category: str = Query(None, description="Filter by category ID"),
    search: str = Query(None, description="Search query"),
    free_only: bool = Query(False, description="Show only free bots"),
) -> Any:
    """
    Retrieve bots with filtering and pagination.
    
    Args:
        db: Database session
        skip: Number of items to skip for pagination
        limit: Maximum number of items to return
        category: Optional category filter
        search: Optional search query
        free_only: Whether to show only free bots
        
    Returns:
        List of bot data
    """
    if free_only:
        bots = bot_crud.get_free_bots(db, skip=skip, limit=limit)
    elif category:
        bots = bot_crud.get_by_category(db, category_id=category, skip=skip, limit=limit)
    elif search:
        bots = bot_crud.search_bots(db, query=search, skip=skip, limit=limit)
    else:
        bots = bot_crud.get_active_bots(db, skip=skip, limit=limit)
    
    return bots

@router.get("/{bot_id}", response_model=BotResponse)
def read_bot(
    *,
    db: Session = Depends(get_db),
    bot_id: str,
) -> Any:
    """
    Get bot by ID.
    
    Args:
        db: Database session
        bot_id: Bot UUID
        
    Returns:
        Bot data
        
    Raises:
        HTTPException: If bot not found
    """
    bot = bot_crud.get(db, id=bot_id)
    if not bot:
        raise HTTPException(
            status_code=404, 
            detail="Bot not found"
        )
    return bot