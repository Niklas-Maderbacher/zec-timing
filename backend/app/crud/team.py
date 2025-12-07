from app.database.dependency import SessionDep
from app.schemas.team import TeamCreate, TeamUpdate
from app.models.team import Team

def create_team(*, db: SessionDep, team: TeamCreate):
    team_data = team.model_dump(exclude_unset=True)
    db_team = Team(**team_data)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def update_team(*, db: SessionDep, team_update: TeamUpdate):
    team_id = team_update.id
    db_team = get_team(db=db, team_id=team_id)
    update_data = team_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_team, field, value)
    db.commit()
    db.refresh(db_team)
    return db_team

def delete_team(*, db: SessionDep, team_id: int):
    db_team = get_team(db=db, team_id=team_id)
    db.delete(db_team)
    db.commit()
    return db_team

def get_team(*, db: SessionDep, team_id: int):
    return db.query(Team).filter(Team.id == team_id).first()

def get_teams(*, db: SessionDep):
    return db.query(Team).all()