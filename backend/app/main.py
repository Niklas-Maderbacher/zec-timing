from fastapi import FastAPI 
from fastapi.routing import APIRoute 
 
from app.api.main import api_router 
 
def cstm_generate_unique_id(route: APIRoute) -
 
app = FastAPI(title="4AHIT",  
              openapi_url="/api/v1/openapi.json",  
              generate_unique_id_function=cstm_generate_unique_id) 
 
app.include_router(api_router, prefix="/api/v1") 
