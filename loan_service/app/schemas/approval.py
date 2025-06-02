from pydantic import BaseModel

class LoanApproval(BaseModel):
    approved_by: int

