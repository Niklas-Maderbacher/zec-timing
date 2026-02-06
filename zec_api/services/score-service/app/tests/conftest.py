import os
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
os.environ.setdefault("ENVIRONMENT", "testing")
os.environ.setdefault("PROJECT_NAME", "test")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("TEAM_SERVICE_URL", "http://team-service")
os.environ.setdefault("CHALLENGE_SERVICE_URL", "http://challenge-service")
os.environ.setdefault("ATTEMPT_SERVICE_URL", "http://attempt-service")
os.environ.setdefault("SCORE_SERVICE_URL", "http://score-service")

from app.main import app as fastapi_app
from app.database.session import Base
from app.database.dependency import get_db
from app.models.penalty_type import PenaltyType
from app.models.penalty import Penalty
from app.models.score import Score

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_score.db"

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
def seeded_penalty_types(db):
    items = [
        PenaltyType(id=1, type="Cone Hit", amount=2),
        PenaltyType(id=2, type="Off Course", amount=5),
        PenaltyType(id=3, type="Wrong Gate", amount=3),
        PenaltyType(id=4, type="DNF", amount=999),
    ]
    db.add_all(items)
    db.commit()
    return items

@pytest.fixture(scope="function")
def seeded_penalties(db, seeded_penalty_types):
    items = [
        Penalty(id=1, attempt_id=1, penalty_type_id=1, count=2),
        Penalty(id=2, attempt_id=1, penalty_type_id=2, count=1),
        Penalty(id=3, attempt_id=2, penalty_type_id=1, count=1),
        Penalty(id=4, attempt_id=3, penalty_type_id=3, count=1),
    ]
    db.add_all(items)
    db.commit()
    return items

@pytest.fixture(scope="function")
def seeded_scores(db):
    base = datetime.utcnow()
    items = [
        Score(id=1, attempt_id=1, challenge_id=1, value=95.5, created_at=base),
        Score(id=2, attempt_id=2, challenge_id=1, value=88.3, created_at=base),
        Score(id=3, attempt_id=3, challenge_id=1, value=92.1, created_at=base),
        Score(id=4, attempt_id=4, challenge_id=1, value=85.7, created_at=base),
        Score(id=5, attempt_id=5, challenge_id=1, value=78.9, created_at=base),
        Score(id=6, attempt_id=6, challenge_id=2, value=82.3, created_at=base),
    ]
    db.add_all(items)
    db.commit()
    return items

@pytest.fixture(scope="function")
def mock_score_requests():
    with patch("app.crud.score.requests") as mock_requests, \
         patch("app.crud.penalty.requests"), \
         patch("app.crud.leaderboard.requests"):
        yield mock_requests

@pytest.fixture(scope="function")
def mock_leaderboard_requests():
    with patch("app.crud.leaderboard.requests") as mock_requests, \
         patch("app.crud.score.requests"), \
         patch("app.crud.penalty.requests"):
        yield mock_requests


@pytest.fixture(autouse=True)
def mock_requests_penalty():
    with patch("app.crud.penalty.requests.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.status_code = 200 
        mock_get.return_value = mock_resp
        yield mock_get

@pytest.fixture(scope="function")
def client(
    db,
    seeded_penalty_types,
    seeded_penalties,
    seeded_scores,
    mock_requests,
):
    def override_get_db():
        yield db

    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def minimal_client(db, mock_requests):
    def override_get_db():
        yield db

    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()
