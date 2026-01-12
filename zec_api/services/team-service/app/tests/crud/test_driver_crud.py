import pytest
from app.crud.driver import (
    create_driver,
    get_driver,
    get_drivers,
    update_driver,
    delete_driver,
)
from app.schemas.driver import DriverCreate, DriverUpdate
from app.exceptions.exceptions import EntityDoesNotExistError, ServiceError

def test_get_driver(db, seeded_data):
    driver = seeded_data["drivers"][0]
    fetched = get_driver(db=db, driver_id=driver.id)
    assert fetched.name == driver.name

def test_list_drivers(db, seeded_data):
    drivers = get_drivers(db=db)
    assert len(drivers) == 2

def test_delete_driver(db, seeded_data):
    driver = seeded_data["drivers"][0]
    deleted = delete_driver(db=db, driver_id=driver.id)
    assert deleted.id == driver.id

def test_get_driver_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        get_driver(db=db, driver_id=999)

def test_create_driver(db, seeded_data):
    team = seeded_data["teams"][0]
    driver_in = DriverCreate(
        name="New Driver",
        weight=68,
        team_id=team.id,
    )
    driver = create_driver(db=db, driver=driver_in)
    assert driver.id is not None
    assert driver.name == "New Driver"
    assert driver.weight == 68
    assert driver.team_id == team.id

def test_create_driver_service_error(db, seeded_data, monkeypatch):
    team = seeded_data["teams"][0]
    def fail_commit():
        raise Exception("DB failure")
    monkeypatch.setattr(db, "commit", fail_commit)
    driver_in = DriverCreate(
        name="Broken Driver",
        weight=70,
        team_id=team.id,
    )
    with pytest.raises(ServiceError):
        create_driver(db=db, driver=driver_in)

def test_update_driver_success(db, seeded_data):
    driver = seeded_data["drivers"][0]
    update = DriverUpdate(
        name="Updated Name",
    )
    updated = update_driver(
        db=db,
        driver_id=driver.id,
        driver_update=update,
    )
    assert updated.id == driver.id
    assert updated.name == "Updated Name"

def test_update_driver_not_found(db):
    update = DriverUpdate(name="Does Not Matter")
    with pytest.raises(EntityDoesNotExistError):
        update_driver(
            db=db,
            driver_id=999,
            driver_update=update,
        )

def test_update_driver_service_error(db, seeded_data, monkeypatch):
    driver = seeded_data["drivers"][0]
    def fail_commit():
        raise Exception("Commit failed")
    monkeypatch.setattr(db, "commit", fail_commit)
    update = DriverUpdate(name="Will Fail")
    with pytest.raises(ServiceError):
        update_driver(
            db=db,
            driver_id=driver.id,
            driver_update=update,
        )

def test_delete_driver_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        delete_driver(db=db, driver_id=999)

def test_delete_driver_service_error(db, seeded_data, monkeypatch):
    driver = seeded_data["drivers"][0]
    def fail_commit():
        raise Exception("Commit failed")
    monkeypatch.setattr(db, "commit", fail_commit)
    with pytest.raises(ServiceError):
        delete_driver(db=db, driver_id=driver.id)
