from fastapi import APIRouter
from app.database.dependency import SessionDep, CurrentUser
from app.database.dependency import AdminUser

router = APIRouter()

"""
Protected route that requires Keycloak token authentication
For testing purposes only.
"""
@router.get("/public")
def public_route(db: SessionDep):
    return {"message": "das geht immer"}

@router.get("/admin-only")
async def admin_route(user: AdminUser):
    return {"message": f"Welcome admin {user['username']}"}

@router.get("/protected")  
def protected_route(db: SessionDep, current_user: CurrentUser):
    return {
        "message": f"{current_user['username']}",
    }

@router.get("/profile")
async def get_profile(user: CurrentUser):
    return {
        "username": user["username"],
        "email": user["email"],
        "roles": user["roles"]
    }
