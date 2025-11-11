from fastapi import APIRouter
from app.database.dependency import SessionDep, CurrentUser

router = APIRouter()

"""Protected route that requires Keycloak token authentication
    For testing purposes only.
"""
@router.get("/public")
def public_route(db: SessionDep):
    return {"message": "das geht immer"}

@router.get("/protected")  
def protected_route(db: SessionDep, current_user: CurrentUser):
    return {
        "message": f"{current_user['preferred_username']}",
    }
