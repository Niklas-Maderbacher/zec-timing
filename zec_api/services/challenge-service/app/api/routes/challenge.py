from fastapi import APIRouter
from typing import List
from app.database.dependency import SessionDep
from app.schemas.challenge import ChallengeUpdate, ChallengeResponse
from app.crud import challenge as crud

router = APIRouter()

@router.put("/{challenge_id}", response_model=ChallengeResponse)
def update_challenge(db: SessionDep, challenge_id: int, challenge_update: ChallengeUpdate):
    challenge = crud.update_challenge(db=db, challenge_id=challenge_id, challenge_update=challenge_update)
    return challenge

@router.get("/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(db: SessionDep, challenge_id: int):
    challenge = crud.get_challenge(db=db, challenge_id=challenge_id)
    return challenge

@router.get("/name/{challenge_name}", response_model=ChallengeResponse)
def get_challenge_by_name(db: SessionDep, challenge_name: str):
    challenge = crud.get_challenge_by_name(db=db, challenge_name=challenge_name)
    return challenge

@router.get("/", response_model=List[ChallengeResponse])
def list_challenges(db: SessionDep):
    challenges = crud.get_challenges(db=db)
    return challenges