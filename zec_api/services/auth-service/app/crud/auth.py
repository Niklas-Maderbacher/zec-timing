from fastapi import Depends
from jose import jwt, jwk
from fastapi.security import HTTPBearer
import requests
from app.core.config import settings

KC_URL = settings.KEYCLOAK_URL
KC_ADMIN_CLIENT_ID = settings.KEYCLOAK_ADMIN_CLIENT_ID
KC_ADMIN_CLIENT_SECRET = settings.KEYCLOAK_ADMIN_CLIENT_SECRET
KC_CLIENT_ID = settings.KEYCLOAK_CLIENT_ID
KC_CLIENT_SECRET = settings.KEYCLOAK_CLIENT_SECRET
KC_TOKEN_URL = settings.KEYCLOAK_TOKEN_URL
KC_JWKS_URL = settings.KEYCLOAK_JWKS_URL

security = HTTPBearer(auto_error=False) 

def get_keycloak_public_key():
    response = requests.get(KC_JWKS_URL)
    return response.json()

def decode_keycloak_token(credentials = Depends(security)):
    if not credentials:
        pass
        #throw authorization header required
    
    token = credentials.credentials
    if not token or len(token.split('.')) != 3:
        # throw invalid token format
        pass
    
    jwks = get_keycloak_public_key()
    headers = jwt.get_unverified_header(token)

    if not headers or 'kid' not in headers:
        # throw invalid token header
        pass

    key_data = next((k for k in jwks['keys'] if k['kid'] == headers['kid']), None)
    if not key_data:
        # throw public key not found
        pass

    try:
        public_key = jwk.construct(key_data).public_key()
    except Exception:
        # throw invalid public key
        pass

    try:
        payload = jwt.decode(
            token, 
            public_key, 
            algorithms=['RS256'], 
            options={"verify_aud": False}  
        )
    except jwt.ExpiredSignatureError:
        # throw token expired
        pass
    except jwt.JWTClaimsError:
        # throw invalid claims
        pass 
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

    response = requests.post(KC_TOKEN_URL, data=payload)
    return response.json()

def keycloak_refresh(refresh_token: str):
    payload = {
        "grant_type": "refresh_token",
        "client_id": KC_CLIENT_ID,
        "client_secret": KC_CLIENT_SECRET,
        "refresh_token": refresh_token,
    }

    response = requests.post(KC_TOKEN_URL, data=payload)
    return response.json()

def extract_roles_from_payload(payload: dict) -> list[str]:
    roles = []   
    if "resource_access" in payload and KC_CLIENT_ID in payload["resource_access"]:
        client_roles = payload["resource_access"][KC_CLIENT_ID].get("roles", [])
        roles.extend(client_roles)
    return roles

def get_current_user(payload: dict = Depends(decode_keycloak_token)):
    roles = extract_roles_from_payload(payload)
    return {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
        "username": payload.get("preferred_username"),
        "roles": roles,
        "token_payload": payload
    }

def get_admin_token():
    response = requests.post(
        KC_TOKEN_URL,
        data={
            "client_id": KC_ADMIN_CLIENT_ID,
            "client_secret": KC_ADMIN_CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    token_data = response.json()
    access_token = token_data.get("access_token")
    return access_token

