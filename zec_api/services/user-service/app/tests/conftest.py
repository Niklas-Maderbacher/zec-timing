import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

from app.main import app
from app.database.session import Base
from app.database.dependency import get_db
from app.models.user import User

os.environ.setdefault("PROJECT_NAME", "test")
os.environ.setdefault("KEYCLOAK_USER_URL", "http://keycloak/users")
os.environ.setdefault("KC_CLIENTS_URL", "http://keycloak/clients")
os.environ.setdefault("KC_ADMIN_CLIENT_ID", "admin-cli")
os.environ.setdefault("AUTH_SERVICE_URL", "http://auth")

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
        mock_requests.get.return_value = MagicMock(
            status_code=200,
            json=lambda: [{"id": "kc-123", "username": "testuser"}],
        )
        mock_requests.post.return_value = MagicMock(status_code=201)
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
