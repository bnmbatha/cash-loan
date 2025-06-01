from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import datetime

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float, nullable=False)
    term_months = Column(Integer)
    interest_rate = Column(Float)
    status = Column(String, default="pending")  # pending, approved, rejected
    approved_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
