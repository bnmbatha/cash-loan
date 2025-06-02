from fastapi import FastAPI
from app.api.v1.endpoints import loan
from app.api.v1.endpoints import approval

app = FastAPI(title="Loan Service")

app.include_router(loan.router, prefix="/api/v1/loans", tags=["loans"])
app.include_router(approval.router, prefix="/api/v1/loans", tags=["approval"])
