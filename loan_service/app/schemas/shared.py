from typing import List
from pydantic import BaseModel
from app.schemas.loan import LoanOut

class PaginatedLoans(BaseModel):
    total: int
    items: List[LoanOut]
