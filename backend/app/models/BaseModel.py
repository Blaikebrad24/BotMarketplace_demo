
from sqlalchemy import Column, DateTime, func 
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.ext.declarative import declared_attr 
from app.db.session.database import Base 
import uuid 


class BaseModel(Base):
    
    """
     Base model that other models inherit from. 
     
     Why use a base model?
     1. Provides common fields (id, created_at, updated_at)
     2. Ensures consistency across all tables 
     3. Reduces code duplication 
     4. Makes database design patterns consistent 
    """
    
    __abstract__ = True 
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, comment="Unique identifier for the record")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Timestamp when the record was created")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="Timestamp when the record was last updated")
    
    @declared_attr
    def __tablename__(cls):
        """
        Automatically generates the table name based on the class name.
        
        This ensures that each model has a unique table name in the database.
        """
        return cls.__name__.lower().replace('model', 's')
    
    