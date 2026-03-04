import io

def test_export_attempts_csv_default(client):
    response = client.get("/api/export/attempts", params={"challenge_id": 1})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attempts_challenge1.csv" in response.headers["content-disposition"]

def test_export_attempts_csv_content(client):
    response = client.get("/api/export/attempts", params={"challenge_id": 1})
    content = response.text
    assert "attempt_id" in content
    assert "challenge_name" in content
    assert "team_name" in content

def test_export_attempts_xlsx(client):
    response = client.get("/api/export/attempts", params={"challenge_id": 1, "format": "xlsx"})
    assert response.status_code == 200
    assert "spreadsheetml" in response.headers["content-type"]
    assert "attempts_challenge1.xlsx" in response.headers["content-disposition"]

def test_export_attempts_xlsx_readable(client):
    import pandas as pd
    response = client.get("/api/export/attempts", params={"challenge_id": 1, "format": "xlsx"})
    df = pd.read_excel(io.BytesIO(response.content))
    assert len(df) == 2
    assert "team_name" in df.columns

def test_export_attempts_with_category(client):
    response = client.get("/api/export/attempts", params={"challenge_id": 1, "category": "A"})
    assert response.status_code == 200
    assert "attempts_challenge1_A.csv" in response.headers["content-disposition"]

def test_export_attempts_csv_has_correct_rows(client):
    import csv
    response = client.get("/api/export/attempts", params={"challenge_id": 1})
    reader = csv.DictReader(io.StringIO(response.text))
    rows = list(reader)
    assert len(rows) == 2

def test_export_attempts_not_found(client):
    response = client.get("/api/export/attempts", params={"challenge_id": 999})
    assert response.status_code == 404

def test_export_attempts_category_not_found(client):
    response = client.get("/api/export/attempts", params={"challenge_id": 1, "category": "Z"})
    assert response.status_code == 404
    assert response.json()["detail"] is not None

def test_export_attempts_missing_challenge_id(client):
    response = client.get("/api/export/attempts")
    assert response.status_code == 422
