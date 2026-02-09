def test_list_challenges(client):
    response = client.get("/api/challenges/")
    assert response.status_code == 200
    names = [c["name"] for c in response.json()]
    assert "challenge-one" in names
    assert "challenge-two" in names

def test_get_challenge(client):
    response = client.get("/api/challenges/1")
    assert response.status_code == 200
    assert response.json()["name"] == "challenge-one"

def test_get_challenge_by_name(client):
    response = client.get("/api/challenges/name/challenge-two")
    assert response.status_code == 200
    assert response.json()["name"] == "challenge-two"

def test_update_challenge(client):
    payload = {
        "id": 1,
        "max_attempts": 10,
    }

    response = client.put("/api/challenges/1", json=payload)
    assert response.status_code == 200
    assert response.json()["max_attempts"] == 10
