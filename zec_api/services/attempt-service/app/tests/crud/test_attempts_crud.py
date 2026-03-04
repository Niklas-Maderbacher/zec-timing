import pytest
from datetime import timedelta, datetime
from app.crud import attempt as crud
from app.schemas.attempt import AttemptUpdate, AttemptCreate
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError, AuthenticationFailed

def test_get_attempt(db, seeded_attempts):
    attempt = crud.get_attempt(db=db, attempt_id=seeded_attempts[0].id)
    assert attempt.team_id == 1

def test_get_attempts(db, seeded_attempts):
    attempts = crud.get_attempts(db=db)
    assert len(attempts) == 2

def test_get_attempts_for_challenge(db, seeded_attempts):
    attempts = crud.get_all_attempts_for_challenge(db=db, challenge_id=1)
    assert len(attempts) == 2

def test_fastest_attempt(db, seeded_attempts):
    attempt = crud.get_fastest_attempt(db=db, challenge_id=1)
    time = attempt.end_time - attempt.start_time
    assert time == timedelta(seconds=9)

def test_fastest_attempt_for_team(db, seeded_attempts):
    attempt = crud.get_fastest_attempt_for_team(
        db=db, team_id=1, challenge_id=1
    )
    assert attempt.team_id == 1

def test_least_energy_attempt(db, seeded_attempts):
    attempt = crud.get_least_energy_attempt(db=db, challenge_id=1)
    assert attempt.energy_used == 40

def test_delete_attempt(db, seeded_attempts):
    deleted = crud.delete_attempt(db=db, attempt_id=seeded_attempts[0].id)
    assert deleted.id == seeded_attempts[0].id
    with pytest.raises(EntityDoesNotExistError):
        crud.get_attempt(db=db, attempt_id=deleted.id)

def test_invalidate_attempt_deletes_score(db, seeded_attempts, monkeypatch):
    deleted_url = {}
    def fake_delete(url):
        deleted_url["url"] = url
        class R:
            status_code = 200
        return R()
    monkeypatch.setattr("app.crud.attempt.requests.delete", fake_delete)
    update = AttemptUpdate(is_valid=False)
    updated = crud.update_attempt(
        db=db,
        attempt_id=seeded_attempts[0].id,
        attempt_update=update,
    )
    assert updated.is_valid is False
    assert deleted_url["url"].endswith(
        f"/api/scores/attempt/{seeded_attempts[0].id}"
    )

def test_invalid_attempts_ignored_in_fastest(db, seeded_attempts):
    fastest = seeded_attempts[1]
    fastest.is_valid = False
    db.commit()
    attempt = crud.get_fastest_attempt(db=db, challenge_id=1)
    assert attempt.id != fastest.id

def test_create_attempt_success(db, mock_requests):
    mock_attempt, _ = mock_requests
    now = datetime.now().replace(microsecond=123456)
    payload = AttemptCreate(
        team_id=1,
        driver_id=1,
        challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=30,
        is_valid=True,
    )
    created = crud.create_attempt(db=db, attempt=payload)
    assert created.id is not None
    assert created.energy_used == 30

def test_create_attempt_max_attempts_reached(db, seeded_attempts, mock_requests):
    mock_attempt, _ = mock_requests
    now = datetime.now().replace(microsecond=123456)
    payload = AttemptCreate(
        team_id=1,
        driver_id=1,
        challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=20,
        is_valid=True,
    )

    def challenge_limit(url, *_, **__):
        class R:
            status_code = 200
            def json(self):
                return {"id": 1, "max_attempts": 2}
        return R()
    mock_attempt.get.side_effect = challenge_limit
    with pytest.raises(ServiceError, match="Maximum attempts"):
        crud.create_attempt(db=db, attempt=payload)

def test_create_attempt_team_not_found(db, mock_requests):
    mock_attempt, _ = mock_requests

    def team_404(url, *_, **__):
        class R:
            status_code = 404
            text = "not found"
            def json(self): return {}
        return R()

    mock_attempt.get.side_effect = team_404
    now = datetime.now()
    payload = AttemptCreate(
        team_id=99, driver_id=1, challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
    )
    with pytest.raises(EntityDoesNotExistError, match="Team"):
        crud.create_attempt(db=db, attempt=payload)

def test_create_attempt_team_unauthorized(db, mock_requests):
    mock_attempt, _ = mock_requests

    def team_401(url, *_, **__):
        class R:
            status_code = 401
            text = "unauthorized"
            def json(self): return {}
        return R()
    mock_attempt.get.side_effect = team_401
    now = datetime.now()
    payload = AttemptCreate(
        team_id=1, driver_id=1, challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
    )
    with pytest.raises(AuthenticationFailed):
        crud.create_attempt(db=db, attempt=payload)

