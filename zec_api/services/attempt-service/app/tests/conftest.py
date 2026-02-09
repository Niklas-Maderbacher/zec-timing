import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, Mock
from datetime import datetime, timedelta, timezone
os.environ.setdefault("ENVIRONMENT", "testing")
os.environ.setdefault("PROJECT_NAME", "test")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("TEAM_SERVICE_URL", "http://team-service")
os.environ.setdefault("CHALLENGE_SERVICE_URL", "http://challenge-service")
os.environ.setdefault("SCORE_SERVICE_URL", "http://score-service")
from app.main import app
from app.database.session import Base
from app.database.dependency import get_db
from app.models.attempt import Attempt

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_attempt.db"

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
def seeded_attempts(db):
    base = datetime.now(timezone.utc)
    attempts = [
        Attempt(
            team_id=1,
            driver_id=1,
            challenge_id=1,
            start_time=base,
            end_time=base + timedelta(seconds=10),
            energy_used=50,
            is_valid=True,
        ),
        Attempt(
            team_id=1,
            driver_id=2,
            challenge_id=1,
            start_time=base + timedelta(seconds=1),
            end_time=base + timedelta(seconds=10),
            energy_used=40,
            is_valid=True,
        ),
    ]
    db.add_all(attempts)
    db.commit()
    return attempts

@pytest.fixture(autouse=True)
def mock_requests():
    with patch("app.crud.attempt.requests") as mock_requests:
        def mock_get(url, *args, **kwargs):
            response = Mock()
            response.status_code = 200

            if "/api/challenges/" in url:
                response.json.return_value = {
                    "id": 1,
                    "max_attempts": 3,
                }
            elif "/api/teams/" in url:
                response.json.return_value = {"id": 1}
            elif "/api/drivers/" in url:
                response.json.return_value = {"id": 1}
            else:
                response.json.return_value = {}
            return response
        def mock_response(*args, **kwargs):
            response = Mock()
            response.status_code = 200
            return response
        mock_requests.get.side_effect = mock_get
        mock_requests.post.side_effect = mock_response
        mock_requests.delete.side_effect = mock_response
        yield mock_requests

@pytest.fixture(scope="function")
def client(db, seeded_attempts, mock_requests):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
