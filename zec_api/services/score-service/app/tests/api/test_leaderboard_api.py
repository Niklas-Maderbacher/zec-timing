import pytest
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.database.dependency import get_db

class MockResp:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data
    def json(self):
        return self._json
    @property
    def text(self):
        return str(self._json)

def test_leaderboard_category_endpoint(db, override_get_db, seeded_scores, mock_leaderboard_requests):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
            {"id": 2, "team_id": 20},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
            {"id": 20, "name": "Team B", "category": "advanced_class"},
        ]),
    ]
    with TestClient(fastapi_app) as client:
        resp = client.get("/api/leaderboard/1/category/close_to_series")
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["team"]["id"] == 10
    assert data[0]["team"]["category"] == "close_to_series"

def test_leaderboard_endpoint_not_found(db, override_get_db, mock_leaderboard_requests):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_leaderboard_requests.get.return_value = MockResp(404, "not found")
    with TestClient(fastapi_app) as client:
        resp = client.get("/api/leaderboard/999/category/close_to_series")
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code in [404]

def test_leaderboard_endpoint_invalid_category(db, override_get_db, seeded_scores, mock_leaderboard_requests):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
        ]),
    ]
    with TestClient(fastapi_app) as client:
        resp = client.get("/api/leaderboard/1/category/nonexistent_category")
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code in [404]