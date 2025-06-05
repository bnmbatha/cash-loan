# Import Pydantic's base model for data validation
from pydantic import BaseModel

# Import utilities for optional fields, fixed values, and lists
from typing import Optional, Literal, List

# Import datetime to represent timestamps
from datetime import datetime

# ----------------------------------------------
# Schema for creating a loan (used in POST /apply)
# ----------------------------------------------
class LoanCreate(BaseModel):
    amount: float               # The total amount of the loan
    term_months: int            # Duration of the loan in months
    interest_rate: Optional[float] = 15.0  # Optional interest rate, defaults to 15%


# ------------------------------------------------------
# Schema for reading a loan record (used in responses)
# ------------------------------------------------------
class LoanOut(BaseModel):
    id: int                     # Unique ID of the loan
    user_id: int                # ID of the user who owns the loan
    amount: float               # Total amount of the loan
    term_months: int            # Loan duration in months
    interest_rate: float        # Annual interest rate for the loan
    status: Literal["pending", "approved", "rejected"]  # Loan status (limited to 3 values)
    approved_by: Optional[int] = None  # ID of the admin who approved/rejected the loan
    created_at: datetime        # Timestamp when the loan was created
    monthly_payment: Optional[float] = None  # Calculated monthly payment (set manually)

    class Config:
        # Enable compatibility with SQLAlchemy models (ORM mode)
        from_attributes = True


# -------------------------------------------------------
# Schema for paginated list of loans (used in GET /me)
# -------------------------------------------------------
class PaginatedLoans(BaseModel):
    total: int                  # Total number of loans available
    items: List[LoanOut]        # List of loan records returned on the current page
