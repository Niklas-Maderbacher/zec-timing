import pytest
from app.crud import attempt as crud
from app.schemas.attempt import AttemptCreate, AttemptUpdate
from app.exceptions.exceptions import EntityDoesNotExistError

def test_get_attempt(db, seeded_attempts):
    attempt = crud.get_attempt(db=db, attempt_id=seeded_attempts[0].id)
    assert attempt.team_id == 1

def test_get_attempts(db, seeded_attempts):
    attempts = crud.get_attempts(db=db)
    assert len(attempts) == 3

def test_get_attempts_for_challenge(db, seeded_attempts):
    attempts = crud.get_attempts_for_challenge(db=db, challenge_id=1)
    assert len(attempts) == 3

def test_fastest_attempt(db, seeded_attempts):
    attempt = crud.get_fastest_attempt(db=db, challenge_id=1)
    assert attempt.end_time - attempt.start_time == min(
        a.end_time - a.start_time for a in seeded_attempts
    )

def test_fastest_attempt_for_team(db, seeded_attempts):
    attempt = crud.get_fastest_attempt_for_team(db=db, team_id=1, challenge_id=1)
    assert attempt.team_id == 1

def test_least_energy_attempt(db, seeded_attempts):
    attempt = crud.get_least_energy_attempt(db=db, challenge_id=1)
    assert attempt.energy_used == 30

def test_delete_attempt(db, seeded_attempts):
    deleted = crud.delete_attempt(db=db, attempt_id=seeded_attempts[0].id)
    assert deleted.id == seeded_attempts[0].id
    with pytest.raises(EntityDoesNotExistError):
        crud.get_attempt(db=db, attempt_id=deleted.id)


def test_invalidate_attempt_deletes_score(db, seeded_attempts, monkeypatch):
    deleted_url = {}
    def fake_delete(url):
        deleted_url['url'] = url
        class R:
            status_code = 200
        return R()
    monkeypatch.setattr("app.crud.attempt.requests.delete", fake_delete)
    update = AttemptUpdate(is_valid=False)
    updated = crud.update_attempt(db=db, attempt_id=seeded_attempts[0].id, attempt_update=update)
    assert updated.is_valid is False
    assert deleted_url['url'].endswith(f"/api/scores/attempt/{seeded_attempts[0].id}")


def test_invalid_attempts_ignored_in_fastest(db, seeded_attempts):
    # mark the fastest seeded attempt invalid and ensure it's ignored
    fastest = seeded_attempts[1]
    fastest.is_valid = False
    db.commit()
    attempt = crud.get_fastest_attempt(db=db, challenge_id=1)
    assert attempt.id != fastest.id
