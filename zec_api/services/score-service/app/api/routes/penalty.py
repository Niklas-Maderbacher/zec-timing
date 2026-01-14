from fastapi import APIRouter
from typing import List
from app.database.dependency import SessionDep
from app.schemas.penalty import PenaltyCreate, PenaltyUpdate, PenaltyResponse
from app.crud import penalty as crud

router = APIRouter()

@router.post("/", response_model=PenaltyResponse)
def create_penalty(db: SessionDep, penalty: PenaltyCreate):
    penalty = crud.create_penalty(db=db, penalty=penalty)
    return penalty

@router.put("/{penalty_id}", response_model=PenaltyResponse)
def update_penalty(db: SessionDep, penalty_id: int, penalty_update: PenaltyUpdate):
    penalty = crud.update_penalty(db=db, penalty_id=penalty_id, penalty_update=penalty_update)
    return penalty

@router.delete("/{penalty_id}", response_model=PenaltyResponse)
def delete_penalty(db: SessionDep, penalty_id: int):
    penalty = crud.delete_penalty(db=db, penalty_id=penalty_id)
    return penalty

@router.get("/{penalty_id}", response_model=PenaltyResponse)
def get_penalty(db: SessionDep, penalty_id: int):
    penalty = crud.get_penalty(db=db, penalty_id=penalty_id)
    return penalty

@router.get("/", response_model=List[PenaltyResponse])
def list_penalties(db: SessionDep):
    penalties = crud.get_penalties(db=db)
    return penalties

@router.get("/attempt/{attempt_id}", response_model=List[PenaltyResponse])
def list_penalties_by_attempt(db: SessionDep, attempt_id: int):
    penalties = crud.get_penalties_by_attempt(db=db, attempt_id=attempt_id)
    return penalties