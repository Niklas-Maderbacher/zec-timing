from app.database.dependency import SessionDep
from app.schemas.team import TeamCreate, TeamUpdate
from app.models.team import Team
from app.exceptions.exceptions import (
    EntityDoesNotExistError,
    InvalidOperationError,
    ServiceError,
    InsufficientPermissions,
)
from fastapi import Request
import requests
from app.core.config import settings 

ATTEMPT_URL = settings.ATTEMPT_SERVICE_URL

def check_team_permissions(*, db: SessionDep, team_id: int | None = None, request: Request):
    role = request.headers.get("X-Role")
    user_team_id = request.headers.get("X-Team-Id")
    if role == "TEAM_LEAD" and team_id is not None:
        if int(team_id) != int(user_team_id):
            raise InsufficientPermissions("Teamleads can only operate on their own team. Attempted to operate on a team that he is not assigned to")

def create_team(*, db: SessionDep, team: TeamCreate):
    try:
        team_data = team.model_dump(exclude_unset=True)
        db_team = Team(**team_data)
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def update_team(*, db: SessionDep, team_id: int, team_update: TeamUpdate, request: Request):
    check_team_permissions(db=db, team_id=team_id, request=request)
    try:
        db_team = get_team(db=db, team_id=team_id, request=request)
        update_data = team_update.model_dump(
            exclude_unset=True,
            exclude={"id"},
        )
        for field, value in update_data.items():
            setattr(db_team, field, value)
        db.commit()
        db.refresh(db_team)
        return db_team
    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def delete_team(*, db: SessionDep, team_id: int, request: Request):
    check_team_permissions(db=db, team_id=team_id, request=request)
    db_attempts = requests.get(f"{ATTEMPT_URL}/api/attempts/per-team/{team_id}").json()
    has_attempts = (
        isinstance(db_attempts, list) and len(db_attempts) > 0
    ) or (
        isinstance(db_attempts, dict)
        and db_attempts.get("detail") != "No attempts found for this team [Attemptservice]:"
    )
    if has_attempts:
        raise InvalidOperationError(f"Cannot delete team {team_id} because it has made attempts")
    try:
        db_team = get_team(db=db, team_id=team_id, request=request)
        db.delete(db_team)
        db.commit()
        return db_team
    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def get_team(*, db: SessionDep, team_id: int, request: Request):
    check_team_permissions(db=db, team_id=team_id, request=request)
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise EntityDoesNotExistError(
            message=f"Team with id {team_id} does not exist"
        )
    return team

def get_teams(*, db: SessionDep):
    return db.query(Team).all()

def get_teams_by_ids(*, db: SessionDep, team_ids: set[int]):
    teams = db.query(Team).filter(Team.id.in_(team_ids)).all()
    if len(teams) != len(team_ids):
        raise EntityDoesNotExistError(
            message="One or more teams do not exist for the provided IDs"
        )
    return teams
