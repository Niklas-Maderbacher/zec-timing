from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.database.dependency import SessionDep
from app.crud.export import get_leaderboard_export
import pandas as pd
import io

router = APIRouter()

def stream_response(df: pd.DataFrame, format: str, filename: str) -> StreamingResponse:
    if format == "xlsx":
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}.xlsx"}
        )
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}.csv"}
    )

@router.get("/leaderboard/{challenge_id}/category/{category}")
def export_leaderboard(
    challenge_id: int,
    category: str,
    format: str = Query("csv", enum=["csv", "xlsx"]),
    db: SessionDep = None,
):
    df = get_leaderboard_export(db, challenge_id, category)
    filename = f"leaderboard_challenge{challenge_id}_{category}"
    return stream_response(df, format, filename)
