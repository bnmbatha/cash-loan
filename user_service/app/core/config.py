import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_secret():
    secret_name = os.getenv("AWS_SECRET_NAME", "cashloan/user_service/config")
    region_name = os.getenv("AWS_REGION", "eu-central-1")

    client = boto3.client("secretsmanager", region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)

# Load secrets
aws_secret = get_secret()

class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "yourpassword")
    DB_NAME: str = os.getenv("DB_NAME", "cash_loans_db")
    SECRET_KEY: str = aws_secret.get("SECRET_KEY", "fallback-key")

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
