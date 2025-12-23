from app.models.team import Team
from app.schemas.leaderboard import LeaderboardResponse
from app.database.dependency import SessionDep
from app.models.score import Score
from app.models.attempt import Attempt
from sqlalchemy import func
def get_leaderboard(
    db: SessionDep,
    challenge_id: int | None = None,
):
    subquery = (
        db.query(
            Attempt.challenge_id.label("challenge_id"),
            func.max(Score.value).label("max_score"),
        )
        .join(Score, Score.attempt_id == Attempt.id)
        .group_by(Attempt.challenge_id)
    )

    if challenge_id is not None:
        subquery = subquery.filter(Attempt.challenge_id == challenge_id)

    subquery = subquery.subquery()

    query = (
        db.query(Score, Team)
        .join(Attempt, Score.attempt_id == Attempt.id)
        .join(Team, Attempt.team_id == Team.id)
        .join(
            subquery,
            (Attempt.challenge_id == subquery.c.challenge_id)
            & (Score.value == subquery.c.max_score),
        )
    )

    results = query.all()

    return [
        LeaderboardResponse(
            score=score,
            team=team,
        )
        for score, team in results
    ]
