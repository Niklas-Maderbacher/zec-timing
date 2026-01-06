import requests
from app.core.config import settings
from app.schemas.user import CreateUserKC, UpdateUserKC
from app.models.user import User
from datetime import datetime, timezone
from typing import Optional
from app.database.dependency import SessionDep

KC_USER_URL = settings.KEYCLOAK_USER_URL
KC_CLIENTS_URL = settings.KC_CLIENTS_URL
KC_ADMIN_CLIENT_ID = settings.KC_ADMIN_CLIENT_ID

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
        "emailVerified": True,
        "enabled": True,
    }
    user_data["credentials"] = [{
        "type": "password",
        "value": request.password,
        "temporary": False
    }]
    
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
    db_user = get_user_by_id_db(db=db, user_id=user_id)
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
    db_user = get_user_by_id_db(db=db, user_id=user_id)
    db.delete(db_user)
    db.commit()
    user_url = f"{KC_USER_URL}/{user_id}"
    response = requests.delete(user_url, headers=headers)

def add_roles_to_user(user_id: str, roles: list[str]) -> None:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    client_search_url = f"{KC_CLIENTS_URL}?clientId={KC_ADMIN_CLIENT_ID}"
    client_resp = requests.get(client_search_url, headers=headers)
    client_resp.raise_for_status()
    clients = client_resp.json()
    client_uuid = clients[0]["id"]

    role_representations = []
    for role_name in roles:
        role_url = f"{KC_CLIENTS_URL}/{client_uuid}/roles/{role_name}"
        role_resp = requests.get(role_url, headers=headers)
        role_resp.raise_for_status()
        role_representations.append(role_resp.json())

    role_mapping_url = (
        f"{KC_USER_URL}/{user_id}/role-mappings/clients/{client_uuid}"
    )
    assign_resp = requests.post(
        role_mapping_url,
        json=role_representations,
        headers=headers,
    )
    assign_resp.raise_for_status()

def remove_roles_from_user(user_id: str, roles: list[str]) -> None:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    client_search_url = f"{KC_CLIENTS_URL}?clientId={KC_ADMIN_CLIENT_ID}"
    client_resp = requests.get(client_search_url, headers=headers)
    client_resp.raise_for_status()

    clients = client_resp.json()
    client_uuid = clients[0]["id"]

    role_representations = []
    for role_name in roles:
        role_url = f"{KC_CLIENTS_URL}/{client_uuid}/roles/{role_name}"
        role_resp = requests.get(role_url, headers=headers)
        role_resp.raise_for_status()
        role_representations.append(role_resp.json())

    role_mapping_url = (
        f"{KC_USER_URL}/{user_id}/role-mappings/clients/{client_uuid}"
    )
    remove_resp = requests.delete(
        role_mapping_url,
        json=role_representations,
        headers=headers,
    )
    remove_resp.raise_for_status()

def get_user_by_id_db(db: SessionDep, user_id: str):
    db_user = db.query(User).filter(User.kc_id == user_id).first()
    return db_user

def get_admin_token() -> str:
    access_token = requests.get(f"{settings.AUTH_SERVICE_URL}/api/auth/internal/get-admin-token").json()
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
