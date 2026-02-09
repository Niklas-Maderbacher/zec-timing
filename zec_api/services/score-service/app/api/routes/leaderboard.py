from fastapi import APIRouter
from app.database.dependency import SessionDep
from app.schemas.leaderboard import LeaderboardResponse
from app.crud import leaderboard as crud

router = APIRouter()

@router.get("/{challenge_id}/category/{category}", response_model=list[LeaderboardResponse])
def get_leaderboard_by_category(challenge_id: int, category: str, db: SessionDep,):
    leaderboard = crud.get_leaderboard(db, challenge_id, category=category)
    return leaderboard
