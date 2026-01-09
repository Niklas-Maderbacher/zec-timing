from fastapi import APIRouter
from typing import List
from app.database.dependency import SessionDep
from app.schemas.driver import DriverCreate, DriverUpdate, DriverResponse
from app.crud import driver as crud

router = APIRouter()

@router.post("/", response_model=DriverResponse)
def create_driver(db: SessionDep, driver: DriverCreate):
    driver = crud.create_driver(db=db, driver=driver)
    return driver

@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(db: SessionDep, driver_id: int, driver_update: DriverUpdate):
    driver = crud.update_driver(db=db, driver_id=driver_id, driver_update=driver_update)
    return driver

@router.delete("/{driver_id}", response_model=DriverResponse)
def delete_driver(db: SessionDep, driver_id: int):
    driver = crud.delete_driver(db=db, driver_id=driver_id)
    return driver

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(db: SessionDep, driver_id: int):
    driver = crud.get_driver(db=db, driver_id=driver_id)
    return driver

@router.get("/", response_model=List[DriverResponse])
def list_drivers(db: SessionDep):
    drivers = crud.get_drivers(db=db)
    return drivers