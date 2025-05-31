import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_secret():
    secret_name = os.getenv("AWS_SECRET_NAME", "cashloan/user_service/config2")
    region_name = os.getenv("AWS_REGION", "eu-central-1")

    client = boto3.client("secretsmanager", region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)

# Load secrets from AWS
aws_secret = get_secret()

class Settings:
    DB_HOST: str = aws_secret.get("DB_HOST")
    DB_PORT: str = aws_secret.get("DB_PORT", "5432")
    DB_USER: str = aws_secret.get("DB_USER")
    DB_PASSWORD: str = aws_secret.get("DB_PASSWORD")
    DB_NAME: str = aws_secret.get("DB_NAME")
    SECRET_KEY: str = aws_secret.get("SECRET_KEY", "fallback-key")

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
