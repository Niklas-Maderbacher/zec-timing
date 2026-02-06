import pytest
from datetime import datetime
from unittest.mock import MagicMock, call

from app.crud.leaderboard import get_leaderboard
from app.models.score import Score
from app.exceptions.exceptions import (
    EntityDoesNotExistError,
    ServiceError,
    AuthenticationFailed,
)

class MockResp:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json

    @property
    def text(self):
        return str(self._json)

def test_get_leaderboard(db, seeded_scores, mock_leaderboard_requests):
    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
            {"id": 2, "team_id": 20},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
            {"id": 20, "name": "Team B", "category": "advanced_class"},
        ])
    ]
    leaderboard = get_leaderboard(db=db, challenge_id=1)
    assert len(leaderboard) == 2
    assert leaderboard[0].score.value == 95.5
    assert leaderboard[1].score.value == 88.3


def test_get_leaderboard_by_category(db, seeded_scores, mock_leaderboard_requests):
    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
            {"id": 2, "team_id": 20},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
            {"id": 20, "name": "Team B", "category": "advanced_class"},
        ])
    ]
    leaderboard = get_leaderboard(
        db=db,
        challenge_id=1,
        category="close_to_series",
    )
    assert len(leaderboard) == 1
    assert leaderboard[0].team.id == 10
    assert leaderboard[0].team.category == "close_to_series"

def test_get_leaderboard_best_score_per_team(db, mock_leaderboard_requests):
    db.add_all([
        Score(id=1, attempt_id=1, challenge_id=1, value=85.0, created_at=datetime.utcnow()),
        Score(id=2, attempt_id=2, challenge_id=1, value=95.0, created_at=datetime.utcnow()),
        Score(id=3, attempt_id=3, challenge_id=1, value=90.0, created_at=datetime.utcnow()),
    ])
    db.commit()

    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
            {"id": 2, "team_id": 10},
            {"id": 3, "team_id": 20},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
            {"id": 20, "name": "Team B", "category": "advanced_class"},
        ])
    ]
    leaderboard = get_leaderboard(db=db, challenge_id=1)
    assert len(leaderboard) == 2
    team_10_entry = [entry for entry in leaderboard if entry.team.id == 10][0]
    assert team_10_entry.score.value == 95.0


def test_get_leaderboard_sorted_descending(db, mock_leaderboard_requests):
    db.add_all([
        Score(id=1, attempt_id=1, challenge_id=1, value=75.0, created_at=datetime.utcnow()),
        Score(id=2, attempt_id=2, challenge_id=1, value=95.0, created_at=datetime.utcnow()),
        Score(id=3, attempt_id=3, challenge_id=1, value=85.0, created_at=datetime.utcnow()),
    ])
    db.commit()

    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
            {"id": 2, "team_id": 20},
            {"id": 3, "team_id": 30},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
            {"id": 20, "name": "Team B", "category": "advanced_class"},
            {"id": 30, "name": "Team C", "category": "close_to_series"},
        ])
    ]

    leaderboard = get_leaderboard(db=db, challenge_id=1)

    assert len(leaderboard) == 3
    assert leaderboard[0].score.value == 95.0
    assert leaderboard[1].score.value == 85.0
    assert leaderboard[2].score.value == 75.0

def test_get_leaderboard_no_attempts_404(db, mock_leaderboard_requests):
    mock_leaderboard_requests.get.return_value = MockResp(404, "not found")
    with pytest.raises(EntityDoesNotExistError, match="No attempts found for this challenge"):
        get_leaderboard(db=db, challenge_id=999)

def test_get_leaderboard_empty_attempts_list(db, mock_leaderboard_requests):
    mock_leaderboard_requests.get.return_value = MockResp(200, [])

    with pytest.raises(EntityDoesNotExistError, match="No attempts found for this challenge"):
        get_leaderboard(db=db, challenge_id=1)


def test_get_leaderboard_no_scores_for_attempts(db, mock_leaderboard_requests):
    mock_leaderboard_requests.get.return_value = MockResp(200, [
        {"id": 999, "team_id": 10},
    ])
    with pytest.raises(EntityDoesNotExistError, match="No scores found for the challenge attempts"):
        get_leaderboard(db=db, challenge_id=1)

def test_get_leaderboard_teams_not_found(db, seeded_scores, mock_leaderboard_requests):
    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
        ]),
        MockResp(404, "teams not found")
    ]
    with pytest.raises(EntityDoesNotExistError, match="Teams not found"):
        get_leaderboard(db=db, challenge_id=1)

def test_get_leaderboard_teams_unauthorized(db, seeded_scores, mock_leaderboard_requests):
    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
        ]),
        MockResp(401, "unauthorized")
    ]

    with pytest.raises(AuthenticationFailed, match="Unauthorized to fetch teams"):
        get_leaderboard(db=db, challenge_id=1)

def test_get_leaderboard_team_data_missing(db, seeded_scores, mock_leaderboard_requests):
    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
        ]),
        MockResp(200, [])
    ]

    with pytest.raises(EntityDoesNotExistError, match="Team data missing for team_id 10"):
        get_leaderboard(db=db, challenge_id=1)

def test_get_leaderboard_category_no_matches(db, seeded_scores, mock_leaderboard_requests):
    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
        ])
    ]

    with pytest.raises(EntityDoesNotExistError, match="No teams found for category advanced_class with scores"):
        get_leaderboard(db=db, challenge_id=1, category="advanced_class")

def test_get_leaderboard_empty_after_filtering(db, mock_leaderboard_requests):
    db.add_all([
        Score(id=1, attempt_id=1, challenge_id=1, value=95.0, created_at=datetime.utcnow()),
    ])
    db.commit()

    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
        ])
    ]
    with pytest.raises(EntityDoesNotExistError, match="No teams found for category nonexistent"):
        get_leaderboard(db=db, challenge_id=1, category="nonexistent")

def test_get_leaderboard_single_team(db, mock_leaderboard_requests):
    db.add_all([
        Score(id=1, attempt_id=1, challenge_id=1, value=95.0, created_at=datetime.utcnow()),
    ])
    db.commit()

    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
        ])
    ]

    leaderboard = get_leaderboard(db=db, challenge_id=1)
    assert len(leaderboard) == 1
    assert leaderboard[0].team.id == 10
    assert leaderboard[0].score.value == 95.0


def test_get_leaderboard_many_attempts_one_team(db, mock_leaderboard_requests):
    db.add_all([
        Score(id=1, attempt_id=1, challenge_id=1, value=70.0, created_at=datetime.utcnow()),
        Score(id=2, attempt_id=2, challenge_id=1, value=80.0, created_at=datetime.utcnow()),
        Score(id=3, attempt_id=3, challenge_id=1, value=95.0, created_at=datetime.utcnow()),
        Score(id=4, attempt_id=4, challenge_id=1, value=85.0, created_at=datetime.utcnow()),
    ])
    db.commit()

    mock_leaderboard_requests.get.side_effect = [
        MockResp(200, [
            {"id": 1, "team_id": 10},
            {"id": 2, "team_id": 10},
            {"id": 3, "team_id": 10},
            {"id": 4, "team_id": 10},
        ]),
        MockResp(200, [
            {"id": 10, "name": "Team A", "category": "close_to_series"},
        ])
    ]

    leaderboard = get_leaderboard(db=db, challenge_id=1)
    assert len(leaderboard) == 1
    assert leaderboard[0].score.value == 95.0
