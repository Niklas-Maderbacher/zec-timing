from fastapi import APIRouter, status

from app.crud.penalties import get_penalties as crud_get_penalties
from app.schemas.penalties import Penalty as schema_panal
from app.api.deps import SessionDep


router = APIRouter(prefix="/penalties", tags=["penalties"])

@router.get("/", response_model=list[schema_panal], status_code=status.HTTP_200_OK)
def get_penalties(db: SessionDep):
    return crud_get_penalties(db)
