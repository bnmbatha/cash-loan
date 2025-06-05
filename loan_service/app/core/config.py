# Import the BaseSettings class from pydantic_settings.
# This is used to load environment variables into a Python class.
from pydantic_settings import BaseSettings

# Define a configuration class that reads environment variables
class Settings(BaseSettings):
    # Database connection settings
    DB_HOST: str               # Hostname or IP of the database server
    DB_USER: str               # Username for the database
    DB_PASSWORD: str           # Password for the database user
    DB_NAME: str               # Name of the database
    DB_PORT: int = 5432        # Port number for PostgreSQL (default is 5432)

    # Secret key used for things like JWT signing
    SECRET_KEY: str

    # AWS-related configurations
    aws_region: str            # AWS region (e.g., eu-central-1)
    aws_secret_name: str       # Name of the AWS Secrets Manager secret

    # Internal service URL
    user_service_url: str      # URL of the user service for inter-service communication

    # Configuration class to specify how to load settings
    class Config:
        # Allow loading additional environment variables not defined here
        extra = "allow"
        # Specify that environment variables should be read from a file named `.env`
        env_file = ".env"

# Create an instance of the Settings class to load all environment variables
settings = Settings()

