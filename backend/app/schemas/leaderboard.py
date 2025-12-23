from pydantic import BaseModel
from app.schemas.score import ScoreResponse
from app.schemas.team import TeamResponse

class LeaderboardResponse(BaseModel):
    score: ScoreResponse
    team: TeamResponse

    class Config:
        orm_mode = True