def test_create_attempt_team_service_error(db, mock_requests):
    mock_attempt, _ = mock_requests

    def team_500(url, *_, **__):
        class R:
            status_code = 500
            text = "error"
            def json(self): return {}
        return R()
    mock_attempt.get.side_effect = team_500
    now = datetime.now()
    payload = AttemptCreate(
        team_id=1, driver_id=1, challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
    )
    with pytest.raises(ServiceError, match="Failed to fetch team"):
        crud.create_attempt(db=db, attempt=payload)

def test_create_attempt_driver_not_found(db, mock_requests):
    mock_attempt, _ = mock_requests
    def driver_404(url, *_, **__):
        class R:
            status_code = 404 if "/api/drivers/" in url else 200
            text = "not found"
            def json(self): return {"id": 1, "max_attempts": 3}
        return R()
    mock_attempt.get.side_effect = driver_404
    now = datetime.now()
    payload = AttemptCreate(
        team_id=1, driver_id=99, challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
    )
    with pytest.raises(EntityDoesNotExistError, match="Driver"):
        crud.create_attempt(db=db, attempt=payload)

def test_create_attempt_challenge_not_found(db, mock_requests):
    mock_attempt, _ = mock_requests
    def challenge_404(url, *_, **__):
        class R:
            status_code = 404 if "/api/challenges/" in url else 200
            text = "not found"
            def json(self): return {"id": 1}
        return R()
    mock_attempt.get.side_effect = challenge_404
    now = datetime.now()
    payload = AttemptCreate(
        team_id=1, driver_id=1, challenge_id=99,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
    )
    with pytest.raises(EntityDoesNotExistError, match="Challenge"):
        crud.create_attempt(db=db, attempt=payload)

def test_create_attempt_score_service_error(db, mock_requests):
    mock_attempt, _ = mock_requests

    mock_attempt.get.side_effect = lambda url, *a, **kw: type("R", (), {
        "status_code": 200,
        "text": "",
        "json": lambda self: {"id": 1, "max_attempts": 3},
    })()
    def score_500(*_, **__):
        class R:
            status_code = 500
            text = "error"
        return R()
    mock_attempt.post.side_effect = score_500
    now = datetime.now()
    payload = AttemptCreate(
        team_id=1, driver_id=1, challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
    )
    with pytest.raises(ServiceError, match="Failed to create score"):
        crud.create_attempt(db=db, attempt=payload)

def test_create_attempt_score_unauthorized(db, mock_requests):
    mock_attempt, _ = mock_requests
    mock_attempt.get.side_effect = lambda url, *a, **kw: type("R", (), {
        "status_code": 200,
        "text": "",
        "json": lambda self: {"id": 1, "max_attempts": 3},
    })()
    def score_401(*_, **__):
        class R:
            status_code = 401
            text = "unauthorized"
        return R()
    mock_attempt.post.side_effect = score_401
    now = datetime.now()
    payload = AttemptCreate(
        team_id=1, driver_id=1, challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
    )
    with pytest.raises(AuthenticationFailed):
        crud.create_attempt(db=db, attempt=payload)

def test_create_attempt_with_penalty(db, mock_requests):
    mock_attempt, _ = mock_requests
    mock_attempt.get.side_effect = lambda url, *a, **kw: type("R", (), {
        "status_code": 200,
        "text": "",
        "json": lambda self: {"id": 1, "max_attempts": 3},
    })()
    posted_urls = []
    def capture_post(url, *_, **kw):
        posted_urls.append(url)
        class R:
            status_code = 200
        return R()
    mock_attempt.post.side_effect = capture_post
    now = datetime.now()
    payload = AttemptCreate(
        team_id=1, driver_id=1, challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
        penalty_count=2,
        penalty_type=1,
    )
    created = crud.create_attempt(db=db, attempt=payload)
    assert created.id is not None
    assert any("penalties" in url for url in posted_urls)

def test_create_attempt_penalty_service_error(db, mock_requests):
    mock_attempt, _ = mock_requests
    mock_attempt.get.side_effect = lambda url, *a, **kw: type("R", (), {
        "status_code": 200,
        "text": "",
        "json": lambda self: {"id": 1, "max_attempts": 3},
    })()

    def penalty_500(url, *_, **__):
        class R:
            status_code = 500
            text = "error"
        return R()
    mock_attempt.post.side_effect = penalty_500
    now = datetime.now()
    payload = AttemptCreate(
        team_id=1, driver_id=1, challenge_id=1,
        start_time=now.isoformat(),
        end_time=(now + timedelta(seconds=5)).isoformat(),
        energy_used=10, is_valid=True,
        penalty_count=1,
        penalty_type=1,
    )
    with pytest.raises(ServiceError, match="Failed to create penalty"):
        crud.create_attempt(db=db, attempt=payload)

