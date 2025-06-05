from fastapi import FastAPI
from app.api.v1.endpoints import disburse
from app.db.models.disbursement import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(disburse.router, prefix="/api/v1/disbursements", tags=["Disbursements"])

@app.get("/")
def root():
    return {"message": "Disbursement service is running"}
