from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.loan import Loan
from app.schemas.approval import LoanApproval
from common_libs.auth.dependencies import get_current_user

router = APIRouter()

@router.put("/{loan_id}/approve")
def approve_loan(
    loan_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan is not in pending status")

    loan.status = "approved"
    loan.approved_by = current_user["user_id"]
    db.commit()
    db.refresh(loan)
    return {"message": "Loan approved", "loan_id": loan.id}

@router.put("/{loan_id}/reject")
def reject_loan(
    loan_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan is not in pending status")

    loan.status = "rejected"
    loan.approved_by = current_user["user_id"]
    db.commit()
    db.refresh(loan)
    return {"message": "Loan rejected", "loan_id": loan.id}

