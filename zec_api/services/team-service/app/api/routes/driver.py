from fastapi import APIRouter, Request, Query
from typing import List
from app.database.dependency import SessionDep
from app.schemas.driver import DriverCreate, DriverUpdate, DriverResponse
from app.crud import driver as crud

router = APIRouter()

@router.post("/", response_model=DriverResponse)
def create_driver(db: SessionDep, driver: DriverCreate, request: Request):
    driver = crud.create_driver(db=db, driver=driver, request=request)
    return driver

@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(db: SessionDep, driver_id: int, driver_update: DriverUpdate, request: Request):
    driver = crud.update_driver(db=db, driver_id=driver_id, driver_update=driver_update, request=request)
    return driver

@router.delete("/{driver_id}", response_model=DriverResponse)
def delete_driver(db: SessionDep, driver_id: int, request: Request):
    driver = crud.delete_driver(db=db, driver_id=driver_id, request=request)
    return driver

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(db: SessionDep, driver_id: int, request: Request):
    driver = crud.get_driver(db=db, driver_id=driver_id, request=request)
    return driver

@router.get("/", response_model=List[DriverResponse])
def get_all_drivers(db: SessionDep):
    drivers = crud.get_drivers(db=db)
    return drivers

@router.get("/team/{team_id}", response_model=List[DriverResponse])
def get_drivers_by_team(db: SessionDep, team_id: int, request: Request):
    drivers = crud.get_drivers_by_team(db=db, team_id=team_id, request=request)
    return drivers

@router.get("/by-ids/", response_model=List[DriverResponse])
def get_drivers_by_ids(db: SessionDep, driver_ids: List[int] = Query(...)):
    drivers = crud.get_drivers_by_ids(db=db, driver_ids=driver_ids)
    return drivers