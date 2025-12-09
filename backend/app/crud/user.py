import requests
from app.core.config import settings
from app.schemas.user import CreateUserKC
from app.models.user import User
from datetime import datetime, timezone
from typing import Optional
from app.database.dependency import SessionDep

#temporary constants for Keycloak admin client
KC_TOKEN_URL = settings.KEYCLOAK_TOKEN_URL
KC_USER_URL = settings.KEYCLOAK_USER_URL
KC_CLIENT_ID = "admin-cli"
KC_CLIENT_SECRET = "iLNBNaJwfV2paV8jCtneGF2tM3IKH4Fj"

def get_token():
    response = requests.post(
        KC_TOKEN_URL,
        data={
            "client_id": KC_CLIENT_ID,
            "client_secret": KC_CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    token_data = response.json()
    access_token = token_data.get("access_token")
    return access_token

def get_user_by_username(username: str) -> Optional[dict]:
    access_token = get_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    search_url = f"{KC_USER_URL}?exact=true&username={username}"
    response = requests.get(search_url, headers=headers)
    
    users = response.json()
    return users[0]

def create_user(db: SessionDep, request: CreateUserKC):
    acces_token = get_token()
    bearer_token = f"Bearer {acces_token}"
    placeholder_email = f"{request.username}@placeholder.local"

    user_data = {
        "username": request.username,
        #needed due to a bug in Keycloak
        "firstName": "placeholder",
        "lastName": "placeholder",
        "email": placeholder_email,
        "emailVerified": request.emailVerified,
        "enabled": request.enabled,
    }

    if request.credentials:
        user_data["credentials"] = [cred.dict() for cred in request.credentials]

    headers = {
        "Authorization": bearer_token,
        "Content-Type": "application/json",
    }

    response = requests.post(KC_USER_URL, json=user_data, headers=headers)
    if response.status_code == 201:
        kcuser = get_user_by_username(request.username)
        if kcuser:
            kc_id = kcuser.get("id")
            db_user = User(
                username=request.username,
                kc_id=kc_id,
                created_at=datetime.now(timezone.utc)
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
    