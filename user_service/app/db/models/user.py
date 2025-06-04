# Import SQLAlchemy types and base class factory
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative class definitions (used by all SQLAlchemy models)
Base = declarative_base()

#  User Model Definition
# This class represents the 'users' table in the database.
class User(Base):
    # Define the name of the table in the database
    __tablename__ = "users"

    # Primary key column 'id', auto-incremented and indexed
    id = Column(Integer, primary_key=True, index=True)

    # Full name of the user (required field)
    full_name = Column(String, nullable=False)

    # User's email address (must be unique and not null, indexed for quick lookup)
    email = Column(String, unique=True, index=True, nullable=False)

    # Hashed password for authentication (required field)
    hashed_password = Column(String, nullable=False)

    # Boolean flag to check if the user's account is active (default is False)
    is_active = Column(Boolean, default=False)
    
    # Role field added
    role = Column(String, nullable=False, default="customer")


