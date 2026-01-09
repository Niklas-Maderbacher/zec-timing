import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

os.environ.setdefault("ENVIRONMENT", "testing")
os.environ.setdefault("PROJECT_NAME", "test")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_USER", "test")
os.environ.setdefault("POSTGRES_PASSWORD", "test")
os.environ.setdefault("POSTGRES_DB", "test")
os.environ.setdefault("PROJECT_NAME", "test")
os.environ.setdefault("ATTEMPT_SERVICE_URL", "http://attempt")
os.environ.setdefault("TEAM_SERVICE_URL", "http://team")
os.environ.setdefault("CHALLENGE_SERVICE_URL", "http://challenge")

from app.main import app
from app.database.session import Base
from app.database.dependency import get_db
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
def seeded_scores(db):
    scores = [
        Score(attempt_id=1, challenge_id=1, value=95.0),
        Score(attempt_id=2, challenge_id=1, value=90.0),
    ]
    db.add_all(scores)
    db.commit()
    return scores

@pytest.fixture(scope="function")
def mock_requests():
    with patch("app.crud.score.requests") as mock:
        yield mock

@pytest.fixture(scope="function")
def client(db, seeded_scores, mock_requests):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
