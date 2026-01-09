from app.database.dependency import SessionDep
from app.schemas.driver import DriverCreate, DriverUpdate
from app.models.driver import Driver
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError

def create_driver(*, db: SessionDep, driver: DriverCreate):
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

def update_driver(*, db: SessionDep, driver_id: int, driver_update: DriverUpdate):
    try:
        db_driver = get_driver(db=db, driver_id=driver_id)
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

def delete_driver(*, db: SessionDep, driver_id: int):
    try:
        db_driver = get_driver(db=db, driver_id=driver_id)
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

def get_driver(*, db: SessionDep, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise EntityDoesNotExistError(
            message=f"Driver with id {driver_id} does not exist"
        )
    return driver

def get_drivers(*, db: SessionDep):
    return db.query(Driver).all()
