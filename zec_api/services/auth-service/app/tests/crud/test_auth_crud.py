import pytest
import requests
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt
from app.crud import auth as crud
import app.exceptions.exceptions as exc

def test_extract_roles_success():
    payload = {
        "resource_access": {
            "admin-client": {
                "roles": ["admin", "user"]
            }
        }
    }
    roles = crud.extract_roles_from_payload(payload)
    assert roles == ["admin", "user"]

def test_extract_roles_empty():
    roles = crud.extract_roles_from_payload({})
    assert roles == []

def test_extract_roles_invalid_type():
    roles = crud.extract_roles_from_payload({"resource_access": "invalid"})
    assert roles == []

def test_extract_roles_payload_not_dict():
    with pytest.raises(exc.InvalidClaims):
        crud.extract_roles_from_payload("invalid")  

def test_extract_roles_roles_not_list():
    payload = {
        "resource_access": {
            "admin-client": {
                "roles": "admin"
            }
        }
    }
    with pytest.raises(exc.InvalidClaims):
        crud.extract_roles_from_payload(payload)

def test_extract_roles_filters_non_strings():
    payload = {
        "resource_access": {
            "admin-client": {
                "roles": ["admin", 123, None]
            }
        }
    }
    roles = crud.extract_roles_from_payload(payload)
    assert roles == ["admin"]

def test_decode_token_success(mock_jwks):
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="header.payload.signature",
    )
    payload = crud.decode_keycloak_token(credentials)
    assert payload["preferred_username"] == "test"
    assert payload["email"] == "test@test.com"

def test_decode_token_missing_header():
    with pytest.raises(exc.TokenHeaderRequired):
        crud.decode_keycloak_token(None)

def test_decode_token_invalid_format():
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )
    with pytest.raises(exc.InvalidTokenFormat):
        crud.decode_keycloak_token(credentials)

def test_decode_token_missing_kid(mock_jwks, mocker):
    mocker.patch(
        "app.crud.auth.jwt.get_unverified_header",
        return_value={},
    )
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="a.b.c",
    )
    with pytest.raises(exc.InvalidTokenHeader):
        crud.decode_keycloak_token(credentials)


def test_decode_token_public_key_not_found(mock_jwks, mocker):
    mocker.patch(
        "app.crud.auth.jwt.get_unverified_header",
        return_value={"kid": "missing"},
    )
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="a.b.c",
    )
    with pytest.raises(exc.PublicKeyNotFound):
        crud.decode_keycloak_token(credentials)

def test_decode_token_invalid_public_key(mock_jwks, mocker):
    mocker.patch(
        "app.crud.auth.jwk.construct",
        side_effect=Exception("bad key"),
    )
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="a.b.c",
    )
    with pytest.raises(exc.InvalidPublicKey):
        crud.decode_keycloak_token(credentials)

def test_decode_token_expired(mock_jwks, mocker):
    mocker.patch(
        "app.crud.auth.jwt.decode",
        side_effect=jwt.ExpiredSignatureError(),
    )
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="a.b.c",
    )
    with pytest.raises(exc.TokenExpired):
        crud.decode_keycloak_token(credentials)

def test_decode_token_invalid_claims(mock_jwks, mocker):
    mocker.patch(
        "app.crud.auth.jwt.decode",
        side_effect=jwt.JWTClaimsError(),
    )
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="a.b.c",
    )
    with pytest.raises(exc.InvalidClaims):
        crud.decode_keycloak_token(credentials)

def test_get_current_user_success(mock_jwks):
    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="a.b.c",
    )
    payload = crud.decode_keycloak_token(credentials)
    user = crud.get_current_user(payload)
    assert user["username"] == "test"
    assert "admin" in user["roles"]

def test_get_current_user_insufficient_roles():
    payload = {
        "sub": "123",
        "email": "test@test.com",
        "preferred_username": "test",
        "resource_access": {},
    }
    with pytest.raises(exc.InsufficientPermissions):
        crud.get_current_user(payload)

def test_keycloak_login_success(mocker):
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(
            json=lambda: {"access_token": "token"},
            raise_for_status=lambda: None,
        ),
    )
    data = crud.keycloak_login("user", "pass")
    assert "access_token" in data

def test_keycloak_login_invalid_credentials(mocker):
    err = requests.HTTPError()
    err.response = mocker.Mock(status_code=401)
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(raise_for_status=mocker.Mock(side_effect=err)),
    )
    with pytest.raises(exc.InvalidCredentials):
        crud.keycloak_login("user", "pass")

def test_keycloak_refresh_success(mocker):
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(
            json=lambda: {"access_token": "new"},
            raise_for_status=lambda: None,
        ),
    )

    data = crud.keycloak_refresh("refresh")
    assert "access_token" in data

def test_keycloak_refresh_failure(mocker):
    err = requests.HTTPError()
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(raise_for_status=mocker.Mock(side_effect=err)),
    )
    with pytest.raises(exc.TokenRefreshFailed):
        crud.keycloak_refresh("refresh")

def test_get_admin_token_success(mocker):
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(
            json=lambda: {"access_token": "admin-token"},
            raise_for_status=lambda: None,
        ),
    )
    token = crud.get_admin_token()
    assert token == "admin-token"

def test_get_admin_token_failure(mocker):
    err = requests.HTTPError()
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(raise_for_status=mocker.Mock(side_effect=err)),
    )
    with pytest.raises(exc.AuthserviceApiError):
        crud.get_admin_token()
