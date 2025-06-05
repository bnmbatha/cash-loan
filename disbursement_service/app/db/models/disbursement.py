from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base

class Disbursement(Base):
    __tablename__ = "disbursements"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, completed, failed
    reference = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
