from datetime import datetime, timedelta, timezone

def test_list_attempts(client):
    response = client.get("/api/attempts/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_attempt(client):
    response = client.get("/api/attempts/1")
    assert response.status_code == 200
    assert response.json()["team_id"] == 1

def test_get_attempts_per_challenge(client):
    response = client.get("/api/attempts/challenges/1")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_fastest_attempt(client):
    response = client.get("/api/attempts/fastest/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_fastest_attempt_per_team(client):
    response = client.get("/api/attempts/fastest/per-team/", params={"challenge_id": 1, "team_id": 1})
    assert response.status_code == 200
    assert response.json()["team_id"] == 1

def test_create_attempt_success(client):
    payload = {
        "team_id": 1,
        "driver_id": 1,
        "challenge_id": 1,
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat(),
        "energy_used": 25,
        "is_valid": True,
    }
    resp = client.post("/api/attempts/", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["team_id"] == 1
    assert body["energy_used"] == 25

def test_update_attempt_success(client):
    payload = {
        "energy_used": 99,
    }
    resp = client.put("/api/attempts/1", json=payload)
    assert resp.status_code == 200
    assert resp.json()["energy_used"] == 99


def test_update_attempt_invalidates_score(client):
    payload = {
        "is_valid": False,
    }
    resp = client.put("/api/attempts/1", json=payload)
    assert resp.status_code == 200
    assert resp.json()["is_valid"] is False

def test_delete_attempt_success(client):
    resp = client.delete("/api/attempts/1")
    assert resp.status_code == 200
    assert resp.json()["id"] == 1
    resp = client.get("/api/attempts/1")
    assert resp.status_code == 404

def test_least_energy_attempt(client):
    resp = client.get("/api/attempts/least-energy/1")
    assert resp.status_code == 200
    assert resp.json()["energy_used"] == 40

def test_least_energy_attempt_per_team(client):
    resp = client.get(
        "/api/attempts/least-energy/per-team/",
        params={"challenge_id": 1, "team_id": 1},
    )
    assert resp.status_code == 200
    assert resp.json()["team_id"] == 1

def test_get_attempt_not_found(client):
    resp = client.get("/api/attempts/999")
    assert resp.status_code == 404
    assert "does not exist" in resp.json()["detail"]

def test_fastest_attempt_not_found(client):
    resp = client.get("/api/attempts/fastest/999")
    assert resp.status_code == 404

def test_least_energy_attempt_not_found(client):
    resp = client.get("/api/attempts/least-energy/999")
    assert resp.status_code == 404
