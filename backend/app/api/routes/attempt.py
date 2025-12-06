from fastapi import APIRouter
from typing import List
from app.database.dependency import SessionDep
from app.schemas.attempt import AttemptCreate, AttemptUpdate, AttemptResponse
from app.crud import attempt as crud

router = APIRouter()

@router.post("/", response_model=AttemptResponse)
def create_attempt(db: SessionDep, attempt: AttemptCreate):
    attempt = crud.create_attempt(db=db, attempt=attempt)
    return attempt

@router.put("/{attempt_id}", response_model=AttemptResponse)
def update_attempt(db: SessionDep, attempt_update: AttemptUpdate):
    attempt = crud.update_attempt(db=db, attempt_update=attempt_update)
    return attempt

@router.delete("/{attempt_id}", response_model=AttemptResponse)
def delete_attempt(db: SessionDep, attempt_id: int):
    attempt = crud.delete_attempt(db=db, attempt_id=attempt_id)
    return attempt

@router.get("/{attempt_id}", response_model=AttemptResponse)
def get_attempt(db: SessionDep, attempt_id: int):
    attempt = crud.get_attempt(db=db, attempt_id=attempt_id)
    return attempt

@router.get("/", response_model=List[AttemptResponse])
def list_attempts(db: SessionDep):
    attempts = crud.get_attempts(db=db)
    return attempts