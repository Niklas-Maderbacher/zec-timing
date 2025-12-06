from fastapi import APIRouter, status

from app.crud.challenges import get_challenges as crud_get_challenges
from app.schemas.challenges import Challenge as schema_chal
from app.api.deps import SessionDep

router = APIRouter(prefix="/challenges", tags=["challenges"])

@router.get("/", response_model=list[schema_chal], status_code=status.HTTP_200_OK)
def get_challenges(db: SessionDep):
    return crud_get_challenges(db)

