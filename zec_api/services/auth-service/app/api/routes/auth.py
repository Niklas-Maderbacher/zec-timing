from fastapi import APIRouter, Form, HTTPException, Response, status, Request
import app.crud.auth as crud
from app.database.dependency import AdminUser, TeamLeadUser, ViewerUser
import requests
from app.core.config import settings

USER_URL = settings.USER_SERVICE_URL

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

@router.get("/internal/get-admin-token")
def get_admin_token():
    access_token = crud.get_admin_token()
    return access_token

@router.get("/internal/verify/admin", status_code=status.HTTP_200_OK)
def verify_admin(current_user: AdminUser):
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

@router.get("/internal/verify/teamlead", status_code=status.HTTP_200_OK)
def verify_teamlead(request: Request, response: Response, current_user: TeamLeadUser):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    authorization = request.headers.get("Authorization")
    user_resp = requests.get(f"{USER_URL}/api/users/me", headers={"Authorization": authorization})
    user_resp.raise_for_status()
    user_data = user_resp.json()
    response.headers["X-User-Id"] = current_user["sub"]
    response.headers["X-Team-Id"] = str(user_data.get("team_id"))
    response.headers["X-Role"] = current_user["roles"][0] if current_user["roles"] else ""
    return {
        "active": True,
        "sub": current_user["sub"],
        "username": current_user["username"],
        "team_id": user_data.get("team_id"),
        "email": current_user["email"],
        "roles": current_user["roles"],
    }

@router.get("/internal/verify/viewer", status_code=status.HTTP_200_OK)
def verify_viewer(current_user: ViewerUser):
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
