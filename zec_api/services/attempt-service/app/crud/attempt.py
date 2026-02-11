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
    if not db_challenge:
        raise EntityDoesNotExistError(f"Challenge {attempt.challenge_id} does not exist")
    attempt_count = get_attempts_for_team_per_challenge(db=db, team_id=attempt.team_id, challenge_id=attempt.challenge_id)
    if len(attempt_count) >= db_challenge["max_attempts"]:
        raise ServiceError("Maximum attempts reached for this challenge")
    db_attempt = Attempt(
        team_id = attempt.team_id,
        driver_id = attempt.driver_id,
        challenge_id = attempt.challenge_id,
        is_valid = attempt.is_valid,
        start_time = attempt.start_time,
        end_time = attempt.end_time,
        energy_used = attempt.energy_used,
    )
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    if attempt.penalty_count and attempt.penalty_type:
        penalty_payload = {
            "attempt_id": db_attempt.id,
            "count": attempt.penalty_count,
            "penalty_type_id": attempt.penalty_type,
        }
        pen_resp = requests.post(f"{SCORE_URL}/api/penalties/", json=penalty_payload)
        if pen_resp.status_code in (401, 403):
            raise AuthenticationFailed("Unauthorized to create penalty")
        if pen_resp.status_code != 200:
            raise ServiceError(f"Failed to create penalty for attempt {db_attempt.id}")
    score_payload = {"attempt_id": db_attempt.id}
    score_resp = requests.post(f"{SCORE_URL}/api/scores/", json=score_payload)
    if score_resp.status_code in (401, 403):
        raise AuthenticationFailed("Unauthorized to create score")
    if score_resp.status_code != 200:
        raise ServiceError(f"Failed to create score for attempt {db_attempt.id}")
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
    score_resp = requests.delete(f"{SCORE_URL}/api/scores/attempt/{attempt_id}")
    if score_resp.status_code in (401, 403):
        raise AuthenticationFailed("Unauthorized to delete score for attempt")
    if score_resp.status_code not in (200, 404):
        raise ServiceError(f"Failed to delete score for attempt {attempt_id}: {score_resp.text}")
    pen_resp = requests.delete(f"{SCORE_URL}/api/penalties/attempt/{attempt_id}")
    if pen_resp.status_code in (401, 403):
        raise AuthenticationFailed("Unauthorized to delete penalties for attempt")
    if pen_resp.status_code not in (200, 404):
        raise ServiceError(f"Failed to delete penalties for attempt {attempt_id}: {pen_resp.text}")
    return db_attempt

def get_attempt(*, db: SessionDep, attempt_id: int):
    db_attempt = db.query(Attempt).filter(Attempt.id == attempt_id).first()
    if not db_attempt:
        raise EntityDoesNotExistError(f"Attempt {attempt_id} does not exist")
    return db_attempt

def get_attempts(*, db: SessionDep):
    return db.query(Attempt).all()

def get_all_attempts_for_challenge(*, db: SessionDep, challenge_id: int):
    db_attempt = db.query(Attempt).filter(Attempt.challenge_id == challenge_id).all()
    if not db_attempt:
        raise EntityDoesNotExistError("No attempts found for this challenge")
    return db_attempt

def get_valid_attempts_for_challenge(*, db: SessionDep, challenge_id: int):
    db_attempt = db.query(Attempt).filter(Attempt.challenge_id == challenge_id, Attempt.is_valid).all()
    if not db_attempt:
        raise EntityDoesNotExistError("No valid attempts found for this challenge")
    return db_attempt

def get_fastest_attempt(*, db: SessionDep, challenge_id: int):
    db_attempts = (
        db.query(Attempt)
        .filter(
            Attempt.challenge_id == challenge_id, 
            Attempt.is_valid)
        .all()
    )
    if not db_attempts:
        raise EntityDoesNotExistError("Attempt does not exist")
    fastest = min(db_attempts, key=lambda a: (a.end_time - a.start_time))
    return fastest

def get_fastest_attempt_for_team(*, db: SessionDep, team_id: int, challenge_id: int):
    db_attempts = (
        db.query(Attempt)
        .filter(
            Attempt.team_id == team_id,
            Attempt.challenge_id == challenge_id,
            Attempt.is_valid

        )
        .all()
    )
    if not db_attempts:
        raise EntityDoesNotExistError("Attempt does not exist")
    fastest = min(db_attempts, key=lambda a: (a.end_time - a.start_time))
    return fastest

def get_least_energy_attempt(*, db: SessionDep, challenge_id: int):
    db_attempt = (
        db.query(Attempt)
        .filter(Attempt.challenge_id == challenge_id, Attempt.is_valid)
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
            Attempt.is_valid
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
            Attempt.is_valid
        )
        .all()
    )
    return db_attempts
