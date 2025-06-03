# Import AWS SDK for Python to interact with AWS Secrets Manager
import boto3

# Standard libraries for parsing JSON and accessing environment variables
import json
import os

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

#  Function to retrieve secrets from AWS Secrets Manager
def get_secret():
    # Retrieve the secret name and AWS region from environment variables (with defaults)
    secret_name = os.getenv("AWS_SECRET_NAME", "cashloan/user_service/config2")
    region_name = os.getenv("AWS_REGION", "eu-central-1")

    # Create a Secrets Manager client
    client = boto3.client("secretsmanager", region_name=region_name)

    # Fetch the secret value using the secret name
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)

    # Extract and parse the secret string as JSON
    secret = get_secret_value_response["SecretString"]
    return json.loads(secret)

#  Load secrets from AWS Secrets Manager when the module is imported
aws_secret = get_secret()

#  Configuration class for storing application settings
class Settings:
    # Database configuration values
    DB_HOST: str = aws_secret.get("DB_HOST")
    DB_PORT: str = aws_secret.get("DB_PORT", "5432")
    DB_USER: str = aws_secret.get("DB_USER")
    DB_PASSWORD: str = aws_secret.get("DB_PASSWORD")
    DB_NAME: str = aws_secret.get("DB_NAME")

    # Secret key used for JWT and other cryptographic functions
    SECRET_KEY: str = aws_secret.get("SECRET_KEY", "fallback-key")

    #  Construct the full database connection URL
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

#  Instantiate a global settings object to be reused across the app
settings = Settings()
