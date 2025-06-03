# FastAPI framework import for building the web application
from fastapi import FastAPI

# Import API route definitions from the user module
from app.api.v1 import user_routes

# Import SQLAlchemy base class and database engine
from app.db.models.user import Base
from app.db.session import engine

# 🛠 Automatically create database tables based on SQLAlchemy models
# This is useful in development; in production, use Alembic for migrations
print("🔧 Creating tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("✅ Tables ready.")

# Initialize the FastAPI app instance
app = FastAPI()

# Include user-related routes with a common prefix and tag for API docs
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Users"])

# Simple root endpoint to confirm the service is running
@app.get("/")
def root():
    return {"message": "User service is running"}
