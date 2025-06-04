# FastAPI modules
from fastapi import APIRouter, Depends, HTTPException, Body

# SQLAlchemy and app-specific imports
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.loan import Loan
from app.db.models.loan_audit_log import LoanAuditLog
from common_libs.auth.dependencies import get_current_user
from common_libs.auth.roles import require_role
from common_libs.notifications import send_email
from common_libs.disbursement import disburse_funds
from common_libs.users import get_user_email  # Calls user_service API
from app.db.models.repayment import Repayment
from datetime import timedelta
from datetime import datetime

router = APIRouter()

# After loan.status is set to 'approved'
repayment_schedule = []
monthly_amount = loan.amount / loan.term_months

for i in range(loan.term_months):
    due_date = datetime.utcnow() + timedelta(days=30 * (i + 1))
    repayment_schedule.append(
        Repayment(
            loan_id=loan.id,
            due_date=due_date,
            amount_due=monthly_amount,
            status="pending"
        )
    )

db.add_all(repayment_schedule)

# ------------------------
# Admin: Approve a loan
# ------------------------
@router.put("/{loan_id}/approve")
def approve_loan(
    loan_id: int,
    current_user: dict = Depends(require_role("admin")),  # ✅ Secured with admin role
    db: Session = Depends(get_db)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan is not in pending status")

    loan.status = "approved"
    loan.approved_by = current_user["user_id"]

    db.add(LoanAuditLog(
        loan_id=loan.id,
        action="approved",
        actor_id=current_user["user_id"]
    ))

    db.commit()
    db.refresh(loan)

    try:
        email = get_user_email(loan.user_id)  # Calls user_service
        send_email(to=email, subject="Loan Approved", body=f"Your loan #{loan.id} has been approved.")
    except Exception as e:
        print(f"Email error: {e}")

    try:
        disburse_funds(user_id=loan.user_id, amount=loan.amount, loan_id=loan.id)
    except Exception as e:
        print(f"Disbursement error: {e}")

    return {"message": "Loan approved", "loan_id": loan.id}

# ------------------------
# Admin: Reject a loan
# ------------------------
@router.put("/{loan_id}/reject")
def reject_loan(
    loan_id: int,
    reason: str = Body(..., embed=True),
    current_user: dict = Depends(require_role("admin")),  # ✅ Secured with admin role
    db: Session = Depends(get_db)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan is not in pending status")

    loan.status = "rejected"
    loan.approved_by = current_user["user_id"]

    db.add(LoanAuditLog(
        loan_id=loan.id,
        action="rejected",
        actor_id=current_user["user_id"],
        reason=reason
    ))

    db.commit()
    db.refresh(loan)

    try:
        email = get_user_email(loan.user_id)
        send_email(
            to=email,
            subject="Loan Rejected",
            body=f"Unfortunately, your loan #{loan.id} was rejected. Reason: {reason}"
        )
    except Exception as e:
        print(f"Email error: {e}")

    return {"message": "Loan rejected", "loan_id": loan.id}

@router.put("/{loan_id}/review")
def review_loan_by_agent(
    loan_id: int,
    comment: str = Body(..., embed=True),
    current_user: dict = Depends(require_role("agent")),
    db: Session = Depends(get_db)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan or loan.review_status != "pending":
        raise HTTPException(status_code=400, detail="Invalid loan or already reviewed")
    
    loan.review_status = "under_review"
    loan.reviewed_by = current_user["user_id"]
    loan.reviewed_at = datetime.utcnow()
    loan.approval_comment = comment

    db.commit()
    return {"message": "Loan reviewed by agent", "loan_id": loan.id}
