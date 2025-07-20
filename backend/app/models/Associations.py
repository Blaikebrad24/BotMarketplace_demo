# File: app/models/associations.py
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.session.database import Base

"""
Association tables for Many-to-Many relationships.

Why separate association tables?
- Many-to-Many relationships need a "junction" table
- This table only stores the relationships, no extra data
- SQLAlchemy handles the complexity for us
"""

# Bot-Category association table
bot_categories = Table('bot_categories',Base.metadata, 
    Column(
        'bot_id', 
        UUID(as_uuid=True), 
        ForeignKey('bots.id', ondelete='CASCADE'),
        primary_key=True,
        
    ),
    Column(
        'category_id', 
        UUID(as_uuid=True), 
        ForeignKey('categories.id', ondelete='CASCADE'),
        primary_key=True,
        
    ),

)