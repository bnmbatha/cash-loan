from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.loan import LoanCreate, LoanOut
from app.db.models.loan import Loan

router = APIRouter()

@router.post("/apply", response_model=LoanOut)
def apply_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    new_loan = Loan(**loan.dict())
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan
