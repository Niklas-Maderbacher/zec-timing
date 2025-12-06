from fastapi import APIRouter, status

from app.crud.drivers import get_drivers as crud_get_drivers
from app.schemas.drivers import Driver as schema_driv
from app.api.deps import SessionDep


router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.get("/", response_model=list[schema_driv], status_code=status.HTTP_200_OK)
def get_drivers(db: SessionDep):
    return crud_get_drivers(db)
