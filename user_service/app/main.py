from fastapi import FastAPI
from app.api.v1 import user_routes
from app.db.models.user import Base
from app.db.session import engine

# Auto-create tables
print("🔧 Creating tables if they don't exist...")
Base.metadata.create_all(bind=engine)
print("✅ Tables ready.")

app = FastAPI()
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "User service is running"}

