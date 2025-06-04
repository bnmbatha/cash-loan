from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.db.session import get_db
from app.db.models.loan import Loan
from common_libs.auth.dependencies import get_current_user
from common_libs.auth.roles import require_role

router = APIRouter()

@router.get("/admin/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("admin"))
):
    today = datetime.utcnow().date()
    start_of_week = today - timedelta(days=today.weekday())

    # Applications submitted today
    applications_today = db.query(func.count()).filter(
        func.date(Loan.created_at) == today
    ).scalar()

    # Loans approved this week
    approved_this_week = db.query(func.count()).filter(
        and_(
            Loan.status == "approved",
            func.date(Loan.created_at) >= start_of_week
        )
    ).scalar()

    # Default rate = unpaid loans / all approved loans
    total_approved = db.query(func.count()).filter(Loan.status == "approved").scalar()
    total_unpaid = db.query(func.count()).filter(
        and_(Loan.status == "approved", Loan.paid == False)
    ).scalar() if hasattr(Loan, "paid") else 0

    default_rate = (total_unpaid / total_approved * 100) if total_approved > 0 else 0.0

    return {
        "applications_today": applications_today,
        "loans_approved_this_week": approved_this_week,
        "default_rate_percent": round(default_rate, 2)
    }
