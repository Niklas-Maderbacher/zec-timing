from fastapi import APIRouter
from app.schemas.user import CreateUserKC, UpdateUserKC
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