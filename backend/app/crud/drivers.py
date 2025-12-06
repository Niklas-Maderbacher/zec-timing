from sqlalchemy.orm import Session

from app.models.drivers import Driver as model_driv
from app.schemas.drivers import Driver as schema_driv

def get_drivers(db: Session) -> list[schema_driv]:
    drivers_db = db.query(model_driv).all()

    drivers = []

    for driver in drivers_db:
        drivers.append(schema_driv(
            id=driver.id,
            driver_name=driver.name,
            team_id=driver.team_id,
        ))

    return drivers
