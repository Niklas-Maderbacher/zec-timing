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
def update_attempt(db: SessionDep, attempt_id: int, attempt_update: AttemptUpdate):
    attempt = crud.update_attempt(db=db, attempt_id=attempt_id, attempt_update=attempt_update)
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

@router.get("/challenges/{challenge_id}", response_model=List[AttemptResponse])
def get_attempts_per_challenge(db: SessionDep, challenge_id: int):
    attempts = crud.get_attempts_for_challenge(db=db, challenge_id=challenge_id)
    return attempts

@router.get("/fastest/{challenge_id}", response_model=AttemptResponse)
def fastest_attempt(db: SessionDep, challenge_id: int):
    attempts = crud.get_fastest_attempt(db=db, challenge_id=challenge_id)
    return attempts

@router.get("/fastest/per-team/", response_model=AttemptResponse)
def fastest_attempts_per_team(db: SessionDep, challenge_id: int, team_id: int):
    attempts = crud.get_fastest_attempt_for_team(db=db, challenge_id=challenge_id, team_id=team_id)
    return attempts

@router.get("/least-energy/{challenge_id}", response_model=AttemptResponse)
def least_energy_attempt(db: SessionDep, challenge_id: int):
    attempts = crud.get_least_energy_attempt(db=db, challenge_id=challenge_id)
    return attempts

@router.get("/least-energy/per-team/", response_model=AttemptResponse)
def least_energy_attempts_per_team(db: SessionDep, challenge_id: int, team_id: int):
    attempts = crud.get_least_energy_attempt_for_team(db=db, challenge_id=challenge_id, team_id=team_id)
    return attempts
