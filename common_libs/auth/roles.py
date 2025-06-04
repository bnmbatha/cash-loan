from fastapi import Depends, HTTPException, status
from common_libs.auth.dependencies import get_current_user

def require_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: {required_role} role required"
            )
        return user
    return role_checker

def require_roles(*roles: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: one of {roles} roles required"
            )
        return user
    return role_checker
