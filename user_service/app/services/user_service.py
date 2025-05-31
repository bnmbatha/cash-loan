from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.db.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = User(full_name=user.full_name, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
