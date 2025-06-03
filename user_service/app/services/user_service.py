# Import required modules for ORM, password hashing, JWTs, and config
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.db.models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt, JWTError
from app.core.config import settings

# Create a password context for hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token expiration time for password reset tokens (in minutes)
RESET_TOKEN_EXPIRE_MINUTES = 30

# 🔐 Generate a JWT token for password reset with a short expiry time
def generate_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}  # "sub" holds the email as the subject
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

# 🧂 Hash a plain-text password using bcrypt
def get_password_hash(password):
    return pwd_context.hash(password)

# 🧑‍💻 Create a new user in the database from a UserCreate schema object
def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)  # Securely hash the user's password
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)     # Add new user to the session
    db.commit()         # Commit changes to the DB
    db.refresh(db_user) # Refresh instance with DB-generated fields (like ID)
    return db_user

# ✉️ Generate a token to confirm a user's email address (24-hour expiry)
def generate_email_token(email: str):
    return jwt.encode(
        {"sub": email, "exp": datetime.utcnow() + timedelta(hours=24)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

# ✅ Verify a user's email using a token and activate their account
def verify_email_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")  # Extract email from token
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Find the user in the DB by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Mark user as active/verified
    user.is_active = True
    db.commit()
    return {"message": "Email verified successfully"}
