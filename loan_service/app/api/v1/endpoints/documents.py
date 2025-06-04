from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.document import Document
from common_libs.auth.dependencies import get_current_user
from app.utils.s3 import upload_file_to_s3  # You’ll create this helper

router = APIRouter()

@router.post("/loans/{loan_id}/upload-doc")
async def upload_document(
    loan_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Upload file to S3
    try:
        s3_url = upload_file_to_s3(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")

    doc = Document(
        loan_id=loan_id,
        file_name=file.filename,
        file_url=s3_url
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"message": "Document uploaded", "url": s3_url}
