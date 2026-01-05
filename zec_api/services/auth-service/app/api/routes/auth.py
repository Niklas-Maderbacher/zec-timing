from fastapi import APIRouter, Form, HTTPException, status
import app.crud.auth as crud
from fastapi import Depends

router = APIRouter()

@router.post("/login")
def login(username: str = Form(...),password: str = Form(...)):
    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password are required")
    token_data = crud.keycloak_login(username, password)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Authentication service is unavailable")
    return token_data

@router.post("/refresh")
def refresh(refresh_token: str = Form(...)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token is required")
    token_data = crud.keycloak_refresh(refresh_token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Failed to refresh token")
    return token_data

@router.get("/get-admin-token")
def get_admin_token():
    access_token = crud.get_admin_token()
    return access_token

@router.get("/verify", status_code=status.HTTP_200_OK)
def verify_token(current_user: dict = Depends(crud.get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )

    return {
        "active": True,
        "sub": current_user["sub"],
        "username": current_user["username"],
        "email": current_user["email"],
        "roles": current_user["roles"],
    }
