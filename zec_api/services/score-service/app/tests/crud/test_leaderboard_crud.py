from app.crud.leaderboard import get_leaderboard


def test_get_leaderboard(db, seeded_scores, mock_requests):
    mock_requests.get.side_effect = [
        # Attempts for challenge
        type(
            "Resp",
            (),
            {
                "status_code": 200,
                "json": lambda: [
                    {"id": 1, "team_id": 10},
                    {"id": 2, "team_id": 20},
                ],
            },
        )(),
        # Teams by ids
        type(
            "Resp",
            (),
            {
                "status_code": 200,
                "json": lambda: [
                    {"id": 10, "name": "Team A", "category": "close_to_series"},
                    {"id": 20, "name": "Team B", "category": "advanced_class"},
                ],
            },
        )(),
    ]

    leaderboard = get_leaderboard(db=db, challenge_id=1)

    assert len(leaderboard) == 2
    assert leaderboard[0].score.value == 95.0
    assert leaderboard[1].score.value == 90.0


def test_get_leaderboard_by_category(db, seeded_scores, mock_requests):
    mock_requests.get.side_effect = [
        # Attempts
        type(
            "Resp",
            (),
            {
                "status_code": 200,
                "json": lambda: [
                    {"id": 1, "team_id": 10},
                    {"id": 2, "team_id": 20},
                ],
            },
        )(),
        # Teams
        type(
            "Resp",
            (),
            {
                "status_code": 200,
                "json": lambda: [
                    {"id": 10, "name": "Team A", "category": "close_to_series"},
                    {"id": 20, "name": "Team B", "category": "advanced_class"},
                ],
            },
        )(),
    ]

    leaderboard = get_leaderboard(
        db=db,
        challenge_id=1,
        category="close_to_series",
    )

    assert len(leaderboard) == 1
    assert leaderboard[0].team.id == 10
    assert leaderboard[0].team.category == "close_to_series"
