from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from app.api.main import api_router
from app.core.config import settings
from sqlalchemy.orm import Session
from app.database.session import engine, Base

def cstm_generate_unique_id(route: APIRoute) -> str:
    if route.tags and len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    else:
        return f"untagged-{route.name}"

app = FastAPI(
    title="Score Service API",
    openapi_url=f"{settings.API_STR}/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_STR)
Base.metadata.create_all(bind=engine)
