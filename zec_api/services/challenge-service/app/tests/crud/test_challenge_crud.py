import pytest
from app.crud import challenge as crud
from app.schemas.challenge import ChallengeUpdate
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError

def test_get_challenge(db, seeded_challenges):
    challenge = crud.get_challenge(db=db, challenge_id=seeded_challenges[0].id)
    assert challenge.name == "challenge-one"

def test_get_challenge_by_name(db, seeded_challenges):
    challenge = crud.get_challenge_by_name(
        db=db,
        challenge_name="challenge-two",
    )
    assert challenge.name == "challenge-two"

def test_get_challenges(db, seeded_challenges):
    challenges = crud.get_challenges(db=db)
    names = [c.name for c in challenges]
    assert "challenge-one" in names
    assert "challenge-two" in names

def test_update_challenge(db, seeded_challenges):
    update = ChallengeUpdate(
        max_attempts=10,
    )
    updated = crud.update_challenge(
        db=db,
        challenge_id=seeded_challenges[0].id,
        challenge_update=update,
    )
    assert updated.max_attempts == 10

def test_get_challenge_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_challenge(db=db, challenge_id=999)

def test_get_challenge_by_name_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_challenge_by_name(db=db, challenge_name="missing-challenge")

def test_update_challenge_not_found(db):
    update = ChallengeUpdate(max_attempts=99)
    with pytest.raises(EntityDoesNotExistError):
        crud.update_challenge(
            db=db,
            challenge_id=999,
            challenge_update=update,
        )

def test_update_challenge_service_error(db, seeded_challenges, monkeypatch):
    def fail_commit():
        raise Exception("Commit failed")
    monkeypatch.setattr(db, "commit", fail_commit)
    update = ChallengeUpdate(max_attempts=7)
    with pytest.raises(ServiceError):
        crud.update_challenge(
            db=db,
            challenge_id=seeded_challenges[0].id,
            challenge_update=update,
        )

def test_get_challenges_service_error(db, monkeypatch):
    def fail_query(*args, **kwargs):
        raise Exception("Query failed")

    monkeypatch.setattr(db, "query", fail_query)

    with pytest.raises(ServiceError):
        crud.get_challenges(db=db)
