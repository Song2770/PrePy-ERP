import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.exc import SQLAlchemyError
from backend.app.config.database import engine, Base, get_db
from backend.app.utils.setup import initialize_db
from backend.app.models import (
    user,  # Import all model modules to ensure they are registered with Base.metadata
    sales,
    technical,
)

def setup_database():
    """
    Set up database tables and initialize with sample data.
    """
    try:
        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created.")
        
        # Initialize with sample data
        db = next(get_db())
        initialize_db(db)
        
        print("Database setup completed successfully.")
    except SQLAlchemyError as e:
        print(f"An error occurred during database setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database() 