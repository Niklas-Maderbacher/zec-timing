from app.database.dependency import SessionDep
from app.schemas.score import ScoreUpdate, ScoreCreate
from app.models.score import Score
from app.models.penalty_type import PenaltyType
from datetime import timedelta
from app.core.config import settings
import requests
from app.crud.penalty import get_penalties_by_attempt
from datetime import datetime, timezone
from app.exceptions.exceptions import (
    ScoreserviceApiError,
    EntityDoesNotExistError,
    InvalidOperationError,
    ServiceError,
)

CHALLENGE_URL = settings.CHALLENGE_SERVICE_URL
ATTEMPT_URL = settings.ATTEMPT_SERVICE_URL
TEAM_URL = settings.TEAM_SERVICE_URL

score_processors = {}

def apply_penalties_to_attempt(db, attempt):
    try:
        penalties = get_penalties_by_attempt(db, attempt['id'])
        total_penalty_time = 0
        for penalty in penalties:
            penalty_type = db.query(PenaltyType).filter(PenaltyType.id == penalty.penalty_type_id).first()
            if penalty_type:
                total_penalty_time += penalty_type.amount * penalty.count
        if total_penalty_time > 0:
            end_time = datetime.strptime(attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f")
            end_time += timedelta(seconds=total_penalty_time)
            attempt["end_time"] = end_time.strftime("%Y-%m-%dT%H:%M:%S.%f")
    except Exception:
        pass
    return attempt

def calculate_f_pm(db_attempt):
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/{db_attempt['id']}")
    if resp.status_code != 200:
        raise ServiceError("Failed to get attempt")
    attempt = resp.json()
    team_resp = requests.get(f"{TEAM_URL}/api/teams/{attempt['team_id']}")
    if team_resp.status_code == 404:
        raise EntityDoesNotExistError("Team does not exist")
    if team_resp.status_code != 200:
        raise ServiceError(team_resp.text)
    driver_resp = requests.get(f"{TEAM_URL}/api/drivers/{attempt['driver_id']}")
    if driver_resp.status_code == 404:
        raise EntityDoesNotExistError("Driver does not exist")
    if driver_resp.status_code != 200:
        raise ServiceError(driver_resp.text)
    team = team_resp.json()
    driver = driver_resp.json()
    return (team["vehicle_weight"] + driver["weight"]) / team["mean_power"]

def register_score_processor(challenge_name):
    def decorator(func):
        score_processors[challenge_name] = func
        return func
    return decorator

@register_score_processor("Skidpad")
def handle_skidpad(db_attempt, db=None):
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code == 404:
        raise EntityDoesNotExistError("Fastest attempt not found")
    if resp.status_code != 200:
        raise ServiceError(resp.text)
    fastest_attempt = resp.json()
    if db:
        fastest_attempt = apply_penalties_to_attempt(db, fastest_attempt)
    best_time = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
            datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    team_time = datetime.strptime(db_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
             datetime.strptime(db_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    return round(100 * best_time.total_seconds() / team_time.total_seconds(), 2)

@register_score_processor("Acceleration")
def handle_acceleration(db_attempt, db=None):
    try:
        f_pm_besteam_time = calculate_f_pm(db_attempt)
    except ScoreserviceApiError:
        raise
    f_points = 50 - f_pm_besteam_time / 20
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code != 200:
        raise ServiceError("Failed to get fastest attempt")
    fastest_attempt = resp.json()
    if db:
        fastest_attempt = apply_penalties_to_attempt(db, fastest_attempt)
    best_time = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
            datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    team_time = datetime.strptime(db_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
             datetime.strptime(db_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    f_pm = calculate_f_pm(db_attempt)
    return round(f_points * (best_time.total_seconds() / team_time.total_seconds()) + f_pm / 20, 2)

@register_score_processor("Slalom")
def handle_slalom(db_attempt, db=None):
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code != 200:
        raise ServiceError("Failed to get fastest attempt")
    fastest_attempt = resp.json()
    if db:
        fastest_attempt = apply_penalties_to_attempt(db, fastest_attempt)
    best_time = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
            datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    team_time = datetime.strptime(db_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
             datetime.strptime(db_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    return round(100 * best_time.total_seconds() / team_time.total_seconds(), 2)

@register_score_processor("Endurance")
def handle_endurance(db_attempt, db=None):
    # Time score
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code != 200:
        raise ServiceError("Failed to get fastest attempt")
    fastest_attempt = resp.json()
    if db:
        fastest_attempt = apply_penalties_to_attempt(db, fastest_attempt)
    best_time = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
            datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    team_time = datetime.strptime(db_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
             datetime.strptime(db_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    time_score = 75 * best_time.total_seconds() / team_time.total_seconds()
    # Energy score
    resp_energy = requests.get(f"{ATTEMPT_URL}/api/attempts/least-energy/{db_attempt['challenge_id']}")
    if resp_energy.status_code != 200:
        raise ServiceError("Failed to get least-energy attempt")
    least_energy_attempt = resp_energy.json()
    e_min = least_energy_attempt["energy_used"]
    e_team = db_attempt["energy_used"]
    energy_score = 175 * e_min / e_team
    return round(time_score + energy_score, 2)

def create_score(*, db: SessionDep, score: ScoreCreate):
    attempt_resp = requests.get(f"{ATTEMPT_URL}/api/attempts/{score.attempt_id}")
    if attempt_resp.status_code == 404:
        raise EntityDoesNotExistError("Attempt does not exist")
    if attempt_resp.status_code != 200:
        raise ServiceError(attempt_resp.text)
    db_attempt = attempt_resp.json()
    db_attempt = apply_penalties_to_attempt(db, db_attempt)
    challenge_resp = requests.get(
        f"{CHALLENGE_URL}/api/challenges/{db_attempt['challenge_id']}"
    )
    if challenge_resp.status_code == 404:
        raise EntityDoesNotExistError("Challenge does not exist")
    if challenge_resp.status_code != 200:
        raise ServiceError("Failed to create score")
    challenge = challenge_resp.json()
    processor = score_processors.get(challenge["name"])
    if not processor:
        raise InvalidOperationError(
            f"No score processor registered for {challenge['name']}"
        )
    score_value = processor(db_attempt, db=db)
    db_score = Score(
        attempt_id=score.attempt_id,
        challenge_id=db_attempt["challenge_id"],
        value=score_value,
        created_at=datetime.now(timezone.utc),
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    try:
        fastest_resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
        if fastest_resp.status_code == 200:
            fastest_attempt = fastest_resp.json()
            if fastest_attempt['id'] == score.attempt_id:
                recalculate_scores_for_challenge(db=db, challenge_id=db_attempt['challenge_id'])
    except Exception:
        pass
    return db_score

def update_score(*, db: SessionDep, score_id: int, score_update: ScoreUpdate):
    db_score = get_score(db=db, score_id=score_id)
    if not db_score:
        raise EntityDoesNotExistError("Score does not exist")
    update_data = score_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_score, field, value)
    db.commit()
    db.refresh(db_score)
    return db_score

def delete_score(*, db: SessionDep, score_id: int):
    db_score = get_score(db=db, score_id=score_id)
    if not db_score:
        raise EntityDoesNotExistError("Score does not exist")
    db.delete(db_score)
    db.commit()
    return db_score

def delete_scores_for_attempt(*, db: SessionDep, attempt_id: int):
    db_scores = db.query(Score).filter(Score.attempt_id == attempt_id).all()
    if not db_scores:
        raise EntityDoesNotExistError("No scores found for the given attempt")
    for db_score in db_scores:
        db.delete(db_score)
    db.commit()
    return db_scores

def get_score(*, db: SessionDep, score_id: int):
    db_score = db.query(Score).filter(Score.id == score_id).first()
    if not db_score:
        raise EntityDoesNotExistError(f"No score for id: {score_id}")
    return db_score

def get_scores(*, db: SessionDep):
    return db.query(Score).all()

def get_score_for_attempt(*, db: SessionDep, attempt_id: int):
    db_score = db.query(Score).filter(Score.attempt_id == attempt_id).first()
    if not db_score:
        raise EntityDoesNotExistError(f"No score for attempt_id: {attempt_id}")
    return db_score

def recalculate_scores_for_challenge(*, db: SessionDep, challenge_id: int):
    attempts_resp = requests.get(f"{ATTEMPT_URL}/api/attempts?challenge_id={challenge_id}")
    if attempts_resp.status_code != 200:
        raise ServiceError("Failed to get attempts for challenge")
    attempts = attempts_resp.json()
    if not attempts:
        return []
    challenge_resp = requests.get(f"{CHALLENGE_URL}/api/challenges/{challenge_id}")
    if challenge_resp.status_code != 200:
        raise ServiceError("Failed to get challenge")
    challenge = challenge_resp.json()
    processor = score_processors.get(challenge["name"])
    updated_scores = []
    for attempt in attempts:
        db_attempt = apply_penalties_to_attempt(db, attempt)
        score_value = processor(db_attempt, db=db)
        score = db.query(Score).filter(
            Score.attempt_id == attempt['id']
        ).first()
        if score:
            score.value = score_value
            db.add(score)
        updated_scores.append(attempt['id'])
    db.commit()
    return updated_scores
