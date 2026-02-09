def test_create_user_api(client):
    resp = client.post(
        "/api/users/",
        json={"username": "apiuser", "password": "password"},
    )
    assert resp.status_code == 200
    assert resp.json()["username"] == "apiuser"

def test_get_user_by_username_api(client):
    resp = client.get("/api/users/username/testuser")
    assert resp.status_code == 200
    assert resp.json()["username"] == "testuser"

def test_update_user_api(client):
    resp = client.put(
        "/api/users/kc-123",
        json={"username": "changed"},
    )
    assert resp.status_code == 200
    assert resp.json()["username"] == "changed"

def test_delete_user_api(client):
    resp = client.delete("/api/users/kc-123")
    assert resp.status_code == 200
