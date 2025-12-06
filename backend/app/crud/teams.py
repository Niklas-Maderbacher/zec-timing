from sqlalchemy.orm import Session

from app.models.teams import Team as model_team
from app.schemas.teams import Team as schema_team

def get_teams(db: Session) -> list[schema_team]:
    teams_db = db.query(model_team).all()

    teams = []

    for team in teams_db:
        teams.append(schema_team(
            id=team.id,
            name=team.name,
        ))

    return teams
