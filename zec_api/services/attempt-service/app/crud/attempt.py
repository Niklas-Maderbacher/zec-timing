from app.database.dependency import SessionDep
from app.schemas.attempt import AttemptCreate, AttemptUpdate
from app.models.attempt import Attempt
from app.core.config import settings
import requests
from app.exceptions.exceptions import (
    ServiceError,
    EntityDoesNotExistError,
    AuthenticationFailed,
)

SCORE_URL = settings.SCORE_SERVICE_URL
TEAM_URL = settings.TEAM_SERVICE_URL
CHALLENGE_URL = settings.CHALLENGE_SERVICE_URL

def _validate_team(team_id: int):
    resp = requests.get(f"{TEAM_URL}/api/teams/{team_id}", params={"team_id": team_id})
    if resp.status_code == 404:
        raise EntityDoesNotExistError(f"Team {team_id} does not exist")
    if resp.status_code in (401, 403):
        raise AuthenticationFailed(f"Unauthorized to fetch team {team_id}")
    if resp.status_code != 200:
        raise ServiceError(f"Failed to fetch team {team_id}: {resp.text}")

def _validate_driver(driver_id: int):
    resp = requests.get(f"{TEAM_URL}/api/drivers/{driver_id}", params={"driver_id": driver_id})
    if resp.status_code == 404:
        raise EntityDoesNotExistError(f"Driver {driver_id} does not exist")
    if resp.status_code in (401, 403):
        raise AuthenticationFailed(f"Unauthorized to fetch driver {driver_id}")
    if resp.status_code != 200:
        raise ServiceError(f"Failed to fetch driver {driver_id}: {resp.text}")

def _validate_challenge(challenge_id: int):
    resp = requests.get(f"{CHALLENGE_URL}/api/challenges/{challenge_id}", params={"challenge_id": challenge_id})
    if resp.status_code == 404:
        raise EntityDoesNotExistError(f"Challenge {challenge_id} does not exist")
    if resp.status_code in (401, 403):
        raise AuthenticationFailed(f"Unauthorized to fetch challenge {challenge_id}")
    if resp.status_code != 200:
        raise ServiceError(f"Failed to fetch challenge {challenge_id}: {resp.text}")

def create_attempt(*, db: SessionDep, attempt: AttemptCreate):
    _validate_team(attempt.team_id)
    _validate_driver(attempt.driver_id)
    _validate_challenge(attempt.challenge_id)
    db_challenge = requests.get(f"{CHALLENGE_URL}/api/challenges/{attempt.challenge_id}").json()
    attempt_count = get_attempts_for_team_per_challenge(db=db, team_id=attempt.team_id, challenge_id=attempt.challenge_id)
    if len(attempt_count) >= db_challenge["max_attempts"]:
        raise ServiceError("Maximum attempts reached for this challenge")
    attempt_data = attempt.model_dump(exclude_unset=True)
    db_attempt = Attempt(**attempt_data)
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    payload = {"attempt_id": db_attempt.id}
    resp = requests.post(f"{SCORE_URL}/api/scores/", json=payload)
    if resp.status_code in (401, 403):
        raise AuthenticationFailed("Unauthorized to create score")
    if resp.status_code != 200:
        raise ServiceError(f"Failed to create score for attempt {db_attempt.id}: {resp.text}")
    return db_attempt

def update_attempt(*, db: SessionDep, attempt_id: int, attempt_update: AttemptUpdate):
    db_attempt = get_attempt(db=db, attempt_id=attempt_id)
    update_data = attempt_update.model_dump(exclude_unset=True, exclude={"id"})
    for field, value in update_data.items():
        setattr(db_attempt, field, value)
    if "is_valid" in update_data and update_data.get("is_valid") is False:
        resp = requests.delete(f"{SCORE_URL}/api/scores/attempt/{db_attempt.id}")
        if resp.status_code in (401, 403):
            raise AuthenticationFailed("Unauthorized to delete score for attempt")
        if resp.status_code not in (200, 404):
            raise ServiceError(f"Failed to delete score for attempt {db_attempt.id}: {resp.text}")
    db.commit()
    db.refresh(db_attempt)
    return db_attempt

def delete_attempt(*, db: SessionDep, attempt_id: int):
    db_attempt = get_attempt(db=db, attempt_id=attempt_id)
    db.delete(db_attempt)
    db.commit()
    return db_attempt

def get_attempt(*, db: SessionDep, attempt_id: int):
    db_attempt = db.query(Attempt).filter(Attempt.id == attempt_id).first()
    if not db_attempt:
        raise EntityDoesNotExistError(f"Attempt {attempt_id} does not exist")
    return db_attempt

def get_attempts(*, db: SessionDep):
    return db.query(Attempt).all()

def get_attempts_for_challenge(*, db: SessionDep, challenge_id: int):
    db_attempt = db.query(Attempt).filter(Attempt.challenge_id == challenge_id, Attempt.is_valid == True).all()
    if not db_attempt:
        raise EntityDoesNotExistError("Attempt does not exist")
    return db_attempt

def get_fastest_attempt(*, db: SessionDep, challenge_id: int):
    db_attempt = (
        db.query(Attempt)
        .filter(Attempt.challenge_id == challenge_id, Attempt.is_valid == True)
        .order_by(Attempt.end_time - Attempt.start_time)
        .first()
    )
    if not db_attempt:
        raise EntityDoesNotExistError("Attempt does not exist")
    return db_attempt

def get_fastest_attempt_for_team(*, db: SessionDep, team_id: int, challenge_id: int):
    db_attempt = (
        db.query(Attempt)
        .filter(
            Attempt.team_id == team_id,
            Attempt.challenge_id == challenge_id,
            Attempt.is_valid == True
        )
        .order_by(Attempt.end_time - Attempt.start_time)
        .first()
    )
    if not db_attempt:
        raise EntityDoesNotExistError("Attempt does not exist")
    return db_attempt

def get_least_energy_attempt(*, db: SessionDep, challenge_id: int):
    db_attempt = (
        db.query(Attempt)
        .filter(Attempt.challenge_id == challenge_id, Attempt.is_valid == True)
        .order_by(Attempt.energy_used)
        .first()
    )
    if not db_attempt:
        raise EntityDoesNotExistError("Attempt does not exist")
    return db_attempt

def get_least_energy_attempt_for_team(*, db: SessionDep, team_id: int, challenge_id: int):
    db_attempt = (
        db.query(Attempt)
        .filter(
            Attempt.team_id == team_id,
            Attempt.challenge_id == challenge_id,
            Attempt.is_valid == True
        )
        .order_by(Attempt.energy_used)
        .first()
    )
    if not db_attempt:
        raise EntityDoesNotExistError("Attempt does not exist")
    return db_attempt

def get_attempts_for_team_per_challenge(*, db: SessionDep, team_id: int, challenge_id: int):
    db_attempts = (
        db.query(Attempt)
        .filter(
            Attempt.team_id == team_id,
            Attempt.challenge_id == challenge_id,
            Attempt.is_valid == True
        )
        .all()
    )
    return db_attempts
