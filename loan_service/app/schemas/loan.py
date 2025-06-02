from pydantic import BaseModel
from typing import Optional, Literal, List
from datetime import datetime

# 🔹 Used when creating a loan
class LoanCreate(BaseModel):
    amount: float
    term_months: int
    interest_rate: Optional[float] = 15.0  # Default rate

# 🔹 Used for reading loan data (e.g. /me, /{loan_id})
class LoanOut(BaseModel):
    id: int
    user_id: int
    amount: float
    term_months: int
    interest_rate: float
    status: Literal["pending", "approved", "rejected"]
    approved_by: Optional[int] = None
    created_at: datetime
    monthly_payment: Optional[float] = None

    class Config:
        from_attributes = True  # for ORM conversion (Pydantic v2)

# 🔹 Used for paginated responses
class PaginatedLoans(BaseModel):
    total: int
    items: List[LoanOut]

