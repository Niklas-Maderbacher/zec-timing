from app.database.dependency import SessionDep
from app.schemas.challenge import ChallengeUpdate
from app.models.challenge import Challenge
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError

def update_challenge(*, db: SessionDep, challenge_id: int, challenge_update: ChallengeUpdate):
    try:
        db_challenge = get_challenge(db=db, challenge_id=challenge_id)
        if not db_challenge:
            raise EntityDoesNotExistError(
                message=f"Challenge with id {challenge_id} does not exist"
            )
        update_data = challenge_update.model_dump(
            exclude_unset=True,
            exclude={"id"},
        )
        for field, value in update_data.items():
            setattr(db_challenge, field, value)
        db.commit()
        db.refresh(db_challenge)
        return db_challenge
    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError(message="Failed to update challenge") from exc

def get_challenge(*, db: SessionDep, challenge_id: int):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise EntityDoesNotExistError(
            message=f"Challenge with id {challenge_id} does not exist"
        )
    return challenge

def get_challenge_by_name(*, db: SessionDep, challenge_name: str):
    challenge = db.query(Challenge).filter(Challenge.name == challenge_name).first()
    if not challenge:
        raise EntityDoesNotExistError(
            message=f"Challenge with name '{challenge_name}' does not exist"
        )
    return challenge

def get_challenges(*, db: SessionDep):
    try:
        return db.query(Challenge).all()
    except Exception as exc:
        raise ServiceError(message="Failed to retrieve challenges") from exc
