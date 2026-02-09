from app.schemas.leaderboard import LeaderboardResponse
from app.database.dependency import SessionDep
from app.models.score import Score
from app.core.config import settings
from app.schemas.score import ScoreResponse
from app.schemas.team import TeamResponse
import requests
from app.exceptions.exceptions import (
    ServiceError,
    EntityDoesNotExistError,
    AuthenticationFailed,
)

ATTEMPT_URL = settings.ATTEMPT_SERVICE_URL
TEAM_URL = settings.TEAM_SERVICE_URL

def get_leaderboard(db: SessionDep, challenge_id: int, category: str | None = None):
    attempts_resp = requests.get(f"{ATTEMPT_URL}/api/attempts/challenges/{challenge_id}")
    if attempts_resp.status_code == 404:
        raise EntityDoesNotExistError("No attempts found for this challenge")
    if attempts_resp.status_code in (401, 403):
        raise AuthenticationFailed("Unauthorized to fetch attempts")
    if attempts_resp.status_code != 200:
        raise ServiceError(f"Failed to fetch attempts: {attempts_resp.text}")
    attempts = attempts_resp.json()
    if not attempts:
        raise EntityDoesNotExistError("No attempts found for this challenge")
    attempt_by_id = {a["id"]: a for a in attempts}
    attempt_ids = list(attempt_by_id.keys())
    scores = (
        db.query(Score)
        .filter(Score.attempt_id.in_(attempt_ids))
        .all()
    )
    if not scores:
        raise EntityDoesNotExistError("No scores found for the challenge attempts")
    best_score_by_team = {}
    for score in scores:
        team_id = attempt_by_id[score.attempt_id]["team_id"]
        current = best_score_by_team.get(team_id)
        if current is None or score.value > current.value:
            best_score_by_team[team_id] = score
    team_ids = list(best_score_by_team.keys())
    if not team_ids:
        raise EntityDoesNotExistError("No teams with scores found")
    teams_resp = requests.get(f"{TEAM_URL}/api/teams/by-ids/", params={"team_ids": team_ids})
    if teams_resp.status_code == 404:
        raise EntityDoesNotExistError("Teams not found")
    if teams_resp.status_code in (401, 403):
        raise AuthenticationFailed("Unauthorized to fetch teams")
    if teams_resp.status_code != 200:
        raise ServiceError(f"Failed to fetch teams: {teams_resp.text}")
    teams = teams_resp.json()
    team_by_id = {t["id"]: t for t in teams}
    leaderboard = []
    for team_id, score in best_score_by_team.items():
        team = team_by_id.get(team_id)
        if not team:
            raise EntityDoesNotExistError(f"Team data missing for team_id {team_id}")
        if category is not None and team.get("category") != category:
            continue
        leaderboard.append(
            LeaderboardResponse(
                score=ScoreResponse.model_validate(score),
                team=TeamResponse.model_validate(team),
            )
        )
    if not leaderboard:
        if category is not None:
            raise EntityDoesNotExistError(f"No teams found for category {category} with scores")
        raise EntityDoesNotExistError("No teams with scores found")
    leaderboard.sort(key=lambda x: x.score.value, reverse=True)
    return leaderboard
