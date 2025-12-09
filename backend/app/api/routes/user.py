from fastapi import APIRouter
from app.schemas.user import CreateUserKC
from app.crud import user as crud
from app.database.dependency import SessionDep

router = APIRouter()

@router.post("/")
def create_user(db: SessionDep, request: CreateUserKC):
    response = crud.create_user(db=db, request=request)
    return response