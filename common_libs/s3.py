import boto3
from uuid import uuid4
from fastapi import UploadFile
import os

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client("s3")

def upload_to_s3(file: UploadFile, folder: str = "documents"):
    key = f"{folder}/{uuid4()}_{file.filename}"
    s3_client.upload_fileobj(file.file, BUCKET_NAME, key)
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