def test_update_attempt_score_delete_unauthorized(db, seeded_attempts, monkeypatch):
    def fake_delete(url):
        class R:
            status_code = 401
            text = "unauthorized"
        return R()

    monkeypatch.setattr("app.crud.attempt.requests.delete", fake_delete)
    update = AttemptUpdate(is_valid=False)
    with pytest.raises(AuthenticationFailed):
        crud.update_attempt(db=db, attempt_id=seeded_attempts[0].id, attempt_update=update)

def test_update_attempt_score_delete_service_error(db, seeded_attempts, monkeypatch):
    def fake_delete(url):
        class R:
            status_code = 500
            text = "error"
        return R()
    monkeypatch.setattr("app.crud.attempt.requests.delete", fake_delete)
    update = AttemptUpdate(is_valid=False)
    with pytest.raises(ServiceError, match="Failed to delete score"):
        crud.update_attempt(db=db, attempt_id=seeded_attempts[0].id, attempt_update=update)

def test_delete_attempt_score_unauthorized(db, seeded_attempts, monkeypatch):
    def fake_delete(url):
        class R:
            status_code = 401
            text = "unauthorized"
        return R()
    monkeypatch.setattr("app.crud.attempt.requests.delete", fake_delete)
    with pytest.raises(AuthenticationFailed):
        crud.delete_attempt(db=db, attempt_id=seeded_attempts[0].id)

def test_delete_attempt_score_service_error(db, seeded_attempts, monkeypatch):
    def fake_delete(url):
        class R:
            status_code = 500
            text = "error"
        return R()
    monkeypatch.setattr("app.crud.attempt.requests.delete", fake_delete)
    with pytest.raises(ServiceError, match="Failed to delete score"):
        crud.delete_attempt(db=db, attempt_id=seeded_attempts[0].id)

def test_delete_attempt_penalty_unauthorized(db, seeded_attempts, monkeypatch):
    call_count = {"n": 0}
    def fake_delete(url):
        call_count["n"] += 1
        class R:
            status_code = 401 if call_count["n"] > 1 else 200
            text = "unauthorized"
        return R()
    monkeypatch.setattr("app.crud.attempt.requests.delete", fake_delete)
    with pytest.raises(AuthenticationFailed):
        crud.delete_attempt(db=db, attempt_id=seeded_attempts[0].id)

def test_delete_attempt_penalty_service_error(db, seeded_attempts, monkeypatch):
    call_count = {"n": 0}
    def fake_delete(url):
        call_count["n"] += 1
        class R:
            status_code = 500 if call_count["n"] > 1 else 200
            text = "error"
        return R()
    monkeypatch.setattr("app.crud.attempt.requests.delete", fake_delete)
    with pytest.raises(ServiceError, match="Failed to delete penalties"):
        crud.delete_attempt(db=db, attempt_id=seeded_attempts[0].id)

def test_get_valid_attempts_for_challenge(db, seeded_attempts):
    attempts = crud.get_valid_attempts_for_challenge(db=db, challenge_id=1)
    assert all(a.is_valid for a in attempts)


def test_get_valid_attempts_for_challenge_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_valid_attempts_for_challenge(db=db, challenge_id=999)

def test_get_attempts_for_team(db, seeded_attempts):
    attempts = crud.get_attempts_for_team(db=db, team_id=1)
    assert len(attempts) == 2

def test_get_attempts_for_team_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_attempts_for_team(db=db, team_id=999)

def test_get_attempts_for_driver(db, seeded_attempts):
    attempts = crud.get_attempts_for_driver(db=db, driver_id=1)
    assert len(attempts) == 1

def test_get_attempts_for_driver_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_attempts_for_driver(db=db, driver_id=999)

def test_get_attempts_for_team_per_challenge(db, seeded_attempts):
    attempts = crud.get_attempts_for_team_per_challenge(db=db, team_id=1, challenge_id=1)
    assert len(attempts) == 2

def test_update_attempt_not_found(db):
    update = AttemptUpdate(energy_used=99)
    with pytest.raises(EntityDoesNotExistError):
        crud.update_attempt(db=db, attempt_id=999, attempt_update=update)

def test_delete_attempt_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.delete_attempt(db=db, attempt_id=999)

def test_get_attempts_for_challenge_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_all_attempts_for_challenge(db=db, challenge_id=999)

def test_get_fastest_attempt_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_fastest_attempt(db=db, challenge_id=999)

def test_get_fastest_attempt_for_team_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_fastest_attempt_for_team(
            db=db,
            team_id=1,
            challenge_id=999,
        )

def test_get_least_energy_attempt_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_least_energy_attempt(db=db, challenge_id=999)

def test_get_least_energy_attempt_for_team_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_least_energy_attempt_for_team(
            db=db,
            team_id=1,
            challenge_id=999,
        )