import boto3
from fastapi import UploadFile
import uuid
from app.core.config import settings

s3 = boto3.client("s3", region_name=settings.AWS_REGION)

def upload_file_to_s3(file: UploadFile):
    file_key = f"documents/{uuid.uuid4()}_{file.filename}"
    s3.upload_fileobj(file.file, settings.S3_BUCKET_NAME, file_key)
    return f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
