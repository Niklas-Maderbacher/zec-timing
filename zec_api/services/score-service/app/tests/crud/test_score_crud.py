import pytest
from datetime import datetime, timedelta

from app.crud import score as crud
from app.schemas.score import ScoreCreate, ScoreUpdate
from app.models.score import Score
from app.models.penalty import Penalty
from app.models.penalty_type import PenaltyType
from app.exceptions.exceptions import (
    EntityDoesNotExistError,
    InvalidOperationError,
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

def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")

def mock_attempt(challenge_id=1, energy=50):
    base = datetime.utcnow()
    return {
        "id": 1,
        "challenge_id": challenge_id,
        "team_id": 1,
        "driver_id": 1,
        "energy_used": energy,
        "start_time": iso(base),
        "end_time": iso(base + timedelta(seconds=10)),
        "is_valid": True,
    }

def test_get_score(db):
    score = Score(attempt_id=1, challenge_id=1, value=95.0)
    db.add(score)
    db.commit()
    result = crud.get_score(db=db, score_id=score.id)
    assert result.value == 95.0

def test_get_scores(db):
    db.add_all(
        [
            Score(attempt_id=1, challenge_id=1, value=10),
            Score(attempt_id=2, challenge_id=1, value=20),
            Score(attempt_id=3, challenge_id=2, value=30),
        ]
    )
    db.commit()

    scores = crud.get_scores(db=db)
    assert len(scores) == 3

def test_delete_score(db):
    score = Score(attempt_id=1, challenge_id=1, value=50)
    db.add(score)
    db.commit()

    deleted = crud.delete_score(db=db, score_id=score.id)
    assert deleted.id == score.id

def test_get_score_not_found(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_score(db=db, score_id=999)

def test_create_score_success_skidpad(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Skidpad"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    score = crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

    assert score.value > 0
    assert score.challenge_id == 1

def test_create_score_with_penalty_time(db, mock_requests):
    db.add(PenaltyType(id=1, amount=2))
    db.add(Penalty(attempt_id=1, penalty_type_id=1, count=2))
    db.commit()

    def side_effect(url, *_, **__):
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Slalom"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    score = crud.create_score(db=db, score=ScoreCreate(attempt_id=1))
    assert score.value > 0

def test_create_score_missing_processor(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Unknown"})
        return MockResp(500, "unexpected")

    mock_requests.get.side_effect = side_effect

    with pytest.raises(InvalidOperationError):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_create_score_attempt_not_found(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/" in url:
            return MockResp(404, "not found")
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Skidpad"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(EntityDoesNotExistError):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_update_score(db):
    score = Score(attempt_id=1, challenge_id=1, value=10)
    db.add(score)
    db.commit()

    updated = crud.update_score(
        db=db,
        score_id=score.id,
        score_update=ScoreUpdate(value=99),
    )
    assert updated.value == 99

def test_delete_scores_for_attempt(db):
    db.add_all(
        [
            Score(attempt_id=1, challenge_id=1, value=10),
            Score(attempt_id=1, challenge_id=2, value=20),
        ]
    )
    db.commit()

    deleted = crud.delete_scores_for_attempt(db=db, attempt_id=1)
    assert len(deleted) == 2

    with pytest.raises(EntityDoesNotExistError):
        crud.delete_scores_for_attempt(db=db, attempt_id=1)
