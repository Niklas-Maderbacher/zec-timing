from app.database.dependency import SessionDep
from app.schemas.challenge import ChallengeUpdate
from app.models.challenge import Challenge

def update_challenge(*, db: SessionDep, challenge_update: ChallengeUpdate):
    challenge_id = challenge_update.id
    db_challenge = get_challenge(db=db, challenge_id=challenge_id)
    update_data = challenge_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_challenge, field, value)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def get_challenge(*, db: SessionDep, challenge_id: int):
    return db.query(Challenge).filter(Challenge.id == challenge_id).first()

def get_challenge_by_name(*, db: SessionDep, challenge_name: str):
    return db.query(Challenge).filter(Challenge.name == challenge_name).first()

def get_challenges(*, db: SessionDep):
    return db.query(Challenge).all()