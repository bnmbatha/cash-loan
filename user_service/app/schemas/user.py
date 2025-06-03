# Import base model and email validation type from Pydantic
from pydantic import BaseModel, EmailStr
from typing import Optional

#  Schema used for incoming user registration data
class UserCreate(BaseModel):
    full_name: str           # User's full name (required)
    email: EmailStr          # User's email address (validated format, required)
    password: str            # Plaintext password (to be hashed before saving)

#  Schema used to return user data in API responses (excluding password)
class UserOut(BaseModel):
    id: int                  # Unique identifier for the user
    full_name: str           # Full name of the user
    email: EmailStr          # Email address

#  Schema used for updating user data (all fields optional)
class UserUpdate(BaseModel):
    full_name: Optional[str] = None     # Optional updated name
    email: Optional[EmailStr] = None    # Optional updated email
    password: Optional[str] = None      # Optional updated password

    #  Enable compatibility with ORM objects (e.g., SQLAlchemy models)
    class Config:
        orm_mode = True

