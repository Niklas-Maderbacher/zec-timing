import requests
import time
import jwt
from app.core.config import settings
from app.schemas.user import CreateUserKC, UpdateUserKC, UserResponseKC
from app.models.user import User
from datetime import datetime, timezone
from app.database.dependency import SessionDep
from app.exceptions.exceptions import (
    AuthenticationFailed,
    EntityDoesNotExistError,
    InvalidOperationError,
    ServiceError,
    EntityAlreadyExistsError,
    InvalidTokenError,
)

KC_USER_URL = settings.KEYCLOAK_USER_URL
KC_CLIENTS_URL = settings.KC_CLIENTS_URL
KC_CLIENT_ID = settings.KC_CLIENT_ID
TEAM_URL = settings.TEAM_SERVICE_URL

def _validate_team(team_id: int):
    resp = requests.get(f"{TEAM_URL}/api/teams/{team_id}", params={"team_id": team_id})
    if resp.status_code == 404:
        raise EntityDoesNotExistError(f"Team {team_id} does not exist")
    if resp.status_code in (401, 403):
        raise AuthenticationFailed(f"Unauthorized to fetch team {team_id}")
    if resp.status_code != 200:
        raise ServiceError(f"Failed to fetch team {team_id}: {resp.text}")

def _get_kc_user_by_username(username: str) -> dict:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"{KC_USER_URL}?exact=true&username={username}",
        headers=headers
    )
    if response.status_code in (401, 403):
        raise AuthenticationFailed("Authentication failed")
    if response.status_code == 404:
        raise EntityDoesNotExistError(f"No user for username: {username}")
    users = response.json()
    if not users:
        raise EntityDoesNotExistError(f"No user for username: {username}")
    return users[0]

def _get_kc_user_by_id(user_id: str) -> dict:
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
    return response.json()

def _build_user_response(db: SessionDep, kc_user: dict, client_uuid: str | None = None,) -> UserResponseKC:
    db_user = get_user_by_id_db(db, kc_user["id"])
    team_name = None
    if db_user.team_id is not None:
        try:
            team_resp = requests.get(f"{TEAM_URL}/api/teams/{db_user.team_id}")
            if team_resp.status_code == 200:
                team_name = team_resp.json().get("name")
        except Exception:
            pass
    roles = []
    if client_uuid:
        access_token = get_admin_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        try:
            roles_resp = requests.get(
                f"{KC_USER_URL}/{kc_user['id']}/role-mappings/clients/{client_uuid}",
                headers=headers
            )
            if roles_resp.status_code == 200:
                roles = [r["name"] for r in roles_resp.json()]
        except Exception:
            pass
    return UserResponseKC(
        id=db_user.id,
        kc_id=kc_user["id"],
        username=db_user.username,
        team_id=db_user.team_id,
        team_name=team_name,
        roles=roles,
    )

def get_admin_token() -> str:
    url = f"{settings.AUTH_SERVICE_URL}/api/auth/internal/get-admin-token"
    last_exc = None
    last_resp = None
    for attempt in range(1, 11):
        try:
            resp = requests.get(url, timeout=5)
            last_resp = resp
        except requests.RequestException as e:
            last_exc = e
            time.sleep(0.5 * attempt)
            continue
        if resp.status_code != 200:
            last_exc = Exception(f"Auth service returned status {resp.status_code}")
            time.sleep(0.5 * attempt)
            continue
        try:
            data = resp.json()
        except ValueError:
            raise ServiceError(f"Invalid JSON from auth service: {resp.text}")
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            token = data.get("access_token") or data.get("token") or data.get("accessToken")
            if token:
                return token
            raise ServiceError(f"Auth service JSON missing token field: {data}")
        raise ServiceError(f"Unexpected auth service response: {data}")
    if last_exc:
        raise ServiceError(f"Failed to obtain admin token: {last_exc}")
    if last_resp is not None:
        raise ServiceError(f"Failed to obtain admin token, last response: {last_resp.text}")
    raise ServiceError("Failed to obtain admin token: unknown error")

def create_user(db: SessionDep, request: CreateUserKC) -> UserResponseKC:
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
        "credentials": [{
            "type": "password",
            "value": request.password,
            "temporary": False
        }]
    }
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
    kc_user = _get_kc_user_by_username(request.username)
    db_user = User(
        username=request.username,
        kc_id=kc_user["id"],
        created_at=datetime.now(timezone.utc),
    )
    if request.team_id is not None:
        _validate_team(request.team_id)
        db_user.team_id = request.team_id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return _build_user_response(db, kc_user)
    
def update_user(db: SessionDep, user_id: str, request: UpdateUserKC) -> UserResponseKC:
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
    if request.username is not None:
        db_user.username = request.username
    if request.team_id is not None:
        _validate_team(request.team_id)
        db_user.team_id = request.team_id
    db.commit()
    db.refresh(db_user)
    kc_user = _get_kc_user_by_id(user_id)
    return _build_user_response(db, kc_user)

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
    _get_kc_user_by_id(user_id)
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
        raise InvalidOperationError(f"Failed to assign roles: {roles}")

def remove_roles_from_user(user_id: str, roles: list[str]) -> None:
    _get_kc_user_by_id(user_id)
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
        raise InvalidOperationError(f"Failed to remove roles: {roles}")

def get_user_by_id_db(db: SessionDep, user_id: str):
    db_user = db.query(User).filter(User.kc_id == user_id).first()
    if not db_user:
        raise EntityDoesNotExistError(f"No user for id: {user_id}")
    return db_user

def get_user_by_username(db: SessionDep, username: str) -> UserResponseKC:
    access_token = get_admin_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"{KC_USER_URL}?exact=true&username={username}",
        headers=headers
    )
    if response.status_code in (401, 403):
        raise AuthenticationFailed("Authentication failed")
    if response.status_code == 404:
        raise EntityDoesNotExistError(f"No user for username: {username}")
    users = response.json()
    if not users:
        raise EntityDoesNotExistError(f"No user for username: {username}")
    kc_user = users[0]
    client_resp = requests.get(f"{KC_CLIENTS_URL}?clientId={KC_CLIENT_ID}", headers=headers)
    if client_resp.status_code != 200:
        raise ServiceError("Unable to resolve client")
    client_uuid = client_resp.json()[0]["id"]
    return _build_user_response(db, kc_user, client_uuid)

def get_user_by_id(db: SessionDep, user_id: str) -> UserResponseKC:
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
    kc_user = response.json()
    client_resp = requests.get(f"{KC_CLIENTS_URL}?clientId={KC_CLIENT_ID}", headers=headers)
    if client_resp.status_code != 200:
        raise ServiceError("Unable to resolve client")
    client_uuid = client_resp.json()[0]["id"]
    return _build_user_response(db, kc_user, client_uuid)

def get_all_users(db: SessionDep) -> list[UserResponseKC]:
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
    kc_users = response.json()

    client_resp = requests.get(f"{KC_CLIENTS_URL}?clientId={KC_CLIENT_ID}", headers=headers)
    if client_resp.status_code != 200:
        raise ServiceError("Unable to resolve client")
    client_uuid = client_resp.json()[0]["id"]
    return [_build_user_response(db, kc_user, client_uuid) for kc_user in kc_users]

def get_current_user(db: SessionDep, authorization: str) -> UserResponseKC:
    token = authorization.split(" ")[1]
    decoded = jwt.decode(token, options={"verify_signature": False})
    username = decoded.get("preferred_username") or decoded.get("sub")
    if not username:
        raise InvalidTokenError("Username not found in token")
    user = get_user_by_username(db=db, username=username)
    return user