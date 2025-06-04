# Import necessary modules and functions
from fastapi import APIRouter, Depends, HTTPException, Body  # FastAPI tools for routing, dependency injection, error handling
from sqlalchemy.orm import Session  # Used to interact with the database
from app.db.session import get_db  # Function to retrieve a database session
from app.db.models.loan import Loan  # Loan database model
from app.schemas.approval import LoanApproval  # Schema for loan approval (optional usage)
from common_libs.auth.dependencies import get_current_user  # Function to get the currently logged-in user
from app.db.models.loan_audit_log import LoanAuditLog  # Model to log loan approval/rejection history
from common_libs.notifications import send_email  # Function to send email notifications
from common_libs.disbursement import disburse_funds  # Function to disburse funds to a user's account
from common_libs.users import get_user_email  # Function to fetch a user's email address from the user service

# Create an API router for loan approval/rejection endpoints
router = APIRouter()

# Endpoint to approve a loan by loan ID
@router.put("/{loan_id}/approve")
def approve_loan(
    loan_id: int,  # The ID of the loan to approve
    current_user: dict = Depends(get_current_user),  # Dependency to get the logged-in user's details
    db: Session = Depends(get_db)  # Dependency to get the database session
):
    # Check if the current user is an admin
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    # Look for the loan in the database
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan is not in pending status")

    # Mark the loan as approved and record who approved it
    loan.status = "approved"
    loan.approved_by = current_user["user_id"]

    # Log the approval action
    db.add(LoanAuditLog(
        loan_id=loan.id,
        action="approved",
        actor_id=current_user["user_id"]
    ))

    # Save the changes to the database
    db.commit()
    db.refresh(loan)

    # Attempt to send an email notification to the user
    try:
        email = get_user_email(loan.user_id)  # Fetch the email of the loan owner
        send_email(
            to=email,
            subject="Loan Approved",
            body=f"Your loan #{loan.id} has been approved"
        )
    except Exception as e:
        print(f"Email error: {e}")

    # Attempt to disburse the loan funds to the user
    try:
        disburse_funds(
            user_id=loan.user_id,
            amount=loan.amount,
            loan_id=loan.id
        )
    except Exception as e:
        print(f"Disbursement error: {e}")

    # Return a confirmation message
    return {"message": "Loan approved", "loan_id": loan.id}


# Endpoint to reject a loan by loan ID
@router.put("/{loan_id}/reject")
def reject_loan(
    loan_id: int,  # The ID of the loan to reject
    reason: str = Body(..., embed=True),  # Rejection reason (required in request body)
    current_user: dict = Depends(get_current_user),  # Dependency to get the logged-in user's details
    db: Session = Depends(get_db)  # Dependency to get the database session
):
    # Check if the current user is an admin
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    # Look for the loan in the database
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan is not in pending status")

    # Mark the loan as rejected and record who rejected it
    loan.status = "rejected"
    loan.approved_by = current_user["user_id"]

    # Log the rejection action with a reason
    db.add(LoanAuditLog(
        loan_id=loan.id,
        action="rejected",
        actor_id=current_user["user_id"],
        reason=reason
    ))

    # Save the changes to the database
    db.commit()
    db.refresh(loan)

    # Attempt to send an email notification to the user
    try:
        email = get_user_email(loan.user_id)  # Fetch the email of the loan owner
        send_email(
            to=email,
            subject="Loan Rejected",
            body=f"Unfortunately, your loan #{loan.id} was rejected. Reason: {reason}"
        )
    except Exception as e:
        print(f"Email error: {e}")

    # Return a confirmation message
    return {"message": "Loan rejected", "loan_id": loan.id}
