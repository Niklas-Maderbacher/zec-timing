from app.schemas.leaderboard import LeaderboardResponse
from app.database.dependency import SessionDep
from app.models.score import Score
import requests
from app.core.config import settings

ATTEMPT_URL = settings.ATTEMPT_SERVICE_URL
TEAM_URL = settings.TEAM_SERVICE_URL

def get_leaderboard(db: SessionDep, challenge_id: int):
    attempts_resp = requests.get(f"{ATTEMPT_URL}/api/attempts/challenges/{challenge_id}")
    attempts = attempts_resp.json()
    attempt_by_id = {a["id"]: a for a in attempts}
    attempt_ids = list(attempt_by_id.keys())

    scores = (
        db.query(Score)
        .filter(Score.attempt_id.in_(attempt_ids))
        .all()
    )
    best_score_by_team = {}
    for score in scores:
        team_id = attempt_by_id[score.attempt_id]["team_id"]
        current = best_score_by_team.get(team_id)
        if current is None or score.value > current.value:
            best_score_by_team[team_id] = score

    team_ids = list(best_score_by_team.keys())
    teams_resp = requests.get(f"{TEAM_URL}/api/teams/by-ids/", params={"team_ids": team_ids})
    teams_resp.raise_for_status()
    teams = teams_resp.json()
    team_by_id = {t["id"]: t for t in teams}

    return [
        LeaderboardResponse(
            score=score,
            team=team_by_id[team_id],
        )
        for team_id, score in best_score_by_team.items()
    ]
