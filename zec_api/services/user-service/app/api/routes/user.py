from fastapi import APIRouter
from app.schemas.user import CreateUserKC, UpdateUserKC, UserRolesRequest
from app.crud import user as crud
from app.database.dependency import SessionDep

router = APIRouter()

@router.post("/")
def create_user(db: SessionDep, request: CreateUserKC):
    response = crud.create_user(db=db, request=request)
    return response

@router.get("/username/{username}", response_model=dict)
def get_user_by_username(username: str):
    user = crud.get_user_by_username(username=username)
    return user

@router.get("/id/{id}", response_model=dict)
def get_user_by_id(id: str):
    user = crud.get_user_by_id(user_id=id)
    return user

@router.put("/{user_id}")
async def update_user_endpoint(db: SessionDep, user_id: str,request: UpdateUserKC):
    updated_user = crud.update_user(db=db, user_id=user_id, request=request)
    return updated_user

@router.delete("/{user_id}")
def delete_user_endpoint(db: SessionDep, user_id: str):
    crud.delete_user(db=db, user_id=user_id)

@router.post("/{user_id}/roles")
def assign_client_roles_to_user(user_id: str, roles_request: UserRolesRequest):
    crud.add_roles_to_user(user_id=user_id, roles=roles_request.roles)
    return {
        "message": "Roles assigned successfully",
        "user_id": user_id,
        "assigned_roles": roles_request.roles
    }

@router.delete("/{user_id}/roles")
def remove_roles_from_user(user_id: str, roles_request: UserRolesRequest):
    crud.remove_roles_from_user(user_id=user_id, roles=roles_request.roles)
    return {
        "message": "Roles remove successfully",
        "user_id": user_id,
        "assigned_roles": roles_request.roles
    }
