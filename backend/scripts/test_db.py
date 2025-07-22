
import sys
import os

# Add app directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.session.database import SessionLocal, engine
from app.models import UserModel, BotModel, CategoryModel

def test_database():
    """Test database connection and basic operations."""
    
    print("Testing database connection...")
    
    # Test connection
    try:
        db = SessionLocal()
        
        # Test query
        user_count = db.query(UserModel).count()
        bot_count = db.query(BotModel).count()
        category_count = db.query(CategoryModel).count()
        
        print(f"✅ Database connection successful!")
        print(f"📊 Database stats:")
        print(f"   Users: {user_count}")
        print(f"   Bots: {bot_count}")
        print(f"   Categories: {category_count}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_database()