from app.database.dependency import SessionDep
from app.schemas.score import ScoreUpdate, ScoreCreate
from app.models.score import Score
from app.crud.challenge import get_challenge
import app.crud.attempt as attempt_crud
import app.crud.team as team_crud
import app.crud.driver as driver_crud

score_processors = {}

def calculate_f_pm(db, db_attempt):
    fastest_attempt = attempt_crud.get_fastest_attempt(db=db, challenge_id=db_attempt.challenge_id)
    db_team = team_crud.get_team(db=db, team_id=fastest_attempt.team_id)
    db_driver = driver_crud.get_driver(db=db, driver_id=fastest_attempt.driver_id)
    f_pm = (db_team.vehicle_weight + db_driver.weight) / fastest_attempt.average_power
    return f_pm

def register_score_processor(challenge_name):
    def decorator(func):
        score_processors[challenge_name] = func
        return func
    return decorator

@register_score_processor("Skidpad")
def handle_skidpad(db_attempt, db):
    fastest_attempt = attempt_crud.get_fastest_attempt(db=db, challenge_id=db_attempt.challenge_id)
    t_min = fastest_attempt.end_time - fastest_attempt.start_time
    fastest_attempt_team = attempt_crud.get_fastest_attempt_for_team(db=db, team_id=db_attempt.team_id, challenge_id=db_attempt.challenge_id)
    t_team = fastest_attempt_team.end_time-fastest_attempt_team.start_time
    return 100 * t_min / t_team

@register_score_processor("Acceleration")
def handle_acceleration(db_attempt, db):
    f_pm_best_team = calculate_f_pm(db, db_attempt)
    f_points = 50 - f_pm_best_team / 20
    fastest_attempt = attempt_crud.get_fastest_attempt(db=db, challenge_id=db_attempt.challenge_id)
    t_min = fastest_attempt.end_time - fastest_attempt.start_time
    fastest_attempt_team = attempt_crud.get_fastest_attempt_for_team(db=db, team_id=db_attempt.team_id, challenge_id=db_attempt.challenge_id)
    t_team = fastest_attempt_team.end_time-fastest_attempt_team.start_time
    f_pm = calculate_f_pm(db, db_attempt)
    score = f_points * t_min / t_team + f_pm / 20
    return score


@register_score_processor("Slalom")
def handle_slalom(db_attempt, db):
    fastest_attempt = attempt_crud.get_fastest_attempt(db=db, challenge_id=db_attempt.challenge_id)
    t_min = fastest_attempt.end_time - fastest_attempt.start_time
    fastest_attempt_team = attempt_crud.get_fastest_attempt_for_team(db=db, team_id=db_attempt.team_id, challenge_id=db_attempt.challenge_id)
    t_team = fastest_attempt_team.end_time-fastest_attempt_team.start_time
    return 100 * t_min / t_team

@register_score_processor("Endurance")
def handle_endurance(db_attempt, db):
    #Time Score
    fastest_attempt = attempt_crud.get_fastest_attempt(db=db, challenge_id=db_attempt.challenge_id)
    t_min = fastest_attempt.end_time - fastest_attempt.start_time
    fastest_attempt_team = attempt_crud.get_fastest_attempt_for_team(db=db, team_id=db_attempt.team_id, challenge_id=db_attempt.challenge_id)
    t_team = fastest_attempt_team.end_time-fastest_attempt_team.start_time
    time_score = 75 * t_min / t_team
    # Energy Score
    least_energy_attempt = attempt_crud.get_least_energy_attempt(db=db, challenge_id=db)
    e_min = least_energy_attempt.energy_used
    least_energy_attempt_team = attempt_crud.get_least_energy_attempt_for_team(db=db, team_id=db_attempt.team_id, challenge_id=db_attempt.challenge_id)
    e_team = least_energy_attempt_team.energy_used
    energy_score = 175 * e_min / e_team
    total_score = time_score + energy_score
    return total_score

def create_score(*, db: SessionDep, score: ScoreCreate):
    db_attempt  = attempt_crud.get_attempt(db=db, attempt_id=score.attempt_id)
    db_challenge = get_challenge(db=db, challenge_id=db_attempt.challenge_id)
    if processor := score_processors.get(db_challenge.name):
        score_value = processor(db_attempt, db)
    
    db_score = Score(attempt_id=score.attempt_id, value=score_value)
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
