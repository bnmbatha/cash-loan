from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from common_libs.auth.dependencies import get_current_user
from app.db.models.document import Document
from app.db.models.loan import Loan
from app.schemas.document import DocumentOut
from common_libs.s3 import upload_to_s3

router = APIRouter()

@router.post("/loans/{loan_id}/upload-doc", response_model=DocumentOut)
def upload_document(
    loan_id: int,
    file: UploadFile = File(...),
    document_type: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan or loan.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized or loan not found")

    file_url = upload_to_s3(file)
    doc = Document(
        loan_id=loan_id,
        filename=file.filename,
        file_url=file_url,
        document_type=document_type
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"message": "Document uploaded", "url": s3_url}
