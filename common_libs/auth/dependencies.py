from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from common_libs.auth.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # tokenUrl is required by FastAPI

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")  # ✅ extract role from JWT payload

        if not user_id or not role:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"user_id": user_id, "role": role}
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
