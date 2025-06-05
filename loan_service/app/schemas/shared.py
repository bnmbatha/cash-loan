# Import List type for declaring lists in Pydantic models
from typing import List

# Import BaseModel for creating data schemas
from pydantic import BaseModel

# Import the LoanOut schema (used to define each loan item)
from app.schemas.loan import LoanOut

# Schema for paginated loan responses (used in endpoints like GET /me or /user/{id})
class PaginatedLoans(BaseModel):
    total: int                 # Total number of loan records available (across all pages)
    items: List[LoanOut]       # List of loan records on the current page
