from fastapi import APIRouter
from app.api.routes import team, driver

api_router = APIRouter()

api_router.include_router(team.router, prefix="/teams", tags=["team"])
api_router.include_router(driver.router, prefix="/drivers", tags=["driver"])
