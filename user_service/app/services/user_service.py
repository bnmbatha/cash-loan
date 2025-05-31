from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.db.models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt, JWTError
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def generate_email_token(email: str):
    return jwt.encode(
        {"sub": email, "exp": datetime.utcnow() + timedelta(hours=24)},
        settings.SECRET_KEY,
        algorithm="HS256"
    )

def verify_email_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.commit()
    return {"message": "Email verified successfully"}

