import requests

def test_login_success(client, mocker):
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {"access_token": "token"},
            raise_for_status=lambda: None,
        ),
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "test", "password": "pass"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] == "token"

def test_refresh_success(client, mocker):
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {"access_token": "new-token"},
            raise_for_status=lambda: None,
        ),
    )
    response = client.post(
        "/api/auth/refresh",
        data={"refresh_token": "refresh"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] == "new-token"

def test_verify_admin_success(client, override_admin):
    resp = client.get(
        "/api/auth/internal/verify/admin",
        headers={"Authorization": "Bearer token"},
    )
    assert resp.status_code == 200
    assert resp.json()["active"] is True
    assert "ADMIN" in resp.json()["roles"]

def test_verify_teamlead_success(client, override_teamlead, mocker):
    mocker.patch(
        "app.api.routes.auth.requests.get",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {"team_id": 42},
            raise_for_status=lambda: None,
        ),
    )
    resp = client.get(
        "/api/auth/internal/verify/teamlead",
        headers={"Authorization": "Bearer token"},
    )
    assert resp.status_code == 200
    assert "TEAM_LEAD" in resp.json()["roles"]
    assert resp.json()["team_id"] == 42

def test_verify_teamlead_sets_headers(client, override_teamlead, mocker):
    mocker.patch(
        "app.api.routes.auth.requests.get",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {"team_id": 42},
            raise_for_status=lambda: None,
        ),
    )
    resp = client.get(
        "/api/auth/internal/verify/teamlead",
        headers={"Authorization": "Bearer token"},
    )
    assert resp.headers["x-team-id"] == "42"
    assert resp.headers["x-role"] == "TEAM_LEAD"

def test_verify_viewer_success(client, override_viewer):
    resp = client.get(
        "/api/auth/internal/verify/viewer",
        headers={"Authorization": "Bearer token"},
    )
    assert resp.status_code == 200
    assert "VIEWER" in resp.json()["roles"]

def test_get_admin_token_success(client, mocker):
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {"access_token": "admin-token"},
            raise_for_status=lambda: None,
        ),
    )
    response = client.get("/api/auth/internal/get-admin-token")
    assert response.status_code == 200
    assert response.json() == "admin-token"

def test_login_missing_fields_returns_422(client):
    response = client.post("/api/auth/login", data={})
    assert response.status_code == 422

def test_login_invalid_credentials_returns_401(client, mocker):
    class FakeResponse:
        def raise_for_status(self):
            err = requests.HTTPError()
            err.response = type("R", (), {"status_code": 401})()
            raise err

    mocker.patch("app.crud.auth.requests.post", return_value=FakeResponse())
    response = client.post(
        "/api/auth/login",
        data={"username": "bad", "password": "creds"},
    )
    assert response.status_code == 401

def test_login_keycloak_unavailable_returns_503(client, mocker):
    mocker.patch(
        "app.crud.auth.requests.post",
        side_effect=requests.ConnectionError(),
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "x", "password": "y"},
    )
    assert response.status_code == 503

def test_refresh_missing_token_returns_422(client):
    response = client.post("/api/auth/refresh", data={})
    assert response.status_code == 422

def test_refresh_failure_returns_401(client, mocker):
    class FakeResponse:
        def raise_for_status(self):
            raise requests.HTTPError()
    mocker.patch("app.crud.auth.requests.post", return_value=FakeResponse())
    response = client.post(
        "/api/auth/refresh",
        data={"refresh_token": "bad"},
    )
    assert response.status_code == 401

def test_verify_missing_token_returns_401(client):
    resp = client.get("/api/auth/internal/verify/admin")
    assert resp.status_code == 401

def test_verify_insufficient_permissions_returns_403(client, override_viewer):
    resp = client.get(
        "/api/auth/internal/verify/admin",
        headers={"Authorization": "Bearer token"},
    )
    assert resp.status_code == 403
