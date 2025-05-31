from fastapi import FastAPI
from app.api.v1 import user_routes

app = FastAPI()

app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Users"])
