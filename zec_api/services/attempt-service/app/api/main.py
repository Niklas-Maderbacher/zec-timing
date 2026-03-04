from fastapi import APIRouter
from app.api.routes import attempt, export

api_router = APIRouter()

api_router.include_router(attempt.router, prefix="/attempts", tags=["attempt"])
api_router.include_router(export.router, prefix="/export", tags=["export"])