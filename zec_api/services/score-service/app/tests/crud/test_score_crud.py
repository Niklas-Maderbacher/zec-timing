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
    ServiceError,
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

def mock_attempt(challenge_id=1, energy=50, team_id=1, driver_id=1, attempt_id=1):
    base = datetime.utcnow()
    return {
        "id": attempt_id,
        "challenge_id": challenge_id,
        "team_id": team_id,
        "driver_id": driver_id,
        "energy_used": energy,
        "start_time": iso(base),
        "end_time": iso(base + timedelta(seconds=10)),
        "is_valid": True,
    }

def mock_team(team_id=1, vehicle_weight=500, mean_power=100):
    return {
        "id": team_id,
        "vehicle_weight": vehicle_weight,
        "mean_power": mean_power,
    }

def mock_driver(driver_id=1, weight=70):
    return {
        "id": driver_id,
        "weight": weight,
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

def test_get_score_for_attempt_success(db):
    score = Score(attempt_id=42, challenge_id=1, value=95.0)
    db.add(score)
    db.commit()
    
    result = crud.get_score_for_attempt(db=db, attempt_id=42)
    assert result.value == 95.0
    assert result.attempt_id == 42

def test_get_score_for_attempt_not_found(db):
    with pytest.raises(EntityDoesNotExistError, match="No score for attempt_id: 999"):
        crud.get_score_for_attempt(db=db, attempt_id=999)

def test_create_score_acceleration(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/" in url and "/fastest" in url:
            return MockResp(200, mock_attempt(attempt_id=2))
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/teams/" in url:
            return MockResp(200, mock_team())
        if "/api/drivers/" in url:
            return MockResp(200, mock_driver())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Acceleration"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    score = crud.create_score(db=db, score=ScoreCreate(attempt_id=1))
    assert score.value > 0
    assert score.challenge_id == 1

def test_create_score_endurance(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(200, mock_attempt(attempt_id=2))
        if "/api/attempts/least-energy" in url:
            return MockResp(200, mock_attempt(attempt_id=3, energy=40))
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt(energy=50))
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Endurance"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    score = crud.create_score(db=db, score=ScoreCreate(attempt_id=1))
    assert score.value > 0
    assert score.challenge_id == 1

def test_create_score_challenge_not_found(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(404, "not found")
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(EntityDoesNotExistError, match="Challenge does not exist"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_create_score_challenge_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(500, "Internal server error")
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError, match="Failed to create score"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_create_score_attempt_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/" in url:
            return MockResp(500, "Internal server error")
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_create_score_penalty_exception_ignored(db, mock_requests):
    db.add(Penalty(attempt_id=1, penalty_type_id=999, count=2))
    db.commit()

    def side_effect(url, *_, **__):
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Skidpad"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    score = crud.create_score(db=db, score=ScoreCreate(attempt_id=1))
    assert score.value > 0

def test_acceleration_team_not_found(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(200, mock_attempt(attempt_id=2))
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/teams/" in url:
            return MockResp(404, "not found")
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Acceleration"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(EntityDoesNotExistError, match="Team does not exist"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_acceleration_team_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(200, mock_attempt(attempt_id=2))
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/teams/" in url:
            return MockResp(500, "Internal server error")
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Acceleration"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_acceleration_driver_not_found(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(200, mock_attempt(attempt_id=2))
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/teams/" in url:
            return MockResp(200, mock_team())
        if "/api/drivers/" in url:
            return MockResp(404, "not found")
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Acceleration"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(EntityDoesNotExistError, match="Driver does not exist"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_acceleration_driver_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(200, mock_attempt(attempt_id=2))
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/teams/" in url:
            return MockResp(200, mock_team())
        if "/api/drivers/" in url:
            return MockResp(500, "Internal server error")
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Acceleration"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_acceleration_attempt_fetch_in_calculate_fpm_fails(db, mock_requests):
    call_count = {"attempts": 0}
    
    def side_effect(url, *_, **__):
        if "/api/attempts/" in url and "/fastest" not in url:
            call_count["attempts"] += 1
            if call_count["attempts"] == 1:
                return MockResp(200, mock_attempt())
            else:
                return MockResp(500, "Internal error")
        if "/api/attempts/fastest" in url:
            return MockResp(200, mock_attempt(attempt_id=2))
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Acceleration"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError, match="Failed to fetch attempt"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_skidpad_fastest_attempt_not_found(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(404, "not found")
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Skidpad"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(EntityDoesNotExistError, match="Fastest attempt not found"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_skidpad_fastest_attempt_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(500, "Internal server error")
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Skidpad"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_acceleration_fastest_attempt_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(500, "Internal server error")
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/teams/" in url:
            return MockResp(200, mock_team())
        if "/api/drivers/" in url:
            return MockResp(200, mock_driver())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Acceleration"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError, match="Failed to fetch fastest attempt"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_slalom_fastest_attempt_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(500, "Internal server error")
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Slalom"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError, match="Failed to fetch fastest attempt"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_endurance_fastest_attempt_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(500, "Internal server error")
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Endurance"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError, match="Failed to fetch fastest attempt"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_endurance_least_energy_service_error(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            return MockResp(200, mock_attempt(attempt_id=2))
        if "/api/attempts/least-energy" in url:
            return MockResp(500, "Internal server error")
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Endurance"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    with pytest.raises(ServiceError, match="Failed to fetch least-energy attempt"):
        crud.create_score(db=db, score=ScoreCreate(attempt_id=1))

def test_update_score_not_found(db):
    with pytest.raises(EntityDoesNotExistError, match="No score for id: 999"):
        crud.update_score(
            db=db,
            score_id=999,
            score_update=ScoreUpdate(value=99),
        )

def test_delete_score_not_found(db):
    with pytest.raises(EntityDoesNotExistError, match="No score for id: 999"):
        crud.delete_score(db=db, score_id=999)

def test_create_score_multiple_penalties(db, mock_requests):
    db.add(PenaltyType(id=1, amount=2))
    db.add(PenaltyType(id=2, amount=5))
    db.add(Penalty(attempt_id=1, penalty_type_id=1, count=2))
    db.add(Penalty(attempt_id=1, penalty_type_id=2, count=1))
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

def test_get_scores_empty(db):
    scores = crud.get_scores(db=db)
    assert len(scores) == 0

def test_delete_scores_for_attempt_single(db):
    db.add(Score(attempt_id=5, challenge_id=1, value=10))
    db.commit()

    deleted = crud.delete_scores_for_attempt(db=db, attempt_id=5)
    assert len(deleted) == 1

def test_score_value_rounding(db, mock_requests):
    def side_effect(url, *_, **__):
        if "/api/attempts/fastest" in url:
            base = datetime.utcnow()
            return MockResp(200, {
                "id": 2,
                "challenge_id": 1,
                "team_id": 1,
                "driver_id": 1,
                "energy_used": 50,
                "start_time": iso(base),
                "end_time": iso(base + timedelta(seconds=9.333)),
                "is_valid": True,
            })
        if "/api/attempts/" in url:
            return MockResp(200, mock_attempt())
        if "/api/challenges/" in url:
            return MockResp(200, {"id": 1, "name": "Skidpad"})
        return MockResp(200, {})

    mock_requests.get.side_effect = side_effect

    score = crud.create_score(db=db, score=ScoreCreate(attempt_id=1))
    assert score.value == round(score.value, 2)
    assert len(str(score.value).split('.')[-1]) <= 2 or str(score.value).endswith('0')