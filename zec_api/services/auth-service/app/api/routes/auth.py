from fastapi import APIRouter, Form, HTTPException, status
from app.database.dependency import SessionDep
from app.crud.auth import keycloak_login, keycloak_refresh

router = APIRouter()

@router.post("/login")
def login(db: SessionDep, username: str = Form(...),password: str = Form(...)):
    try:
        if not username or not password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password are required")
        token_data = keycloak_login(username, password)
        if not token_data:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Authentication service is unavailable")
        return token_data
    except HTTPException as http_exc:
        raise http_exc
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Authentication failed") 

@router.post("/refresh")
def refresh(refresh_token: str = Form(...)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token is required")
    token_data = keycloak_refresh(refresh_token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Failed to refresh token")
    return token_data