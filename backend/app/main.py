from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware


from app.api.main import api_router

from app.config.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
def startup_event():
    if settings.DESKTOP_APP_STANDALONE:
        from app.db.session import Base, engine
        from app.models.attempt import Attempt
        from app.models.challenges import Challenge
        from app.models.drivers import Driver
        from app.models.leaderboard import Leaderboard
        from app.models.penalties import Penalty
        from app.models.score import Score
        from app.models.teams import Team
        from app.models.user import User

        Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix=settings.API_V1_STR)
