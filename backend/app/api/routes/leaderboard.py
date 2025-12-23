from fastapi import APIRouter
from app.database.dependency import SessionDep
from app.schemas.leaderboard import LeaderboardResponse
from app.crud import leaderboard as crud

router = APIRouter()

@router.get("/{challenge_id}", response_model=list[LeaderboardResponse],)
def get_leaderboard(challenge_id: int, db: SessionDep,):
    leaderboard = crud.get_leaderboard(db, challenge_id)
    return leaderboard
