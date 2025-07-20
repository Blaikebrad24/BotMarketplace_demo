
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker 
from app.core.config import settings

"""
Database session setup explained

1. Engine: Main or core interface with Postgres database 
2. SessionLocal: A factory for creating database sessions 
3. Base: The base class for all our database models
4. get_db: A dependency that provides database sessions to API endpoints
"""

# Create the sqlalchemy engine from create_engine method 

engine = create_engine(
    settings.DATABASE_URL, 
    pool_size=settings.DB_POOL_SIZE, 
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(
autocommit=False,    # Don't auto-commit transactions
autoflush=False,     # Don't auto-flush changes
bind=engine          # Bind to our engine
    )

# Create a Base class for our models to inherit from
Base = declarative_base()

def get_db():
    """
    Database dependency for FastAPI.
    
    This function will be used as a dependency in our API endpoints.
    It ensures that:
    1. A database session is created for each request
    2. The session is properly closed after the request
    3. Any errors are handled gracefully
    """
    db = SessionLocal()
    try:
        yield db  # This gives the session to the endpoint
    finally:
        db.close()  # This ensures the session is always closed
    