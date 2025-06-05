# common_libs/disbursement.py
import requests
import os

DISBURSEMENT_URL = os.getenv("DISBURSEMENT_SERVICE_URL", "http://disbursement-service:8000")

def disburse_funds(user_id: int, loan_id: int, amount: float):
    payload = {
        "user_id": user_id,
        "loan_id": loan_id,
        "amount": amount
    }
    try:
        response = requests.post(f"{DISBURSEMENT_URL}/disburse/", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise RuntimeError(f"Disbursement failed: {str(e)}")
