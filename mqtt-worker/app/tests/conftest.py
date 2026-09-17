import pytest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.routes.timestamp import router as timestamps_router



@pytest.fixture
def mock_add_timestamp():
    with patch("app.mqtt.pull_timestamps.add_timestamp") as mock:
        yield mock

@pytest.fixture
def mock_redis():
    with patch("app.crud.timestamps.redis_connection") as mock:
        yield mock
 
 
@pytest.fixture
def frozen_time():
    with patch("app.crud.timestamps.time.time", return_value=1_000_000.0) as mock:
        yield mock
 
 
@pytest.fixture
def fixed_expire(monkeypatch):
    monkeypatch.setattr("app.crud.timestamps.settings.TIMESTAMP_EXPIRE_TIME", 3600)
    return 3600

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(timestamps_router)
    return TestClient(app)
 
 
@pytest.fixture
def mock_get_timestamps():
    with patch("app.api.routes.timestamp.get_timestamps") as mock:
        yield mock
 
 
@pytest.fixture
def mock_delete_timestamps():
    with patch("app.api.routes.timestamp.delete_timestamps") as mock:
        yield mock

