import pytest
from datetime import timedelta, datetime
from app.crud import attempt as crud
from app.schemas.attempt import AttemptUpdate, AttemptCreate
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError

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
    monkeypatch.setattr(
        "app.crud.attempt.requests.delete",
        fake_delete,
    )
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
    mock_requests.get.side_effect = challenge_limit
    with pytest.raises(ServiceError, match="Maximum attempts"):
        crud.create_attempt(db=db, attempt=payload)

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
