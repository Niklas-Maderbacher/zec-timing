import pytest
from unittest.mock import MagicMock, patch
from app.mqtt.pull_timestamps import extract_payload

@pytest.fixture
def mock_redis():
    with patch("app.mqtt.pull_timestamps.redis_connection") as mock:
        mock.rpush = MagicMock()
        yield mock

@pytest.fixture
def mock_lock():
    with patch("app.mqtt.pull_timestamps.redis_lock") as lock:
        lock.__enter__ = MagicMock(return_value=None)
        lock.__exit__ = MagicMock(return_value=None)
        yield lock