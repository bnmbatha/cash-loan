from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.repayment import Repayment
from app.db.session import get_db
from common_libs.auth.dependencies import get_current_user
from app.schemas.repayment import RepaymentCreate, RepaymentOut, RepaymentUpdate
from typing import List

router = APIRouter()

# Get repayments by loan ID
@router.get("/loan/{loan_id}", response_model=List[RepaymentOut])
def get_repayments_for_loan(loan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    repayments = db.query(Repayment).filter(Repayment.loan_id == loan_id).all()
    return repayments

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
