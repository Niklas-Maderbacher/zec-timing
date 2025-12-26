import requests
from app.core.config import settings
from app.schemas.user import CreateUserKC, UpdateUserKC
from app.models.user import User
from datetime import datetime, timezone
from typing import Optional
from app.database.dependency import SessionDep

KC_USER_URL = settings.KEYCLOAK_USER_URL

def get_admin_token() -> str:
    access_token = requests.get(f"{settings.AUTH_SERVICE_URL}/api/auth/get-admin-token").json()
    return access_token

def get_user_by_username(username: str) -> Optional[dict]:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    search_url = f"{KC_USER_URL}?exact=true&username={username}"
    response = requests.get(search_url, headers=headers)
    users = response.json()
    user = users[0]
    return {
        "id": user["id"],
        "username": user["username"],
    }

def get_user_by_id(user_id: str) -> dict:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    user_url = f"{KC_USER_URL}/{user_id}"
    response = requests.get(user_url, headers=headers)
    user = response.json()
    return {
        "id": user["id"],
        "username": user["username"],
    }


def create_user(db: SessionDep, request: CreateUserKC):
    access_token = get_admin_token()
    bearer_token = f"Bearer {access_token}"
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
    
def update_user(db: SessionDep, user_id: str, request: UpdateUserKC) -> Optional[dict]:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    update_url = f"{KC_USER_URL}/{user_id}"
    user_data = {}
    if request.username is not None:
        user_data["username"] = request.username
    if request.password is not None:
        user_data["credentials"] = [{
            "type": "password",
            "value": request.password,
            "temporary": False
        }]
    response = requests.put(update_url, json=user_data, headers=headers)
    #make own function
    db_user = db.query(User).filter(User.kc_id == user_id).first()
    if request.username is not None:
        db_user.username = request.username
        db.commit()
        db.refresh(db_user)
    return {"id": db_user.kc_id, "username": db_user.username}

def delete_user(db: SessionDep, user_id: str) -> None:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    #make own function
    db_user = db.query(User).filter(User.kc_id == user_id).first()
    db.delete(db_user)
    db.commit()
    user_url = f"{KC_USER_URL}/{user_id}"
    response = requests.delete(user_url, headers=headers)
