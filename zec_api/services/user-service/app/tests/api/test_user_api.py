import jwt

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

def test_get_user_by_id_api(client, seeded_user):
    resp = client.get(f"/api/users/id/{seeded_user.kc_id}")
    assert resp.status_code == 200
    assert resp.json()["kc_id"] == seeded_user.kc_id

def test_get_all_users_api(client):
    resp = client.get("/api/users/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_get_current_user_api(client, seeded_user):
    token = jwt.encode({"preferred_username": "testuser"}, "secret", algorithm="HS256")
    resp = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
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

def test_assign_roles_api(client):
    resp = client.post(
        "/api/users/kc-123/roles",
        json={"roles": ["admin"]},
    )
    assert resp.status_code == 200
    assert resp.json()["assigned_roles"] == ["admin"]

def test_remove_roles_api(client):
    resp = client.request(
        "DELETE",
        "/api/users/kc-123/roles",
        json={"roles": ["admin"]},
    )
    assert resp.status_code == 200
    assert resp.json()["unassigned_roles"] == ["admin"]
