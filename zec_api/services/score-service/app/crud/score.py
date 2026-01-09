from app.database.dependency import SessionDep
from app.schemas.score import ScoreUpdate, ScoreCreate
from app.models.score import Score
from app.core.config import settings
import requests
from datetime import datetime
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

def calculate_f_pm(db_attempt):
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code != 200:
        raise ServiceError("Failed to fetch fastest attempt")
    fastest_attempt = resp.json()
    team_resp = requests.get(f"{TEAM_URL}/api/teams/{fastest_attempt['team_id']}")
    if team_resp.status_code == 404:
        raise EntityDoesNotExistError("Team does not exist")
    if team_resp.status_code != 200:
        raise ServiceError(team_resp.text)
    driver_resp = requests.get(f"{TEAM_URL}/api/drivers/{fastest_attempt['driver_id']}")
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
def handle_skidpad(db_attempt):
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code == 404:
        raise EntityDoesNotExistError("Fastest attempt not found")
    if resp.status_code != 200:
        raise ServiceError(resp.text)
    fastest_attempt = resp.json()
    resp_team = requests.get(
        f"{ATTEMPT_URL}/api/attempts/fastest/per-team/",
        params={"team_id": db_attempt["team_id"], "challenge_id": db_attempt["challenge_id"]}
    )
    if resp_team.status_code == 404:
        raise EntityDoesNotExistError("Team attempt not found")
    if resp_team.status_code != 200:
        raise ServiceError(resp_team.text)
    fastest_attempt_team = resp_team.json()

    t_min = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
            datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    t_team = datetime.strptime(fastest_attempt_team["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
             datetime.strptime(fastest_attempt_team["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    return 100 * t_min.total_seconds() / t_team.total_seconds()

@register_score_processor("Acceleration")
def handle_acceleration(db_attempt):
    try:
        f_pm_best_team = calculate_f_pm(db_attempt)
    except ScoreserviceApiError:
        raise
    f_points = 50 - f_pm_best_team / 20
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code != 200:
        raise ServiceError("Failed to fetch fastest attempt")
    fastest_attempt = resp.json()
    t_min = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
            datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    t_min_seconds = t_min.total_seconds()
    resp_team = requests.get(
        f"{ATTEMPT_URL}/api/attempts/fastest/per-team/",
        params={"team_id": db_attempt["team_id"], "challenge_id": db_attempt["challenge_id"]}
    )
    if resp_team.status_code != 200:
        raise ServiceError("Failed to fetch team fastest attempt")
    fastest_attempt_team = resp_team.json()
    t_team = datetime.strptime(fastest_attempt_team["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
             datetime.strptime(fastest_attempt_team["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    t_team_seconds = t_team.total_seconds()
    f_pm = calculate_f_pm(db_attempt)
    return f_points * (t_min_seconds / t_team_seconds) + f_pm / 20


@register_score_processor("Slalom")
def handle_slalom(db_attempt):
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code != 200:
        raise ServiceError("Failed to fetch fastest attempt")
    fastest_attempt = resp.json()
    t_min = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
            datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    resp_team = requests.get(
        f"{ATTEMPT_URL}/api/attempts/fastest/per-team/",
        params={"team_id": db_attempt["team_id"], "challenge_id": db_attempt["challenge_id"]}
    )
    if resp_team.status_code != 200:
        raise ServiceError("Failed to fetch team fastest attempt")
    fastest_attempt_team = resp_team.json()
    t_team = datetime.strptime(fastest_attempt_team["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
             datetime.strptime(fastest_attempt_team["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    return 100 * t_min.total_seconds() / t_team.total_seconds()

@register_score_processor("Endurance")
def handle_endurance(db_attempt):
    # Time score
    resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{db_attempt['challenge_id']}")
    if resp.status_code != 200:
        raise ServiceError("Failed to fetch fastest attempt")
    fastest_attempt = resp.json()
    t_min = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
            datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    resp_team = requests.get(
        f"{ATTEMPT_URL}/api/attempts/fastest/per-team/",
        params={"team_id": db_attempt["team_id"], "challenge_id": db_attempt["challenge_id"]}
    )
    if resp_team.status_code != 200:
        raise ServiceError("Failed to fetch team fastest attempt")
    fastest_attempt_team = resp_team.json()
    t_team = datetime.strptime(fastest_attempt_team["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - \
             datetime.strptime(fastest_attempt_team["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    time_score = 75 * t_min.total_seconds() / t_team.total_seconds()
    # Energy score
    resp_energy = requests.get(
        f"{ATTEMPT_URL}/api/attempts/least-energy",
        params={"challenge_id": db_attempt["challenge_id"]}
    )
    if resp_energy.status_code != 200:
        raise ServiceError("Failed to fetch least-energy attempt")
    least_energy_attempt = resp_energy.json()
    e_min = least_energy_attempt["energy_used"]
    resp_energy_team = requests.get(
        f"{ATTEMPT_URL}/api/attempts/least-energy/per-team/",
        params={"team_id": db_attempt["team_id"], "challenge_id": db_attempt["challenge_id"]}
    )
    if resp_energy_team.status_code != 200:
        raise ServiceError("Failed to fetch team least-energy attempt")
    least_energy_attempt_team = resp_energy_team.json()
    e_team = least_energy_attempt_team["energy_used"]
    energy_score = 175 * e_min / e_team
    return time_score + energy_score

def create_score(*, db: SessionDep, score: ScoreCreate):
    attempt_resp = requests.get(f"{ATTEMPT_URL}/api/attempts/{score.attempt_id}")
    if attempt_resp.status_code == 404:
        raise EntityDoesNotExistError("Attempt does not exist")
    if attempt_resp.status_code != 200:
        raise ServiceError(attempt_resp.text)
    db_attempt = attempt_resp.json()
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
    score_value = processor(db_attempt)
    recalculate_acceleration_scores(
        db=db,
        challenge_id=db_attempt["challenge_id"],
    )
    db_score = Score(
        attempt_id=score.attempt_id,
        challenge_id=db_attempt["challenge_id"],
        value=score_value,
        created_at=datetime.utcnow(),
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
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

def recalculate_acceleration_scores(*, db: SessionDep, challenge_id: int):
    challenge_resp = requests.get(f"{CHALLENGE_URL}/api/challenges/{challenge_id}")
    if challenge_resp.status_code != 200:
        raise ServiceError("Failed to fetch challenge")
    challenge = challenge_resp.json()
    if challenge["name"] != "Acceleration":
        return False
    fastest_resp = requests.get(f"{ATTEMPT_URL}/api/attempts/fastest/{challenge_id}")
    if fastest_resp.status_code != 200:
        raise ServiceError("Failed to fetch fastest attempt")
    #fastest_attempt = fastest_resp.json()
    attempts_resp = requests.get(
        f"{ATTEMPT_URL}/api/attempts/",
        params={"challenge_id": challenge_id}
    )
    if attempts_resp.status_code != 200:
        raise ServiceError("Failed to fetch attempts")
    attempts = attempts_resp.json()
    for attempt in attempts:
        existing_score = (
            db.query(Score)
            .filter(Score.attempt_id == attempt["id"])
            .first()
        )
        if existing_score:
            existing_score.value = handle_acceleration(attempt)
    db.commit()
    return True
