from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union 
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel 
from sqlalchemy.orm import Session 
from app.db.session.database import Base 

"""
Simple CRUD Operations class that all other route handler methods will inherit from.
This cuts down on boiler plate code for the route handler classes, and easier to test 
this layer of the application 
"""

ModelType = TypeVar("ModelType", bound=Base)  # Type variable for SQLAlchemy models
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # Type variable for Pydantic create schemas    
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # Type variable for Pydantic update schemas    

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
        basic create/read/update/delete operations using generics
    
    """
    def __init__(self, model: Type[ModelType]):
        """
            Initialize the model 
        """
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
            Get a record by id
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multiple(self, db:Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
            Get multiple records with pagination
        """
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Args:
            db: Database session
            obj_in: Pydantic schema with data to create
            
        Returns:
            Created model instance
        """
        # Convert Pydantic model to dict, excluding unset values
        obj_in_data = jsonable_encoder(obj_in)
        
        # Create SQLAlchemy model instance
        db_obj = self.model(**obj_in_data)
        
        # Add to session and commit
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)  # Get the updated object with generated ID
        
        return db_obj
    
    
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """
            Update a record
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    
    def remove(self, db: Session, *, id: Any) -> ModelType:
        """
        Delete a record by ID.
        
        Args:
            db: Database session
            id: Primary key value
            
        Returns:
            Deleted model instance
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj