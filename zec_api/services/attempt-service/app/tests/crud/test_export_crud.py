import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta, timezone
from app.crud import export as crud
from app.models.attempt import Attempt
from app.exceptions.exceptions import EntityDoesNotExistError

def _make_response(url, challenge_status=200, teams_status=200, drivers_status=200, multi_team=False):
    r = Mock()
    r.text = "error"
    if "/api/challenges/" in url:
        r.status_code = challenge_status
        r.json.return_value = {"id": 1, "name": "Speed Run"}
    elif "/api/teams/by-ids/" in url:
        r.status_code = teams_status
        teams = [{"id": 1, "name": "Team Alpha", "category": "A"}]
        if multi_team:
            teams.append({"id": 2, "name": "Team Beta", "category": "B"})
        r.json.return_value = teams
    elif "/api/drivers/by-ids/" in url:
        r.status_code = drivers_status
        r.json.return_value = [
            {"id": 1, "name": "Alice", "weight": 60},
            {"id": 2, "name": "Bob", "weight": 75},
        ]
    else:
        r.status_code = 200
        r.json.return_value = {}
    return r

def test_get_attempts_export_returns_dataframe(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert len(df) == 2

def test_get_attempts_export_columns(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    expected = {
        "attempt_id", "challenge_name", "team_name", "team_category",
        "driver_name", "driver_weight", "is_valid", "start_time",
        "end_time", "duration_seconds", "energy_used", "created_at",
    }
    assert expected == set(df.columns)

def test_get_attempts_export_challenge_name(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert (df["challenge_name"] == "Speed Run").all()

def test_get_attempts_export_team_name(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert (df["team_name"] == "Team Alpha").all()

def test_get_attempts_export_driver_names(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert set(df["driver_name"]) == {"Alice", "Bob"}

def test_get_attempts_export_duration_calculated(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert (df["duration_seconds"] > 0).all()

def test_get_attempts_export_duration_values(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert sorted(df["duration_seconds"].tolist()) == [9.0, 10.0]

def test_get_attempts_export_energy_values(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert set(df["energy_used"]) == {40, 50}

def test_get_attempts_export_category_filter_match(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1, category="A")
    assert len(df) == 2
    assert (df["team_category"] == "A").all()

def test_get_attempts_export_category_filter_no_match(db, seeded_attempts, mock_requests):
    _, mock_export = mock_requests
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    with pytest.raises(EntityDoesNotExistError):
        crud.get_attempts_export(db=db, challenge_id=1, category="Z")

def test_get_attempts_export_category_filter_excludes_other(db, mock_requests):
    _, mock_export = mock_requests
    base = datetime.now(timezone.utc)
    db.add_all([
        Attempt(team_id=1, driver_id=1, challenge_id=1,
                start_time=base, end_time=base + timedelta(seconds=10),
                energy_used=50, is_valid=True),
        Attempt(team_id=2, driver_id=2, challenge_id=1,
                start_time=base, end_time=base + timedelta(seconds=5),
                energy_used=30, is_valid=True),
    ])
    db.commit()
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url, multi_team=True)
    df = crud.get_attempts_export(db=db, challenge_id=1, category="B")
    assert (df["team_category"] == "B").all()

def test_get_attempts_export_no_driver_fields_are_none(db, mock_requests):
    _, mock_export = mock_requests
    base = datetime.now(timezone.utc)
    db.add(Attempt(team_id=1, driver_id=None, challenge_id=1,
                   start_time=base, end_time=base + timedelta(seconds=5),
                   energy_used=20, is_valid=False))
    db.commit()
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert df.iloc[0]["driver_name"] is None
    assert df.iloc[0]["driver_weight"] is None

def test_get_attempts_export_no_times_duration_is_none(db, mock_requests):
    _, mock_export = mock_requests
    db.add(Attempt(team_id=1, driver_id=None, challenge_id=1,
                   start_time=None, end_time=None,
                   energy_used=10, is_valid=False))
    db.commit()
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    df = crud.get_attempts_export(db=db, challenge_id=1)
    assert df.iloc[0]["duration_seconds"] is None

def test_get_attempts_export_unknown_team_skipped(db, mock_requests):
    _, mock_export = mock_requests
    base = datetime.now(timezone.utc)
    db.add(Attempt(team_id=99, driver_id=None, challenge_id=1,
                   start_time=base, end_time=base + timedelta(seconds=3),
                   energy_used=5, is_valid=True))
    db.commit()
    mock_export.get.side_effect = lambda url, *a, **kw: _make_response(url)
    with pytest.raises(EntityDoesNotExistError):
        crud.get_attempts_export(db=db, challenge_id=1)

def test_get_attempts_export_no_attempts(db):
    with pytest.raises(EntityDoesNotExistError):
        crud.get_attempts_export(db=db, challenge_id=999)
