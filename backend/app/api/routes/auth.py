from fastapi import APIRouter, Form
from app.services.keycloak import keycloak_login, keycloak_refresh
from app.database.dependency import SessionDep

router = APIRouter()

@router.post("/login")
def login(db: SessionDep, username: str = Form(...),password: str = Form(...)):
    token_data = keycloak_login(username, password)
    return token_data

@router.post("/refresh")
def refresh(refresh_token: str = Form(...)):
    token_data = keycloak_refresh(refresh_token)
    return token_data