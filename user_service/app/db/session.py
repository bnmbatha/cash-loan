# Import SQLAlchemy engine and session-related tools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Import settings containing database credentials and connection info
from app.core.config import settings

#  Construct the full database connection URL using credentials from AWS Secrets Manager
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

#  Create a SQLAlchemy engine which manages the connection pool to the PostgreSQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 🛠️ Create a configurable session factory bound to the engine
# - autocommit=False: changes must be explicitly committed
# - autoflush=False: changes are not automatically flushed to DB until committed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Dependency function to get a database session
# - Used in FastAPI routes/services via `Depends(get_db)`
# - Ensures proper session management (open → use → close)
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db  # provide the session for use in API route
    finally:
        db.close()  # ensure the session is closed after request is handled
