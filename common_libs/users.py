import requests
import os

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user-service:8000")

def get_user_email(user_id: int) -> str:
    try:
        resp = requests.get(f"{USER_SERVICE_URL}/api/v1/users/{user_id}")
        resp.raise_for_status()
        return resp.json()["email"]
    except Exception as e:
        print(f"Failed to fetch user email: {e}")
        return "unknown@example.com"
