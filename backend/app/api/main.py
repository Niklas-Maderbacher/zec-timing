from fastapi import APIRouter
from app.api.routes import auth, user, protected, team, driver

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(protected.router, prefix="", tags=["protected"])
api_router.include_router(team.router, prefix="/teams", tags=["team"])
api_router.include_router(driver.router, prefix="/drivers", tags=["driver"])