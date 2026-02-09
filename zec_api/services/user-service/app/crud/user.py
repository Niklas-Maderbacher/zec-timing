import requests
from app.core.config import settings
from app.schemas.user import CreateUserKC, UpdateUserKC
from app.models.user import User
from datetime import datetime, timezone
from typing import Optional
from app.database.dependency import SessionDep
from app.exceptions.exceptions import (
    AuthenticationFailed,
    EntityDoesNotExistError,
    InvalidOperationError,
    ServiceError,
    EntityAlreadyExistsError,
)

KC_USER_URL = settings.KEYCLOAK_USER_URL
KC_CLIENTS_URL = settings.KC_CLIENTS_URL
KC_CLIENT_ID = settings.KC_CLIENT_ID

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
    if response.status_code == 409:
        raise EntityAlreadyExistsError("User already exists")
    if response.status_code in (401, 403):
        raise AuthenticationFailed("Authentication failed")
    if response.status_code != 201:
        raise ServiceError("Keycloak error")
    kc_user = get_user_by_username(request.username)
    if not kc_user:
        raise ServiceError("User created but not retrievable")
    db_user = User(
        username=request.username,
        kc_id=kc_user["id"],
        created_at=datetime.now(timezone.utc),
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
    user_data = {}
    if request.username is not None:
        user_data["username"] = request.username
    if request.password is not None:
        user_data["credentials"] = [{
            "type": "password",
            "value": request.password,
            "temporary": False
        }]
    response = requests.put(f"{KC_USER_URL}/{user_id}", json=user_data, headers=headers)
    if response.status_code == 404:
        raise EntityDoesNotExistError("User does not exist")
    if response.status_code in (401, 403):
        raise AuthenticationFailed("Authentication failed")
    if response.status_code != 204:
        raise InvalidOperationError("Failed to update user")
    db_user = get_user_by_id_db(db=db, user_id=user_id)
    if not db_user:
        raise EntityDoesNotExistError("User not found in database")
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
    if not db_user:
        raise EntityDoesNotExistError("User not found")
    response = requests.delete(f"{KC_USER_URL}/{user_id}",headers=headers)
    if response.status_code == 404:
        raise EntityDoesNotExistError("User does not exist in Keycloak")
    if response.status_code in (401, 403):
        raise AuthenticationFailed("Authentication failed")
    if response.status_code != 204:
        raise ServiceError(response.text)
    db.delete(db_user)
    db.commit()   
    return db_user

def add_roles_to_user(user_id: str, roles: list[str]) -> None:
    get_user_by_id(user_id)
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    client_resp = requests.get(f"{KC_CLIENTS_URL}?clientId={KC_CLIENT_ID}", headers=headers)
    if client_resp.status_code != 200:
        raise ServiceError("Unable to resolve client")
    clients = client_resp.json()
    client_uuid = clients[0]["id"]

    role_representations = []
    for role_name in roles:
        role_resp = requests.get(f"{KC_CLIENTS_URL}/{client_uuid}/roles/{role_name}", headers=headers)
        if role_resp.status_code == 404:
            raise EntityDoesNotExistError(f"Role {role_name} does not exist")
        if role_resp.status_code != 200:
            raise ServiceError("Failed to assign Roles")
        role_representations.append(role_resp.json())

    assign_resp = requests.post(
        f"{KC_USER_URL}/{user_id}/role-mappings/clients/{client_uuid}",
        json=role_representations,
        headers=headers,
    )
    if assign_resp.status_code != 204:
        raise InvalidOperationError("Failed to assign roles: {roles}")

def remove_roles_from_user(user_id: str, roles: list[str]) -> None:
    get_user_by_id(user_id)
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    client_resp = requests.get(f"{KC_CLIENTS_URL}?clientId={KC_CLIENT_ID}", headers=headers)
    if client_resp.status_code != 200:
        raise ServiceError("Unable to resolve client")
    client_uuid = client_resp.json()[0]["id"]
    role_representations = []
    for role_name in roles:
        role_resp = requests.get(f"{KC_CLIENTS_URL}/{client_uuid}/roles/{role_name}", headers=headers)
        if role_resp.status_code == 404:
            raise EntityDoesNotExistError(f"Role {role_name} does not exist")
        if role_resp.status_code != 200:
            raise ServiceError(role_resp.text)
        role_representations.append(role_resp.json())

    remove_resp = requests.delete(
        f"{KC_USER_URL}/{user_id}/role-mappings/clients/{client_uuid}",
        json=role_representations,
        headers=headers,
    )
    if remove_resp.status_code != 204:
        raise InvalidOperationError("Failed to remove roles: {roles}")

def get_user_by_id_db(db: SessionDep, user_id: str):
    db_user = db.query(User).filter(User.kc_id == user_id).first()
    if not db_user:
        raise EntityDoesNotExistError(f"No user for id: {user_id}")
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
    response = requests.get(f"{KC_USER_URL}?exact=true&username={username}", headers=headers)
    if response.status_code in (401, 403):
        raise AuthenticationFailed("Authentication failed")
    if response.status_code == 404:
        raise EntityDoesNotExistError(f"No user for id: {username}")
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
    response = requests.get(f"{KC_USER_URL}/{user_id}", headers=headers)
    if response.status_code in (401, 403):
        raise AuthenticationFailed("Authentication failed")
    if response.status_code == 404:
        raise EntityDoesNotExistError(f"No user for id: {user_id}")
    user = response.json()
    return {
        "id": user["id"],
        "username": user["username"],
    }

def get_all_users() -> list[dict]:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    response = requests.get(KC_USER_URL, headers=headers)
    if response.status_code in (401, 403):
        raise AuthenticationFailed("Authentication failed")
    if response.status_code != 200:
        raise ServiceError("Failed to fetch users from Keycloak")
    
    users = response.json()
    
    client_resp = requests.get(f"{KC_CLIENTS_URL}?clientId={KC_CLIENT_ID}", headers=headers)
    if client_resp.status_code != 200:
        raise ServiceError("Unable to resolve client")
    client_uuid = client_resp.json()[0]["id"]
    
    enriched_users = []
    for user in users:
        user_id = user.get("id")
        user_data = {
            "id": user_id,
            "username": user.get("username"),
            "email": user.get("email"),
            "firstName": user.get("firstName"),
            "lastName": user.get("lastName"),
            "enabled": user.get("enabled", False),
            "emailVerified": user.get("emailVerified", False),
            "roles": []
        }

        try:
            roles_resp = requests.get(
                f"{KC_USER_URL}/{user_id}/role-mappings/clients/{client_uuid}",
                headers=headers
            )
            if roles_resp.status_code == 200:
                roles = roles_resp.json()
                user_data["roles"] = [role["name"] for role in roles]
        except Exception as e:
            print(f"Error getting roles for user {user_id}: {e}")
            user_data["roles"] = []
        
        enriched_users.append(user_data)
    
    return enriched_users
