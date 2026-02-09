from fastapi import APIRouter
from app.api.routes import attempt

api_router = APIRouter()

api_router.include_router(attempt.router, prefix="/attempts", tags=["attempt"])