def test_get_all_drivers(client):
    resp = client.get("/api/drivers/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_get_driver(client):
    resp = client.get("/api/drivers/1")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Driver 1"

def test_get_driver_not_found(client):
    resp = client.get("/api/drivers/999")
    assert resp.status_code == 404

def test_get_drivers_by_team(client, seeded_data):
    team_id = seeded_data["teams"][0].id
    resp = client.get(f"/api/drivers/team/{team_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert all(d["team_id"] == team_id for d in data)

def test_get_drivers_by_team_not_found(client):
    resp = client.get("/api/drivers/team/999")
    assert resp.status_code == 404

def test_get_drivers_by_ids(client, seeded_data):
    ids = [d.id for d in seeded_data["drivers"]]
    resp = client.get("/api/drivers/by-ids/", params=[("driver_ids", i) for i in ids])
    assert resp.status_code == 200
    assert len(resp.json()) == len(ids)

def test_get_drivers_by_ids_not_found(client, seeded_data):
    existing_id = seeded_data["drivers"][0].id
    resp = client.get("/api/drivers/by-ids/", params=[("driver_ids", existing_id), ("driver_ids", 999)])
    assert resp.status_code == 404

def test_create_driver(client, seeded_data):
    team_id = seeded_data["teams"][0].id
    payload = {"name": "New Driver", "weight": 68, "team_id": team_id}
    resp = client.post("/api/drivers/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "New Driver"
    assert data["weight"] == 68
    assert data["team_id"] == team_id

def test_create_driver_team_not_found(client):
    payload = {"name": "Ghost Driver", "weight": 70, "team_id": 999}
    resp = client.post("/api/drivers/", json=payload)
    assert resp.status_code == 404

def test_update_driver(client, seeded_data):
    driver_id = seeded_data["drivers"][0].id
    resp = client.put(f"/api/drivers/{driver_id}", json={"name": "Updated Driver"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated Driver"

def test_update_driver_not_found(client):
    resp = client.put("/api/drivers/999", json={"name": "Does Not Exist"})
    assert resp.status_code == 404

def test_delete_driver(client, mock_attempt_service_no_attempts):
    resp = client.delete("/api/drivers/1")
    assert resp.status_code == 200

def test_delete_driver_with_attempts(client, mock_attempt_service_with_attempts):
    resp = client.delete("/api/drivers/1")
    assert resp.status_code == 400

def test_delete_driver_not_found(client):
    resp = client.delete("/api/drivers/999")
    assert resp.status_code == 404
