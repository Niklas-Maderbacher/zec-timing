from fastapi import Depends
from jose import jwt, jwk
from fastapi.security import HTTPBearer
import requests
from app.core.config import settings
from functools import lru_cache
import app.exceptions.exceptions as exception

KC_URL = settings.KEYCLOAK_URL
KC_ADMIN_CLIENT_ID = settings.KEYCLOAK_ADMIN_CLIENT_ID
KC_ADMIN_CLIENT_SECRET = settings.KEYCLOAK_ADMIN_CLIENT_SECRET
KC_CLIENT_ID = settings.KEYCLOAK_CLIENT_ID
KC_CLIENT_SECRET = settings.KEYCLOAK_CLIENT_SECRET
KC_TOKEN_URL = settings.KEYCLOAK_TOKEN_URL
KC_JWKS_URL = settings.KEYCLOAK_JWKS_URL

security = HTTPBearer(auto_error=False) 

@lru_cache(maxsize=1)
def get_cached_jwks():
    response = requests.get(KC_JWKS_URL)
    response.raise_for_status()
    return response.json()

def decode_keycloak_token(credentials = Depends(security)):
    if not credentials:
        raise exception.TokenHeaderRequired()
    token = credentials.credentials
    if not token or len(token.split('.')) != 3:
        raise exception.InvalidTokenFormat()
    jwks = get_cached_jwks()
    headers = jwt.get_unverified_header(token)
    if not headers or 'kid' not in headers:
        raise exception.InvalidTokenHeader()
    key_data = next((k for k in jwks['keys'] if k['kid'] == headers['kid']), None)
    if not key_data:
        raise exception.PublicKeyNotFound()
    try:
        public_key = jwk.construct(key_data).public_key()
    except Exception:
        raise exception.InvalidPublicKey()
    try:
        payload = jwt.decode(
            token, 
            public_key, 
            algorithms=['RS256'], 
            options={"verify_aud": False}  
        )
    except jwt.ExpiredSignatureError:
        raise exception.TokenExpired()
    except jwt.JWTClaimsError:
        raise exception.InvalidClaims()
    return payload

def keycloak_login(username: str, password: str):
    payload = {
        "grant_type": "password",
        "client_id": KC_CLIENT_ID,
        "client_secret": KC_CLIENT_SECRET,
        "username": username,
        "password": password,
        "scope": "openid profile email"
    }
    try:
        response = requests.post(KC_TOKEN_URL, data=payload)
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 401:
            raise exception.InvalidCredentials()
        raise exception.KeycloakUnavailable()
    return response.json()

def keycloak_refresh(refresh_token: str):
    payload = {
        "grant_type": "refresh_token",
        "client_id": KC_CLIENT_ID,
        "client_secret": KC_CLIENT_SECRET,
        "refresh_token": refresh_token,
    }
    try:
        response = requests.post(KC_TOKEN_URL, data=payload)
        response.raise_for_status()
    except requests.HTTPError:
        raise exception.TokenRefreshFailed()
    return response.json()

def extract_roles_from_payload(payload: dict) -> list[str]:
    if not isinstance(payload, dict):
        raise exception.InvalidClaims("Token payload is not a dictionary")
    resource_access = payload.get("resource_access")
    if not isinstance(resource_access, dict):
        return []
    client_access = resource_access.get(KC_ADMIN_CLIENT_ID)
    if not isinstance(client_access, dict):
        return []
    roles = client_access.get("roles")
    if roles is None:
        return []
    if not isinstance(roles, list):
        raise exception.InvalidClaims("Roles claim is not a list")
    return [role for role in roles if isinstance(role, str)]

def get_current_user(payload: dict = Depends(decode_keycloak_token)):
    roles = extract_roles_from_payload(payload)
    if not roles:
        raise exception.InsufficientPermissions()
    return {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "username": payload.get("preferred_username"),
        "roles": roles,
        "token_payload": payload
    }

def get_admin_token():
    try:
        response = requests.post(
            KC_TOKEN_URL,
            data={
                "client_id": KC_ADMIN_CLIENT_ID,
                "client_secret": KC_ADMIN_CLIENT_SECRET,
                "grant_type": "client_credentials",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
        response.raise_for_status()
    except requests.HTTPError:
        raise exception.AuthserviceApiError()
    token_data = response.json()
    if not token_data:
        raise exception.AuthserviceApiError()
    access_token = token_data.get("access_token")
    return access_token
