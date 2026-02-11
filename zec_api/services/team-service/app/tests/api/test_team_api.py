def test_list_teams(client):
    resp = client.get("/api/teams/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_get_team(client):
    resp = client.get("/api/teams/1")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Team A"
    assert resp.json()["category"] == "close_to_series"

def test_get_teams_by_ids(client):
    resp = client.get("/api/teams/by-ids/", params=[("team_ids", 1), ("team_ids", 2)])
    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_delete_team(client, mock_attempt_service_no_attempts):
    resp = client.delete("/api/teams/1")
    assert resp.status_code == 200

def test_delete_team_with_attempts(client, mock_attempt_service_with_attempts):
    resp = client.delete("/api/teams/1")
    assert resp.status_code == 400

def test_create_team(client):
    payload = {
        "category": "professional_class",
        "name": "Team C",
        "vehicle_weight": 350,
        "mean_power": 90,
        "rfid_identifier": "RFID_C",
    }
    resp = client.post("/api/teams/", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["name"] == "Team C"
    assert body["category"] == "professional_class"

def test_update_team(client):
    payload = {"category": "professional_class"}
    resp = client.put("/api/teams/1", json=payload)
    assert resp.status_code == 200
    assert resp.json()["category"] == "professional_class"
