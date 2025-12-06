from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings
from app.database.seed import seed_challenges
from sqlalchemy.orm import Session
from app.database.session import engine

def cstm_generate_unique_id(route: APIRoute) -> str:
    if route.tags and len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    else:
        return f"untagged-{route.name}"

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_STR)

@app.on_event("startup")
def startup_event():
    db = Session(bind=engine)
    seed_challenges(db)
    db.commit()
