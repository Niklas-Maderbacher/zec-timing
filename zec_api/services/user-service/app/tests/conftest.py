import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

os.environ.setdefault("ENVIRONMENT", "testing")
os.environ.setdefault("PROJECT_NAME", "test")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "test")

os.environ.setdefault("PROJECT_NAME", "test")
os.environ.setdefault("KEYCLOAK_USER_URL", "http://keycloak/users")
os.environ.setdefault("KC_CLIENTS_URL", "http://keycloak/clients")
os.environ.setdefault("KC_ADMIN_CLIENT_ID", "admin-cli")
os.environ.setdefault("AUTH_SERVICE_URL", "http://auth")

from app.main import app
from app.database.session import Base
from app.database.dependency import get_db
from app.models.user import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_user.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def seeded_user(db):
    user = User(
        username="testuser",
        kc_id="kc-123",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture(autouse=True)
def mock_admin_token():
    with patch("app.crud.user.get_admin_token", return_value="admin-token"):
        yield

@pytest.fixture(autouse=True)
def mock_requests():
    with patch("app.crud.user.requests") as mock_requests:
        def _get_side_effect(url, *args, **kwargs):
            if "/users/" in url and "username=" not in url:
                user_id = url.rsplit("/", 1)[-1]
                username = "testuser" if user_id == "kc-123" else ("admin" if user_id == "kc-admin" else user_id)
                return MagicMock(status_code=200, json=lambda: {"id": user_id, "username": username})
            if "username=admin" in url:
                return MagicMock(
                    status_code=200,
                    json=lambda: [{"id": "kc-admin", "username": "admin"}],
                )
            if "username=newuser" in url or "username=apiuser" in url:
                return MagicMock(
                    status_code=200,
                    json=lambda: [{"id": "kc-12345", "username": url.split("username=")[-1]}],
                )
            if "username=testuser" in url:
                return MagicMock(
                    status_code=200,
                    json=lambda: [{"id": "kc-123", "username": "testuser"}],
                )
            if "clients?clientId" in url:
                return MagicMock(status_code=200, json=lambda: [{"id": "client-uuid"}])
            if "/clients/" in url and "/roles/" in url:
                role_name = url.rsplit("/", 1)[-1]
                return MagicMock(status_code=200, json=lambda: {"id": f"role-{role_name}", "name": role_name})
            return MagicMock(status_code=200, json=lambda: [])
        mock_requests.get.side_effect = _get_side_effect
        def _post_side_effect(url, *args, **kwargs):
            rv = getattr(mock_requests.post, "return_value", None)
            if rv is not None and getattr(rv, "status_code", None) in (401, 409, 500):
                return rv
            if "/role-mappings/clients/" in url:
                return MagicMock(status_code=204)
            if url.startswith(os.environ.get("KEYCLOAK_USER_URL", "http://keycloak/users")):
                return MagicMock(status_code=201)
            return MagicMock(status_code=201)
        mock_requests.post.side_effect = _post_side_effect
        mock_requests.put.return_value = MagicMock(status_code=204)
        mock_requests.delete.return_value = MagicMock(status_code=204)
        yield mock_requests

@pytest.fixture(scope="function")
def client(db, seeded_user):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
