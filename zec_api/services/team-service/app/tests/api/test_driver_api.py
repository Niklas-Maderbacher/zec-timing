def test_list_drivers(client):
    resp = client.get("/api/drivers/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2

def test_get_driver(client):
    resp = client.get("/api/drivers/1")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Driver 1"

def test_delete_driver(client):
    resp = client.delete("/api/drivers/1")
    assert resp.status_code == 200
