from app.database.dependency import SessionDep
from app.schemas.attempt import AttemptCreate, AttemptUpdate
from app.models.attempt import Attempt

def create_attempt(*, db: SessionDep, attempt: AttemptCreate):
    attempt_data = attempt.model_dump(exclude_unset=True)
    db_attempt = Attempt(**attempt_data)
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt

def update_attempt(*, db: SessionDep, attempt_update: AttemptUpdate):
    attempt_id = attempt_update.id
    db_attempt = get_attempt(db=db, attempt_id=attempt_id)
    update_data = attempt_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_attempt, field, value)
    db.commit()
    db.refresh(db_attempt)
    return db_attempt

def delete_attempt(*, db: SessionDep, attempt_id: int):
    db_attempt = get_attempt(db=db, attempt_id=attempt_id)
    db.delete(db_attempt)
    db.commit()
    return db_attempt

def get_attempt(*, db: SessionDep, attempt_id: int):
    return db.query(Attempt).filter(Attempt.id == attempt_id).first()

def get_attempts(*, db: SessionDep):
    return db.query(Attempt).all()

def get_fastest_attempt(*, db: SessionDep, challenge_id: int):
    return (db.query(Attempt)
              .filter(Attempt.challenge_id == challenge_id)
              .order_by(Attempt.end_time - Attempt.start_time)
              .first())

def get_fastest_attempt_for_team(*, db: SessionDep, team_id: int, challenge_id: int):
    return (db.query(Attempt)
              .filter(
                  Attempt.team_id == team_id,
                  Attempt.challenge_id == challenge_id
              )
              .order_by(Attempt.end_time - Attempt.start_time)
              .first())

def get_least_energy_attempt(*, db: SessionDep, challenge_id: int):
    return (db.query(Attempt)
              .filter(Attempt.challenge_id == challenge_id)
              .order_by(Attempt.energy_used)
              .first())

def get_least_energy_attempt_for_team(*, db: SessionDep, team_id: int, challenge_id: int):
    return (db.query(Attempt)
              .filter(
                  Attempt.team_id == team_id,
                  Attempt.challenge_id == challenge_id
              )
              .order_by(Attempt.energy_used)
              .first())