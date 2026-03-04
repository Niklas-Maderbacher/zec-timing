import requests
import pandas as pd
from app.database.dependency import SessionDep
from app.models.attempt import Attempt
from app.core.config import settings
from app.exceptions.exceptions import (
    ServiceError,
    EntityDoesNotExistError,
    AuthenticationFailed,
)

TEAM_URL = settings.TEAM_SERVICE_URL
CHALLENGE_URL = settings.CHALLENGE_SERVICE_URL

def get_attempts_export(db: SessionDep, challenge_id: int, category: str | None = None) -> pd.DataFrame:
    attempts = (
        db.query(Attempt)
        .filter(Attempt.challenge_id == challenge_id)
        .all()
    )
    if not attempts:
        raise EntityDoesNotExistError("No attempts found for this challenge")
    challenge_resp = requests.get(f"{CHALLENGE_URL}/api/challenges/{challenge_id}")
    if challenge_resp.status_code == 404:
        raise EntityDoesNotExistError("Challenge not found")
    if challenge_resp.status_code != 200:
        raise ServiceError(f"Failed to fetch challenge: {challenge_resp.text}")
    challenge = challenge_resp.json()
    team_ids = list({a.team_id for a in attempts})
    teams_resp = requests.get(f"{TEAM_URL}/api/teams/by-ids/", params={"team_ids": team_ids})
    if teams_resp.status_code == 404:
        raise EntityDoesNotExistError("Teams not found")
    if teams_resp.status_code in (401, 403):
        raise AuthenticationFailed("Unauthorized to fetch teams")
    if teams_resp.status_code != 200:
        raise ServiceError(f"Failed to fetch teams: {teams_resp.text}")
    team_by_id = {t["id"]: t for t in teams_resp.json()}
    driver_ids = list({a.driver_id for a in attempts if a.driver_id})
    drivers_resp = requests.get(f"{TEAM_URL}/api/drivers/by-ids/", params={"driver_ids": driver_ids})
    if drivers_resp.status_code == 404:
        raise EntityDoesNotExistError("Drivers not found")
    if drivers_resp.status_code != 200:
        raise ServiceError(f"Failed to fetch drivers: {drivers_resp.text}")
    driver_by_id = {d["id"]: d for d in drivers_resp.json()}
    rows = []
    for attempt in attempts:
        team = team_by_id.get(attempt.team_id)
        driver = driver_by_id.get(attempt.driver_id)
        if not team:
            continue
        if category and team.get("category") != category:
            continue
        duration = None
        if attempt.start_time and attempt.end_time:
            duration = (attempt.end_time - attempt.start_time).total_seconds()
        rows.append({
            "attempt_id":      attempt.id,
            "challenge_name":  challenge.get("name"),
            "team_name":       team.get("name"),
            "team_category":   team.get("category"),
            "driver_name":     driver.get("name") if driver else None,
            "driver_weight":   driver.get("weight") if driver else None,
            "is_valid":        attempt.is_valid,
            "start_time":      attempt.start_time,
            "end_time":        attempt.end_time,
            "duration_seconds": duration,
            "energy_used":     attempt.energy_used,
            "created_at":      attempt.created_at,
        })
    if not rows:
        raise EntityDoesNotExistError("No attempts found matching the filters")
    return pd.DataFrame(rows)
