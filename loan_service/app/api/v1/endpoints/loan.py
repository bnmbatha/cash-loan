from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.loan import LoanCreate, LoanOut
from app.db.models.loan import Loan
from fastapi import APIRouter, Depends
from common_libs.auth.dependencies import get_current_user
from app.db.session import Base



router = APIRouter()

@router.post("/apply", operation_id="submit_loan_application")
def apply_for_loan(loan: LoanCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
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

@router.get("/me", response_model=list[LoanOut])
def get_my_loans(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]
    loans = db.query(Loan).filter(Loan.user_id == user_id).all()
    return loans

@router.get("/{loan_id}", response_model=LoanOut)
def get_loan_by_id(
    loan_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    # Ensure user can only access their own loan (unless admin logic is added later)
    if loan.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this loan")

    return loan
