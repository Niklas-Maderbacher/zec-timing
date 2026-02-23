from fastapi import APIRouter, Query, Request
from typing import List
from app.database.dependency import SessionDep
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse
from app.crud import team as crud

router = APIRouter()

@router.post("/", response_model=TeamResponse)
def create_team(db: SessionDep, team: TeamCreate):
    team = crud.create_team(db=db, team=team)
    return team

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(db: SessionDep, team_id: int, team_update: TeamUpdate, request: Request):
    team = crud.update_team(db=db, team_id=team_id, team_update=team_update, request=request)
    return team

@router.delete("/{team_id}", response_model=TeamResponse)
def delete_team(db: SessionDep, team_id: int, request: Request):
    team = crud.delete_team(db=db, team_id=team_id, request=request)
    return team

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(db: SessionDep, team_id: int, request: Request):
    team = crud.get_team(db=db, team_id=team_id, request=request)
    return team

@router.get("/", response_model=List[TeamResponse])
def get_all_teams(db: SessionDep):
    teams = crud.get_teams(db=db)
    return teams

@router.get("/by-ids/", response_model=List[TeamResponse])
def get_teams_by_ids(db: SessionDep, team_ids: list[int] = Query(...)):
    teams = crud.get_teams_by_ids(db=db, team_ids=team_ids)
    return teams