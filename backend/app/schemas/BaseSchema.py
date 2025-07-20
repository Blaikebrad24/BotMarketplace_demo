# File: app/schemas/base.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

"""
Pydantic Schemas Explained:

1. Request Schemas: Validate incoming data (POST, PUT requests)
2. Response Schemas: Format outgoing data (GET responses)
3. Internal Schemas: For data processing within the app

Why separate from SQLAlchemy models?
- API data structure ≠ Database structure
- Security: Control what data is exposed
- Validation: Ensure data quality
- Documentation: Auto-generate API docs
"""

class BaseSchema(BaseModel):
    """
    Base schema with common configuration.
    
    ConfigDict is Pydantic v2 way to configure models.
    """
    model_config = ConfigDict(
        # Allow SQLAlchemy models to be converted to Pydantic models
        from_attributes=True,
        # Use enum values instead of enum objects
        use_enum_values=True,
        # Validate default values
        validate_default=True
    )

class TimestampSchema(BaseSchema):
    """
    Schema for models with timestamps.
    """
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None