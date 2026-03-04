from fastapi import APIRouter
from fastapi import Header
from app.schemas.user import CreateUserKC, UpdateUserKC, UserRolesRequest, UserResponseKC
from app.crud import user as crud
from app.database.dependency import SessionDep

router = APIRouter()

@router.post("/", response_model=UserResponseKC)
def create_user(db: SessionDep, request: CreateUserKC):
    response = crud.create_user(db=db, request=request)
    return response

@router.put("/{user_id}")
async def update_user_endpoint(db: SessionDep, user_id: str, request: UpdateUserKC):
    updated_user = crud.update_user(db=db, user_id=user_id, request=request)
    return updated_user

@router.delete("/{user_id}")
def delete_user_endpoint(db: SessionDep, user_id: str):
    crud.delete_user(db=db, user_id=user_id)
    return {"message": "User deleted successfully", "user_id": user_id}

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
        "unassigned_roles": roles_request.roles
    }

@router.get("/username/{username}", response_model=UserResponseKC)
def get_user_by_username(db: SessionDep, username: str):
    user = crud.get_user_by_username(db=db, username=username)
    return user

@router.get("/id/{id}", response_model=UserResponseKC)
def get_user_by_id(db: SessionDep, id: str):
    user = crud.get_user_by_id(db=db, user_id=id)
    return user

@router.get("/", response_model=list[UserResponseKC])
def get_all_users(db: SessionDep):
    users = crud.get_all_users(db=db)
    return users

@router.get("/me", response_model=UserResponseKC)
def get_current_user(db: SessionDep, authorization: str = Header(...)):
    current_user = crud.get_current_user(db=db, authorization=authorization)
    return current_user
