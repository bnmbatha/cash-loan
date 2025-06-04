# app/db/models/repayment.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime
from typing import Optional

class Repayment(Base):
    """
    Represents a scheduled or actual repayment associated with a loan.
    """
    __tablename__ = "repayments"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier
    loan_id = Column(Integer, ForeignKey("loans.id", ondelete="CASCADE"))  # Link to loan
    due_date = Column(DateTime, nullable=False)  # Date the repayment is due
    amount_due = Column(Float, nullable=False)  # Scheduled amount to be paid
    amount_paid = Column(Float, default=0.0)  # Actual amount paid
    paid_on = Column(DateTime, nullable=True)  # When payment was made (if any)
    status = Column(String, default="pending")  # Status: "pending", "paid", or "late"

    # Relationship to the Loan object
    loan = relationship("Loan", back_populates="repayments")
