# Import FastAPI tools for routing, dependencies, error handling, and query parameters
from fastapi import APIRouter, Depends, HTTPException, Query

# SQLAlchemy tools for interacting with the database
from sqlalchemy.orm import Session
from sqlalchemy import and_

# Standard typing utilities
from typing import Optional, List
from datetime import datetime

# Internal modules and business logic
from app.db.session import get_db  # Function to get a DB session
from app.schemas.loan import LoanCreate, LoanOut, PaginatedLoans  # Pydantic schemas for request and response validation
from app.db.models.loan import Loan  # Loan database model
from common_libs.auth.dependencies import get_current_user  # Dependency to get the authenticated user
from app.core.loan_logic import calculate_monthly_payment  # Function to calculate loan monthly payments

# Create a FastAPI router to define loan-related endpoints
router = APIRouter()

# -----------------------------------------------
# Endpoint to apply for a loan (POST /apply)
# -----------------------------------------------
@router.post("/apply", response_model=LoanOut, operation_id="submit_loan_application")
def apply_for_loan(
    loan: LoanCreate,  # Input data for creating a loan
    current_user: dict = Depends(get_current_user),  # Authenticated user
    db: Session = Depends(get_db)  # Database session
):
    # Get the user ID of the applicant
    user_id = current_user["user_id"]

    # Create a new loan object using the input data
    new_loan = Loan(user_id=user_id, **loan.dict())

    # Add the loan to the database
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)  # Refresh to get the latest data (e.g., auto-generated ID)

    # Return the created loan as a response
    return LoanOut.from_orm(new_loan)


# -------------------------------------------------------------
# Endpoint to fetch the current user's loans (GET /me)
# Supports pagination, filtering by status and date, and sorting
# -------------------------------------------------------------
@router.get("/me", response_model=PaginatedLoans)
def get_my_loans(
    current_user: dict = Depends(get_current_user),  # Get the current user
    db: Session = Depends(get_db),  # Get a database session

    # Pagination parameters
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),

    # Optional filters
    status: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,

    # Sorting options
    sort_by: Optional[str] = Query("created_at", pattern="^(created_at|amount|status)$"),
    sort_order: Optional[str] = Query("desc", pattern="^(asc|desc)$")
):
    # Build filters to narrow down the loan query
    filters = [Loan.user_id == current_user["user_id"]]
    if status:
        filters.append(Loan.status == status)
    if created_after:
        filters.append(Loan.created_at >= created_after)
    if created_before:
        filters.append(Loan.created_at <= created_before)

    # Build and order the query
    query = db.query(Loan).filter(and_(*filters))
    order_column = getattr(Loan, sort_by)
    if sort_order == "desc":
        order_column = order_column.desc()
    query = query.order_by(order_column)

    # Execute pagination and return results
    total = query.count()
    loans = query.offset(skip).limit(limit).all()

    # Add monthly payment calculation to each loan
    items = []
    for loan in loans:
        loan_data = LoanOut.from_orm(loan)
        loan_data.monthly_payment = calculate_monthly_payment(
            loan.amount, loan.term_months, loan.interest_rate
        )
        items.append(loan_data)

    return {"total": total, "items": items}


# --------------------------------------------------
# Endpoint to get details for a specific loan by ID
# --------------------------------------------------
@router.get("/{loan_id}", response_model=LoanOut)
def get_loan_by_id(
    loan_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Look up the loan in the database
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    # Return 404 if loan does not exist
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    # Only the loan owner or an admin can view the loan
    if loan.user_id != current_user["user_id"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Attach monthly payment calculation to the result
    loan_data = LoanOut.from_orm(loan)
    loan_data.monthly_payment = calculate_monthly_payment(
        loan.amount, loan.term_months, loan.interest_rate
    )
    return loan_data


# --------------------------------------------------------------------
# Admin-only endpoint to fetch loans by any user's ID (GET /user/{id})
# Same filtering, pagination, and sorting as the user endpoint
# --------------------------------------------------------------------
@router.get("/user/{user_id}", response_model=PaginatedLoans)
def get_loans_by_user_id(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),

    # Pagination and filtering
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    status: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    sort_by: Optional[str] = Query("created_at", pattern="^(created_at|amount|status)$"),
    sort_order: Optional[str] = Query("desc", pattern="^(asc|desc)$")
):
    # Only admins are allowed to use this endpoint
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    # Build filters based on query parameters
    filters = [Loan.user_id == user_id]
    if status:
        filters.append(Loan.status == status)
    if created_after:
        filters.append(Loan.created_at >= created_after)
    if created_before:
        filters.append(Loan.created_at <= created_before)

    # Build and sort the query
    query = db.query(Loan).filter(and_(*filters))
    order_column = getattr(Loan, sort_by)
    if sort_order == "desc":
        order_column = order_column.desc()
    query = query.order_by(order_column)

    # Execute query and paginate results
    total = query.count()
    loans = query.offset(skip).limit(limit).all()

    # Format and return the loan data
    items = []
    for loan in loans:
        loan_data = LoanOut.from_orm(loan)
        loan_data.monthly_payment = calculate_monthly_payment(
            loan.amount, loan.term_months, loan.interest_rate
        )
        items.append(loan_data)

    return {"total": total, "items": items}
