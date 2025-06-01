from fastapi import FastAPI
from app.api.v1.endpoints import loan

app = FastAPI(title="Loan Service")

app.include_router(loan.router, prefix="/api/v1/loans", tags=["loans"])
