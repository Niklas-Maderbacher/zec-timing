from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from app.database.dependency import SessionDep
from app.crud.export import get_attempts_export
from app.exceptions.exceptions import EntityDoesNotExistError
from fastapi import HTTPException
import io
import pandas as pd

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

@router.get("/attempts")
def export_attempts(
    challenge_id: int = Query(...),
    category: str = Query(None),
    format: str = Query("csv", enum=["csv", "xlsx"]),
    db: SessionDep = None,
):
    try:
        df = get_attempts_export(db, challenge_id, category)
    except EntityDoesNotExistError as e:
        raise HTTPException(status_code=404, detail=str(e))

    filename = f"attempts_challenge{challenge_id}"
    if category:
        filename += f"_{category}"

    return stream_response(df, format, filename)
