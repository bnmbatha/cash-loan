from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.session import Base
from datetime import datetime

class LoanAuditLog(Base):
    __tablename__ = "loan_audit_log"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    action = Column(String)  # "approved" or "rejected"
    actor_id = Column(Integer)  # admin user
    reason = Column(String, nullable=True)  # for rejections
    timestamp = Column(DateTime, default=datetime.utcnow)
