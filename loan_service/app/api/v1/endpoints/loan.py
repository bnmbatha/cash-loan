# Import FastAPI tools for routing, dependencies, and query handling
from fastapi import APIRouter, Depends, HTTPException, Query

# SQLAlchemy tools to interact with the database
from sqlalchemy.orm import Session
from sqlalchemy import and_

# Typing and time libraries
from typing import Optional
from datetime import datetime, timedelta

# Import local modules and functions
from app.db.session import get_db  # DB session provider
from app.schemas.loan import LoanCreate, LoanOut, PaginatedLoans  # Pydantic schemas
from app.db.models.loan import Loan  # Loan model
from common_libs.auth.dependencies import get_current_user  # Get authenticated user info
from app.core.loan_logic import calculate_monthly_payment  # Business logic
from common_libs.auth.roles import require_role  # Role-based access decorator

# Define a router for loan-related endpoints
router = APIRouter()

# -----------------------------
# Endpoint: Apply for a loan
# -----------------------------
@router.post("/apply", response_model=LoanOut, operation_id="submit_loan_application")
def apply_for_loan(
    loan: LoanCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]
    new_loan = Loan(user_id=user_id, **loan.dict())
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return LoanOut.from_orm(new_loan)

# ---------------------------------------------------------
# Endpoint: Get current user's loans with filtering/paging
# ---------------------------------------------------------
@router.get("/me", response_model=PaginatedLoans)
def get_my_loans(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    status: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    sort_by: Optional[str] = Query("created_at", pattern="^(created_at|amount|status)$"),
    sort_order: Optional[str] = Query("desc", pattern="^(asc|desc)$")
):
    filters = [Loan.user_id == current_user["user_id"]]
    if status:
        filters.append(Loan.status == status)
    if created_after:
        filters.append(Loan.created_at >= created_after)
    if created_before:
        filters.append(Loan.created_at <= created_before)

    query = db.query(Loan).filter(and_(*filters))
    order_column = getattr(Loan, sort_by)
    order_column = order_column.desc() if sort_order == "desc" else order_column.asc()
    query = query.order_by(order_column)

    total = query.count()
    loans = query.offset(skip).limit(limit).all()

    items = []
    for loan in loans:
        loan_data = LoanOut.from_orm(loan)
        loan_data.monthly_payment = calculate_monthly_payment(
            loan.amount, loan.term_months, loan.interest_rate
        )
        items.append(loan_data)

    return {"total": total, "items": items}

# ----------------------------
# Endpoint: Get specific loan
# ----------------------------
@router.get("/{loan_id}", response_model=LoanOut)
def get_loan_by_id(
    loan_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    # Only the loan owner or admin can view
    if loan.user_id != current_user["user_id"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    loan_data = LoanOut.from_orm(loan)
    loan_data.monthly_payment = calculate_monthly_payment(
        loan.amount, loan.term_months, loan.interest_rate
    )
    return loan_data

# --------------------------------------------
# Admin-only: Get loans for a specific user
# --------------------------------------------
@router.get("/user/{user_id}", response_model=PaginatedLoans)
def get_loans_by_user_id(
    user_id: int,
    current_user: dict = Depends(require_role("admin")),  # ✅ Secured
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    status: Optional[str] = None,
    created_after: Optional[datetime] = None,
    created_before: Optional[datetime] = None,
    sort_by: Optional[str] = Query("created_at", pattern="^(created_at|amount|status)$"),
    sort_order: Optional[str] = Query("desc", pattern="^(asc|desc)$")
):
    filters = [Loan.user_id == user_id]
    if status:
        filters.append(Loan.status == status)
    if created_after:
        filters.append(Loan.created_at >= created_after)
    if created_before:
        filters.append(Loan.created_at <= created_before)

    query = db.query(Loan).filter(and_(*filters))
    order_column = getattr(Loan, sort_by)
    order_column = order_column.desc() if sort_order == "desc" else order_column.asc()
    query = query.order_by(order_column)

    total = query.count()
    loans = query.offset(skip).limit(limit).all()

    items = []
    for loan in loans:
        loan_data = LoanOut.from_orm(loan)
        loan_data.monthly_payment = calculate_monthly_payment(
            loan.amount, loan.term_months, loan.interest_rate
        )
        items.append(loan_data)

    return {"total": total, "items": items}

@router.get("/calculate")
def calculate_loan_estimate(
    amount: float = Query(..., gt=0),
    term_months: int = Query(..., gt=0),
    interest_rate: float = Query(..., gt=0)
):
    """
    Estimate loan monthly payment, total interest, and payoff date.
    Publicly accessible — no authentication required.
    """
    monthly_payment = calculate_monthly_payment(amount, term_months, interest_rate)
    total_payment = monthly_payment * term_months
    total_interest = total_payment - amount
    payoff_date = datetime.now() + timedelta(days=30 * term_months)

    return {
        "monthly_payment": round(monthly_payment, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2),
        "payoff_date": payoff_date.date()
    }

