# app/db/models/repayment.py

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime
from typing import Optional
from enum import Literal
from pydantic import BaseModel


class Repayment(Base):
    """
    Represents a scheduled or actual repayment associated with a loan.
    """
    __tablename__ = "repayments"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier
    loan_id = Column(Integer, ForeignKey("loans.id", ondelete="CASCADE"), nullable=False)  # Link to loan
    due_date = Column(DateTime, nullable=False)  # Date the repayment is due
    amount_due = Column(Float, nullable=False)  # Scheduled amount to be paid
    amount_paid = Column(Float, default=0.0)  # Actual amount paid
    paid_on = Column(DateTime, nullable=True)  # When payment was made (if any)
    status = Column(String, default="pending")  # Status: "pending", "paid", or "late"

    # Relationship to the Loan object
    loan = relationship("Loan", back_populates="repayments")

# Schema for creating a repayment (normally auto-generated)
class RepaymentCreate(BaseModel):
    due_date: datetime
    amount_due: float

# Schema for marking a repayment as paid
class RepaymentUpdate(BaseModel):
    amount_paid: float
    paid_on: datetime

# Schema for response output
class RepaymentOut(BaseModel):
    id: int
    loan_id: int
    due_date: datetime
    amount_due: float
    amount_paid: Optional[float] = 0
    paid_on: Optional[datetime]
    status: Literal["pending", "paid", "late"]

    class Config:
        orm_mode = True
