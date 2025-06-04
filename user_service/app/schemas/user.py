from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

# Schema used for incoming user registration data
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Literal["admin", "agent", "customer"] = "customer"  # ✅ New field with default

# Schema used to return user data in API responses
class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: Literal["admin", "agent", "customer"]  # ✅ Add role to output schema

# Schema used for updating user data
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Literal["admin", "agent", "customer"]] = None  # ✅ Optional role update

    class Config:
        orm_mode = True
