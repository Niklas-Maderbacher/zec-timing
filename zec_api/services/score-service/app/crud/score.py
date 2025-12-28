from app.database.dependency import SessionDep
from app.schemas.score import ScoreUpdate, ScoreCreate
from app.models.score import Score
from app.core.config import settings
import requests
from datetime import datetime

CHALLENGE_URL = settings.CHALLENGE_SERVICE_URL
ATTEMPT_URL = settings.ATTEMPT_SERVICE_URL
TEAM_URL = settings.TEAM_SERVICE_URL
DRIVER_URL = settings.DRIVER_SERVICE_URL

score_processors = {}

def calculate_f_pm(db_attempt):
    fastest_attempt = requests.get(f"{ATTEMPT_URL}/api/attempts/fast/", params={"challenge_id": db_attempt.challenge_id}).json()
    team = requests.get(f"{TEAM_URL}/api/teams/{fastest_attempt['team_id']}").json()
    driver = requests.get(f"{DRIVER_URL}/api/drivers/{fastest_attempt['driver_id']}").json()
    f_pm = (team["vehicle_weight"] + driver["weight"]) / fastest_attempt["average_power"]
    return f_pm


def register_score_processor(challenge_name):
    def decorator(func):
        score_processors[challenge_name] = func
        return func
    return decorator

@register_score_processor("Skidpad")
def handle_skidpad(db_attempt):
    fastest_attempt = requests.get(f"{ATTEMPT_URL}/api/attempts/fast/", params={"challenge_id": db_attempt["challenge_id"]}).json()
    t_min = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    fastest_attempt_team = requests.get(f"{ATTEMPT_URL}/api/attempts/fast/per-team", params={"team_id": db_attempt["team_id"], "challenge_id": db_attempt["challenge_id"]}).json()
    t_team = datetime.strptime(fastest_attempt_team["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(fastest_attempt_team["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    return 100 * t_min / t_team

@register_score_processor("Acceleration")
def handle_acceleration(db_attempt):
    f_pm_best_team = calculate_f_pm(db_attempt)
    f_points = 50 - f_pm_best_team / 20
    fastest_attempt = requests.get(f"{ATTEMPT_URL}/api/attempts/fast", params={"challenge_id": db_attempt.challenge_id}).json()
    t_min = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    fastest_attempt_team = requests.get(f"{ATTEMPT_URL}/api/attempts/fast/per-team", params={"team_id": db_attempt.team_id, "challenge_id": db_attempt.challenge_id}).json()
    t_team = datetime.strptime(fastest_attempt_team["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(fastest_attempt_team["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    f_pm = calculate_f_pm(db_attempt)
    score = f_points * t_min / t_team + f_pm / 20
    return score

@register_score_processor("Slalom")
def handle_slalom(db_attempt):
    fastest_attempt = requests.get(f"{ATTEMPT_URL}/api/attempts/fast", params={"challenge_id": db_attempt.challenge_id}).json()
    t_min = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    fastest_attempt_team = requests.get(f"{ATTEMPT_URL}/api/attempts/fast/per-team", params={"team_id": db_attempt.team_id, "challenge_id": db_attempt.challenge_id}).json()
    t_team = fastest_attempt_team["end_time"] - fastest_attempt_team["start_time"]
    return 100 * t_min / t_team

@register_score_processor("Endurance")
def handle_endurance(db_attempt):
    # Time score
    fastest_attempt = requests.get(f"{ATTEMPT_URL}/api/attempts/fast", params={"challenge_id": db_attempt.challenge_id}).json()
    t_min = datetime.strptime(fastest_attempt["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(fastest_attempt["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    fastest_attempt_team = requests.get(f"{ATTEMPT_URL}/api/attempts/fast/per-team", params={"team_id": db_attempt.team_id, "challenge_id": db_attempt.challenge_id}).json()
    t_team = datetime.strptime(fastest_attempt_team["end_time"], "%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(fastest_attempt_team["start_time"], "%Y-%m-%dT%H:%M:%S.%f")
    time_score = 75 * t_min / t_team
    # Energy score
    least_energy_attempt = requests.get(f"{ATTEMPT_URL}/api/attempts/least-energy",params={"challenge_id": db_attempt.challenge_id}).json()
    e_min = least_energy_attempt["energy_used"]
    least_energy_attempt_team = requests.get(f"{ATTEMPT_URL}/api/attempts/least-energy/per-team",params={"team_id": db_attempt.team_id, "challenge_id": db_attempt.challenge_id}).json()
    e_team = least_energy_attempt_team["energy_used"]
    energy_score = 175 * e_min / e_team
    return time_score + energy_score

def create_score(*, db: SessionDep, score: ScoreCreate):
    db_attempt = requests.get(f"{ATTEMPT_URL}/api/attempts/{score.attempt_id}").json()
    challenge = requests.get(f"{CHALLENGE_URL}/api/challenges/{db_attempt['challenge_id']}", params={"challenge_id": db_attempt["challenge_id"]}).json()
    if processor := score_processors.get(challenge["name"]):
        score_value = processor(db_attempt)
    db_score = Score(
        attempt_id=score.attempt_id,
        challenge_id=db_attempt["challenge_id"],
        value=score_value
    )
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

def update_score(*, db: SessionDep, score_update: ScoreUpdate):
    score_id = score_update.id
    db_score = get_score(db=db, score_id=score_id)
    update_data = score_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_score, field, value)
    db.commit()
    db.refresh(db_score)
    return db_score

def get_score(*, db: SessionDep, score_id: int):
    return db.query(Score).filter(Score.id == score_id).first()

def get_scores(*, db: SessionDep):
    return db.query(Score).all()

def get_score_for_attempt(*, db: SessionDep, attempt_id: int):
    return db.query(Score).filter(Score.attempt_id == attempt_id).first()
