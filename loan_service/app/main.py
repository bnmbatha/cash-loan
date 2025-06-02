from fastapi import FastAPI
from app.api.v1.endpoints import loan
from app.api.v1.endpoints import approval
from app.db.models.loan_audit_log import LoanAuditLog
from app.db.session import Base, engine

app = FastAPI(title="Loan Service")

app.include_router(loan.router, prefix="/api/v1/loans", tags=["loans"])
app.include_router(approval.router, prefix="/api/v1/loans", tags=["approval"])

Base.metadata.create_all(bind=engine)

