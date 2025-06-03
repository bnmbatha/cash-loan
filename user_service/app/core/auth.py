# Standard library for handling time
from datetime import datetime, timedelta
from typing import Optional

# JWT handling with JOSE
from jose import jwt, JWTError

# Password hashing
from passlib.context import CryptContext

# FastAPI tools for handling security and dependency injection
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# SQLAlchemy session management
from sqlalchemy.orm import Session

# Local project imports
from app.db.session import get_db
from app.db.models.user import User
from app.core.config import settings

# Password hashing context using bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define the OAuth2 scheme for bearer token (e.g., Authorization: Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 🔐 Verifies if the provided plain password matches the stored hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 🔐 Hashes a new password using bcrypt
def get_password_hash(password):
    return pwd_context.hash(password)

# 🔐 Authenticates user based on email and password
# Returns user if credentials are correct, else returns None
def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# 🔐 Creates a JWT token with expiration
# `data` should include user info (e.g., {"sub": user.email})
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})  # Set expiration
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

# 🔐 Retrieves the current authenticated user based on the JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode JWT token using secret key and expected algorithm
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")  # Get email from token payload
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Query user by email
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user  # ✅ Authenticated user object
