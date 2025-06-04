# Import column types and utilities from SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship  # Used to define relationships between tables
from app.db.session import Base  # Import the Base class from your session config
import datetime  # Used to set default timestamps

repayments = relationship("Repayment", back_populates="loan", cascade="all, delete-orphan")

documents = relationship("Document", back_populates="loan", cascade="all, delete-orphan")

# Define a model class for the "loans" table in the database
class Loan(Base):
    # Name of the table in the database
    __tablename__ = "loans"

    # Unique identifier for each loan (Primary Key)
    id = Column(Integer, primary_key=True, index=True)

    # ID of the user who applied for the loan
    user_id = Column(Integer, index=True)

    # Total loan amount requested by the user
    amount = Column(Float, nullable=False)

    # Duration of the loan in months
    term_months = Column(Integer)

    # Annual interest rate for the loan (e.g., 12.5%)
    interest_rate = Column(Float)

    # Status of the loan application (e.g., pending, approved, rejected)
    status = Column(String, default="pending")

    # ID of the admin user who approved or rejected the loan
    approved_by = Column(Integer, nullable=True)

    # Timestamp showing when the loan was created
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    paid = Column(Boolean, default=False)

