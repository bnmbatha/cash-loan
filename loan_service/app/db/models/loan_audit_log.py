# Import SQLAlchemy column types and utilities
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

# Import the Base class for model declaration
from app.db.session import Base

# Import datetime to set default timestamps
from datetime import datetime

# Define a model that represents the loan audit log table in the database
class LoanAuditLog(Base):
    # Name of the table in the database
    __tablename__ = "loan_audit_log"

    # Primary key - unique ID for each audit log entry
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key linking to the loan being logged
    loan_id = Column(Integer, ForeignKey("loans.id"))

    # Action taken on the loan ("approved" or "rejected")
    action = Column(String)

    # ID of the user (admin) who performed the action
    actor_id = Column(Integer)

    # Optional reason for rejection (used when action is "rejected")
    reason = Column(String, nullable=True)

    # Timestamp of when the action occurred
    timestamp = Column(DateTime, default=datetime.utcnow)
