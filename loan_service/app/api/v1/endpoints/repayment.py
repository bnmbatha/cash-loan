from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.repayment import Repayment
from app.db.session import get_db
from common_libs.auth.dependencies import get_current_user
from app.schemas.repayment import RepaymentCreate, RepaymentOut, RepaymentUpdate
from typing import List, Optional

router = APIRouter()

# Get repayments by loan ID
# ✅ Get repayments for a loan, with optional filtering by status and sorting
@router.get("/loan/{loan_id}", response_model=List[RepaymentOut])
def get_repayments_for_loan(
    loan_id: int,
    status: Optional[str] = None,  # e.g. "paid", "pending", "late"
    sort_by: Optional[str] = "due_date",  # Can be "due_date", "amount_due", etc.
    sort_order: Optional[str] = "asc",    # "asc" or "desc"
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Repayment).filter(Repayment.loan_id == loan_id)

    if status:
        query = query.filter(Repayment.status == status)

    # Dynamically apply sorting
    order_column = getattr(Repayment, sort_by)
    query = query.order_by(order_column.asc() if sort_order == "asc" else order_column.desc())

    return query.all()

# Mark repayment as paid
@router.put("/{repayment_id}/pay", response_model=RepaymentOut)
def mark_as_paid(repayment_id: int, update: RepaymentUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repayment = db.query(Repayment).filter(Repayment.id == repayment_id).first()
    if not repayment:
        raise HTTPException(status_code=404, detail="Repayment not found")

    repayment.amount_paid = update.amount_paid
    repayment.paid_on = update.paid_on
    repayment.status = "paid"
    db.commit()
    db.refresh(repayment)
    return repayment
