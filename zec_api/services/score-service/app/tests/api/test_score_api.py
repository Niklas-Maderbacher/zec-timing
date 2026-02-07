from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.database.dependency import get_db
from app.models.penalty import Penalty
from datetime import datetime, timedelta, timezone

class MockResp:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data
    def json(self):
        return self._json
    @property
    def text(self):
        return str(self._json)

def mock_attempt(challenge_id=1, energy=50, team_id=1, driver_id=1, attempt_id=1):
    base = datetime.now(timezone.utc)
    return {
        "id": attempt_id,
        "challenge_id": challenge_id,
        "team_id": team_id,
        "driver_id": driver_id,
        "energy_used": energy,
        "start_time": base.strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "end_time": (base + timedelta(seconds=10)).strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "is_valid": True,
    }

def test_get_score_not_found(client):
    resp = client.get("/api/scores/9999")
    assert resp.status_code == 404
    data = resp.json()
    assert "detail" in data


def test_list_scores_empty(minimal_client):
    resp = minimal_client.get("/api/scores/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_multiple_scores(client):
    for score_id in [1, 2, 3]:
        resp = client.get(f"/api/scores/{score_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == score_id

def test_create_score_skidpad(db, override_get_db, mock_requests):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_requests.get.side_effect = [
        MockResp(200, mock_attempt()),
        MockResp(200, {"id": 1, "name": "Skidpad"}),
        MockResp(200, mock_attempt()),
    ]
    with TestClient(fastapi_app) as client:
        resp = client.post("/api/scores/", json={"attempt_id": 10})
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    data = resp.json()
    assert "value" in data
    assert data["value"] > 0
    assert data["attempt_id"] == 10

def test_create_score_acceleration(db, override_get_db, mock_requests):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_requests.get.side_effect = [
        MockResp(200, mock_attempt(attempt_id=11)),
        MockResp(200, {"id": 1, "name": "Acceleration"}),
        MockResp(200, mock_attempt(attempt_id=11)),
        MockResp(200, {"id": 1, "vehicle_weight": 500, "mean_power": 100}),
        MockResp(200, {"id": 1, "weight": 70}),
        MockResp(200, mock_attempt(attempt_id=11)),
        MockResp(200, mock_attempt(attempt_id=11)),
        MockResp(200, {"id": 1, "vehicle_weight": 500, "mean_power": 100}),
        MockResp(200, {"id": 1, "weight": 70}),
    ]
    with TestClient(fastapi_app) as client:
        resp = client.post("/api/scores/", json={"attempt_id": 11})
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    data = resp.json()
    assert data["value"] > 0

def test_create_score_slalom(db, override_get_db, mock_requests):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_requests.get.side_effect = [
        MockResp(200, mock_attempt()),
        MockResp(200, {"id": 1, "name": "Slalom"}),
        MockResp(200, mock_attempt()),
    ]
    with TestClient(fastapi_app) as client:
        resp = client.post("/api/scores/", json={"attempt_id": 12})
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    data = resp.json()
    assert data["value"] > 0

def test_create_score_endurance(db, override_get_db, mock_requests):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_requests.get.side_effect = [
        MockResp(200, mock_attempt(energy=50)),
        MockResp(200, {"id": 1, "name": "Endurance"}),
        MockResp(200, mock_attempt(energy=50)),
        MockResp(200, mock_attempt(energy=40)),
    ]
    with TestClient(fastapi_app) as client:
        resp = client.post("/api/scores/", json={"attempt_id": 13})
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    data = resp.json()
    assert data["value"] > 0

def test_create_score_attempt_not_found(db, override_get_db, mock_score_requests):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_score_requests.get.return_value = MockResp(404, "not found")
    with TestClient(fastapi_app) as client:
        resp = client.post("/api/scores/", json={"attempt_id": 9999})
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 404

def test_update_score(client):
    resp = client.put("/api/scores/1", json={"value": 99.9})
    assert resp.status_code == 200
    data = resp.json()
    assert data["value"] == 99.9
    assert data["id"] == 1
    resp = client.get("/api/scores/1")
    assert resp.json()["value"] == 99.9

def test_delete_score(client):
    resp = client.delete("/api/scores/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    resp = client.get("/api/scores/1")
    assert resp.status_code == 404

def test_update_score_not_found(client):
    resp = client.put("/api/scores/9999", json={"value": 99.9})
    assert resp.status_code == 404

def test_delete_score_not_found(client):
    resp = client.delete("/api/scores/9999")
    assert resp.status_code == 404

def test_delete_scores_for_attempt_not_found(client):
    resp = client.delete("/api/scores/attempt/9999")
    assert resp.status_code == 404

def test_create_score_with_penalties(db, override_get_db, seeded_penalty_types, mock_requests):
    db.add(Penalty(attempt_id=20, penalty_type_id=1, count=2))
    db.commit()
    fastapi_app.dependency_overrides[get_db] = override_get_db
    mock_requests.get.side_effect = [
        MockResp(200, mock_attempt()),
        MockResp(200, {"id": 1, "name": "Slalom"}),
        MockResp(200, mock_attempt()),
    ]

    with TestClient(fastapi_app) as client:
        resp = client.post("/api/scores/", json={"attempt_id": 20})
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
