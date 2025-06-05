from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.disbursement import Disbursement
from app.schemas.disbursement import DisbursementCreate, DisbursementOut
from datetime import datetime
import uuid
from typing import List

router = APIRouter()

@router.post("/", response_model=DisbursementOut)
def create_disbursement(data: DisbursementCreate, db: Session = Depends(get_db)):
    disbursement = Disbursement(
        loan_id=data.loan_id,
        user_id=data.user_id,
        amount=data.amount,
        status="completed",
        reference=str(uuid.uuid4()),
        completed_at=datetime.utcnow()
    )
    db.add(disbursement)
    db.commit()
    db.refresh(disbursement)
    return disbursement

router = APIRouter()

@router.post("/", response_model=DisbursementOut)
def disburse_funds(disb: DisbursementCreate, db: Session = Depends(get_db)):
    new_disbursement = Disbursement(**disb.dict())
    db.add(new_disbursement)
    db.commit()
    db.refresh(new_disbursement)
    return new_disbursement

@router.get("/loan/{loan_id}", response_model=List[DisbursementOut])
def get_disbursements_by_loan(loan_id: int, db: Session = Depends(get_db)):
    return db.query(Disbursement).filter(Disbursement.loan_id == loan_id).all()
