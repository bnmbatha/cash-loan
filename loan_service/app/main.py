# Import FastAPI to create the web application
from fastapi import FastAPI

# Import routers (route definitions) for loan-related endpoints
from app.api.v1.endpoints import loan        # Routes for applying, viewing, and listing loans
from app.api.v1.endpoints import approval    # Routes for approving or rejecting loans

# Import the audit log model (not directly used here but often triggers table creation)
from app.db.models.loan_audit_log import LoanAuditLog

# Import database base class and engine for schema creation
from app.db.session import Base, engine

# Create the FastAPI application instance
app = FastAPI(title="Loan Service")  # Title will appear in Swagger UI

# Include the loan-related routes under the prefix /api/v1/loans
# Routes from loan.py will be available as /api/v1/loans/...
app.include_router(loan.router, prefix="/api/v1/loans", tags=["loans"])

# Include approval-related routes under the same prefix
# Routes from approval.py will also be available as /api/v1/loans/...
app.include_router(approval.router, prefix="/api/v1/loans", tags=["approval"])

# Create all database tables defined in your models
# This runs only once at startup and ensures tables exist in the database
Base.metadata.create_all(bind=engine)
