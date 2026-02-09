from pydantic import BaseModel, ConfigDict
from app.schemas.score import ScoreResponse
from app.schemas.team import TeamResponse

class LeaderboardResponse(BaseModel):
    score: ScoreResponse
    team: TeamResponse

    model_config = ConfigDict(from_attributes=True)
