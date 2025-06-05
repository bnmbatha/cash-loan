from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DisbursementCreate(BaseModel):
    loan_id: int
    user_id: int
    amount: float

class DisbursementOut(DisbursementCreate):
    id: int
    status: str
    reference: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    processed_at: datetime

    class Config:
        orm_mode = True
