from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
from app.db.session import get_db
from app.schemas.loan import LoanCreate, LoanOut, PaginatedLoans
from app.db.models.loan import Loan
from common_libs.auth.dependencies import get_current_user
from app.core.loan_logic import calculate_monthly_payment

router = APIRouter()

# ✅ Apply for a loan
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


# ✅ Get current user's loans with pagination, filtering, sorting
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
    if sort_order == "desc":
        order_column = order_column.desc()
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


# ✅ Get single loan by ID
@router.get("/{loan_id}", response_model=LoanOut)
def get_loan_by_id(
    loan_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.user_id != current_user["user_id"] and current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    loan_data = LoanOut.from_orm(loan)
    loan_data.monthly_payment = calculate_monthly_payment(
        loan.amount, loan.term_months, loan.interest_rate
    )
    return loan_data


# ✅ Admin-only: view loans by any user ID
@router.get("/user/{user_id}", response_model=PaginatedLoans)
def get_loans_by_user_id(
    user_id: int,
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
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    filters = [Loan.user_id == user_id]
    if status:
        filters.append(Loan.status == status)
    if created_after:
        filters.append(Loan.created_at >= created_after)
    if created_before:
        filters.append(Loan.created_at <= created_before)

    query = db.query(Loan).filter(and_(*filters))

    order_column = getattr(Loan, sort_by)
    if sort_order == "desc":
        order_column = order_column.desc()
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

