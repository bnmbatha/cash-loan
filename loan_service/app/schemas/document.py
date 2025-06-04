from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentOut(BaseModel):
    id: int
    loan_id: int
    filename: str
    file_url: str
    uploaded_at: datetime
    document_type: Optional[str]

    class Config:
        orm_mode = True
