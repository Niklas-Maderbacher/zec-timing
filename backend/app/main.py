from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware


from app.api.main import api_router

from app.core.config import settings

def cstm_generate_unique_id(route: APIRoute) -> str:
  return f"{route.tags[0]}-{route.name}"

app = FastAPI(title=settings.PROJECT_NAME, 
              openapi_url=f"{settings.API_V1_STR}/openapi.json", 
              generate_unique_id_function=cstm_generate_unique_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
