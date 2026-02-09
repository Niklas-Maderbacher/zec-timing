from fastapi import APIRouter
from app.api.routes import score, leaderboard, penalty

api_router = APIRouter()

api_router.include_router(score.router, prefix="/scores", tags=["scores"])
api_router.include_router(penalty.router, prefix="/penalties", tags=["penalties"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
