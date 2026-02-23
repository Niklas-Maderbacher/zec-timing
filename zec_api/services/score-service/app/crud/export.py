from app.database.dependency import SessionDep
from app.crud import leaderboard as crud
import pandas as pd

def get_leaderboard_export(db: SessionDep, challenge_id: int, category: str | None = None) -> pd.DataFrame:
    leaderboard = crud.get_leaderboard(db, challenge_id, category=category)
    rows = []
    for rank, entry in enumerate(leaderboard, start=1):
        rows.append({
            "rank":           rank,
            "team_name":      entry.team.name,
            "category":       entry.team.category,
            "vehicle_weight": entry.team.vehicle_weight,
            "score_value":    entry.score.value,
            "challenge_id":   entry.score.challenge_id,
            "attempt_id":     entry.score.attempt_id,
            "scored_at":      entry.score.created_at,
        })
    return pd.DataFrame(rows)
