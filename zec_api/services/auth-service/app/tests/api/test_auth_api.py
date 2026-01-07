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
        "/login",
        data={"username": "test", "password": "pass"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

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
        "/refresh",
        data={"refresh_token": "refresh"},
    )

    assert response.status_code == 200

def test_verify_token(client, mock_jwks):
    headers = {"Authorization": "Bearer valid.jwt.token"}

    response = client.get("/verify", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["active"] is True
    assert body["username"] == "test"

def test_get_admin_token(client, mocker):
    mocker.patch(
        "app.crud.auth.requests.post",
        return_value=mocker.Mock(
            status_code=200,
            json=lambda: {"access_token": "admin-token"},
            raise_for_status=lambda: None,
        ),
    )

    response = client.get("/internal/get-admin-token")

    assert response.status_code == 200
    assert response.json() == "admin-token"
