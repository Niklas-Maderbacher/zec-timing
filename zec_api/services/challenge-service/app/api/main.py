from fastapi import APIRouter
from app.api.routes import challenge

api_router = APIRouter()

api_router.include_router(challenge.router, prefix="/challenges", tags=["challenges"])
