import pandas as pd
from unittest.mock import MagicMock, patch
from datetime import datetime
from fastapi.testclient import TestClient
from app.main import app as fastapi_app
from app.database.dependency import get_db
from app.api.routes.export import stream_response


def make_entry(team_name="TeamA", category="EV", vehicle_weight=400,
               score_value=95.5, challenge_id=1, attempt_id=10,
               created_at=None):
    entry = MagicMock()
    entry.team.name = team_name
    entry.team.category = category
    entry.team.vehicle_weight = vehicle_weight
    entry.score.value = score_value
    entry.score.challenge_id = challenge_id
    entry.score.attempt_id = attempt_id
    entry.score.created_at = created_at or datetime(2024, 1, 1)
    return entry


def _consume(df, fmt, filename):
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/test")
    def _route():
        return stream_response(df, fmt, filename)

    with TestClient(app) as client:
        return client.get("/test")

def test_stream_response_csv_content_type():
    df = pd.DataFrame([{"name": "Alpha", "score": 95.5}])
    resp = stream_response(df, "csv", "test_file")
    assert resp.media_type == "text/csv"

def test_stream_response_csv_content_disposition():
    df = pd.DataFrame([{"name": "Alpha", "score": 95.5}])
    resp = stream_response(df, "csv", "test_file")
    assert resp.headers["Content-Disposition"] == "attachment; filename=test_file.csv"

def test_stream_response_csv_body_contains_data():
    df = pd.DataFrame([{"name": "Alpha", "score": 95.5}])
    resp = _consume(df, "csv", "myfile")
    assert b"Alpha" in resp.content
    assert b"95.5" in resp.content

def test_stream_response_xlsx_content_type():
    df = pd.DataFrame([{"name": "Alpha", "score": 95.5}])
    resp = stream_response(df, "xlsx", "test_file")
    assert resp.media_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

def test_stream_response_xlsx_content_disposition():
    df = pd.DataFrame([{"name": "Alpha", "score": 95.5}])
    resp = stream_response(df, "xlsx", "test_file")
    assert resp.headers["Content-Disposition"] == "attachment; filename=test_file.xlsx"

def test_stream_response_xlsx_body_is_valid_excel():
    df = pd.DataFrame([{"name": "Alpha", "score": 95.5}])
    resp = _consume(df, "xlsx", "myfile")
    assert resp.content[:2] == b"PK"

def test_stream_response_empty_dataframe_csv():
    resp = _consume(pd.DataFrame(), "csv", "empty")
    assert "text/csv" in resp.headers["content-type"]
    assert resp.content is not None

def test_stream_response_empty_dataframe_xlsx():
    resp = _consume(pd.DataFrame(), "xlsx", "empty")
    assert resp.content[:2] == b"PK"

def test_export_leaderboard_csv_default(db, override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    entry = make_entry()
    with patch("app.crud.export.crud.get_leaderboard", return_value=[entry]):
        with TestClient(fastapi_app) as client:
            resp = client.get("/api/export/leaderboard/1/category/EV")
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]

def test_export_leaderboard_csv_explicit(db, override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    entry = make_entry()
    with patch("app.crud.export.crud.get_leaderboard", return_value=[entry]):
        with TestClient(fastapi_app) as client:
            resp = client.get("/api/export/leaderboard/1/category/EV?format=csv")
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]

def test_export_leaderboard_xlsx(db, override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    entry = make_entry()
    with patch("app.crud.export.crud.get_leaderboard", return_value=[entry]):
        with TestClient(fastapi_app) as client:
            resp = client.get("/api/export/leaderboard/1/category/EV?format=xlsx")
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    assert "spreadsheetml" in resp.headers["content-type"]

def test_export_leaderboard_csv_filename(db, override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    with patch("app.crud.export.crud.get_leaderboard", return_value=[]):
        with TestClient(fastapi_app) as client:
            resp = client.get("/api/export/leaderboard/3/category/ICE")
    fastapi_app.dependency_overrides.clear()
    assert "leaderboard_challenge3_ICE.csv" in resp.headers["content-disposition"]

def test_export_leaderboard_xlsx_filename(db, override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    with patch("app.crud.export.crud.get_leaderboard", return_value=[]):
        with TestClient(fastapi_app) as client:
            resp = client.get("/api/export/leaderboard/3/category/ICE?format=xlsx")
    fastapi_app.dependency_overrides.clear()
    assert "leaderboard_challenge3_ICE.xlsx" in resp.headers["content-disposition"]

def test_export_leaderboard_body_contains_team_name(db, override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    entry = make_entry(team_name="SpeedDemon")
    with patch("app.crud.export.crud.get_leaderboard", return_value=[entry]):
        with TestClient(fastapi_app) as client:
            resp = client.get("/api/export/leaderboard/1/category/EV")
    fastapi_app.dependency_overrides.clear()
    assert b"SpeedDemon" in resp.content

def test_export_leaderboard_empty_returns_200(db, override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    with patch("app.crud.export.crud.get_leaderboard", return_value=[]):
        with TestClient(fastapi_app) as client:
            resp = client.get("/api/export/leaderboard/1/category/EV")
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    assert resp.content is not None

def test_export_leaderboard_unknown_format_falls_back_to_csv(db, override_get_db):
    fastapi_app.dependency_overrides[get_db] = override_get_db
    with patch("app.crud.export.crud.get_leaderboard", return_value=[]):
        with TestClient(fastapi_app) as client:
            resp = client.get("/api/export/leaderboard/1/category/EV?format=pdf")
    fastapi_app.dependency_overrides.clear()
    assert resp.status_code == 200
    assert "text/csv" in resp.headers["content-type"]