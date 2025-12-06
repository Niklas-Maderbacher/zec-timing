from fastapi import APIRouter

# routes imports go here
from app.api.routes import health_check
from app.api.routes import challenges
from app.api.routes import drivers
from app.api.routes import penalties
from app.api.routes import teams

api_router = APIRouter()

api_router.include_router(health_check.router)
api_router.include_router(challenges.router)
api_router.include_router(drivers.router)
api_router.include_router(penalties.router)
api_router.include_router(teams.router)