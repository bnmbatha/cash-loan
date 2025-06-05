# Import the base class for creating data models from Pydantic
from pydantic import BaseModel

# Define a schema (data validation model) for loan approval input
class LoanApproval(BaseModel):
    # The ID of the admin who approved the loan
    approved_by: int
