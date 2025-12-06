from fastapi import HTTPException, status, Depends
from jose import jwt, jwk
from fastapi.security import HTTPBearer
import requests
from app.core.config import settings

KC_URL = settings.KEYCLOAK_URL
KC_CLIENT_ID = settings.KEYCLOAK_CLIENT_ID
KC_CLIENT_SECRET = settings.KEYCLOAK_CLIENT_SECRET
KC_TOKEN_URL = settings.KEYCLOAK_TOKEN_URL
KC_JWKS_URL = settings.KEYCLOAK_JWKS_URL

security = HTTPBearer(auto_error=False) 

def get_keycloak_public_key():
    response = requests.get(KC_JWKS_URL)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Cannot fetch Keycloak public keys"
        )
    return response.json()

def decode_keycloak_token(credentials = Depends(security)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = credentials.credentials
    if token.startswith("Bearer "):
        token = token[7:]
    
    if not token or len(token.split('.')) != 3:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    
    jwks = get_keycloak_public_key()
    headers = jwt.get_unverified_header(token)

    if not headers or 'kid' not in headers:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token header"
        )

    key_data = next((k for k in jwks['keys'] if k['kid'] == headers['kid']), None)
    if not key_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Public key not found"
        )

    try:
        public_key = jwk.construct(key_data).public_key()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid public key"
        )

    try:
        payload = jwt.decode(
            token, 
            public_key, 
            algorithms=['RS256'], 
            options={"verify_aud": False}  
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token expired"
        )
    except jwt.JWTClaimsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid claims"
        )
            
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
    
    if response.status_code != 200:
        print(f"Keycloak login failed with status: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Keycloak error response: {error_data}")
        except Exception:
            print(f"Raw response: {response.text}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return response.json()

def keycloak_refresh(refresh_token: str):
    payload = {
        "grant_type": "refresh_token",
        "client_id": KC_CLIENT_ID,
        "client_secret": KC_CLIENT_SECRET,
        "refresh_token": refresh_token,
    }

    response = requests.post(KC_TOKEN_URL, data=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

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
