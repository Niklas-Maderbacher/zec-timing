from app.database.dependency import SessionDep
from app.schemas.driver import DriverCreate, DriverUpdate
from app.models.driver import Driver

def create_driver(*, db: SessionDep, driver: DriverCreate):
    driver_data = driver.model_dump(exclude_unset=True)
    db_driver = Driver(**driver_data)
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver

def update_driver(*, db: SessionDep, driver_update: DriverUpdate):
    driver_id = driver_update.id
    db_driver = get_driver(db=db, driver_id=driver_id)
    update_data = driver_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_driver, field, value)
    db.commit()
    db.refresh(db_driver)
    return db_driver

def delete_driver(*, db: SessionDep, driver_id: int):
    db_driver = get_driver(db=db, driver_id=driver_id)
    db.delete(db_driver)
    db.commit()
    return db_driver

def get_driver(*, db: SessionDep, driver_id: int):
    return db.query(Driver).filter(Driver.id == driver_id).first()

def get_drivers(*, db: SessionDep):
    return db.query(Driver).all()
