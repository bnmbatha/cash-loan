from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int = 5432
    SECRET_KEY: str
    aws_region: str
    aws_secret_name: str
    user_service_url: str

    class Config:
        extra = "allow"
        env_file = ".env"

settings = Settings()
