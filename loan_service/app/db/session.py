# Import necessary functions and classes from SQLAlchemy
from sqlalchemy import create_engine  # Used to create a connection to the database
from sqlalchemy.orm import sessionmaker, Session  # For managing DB sessions
from sqlalchemy.orm import declarative_base  # Base class for defining DB models

# Import application settings (like DB credentials) from the config file
from app.core.config import settings

# Create a base class that all SQLAlchemy models will inherit from
Base = declarative_base()

# Build the full database connection URL using environment variables
# Format: postgresql://username:password@host/database_name
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"
)

# Create a database engine using the connection URL
# The engine manages the actual connection to the PostgreSQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory that can be used to create database sessions
# - autocommit=False means changes won’t be saved automatically
# - autoflush=False delays writing changes until manually triggered
# - bind=engine tells sessions to use the engine we defined
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function for FastAPI to get a DB session
# This is typically used in route handlers with Depends()
def get_db() -> Session:
    # Create a new session
    db = SessionLocal()
    try:
        # Provide the session to the caller
        yield db
    finally:
        # Make sure the session is closed after the request finishes
        db.close()
