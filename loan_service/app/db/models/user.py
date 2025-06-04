# loan_service/app/db/models/user.py
from sqlalchemy import Column, Integer, String
from app.db.models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
