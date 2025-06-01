from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.session import Base


class LoanCreate(BaseModel):
    user_id: int
    amount: float
    term_months: int
    interest_rate: Optional[float] = 15.0

class LoanOut(LoanCreate):
    id: int
    status: str
    created_at: datetime
