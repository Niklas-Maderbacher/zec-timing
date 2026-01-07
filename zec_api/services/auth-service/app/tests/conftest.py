import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("KEYCLOAK_URL", "http://keycloak")
os.environ.setdefault("KEYCLOAK_TOKEN_URL", "http://keycloak/token")
os.environ.setdefault("KEYCLOAK_JWKS_URL", "http://keycloak/jwks")

os.environ.setdefault("KEYCLOAK_CLIENT_ID", "client")
os.environ.setdefault("KEYCLOAK_CLIENT_SECRET", "secret")
os.environ.setdefault("KEYCLOAK_ADMIN_CLIENT_ID", "admin-client")
os.environ.setdefault("KEYCLOAK_ADMIN_CLIENT_SECRET", "admin-secret")

from app.main import app

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def mock_jwks(mocker):
    jwks = {
        "keys": [
            {
                "kty": "RSA",
                "kid": "test-kid",
                "use": "sig",
                "n": "abc",
                "e": "AQAB",
            }
        ]
    }

    mocker.patch(
        "app.crud.auth.get_cached_jwks",
        return_value=jwks,
    )

    mocker.patch(
        "app.crud.auth.jwk.construct",
        return_value=mocker.Mock(public_key=lambda: "public-key"),
    )

    mocker.patch(
        "app.crud.auth.jwt.get_unverified_header",
        return_value={"kid": "test-kid"},
    )

    mocker.patch(
        "app.crud.auth.jwt.decode",
        return_value={
            "sub": "123",
            "email": "test@test.com",
            "preferred_username": "test",
            "resource_access": {
                "admin-client": {"roles": ["admin"]}
            },
        },
    )
