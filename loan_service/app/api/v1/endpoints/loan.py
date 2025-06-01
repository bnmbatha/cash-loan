from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.loan import LoanCreate, LoanOut
from app.db.models.loan import Loan
from fastapi import APIRouter, Depends
from common_libs.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/apply")
def apply_loan(loan: LoanCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    ...
    new_loan = Loan(user_id=user_id, **loan.dict())

@router.post("/apply", response_model=LoanOut)
def apply_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    new_loan = Loan(**loan.dict())
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan
