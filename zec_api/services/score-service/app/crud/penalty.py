from app.database.dependency import SessionDep
from app.schemas.penalty import PenaltyCreate, PenaltyUpdate
from app.models.penalty import Penalty
from app.models.penalty_type import PenaltyType
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError
from app.core.config import settings
import requests

ATTEMPT_URL = settings.ATTEMPT_SERVICE_URL

def create_penalty(*, db: SessionDep, penalty: PenaltyCreate):
    response = requests.get(f"{ATTEMPT_URL}/api/attempts/{penalty.attempt_id}")
    if response.status_code != 200:
        raise ServiceError("Failed to fetch attempt")
    penaltytyp = db.query(PenaltyType).filter(PenaltyType.id == penalty.penalty_type_id).first()
    if not penaltytyp:
        raise EntityDoesNotExistError("PenaltyType does not exist")
    try:
        penalty_data = penalty.model_dump(exclude_unset=True)
        db_penalty = Penalty(**penalty_data)
        db.add(db_penalty)
        db.commit()
        db.refresh(db_penalty)
        return db_penalty
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def update_penalty(*, db: SessionDep, penalty_id: int, penalty_update: PenaltyUpdate):
    try:
        db_penalty = get_penalty(db=db, penalty_id=penalty_id)
        update_data = penalty_update.model_dump(
            exclude_unset=True,
            exclude={"id"},
        )
        for field, value in update_data.items():
            setattr(db_penalty, field, value)
        db.commit()
        db.refresh(db_penalty)
        return db_penalty

    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def delete_penalty(*, db: SessionDep, penalty_id: int):
    try:
        db_penalty = get_penalty(db=db, penalty_id=penalty_id)
        db.delete(db_penalty)
        db.commit()
        return db_penalty
    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc
    
def delete_penalties_by_attempt(*, db: SessionDep, attempt_id: int):
    try:
        db_penalties = get_penalties_by_attempt(db=db, attempt_id=attempt_id)
        for penalty in db_penalties:
            db.delete(penalty)
        db.commit()
        return db_penalties
    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def get_penalty(*, db: SessionDep, penalty_id: int):
    penalty = db.query(Penalty).filter(Penalty.id == penalty_id).first()
    if not penalty:
        raise EntityDoesNotExistError(
            message=f"Penalty with id {penalty_id} does not exist"
        )
    return penalty

def get_penalties(*, db: SessionDep):
    return db.query(Penalty).all()

def get_penalties_by_attempt(*, db: SessionDep, attempt_id: int):
    db_penalties = db.query(Penalty).filter(Penalty.attempt_id == attempt_id).all()
    if not db_penalties:
        raise EntityDoesNotExistError(
            message=f"No penalties found for attempt id {attempt_id}"
        )
    return db_penalties

def get_all_penalty_types(*, db: SessionDep):
    types = db.query(PenaltyType).all()
    return types