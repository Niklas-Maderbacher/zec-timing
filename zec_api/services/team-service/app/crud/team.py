from app.database.dependency import SessionDep
from app.schemas.team import TeamCreate, TeamUpdate
from app.models.team import Team
from app.exceptions.exceptions import (
    EntityDoesNotExistError,
    ServiceError,
)

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


def update_team(*, db: SessionDep, team_id: int, team_update: TeamUpdate):
    try:
        db_team = get_team(db=db, team_id=team_id)
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

def delete_team(*, db: SessionDep, team_id: int):
    try:
        db_team = get_team(db=db, team_id=team_id)
        db.delete(db_team)
        db.commit()
        return db_team
    except EntityDoesNotExistError:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise ServiceError() from exc

def get_team(*, db: SessionDep, team_id: int):
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
