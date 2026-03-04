import pandas as pd
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from app.crud.export import get_leaderboard_export

def make_entry(team_name="TeamA", category="EV", vehicle_weight=400,
               score_value=95.5, challenge_id=1, attempt_id=10,
               created_at=None):
    """Build a mock leaderboard entry (mimics ORM objects)."""
    entry = MagicMock()
    entry.team.name = team_name
    entry.team.category = category
    entry.team.vehicle_weight = vehicle_weight
    entry.score.value = score_value
    entry.score.challenge_id = challenge_id
    entry.score.attempt_id = attempt_id
    entry.score.created_at = created_at or datetime(2024, 1, 1, tzinfo=timezone.utc)
    return entry

def test_get_leaderboard_export_empty(db):
    with patch("app.crud.export.crud.get_leaderboard", return_value=[]):
        df = get_leaderboard_export(db, challenge_id=1)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0

def test_get_leaderboard_export_columns(db):
    entry = make_entry()
    with patch("app.crud.export.crud.get_leaderboard", return_value=[entry]):
        df = get_leaderboard_export(db, challenge_id=1)
    assert list(df.columns) == [
        "rank", "team_name", "category", "vehicle_weight",
        "score_value", "challenge_id", "attempt_id", "scored_at",
    ]

def test_get_leaderboard_export_rank_increments(db):
    entries = [
        make_entry(team_name="Alpha", score_value=100),
        make_entry(team_name="Beta",  score_value=80),
        make_entry(team_name="Gamma", score_value=60),
    ]
    with patch("app.crud.export.crud.get_leaderboard", return_value=entries):
        df = get_leaderboard_export(db, challenge_id=2)
    assert list(df["rank"]) == [1, 2, 3]

def test_get_leaderboard_export_row_values(db):
    ts = datetime(2025, 6, 15, 12, 0, tzinfo=timezone.utc)
    entry = make_entry(
        team_name="RocketTeam", category="ICE", vehicle_weight=550,
        score_value=88.8, challenge_id=3, attempt_id=42, created_at=ts,
    )
    with patch("app.crud.export.crud.get_leaderboard", return_value=[entry]):
        df = get_leaderboard_export(db, challenge_id=3)
    row = df.iloc[0]
    assert row["team_name"]      == "RocketTeam"
    assert row["category"]       == "ICE"
    assert row["vehicle_weight"] == 550
    assert row["score_value"]    == 88.8
    assert row["challenge_id"]   == 3
    assert row["attempt_id"]     == 42
    assert row["scored_at"]      == ts

def test_get_leaderboard_export_category_forwarded(db):
    with patch("app.crud.export.crud.get_leaderboard", return_value=[]) as mock_get:
        get_leaderboard_export(db, challenge_id=5, category="EV")
    mock_get.assert_called_once_with(db, 5, category="EV")

def test_get_leaderboard_export_no_category_passes_none(db):
    with patch("app.crud.export.crud.get_leaderboard", return_value=[]) as mock_get:
        get_leaderboard_export(db, challenge_id=7)
    mock_get.assert_called_once_with(db, 7, category=None)

def test_get_leaderboard_export_multiple_entries(db):
    entries = [make_entry(team_name=f"Team{i}", score_value=float(90 - i * 5)) for i in range(5)]
    with patch("app.crud.export.crud.get_leaderboard", return_value=entries):
        df = get_leaderboard_export(db, challenge_id=1)
    assert len(df) == 5
    assert list(df["team_name"]) == [f"Team{i}" for i in range(5)]
