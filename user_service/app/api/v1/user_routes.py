# FastAPI and SQLAlchemy dependencies
from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

# Database and models
from app.db.session import SessionLocal
from app.db.models.user import User

# Schemas for request/response models
from app.schemas.user import UserCreate, UserOut, UserUpdate

# User service and utilities
from app.services.user_service import (
    create_user, 
    get_password_hash, 
    verify_email_token, 
    generate_reset_token
)

# Auth handling
from app.core.auth import authenticate_user, create_access_token, get_current_user
from app.core.config import settings

# JWT-related utilities
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr

# Create router for user-related API endpoints
router = APIRouter()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schema for password reset request body
class PasswordReset(BaseModel):
    token: str
    new_password: str

# Endpoint to reset user password using a valid token
@router.post("/reset-password")
def reset_password(data: PasswordReset, db: Session = Depends(get_db)):
    try:
        # Decode the reset token to extract the user's email
        payload = jwt.decode(data.token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Hash the new password and update the user record
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password reset successful"}

# Endpoint to request a password reset link
@router.post("/forgot-password")
def forgot_password(request: Request, email: EmailStr = Body(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate a password reset token and reset URL
    token = generate_reset_token(email)
    reset_url = f"{request.base_url}reset-password?token={token}"
    
    # TODO: Send this reset_url via email
    print("🔗 Reset Link:", reset_url)
    
    return {"message": "Password reset link has been generated. Check your email."}

# Endpoint to register a new user
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(user.password)
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role  # 👈 Assign role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get a user by ID
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update an existing user by ID
@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, updated_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update only the provided fields
    if updated_data.full_name:
        user.full_name = updated_data.full_name
    if updated_data.email:
        user.email = updated_data.email
    if updated_data.password:
        user.hashed_password = get_password_hash(updated_data.password)

    db.commit()
    db.refresh(user)
    return user

# Delete a user by ID
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Endpoint to verify a user's email using a token
@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    return verify_email_token(token, db)

# Login endpoint to authenticate user and return JWT token
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint to get details of the currently authenticated user
@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
