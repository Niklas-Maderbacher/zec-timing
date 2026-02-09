class MockResp:
    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):
        return {}

def test_list_penalties(client):
    resp = client.get("/api/penalties/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_list_penalties_empty(minimal_client):
    resp = minimal_client.get("/api/penalties/")
    assert resp.status_code == 200
    assert resp.json() == []

def test_get_penalty(client):
    resp = client.get("/api/penalties/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["attempt_id"] == 1

def test_get_penalty_not_found(client):
    resp = client.get("/api/penalties/9999")
    assert resp.status_code == 404
    assert "detail" in resp.json()

def test_list_penalties_by_attempt(client):
    resp = client.get("/api/penalties/attempt/1")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    for p in data:
        assert p["attempt_id"] == 1

def test_list_penalties_by_attempt_not_found(client):
    resp = client.get("/api/penalties/attempt/9999")
    assert resp.status_code == 404
    assert "detail" in resp.json()

def test_create_penalty(client, mock_penalty_requests):
    mock_penalty_requests.get.return_value = MockResp(200)
    resp = client.post(
        "/api/penalties/",
        json={
            "attempt_id": 1,
            "penalty_type_id": 1,
            "count": 3,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 3
    assert data["penalty_type_id"] == 1

def test_create_penalty_attempt_not_found(client, mock_penalty_requests):
    mock_penalty_requests.get.return_value = MockResp(404)
    resp = client.post(
        "/api/penalties/",
        json={
            "attempt_id": 9999,
            "penalty_type_id": 1,
            "count": 1,
        },
    )
    assert resp.status_code == 500

def test_create_penalty_invalid_type(client, mock_penalty_requests):
    mock_penalty_requests.get.return_value = MockResp(200)

    resp = client.post(
        "/api/penalties/",
        json={
            "attempt_id": 1,
            "penalty_type_id": 9999,
            "count": 1,
        },
    )
    assert resp.status_code == 404


def test_create_penalty_invalid_payload(client):
    resp = client.post(
        "/api/penalties/",
        json={"attempt_id": 1},
    )
    assert resp.status_code == 422

def test_update_penalty(client):
    resp = client.put(
        "/api/penalties/1",
        json={"count": 10},
    )
    assert resp.status_code == 200
    assert resp.json()["count"] == 10

def test_update_penalty_not_found(client):
    resp = client.put(
        "/api/penalties/9999",
        json={"count": 1},
    )
    assert resp.status_code == 404

def test_delete_penalty(client):
    resp = client.delete("/api/penalties/1")
    assert resp.status_code == 200

    resp = client.get("/api/penalties/1")
    assert resp.status_code == 404

def test_delete_penalty_not_found(client):
    resp = client.delete("/api/penalties/9999")
    assert resp.status_code == 404

def test_delete_penalties_by_attempt(client):
    resp = client.delete("/api/penalties/attempt/1")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    resp = client.get("/api/penalties/attempt/1")
    assert resp.status_code == 404

def test_delete_penalties_by_attempt_not_found(client):
    resp = client.delete("/api/penalties/attempt/9999")
    assert resp.status_code == 404

def test_get_penalty_types(client):
    resp = client.get("/api/penalties/types/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1
    assert {"id", "type", "amount"} <= data[0].keys()
