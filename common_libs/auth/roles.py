from fastapi import Depends, HTTPException, status
from common_libs.auth.dependencies import get_current_user

ALLOWED_ROLES = ["admin", "agent", "customer"]

def require_role(required_role: str):
    def role_dependency(current_user=Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role.capitalize()}s only"
            )
        return current_user
    return role_dependency

def require_roles(*roles: str):
    def roles_dependency(current_user=Depends(get_current_user)):
        if current_user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access requires one of the following roles: {', '.join(roles)}"
            )
        return current_user
    return roles_dependency
