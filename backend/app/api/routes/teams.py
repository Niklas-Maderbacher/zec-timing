from fastapi import APIRouter, status

from app.crud.teams import get_teams as crud_get_teams
from app.schemas.teams import Team as schema_team
from app.api.deps import SessionDep


router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=list[schema_team], status_code=status.HTTP_200_OK)
def get_teams(db: SessionDep):
    return crud_get_teams(db)
