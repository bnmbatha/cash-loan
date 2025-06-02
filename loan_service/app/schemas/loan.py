from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.session import Base
from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class LoanCreate(BaseModel):
    user_id: int
    amount: float
    term_months: int
    interest_rate: Optional[float] = 15.0

class LoanOut(LoanCreate):
    id: int
    status: str
    created_at: datetime

class LoanOut(BaseModel):
    id: int
    user_id: int
    amount: float
    term_months: int
    interest_rate: float
    status: str
    approved_by: int | None = None
    created_at: datetime

class LoanOut(BaseModel):
    id: int
    user_id: int
    amount: float
    term_months: int
    interest_rate: float
    status: Literal["pending", "approved", "rejected"]
    approved_by: int | None = None
    created_at: datetime
    monthly_payment: float | None = None    
    
    class Config:
        from_attributes = True
