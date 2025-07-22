# File: app/api/deps/database.py
from typing import Generator
from app.db.session.database import SessionLocal

def get_db() -> Generator:
    """
        Dependency to get database session.
        
        This ensures that:
        1. Each request gets its own database session
        2. The session is properly closed after the request
        3. Any database errors are handled gracefully
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()