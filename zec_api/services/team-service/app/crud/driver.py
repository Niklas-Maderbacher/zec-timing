from app.database.dependency import SessionDep
from app.schemas.driver import DriverCreate, DriverUpdate
from app.models.driver import Driver
from app.exceptions.exceptions import EntityDoesNotExistError, InvalidOperationError, ServiceError, InsufficientPermissions
import requests
from app.core.config import settings 
from app.crud.team import get_team
from fastapi import Request

ATTEMPT_URL = settings.ATTEMPT_SERVICE_URL

def check_driver_permissions(*, db: SessionDep, driver_id: int | None = None, team_id: int | None = None, request: Request):
    role = request.headers.get("X-Role")
    user_team_id = request.headers.get("X-Team-Id")
    if role == "TEAM_LEAD":
        if driver_id is not None:
            driver = get_driver_no_perm_check(db=db, driver_id=driver_id)
            if driver.team_id != int(user_team_id):
                raise InsufficientPermissions(f"Teamleads can only operate on drivers in their own team. Driver {driver.name} does not belong to the same team as the user")
            return None
        elif team_id is not None:
            if team_id != int(user_team_id):
                raise InsufficientPermissions("Teamleads can only operate on their own team. Attempted to operate on a team that he is not assigned to")
    return None

def create_driver(*, db: SessionDep, driver: DriverCreate, request: Request):
    check_driver_permissions(db=db, team_id=driver.team_id, request=request)
    db_team = get_team(db=db, team_id=driver.team_id, request=request)
    if not db_team:
        raise EntityDoesNotExistError(
            message=f"Team with id {driver.team_id} does not exist"
        )
    try:
        driver_data = driver.model_dump(exclude_unset=True)
        db_driver = Driver(**driver_data)
        db.add(db_driver)
        db.commit()
        db.refresh(db_driver)
        return db_driver
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def update_driver(*, db: SessionDep, driver_id: int, driver_update: DriverUpdate, request: Request):
    check_driver_permissions(db=db, driver_id=driver_id, request=request)
    try:
        db_driver = get_driver_no_perm_check(db=db, driver_id=driver_id)
        if not db_driver:
            raise EntityDoesNotExistError(
                message=f"Driver with id {driver_id} does not exist"
            )
        update_data = driver_update.model_dump(
            exclude_unset=True,
            exclude={"id"},
        )
        for field, value in update_data.items():
            setattr(db_driver, field, value)
        db.commit()
        db.refresh(db_driver)
        return db_driver

    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def delete_driver(*, db: SessionDep, driver_id: int, request: Request):
    check_driver_permissions(db=db, driver_id=driver_id, request=request)
    db_attempts = requests.get(f"{ATTEMPT_URL}/api/attempts/per-driver/{driver_id}").json()
    if db_attempts and db_attempts.get('detail') != "No attempts found for this driver [Attemptservice]":
        raise InvalidOperationError(f"Cannot delete driver {driver_id} because they have made attempts")
    try:
        db_driver = get_driver_no_perm_check(db=db, driver_id=driver_id)
        if not db_driver:
            raise EntityDoesNotExistError(
                message=f"Driver with id {driver_id} does not exist"
            )
        db.delete(db_driver)
        db.commit()
        return db_driver
    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc
    
def get_driver_no_perm_check(*, db: SessionDep, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise EntityDoesNotExistError(
            message=f"Driver with id {driver_id} does not exist"
        )
    return driver

def get_driver(*, db: SessionDep, driver_id: int, request: Request):
    check_driver_permissions(db=db, driver_id=driver_id, request=request)
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise EntityDoesNotExistError(
            message=f"Driver with id {driver_id} does not exist"
        )
    return driver

def get_drivers(*, db: SessionDep):
    return db.query(Driver).all()

def get_drivers_by_team(*, db: SessionDep, team_id: int, request: Request):
    check_driver_permissions(db=db, team_id=team_id, request=request)
    db_drivers = db.query(Driver).filter(Driver.team_id == team_id).all()
    if not db_drivers:
        raise EntityDoesNotExistError(
            message=f"No drivers found for team with id {team_id}"
        )
    return db_drivers
