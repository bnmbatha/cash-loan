from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.loan import Loan
from app.schemas.approval import LoanApproval
from common_libs.auth.dependencies import get_current_user
from app.db.models.loan_audit_log import LoanAuditLog
from common_libs.notifications import send_email
from common_libs.disbursement import disburse_funds
from common_libs.users import get_user_email

# After db.refresh(loan)
email = get_user_email(loan.user_id)

try:
    send_email(
        to=email,
        subject="Loan Approved",
        body=f"Your loan #{loan.id} has been approved 🎉"
    )
except Exception as e:
    print(f"Email error: {e}")


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

    log = LoanAuditLog(
        loan_id=loan.id,
        action="approved",
        actor_id=current_user["user_id"]
    )
    db.add(log)

    db.commit()
    db.refresh(loan)

    # ✅ Send notification
    try:
        send_email(
            to="client@email.com",  # 🔁 Replace with real email via user_service
            subject="Loan Approved",
            body=f"Your loan #{loan.id} has been approved 🎉"
        )
    except Exception as e:
        print(f"Email error: {e}")

    # ✅ Auto-disburse funds
    try:
        disburse_funds(
            user_id=loan.user_id,
            amount=loan.amount,
            loan_id=loan.id
        )
    except Exception as e:
        print(f"Disbursement error: {e}")

    return {"message": "Loan approved", "loan_id": loan.id}


@router.put("/{loan_id}/reject")
def reject_loan(
    loan_id: int,
    reason: str = Body(..., embed=True),
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

    log = LoanAuditLog(
        loan_id=loan.id,
        action="rejected",
        actor_id=current_user["user_id"],
        reason=reason
    )
    db.add(log)

    db.commit()
    db.refresh(loan)

    email = get_user_email(loan.user_id)

    try:
        send_email(
            to=email,
            subject="Loan Approved",
            body=f"Your loan #{loan.id} has been approved 🎉"
        )
    except Exception as e:
        print(f"Email error: {e}")
        
    try:
        send_email(
            to="client@email.com",  # 🔁 Replace with real email via user_service
            subject="Loan Rejected",
            body=f"Unfortunately, your loan #{loan.id} was rejected. Reason: {reason}"
        )
    except Exception as e:
        print(f"Email error: {e}")

    return {"message": "Loan rejected", "loan_id": loan.id}



